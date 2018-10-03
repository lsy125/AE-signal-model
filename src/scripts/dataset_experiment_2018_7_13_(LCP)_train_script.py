import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from keras.callbacks import TensorBoard
from src.experiment_dataset.dataset_experiment_2018_7_13 import AcousticEmissionDataSet_13_7_2018
from src.model_bank.dataset_2018_7_13_lcp_recognition_model import *
from src.utils.helpers import *

ae_data = AcousticEmissionDataSet_13_7_2018(drive='F')
train_x, train_y, test_x, test_y = ae_data.lcp_recognition_binary_class_dataset_seg3(train_split=0.8)

train_x_reshape = train_x.reshape((train_x.shape[0], train_x.shape[1], 1))
test_x_reshape = test_x.reshape((test_x.shape[0], test_x.shape[1], 1))

lcp_model = lcp_recognition_binary_model_2()
lcp_model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])

# saving setting
logger = ModelLogger(model=lcp_model, model_name='LCP_Recog_1')
save_weight_checkpoint = logger.save_best_weight_cheakpoint(monitor='val_loss', period=5)

# tensorboard
tb_save_dir = direct_to_dir(where='result') + 'Graph/run_4, model3'
tb_callback = TensorBoard(log_dir=tb_save_dir,
                          histogram_freq=10,
                          write_graph=False,
                          write_images=False,
                          write_grads=True)

# start training
history = lcp_model.fit(x=train_x_reshape,
                        y=train_y,
                        validation_data=(test_x_reshape, test_y),
                        callbacks=[tb_callback, save_weight_checkpoint],
                        epochs=10000,
                        batch_size=350,
                        shuffle=True,
                        verbose=2)

logger.learning_curve(history=history, show=True)
logger.save_architecture(save_readable=True)


# evaluate
prediction = lcp_model.predict(test_x_reshape)

prediction_quantized = []
for p in prediction:
    if p > 0.5:
        prediction_quantized.append(1)
    else:
        prediction_quantized.append(0)

logger.save_recall_precision_f1(y_pred=prediction_quantized, y_true=test_y, all_class_label=[0, 1])


plt.plot(test_y, color='r', label='Actual')
plt.plot(prediction, color='b', label='Prediction', linestyle='None', marker='x')
plt.title('Classifier Output in Visual')
plt.legend()
plt.show()


