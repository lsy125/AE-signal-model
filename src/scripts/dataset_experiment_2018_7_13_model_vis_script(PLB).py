import numpy as np
import matplotlib.pyplot as plt
import keras.backend as K
# self defined library
from src.utils.helpers import model_loader, get_activations, break_into_train_test, \
                              reshape_3d_to_4d_tocategorical, plot_multiple_horizontal_heatmap, plot_heatmap_series_in_four_column
from src.experiment_dataset.dataset_experiment_2018_7_13 import AcousticEmissionDataSet_13_7_2018


save_dir = 'C:/Users/YH/PycharmProjects/AE-signal-model/result/'

# -------------------[LOADING DATA]----------------------------
data = AcousticEmissionDataSet_13_7_2018(drive='F')
dataset, label = data.plb()

# split to train test data
num_classes = 41
train_x, train_y, test_x, test_y = break_into_train_test(input=dataset,
                                                         label=label,
                                                         num_classes=num_classes,
                                                         train_split=0.95,
                                                         verbose=True,
                                                         shuffled_each_class=False)
# reshape to satisfy conv2d input shape
_, _, test_x_reshape, _ = reshape_3d_to_4d_tocategorical(train_x, train_y, test_x, test_y,
                                                         fourth_dim=1,
                                                         num_classes=num_classes,
                                                         verbose=True)


# -------------------[LOADING MODEL]----------------------------

model = model_loader(model_name='PLB_2018_7_13_Classification_CNN[33k]_take0')
model.compile(loss='categorical_crossentropy', optimizer='adam')

activation = get_activations(model, model_inputs=test_x_reshape, print_shape_only=True)

print(len(activation))

for layer in model.layers:
    print(layer)

# extract specific activation into seperate array
layer_1_act = activation[3]
layer_2_act = activation[4]
layer_3_act = activation[5]
layer_3_act = layer_3_act.reshape((layer_3_act.shape[0], 1, layer_3_act.shape[1]))
print(layer_3_act.shape)
# for all sample
for sample_index in range(test_x.shape[0]):
    layer_1_act_list = [layer_1_act[sample_index, :, :, filter_index] for filter_index in range(layer_1_act.shape[3])]
    layer_2_act_list = [layer_2_act[sample_index, :, :, filter_index] for filter_index in range(layer_2_act.shape[3])]
    layer_3_act_list = [layer_3_act[sample_index]]

    fig_label = 'Sample[{}]_Class[{}m]_p2'.format(sample_index, test_y[sample_index])
    fig = plot_heatmap_series_in_four_column(column_1_heatmap=test_x[sample_index],
                                             column_2_heatmap=layer_1_act_list,
                                             column_3_heatmap=layer_2_act_list,
                                             column_4_heatmap=layer_3_act_list,
                                             main_title='ACTIVATION VISUALIZATION of {}'.format(fig_label),
                                             each_column_title=['Input Xcor Map', 'conv2d_3', 'maxpool_2', 'flatten'],
                                             each_subplot_title=['fmap', 'fmap', 'fmap'])
    save_filename = save_dir + fig_label
    fig.savefig(save_filename)

    plt.close('all')

    print('saved --> ', fig_label)



