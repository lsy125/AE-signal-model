'''
this script train the CNN on recognizing the PLB collected at different points
time series signal -> segmentation -> bandpass -> STFT -> Xcor -> preprocessing -> CNN training
'''
import numpy as np
from keras.callbacks import TensorBoard
from src.experiment_dataset.dataset_experiment_2018_7_13 import AcousticEmissionDataSet_13_7_2018
from src.utils.helpers import break_into_train_test, reshape_3d_to_4d_tocategorical, \
                              ModelLogger, recall_precision_multiclass
from src.model_bank.cnn_model_bank import cnn_general_v1


data = AcousticEmissionDataSet_13_7_2018(drive='F')
dataset, label = data.plb()

# split to train test data
num_classes = 41
train_x, train_y, test_x, test_y = break_into_train_test(input=dataset,
                                                         label=label,
                                                         num_classes=num_classes,
                                                         train_split=0.7,
                                                         verbose=True)

# reshape to satisfy conv2d input shape
train_x, train_y, test_x, test_y = reshape_3d_to_4d_tocategorical(train_x, train_y, test_x, test_y,
                                                                  fourth_dim=1,
                                                                  num_classes=num_classes,
                                                                  verbose=True)

# iterate several times to find best model with F1-score
for i in range(10):
    model = cnn_general_v1(input_shape=(train_x.shape[1], train_x.shape[2]), num_classes=num_classes)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model_logger = ModelLogger(model, model_name='PLB_2018_7_13_Classification_CNN[33k]_take{}'.format(i))
    # tensorboard (folder name in Graph will be used to name the run)
    # tb_callback = TensorBoard(log_dir='./Graph', histogram_freq=2,
    #                           write_graph=True, write_images=True, write_grads=True)
    sbw_callback = model_logger.save_best_weight_cheakpoint(monitor='val_acc', period=1)
    history = model.fit(x=train_x,
                        y=train_y,
                        batch_size=100,
                        validation_data=(test_x, test_y),
                        epochs=150,
                        verbose=1,
                        callbacks=[sbw_callback])
    model_logger.learning_curve(history=history, save=True, show=False)
    model_logger.save_architecture(save_readable=True)
    x = np.concatenate((train_x, test_x), axis=0)
    y = np.concatenate((train_y, test_y), axis=0)
    prediction = model.predict(x)
    prediction = np.argmax(prediction, axis=1)
    actual = np.argmax(y, axis=1)

    print(prediction)
    print(actual)

