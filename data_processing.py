# ------------------------------------------------------
# Process the Raw AE signals for training-ready
# The Raw signal is sampled at 5MHz, So time btw points = 2e-7 s
# ------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import spectrogram
from dataset_experiment1 import AcousticEmissionDataSet


# FAST FOURIER TRANSFORM (FFT)
def fft_scipy(sampled_data=None, fs=1, visualize=True):
    '''
    :param sampled_data: A one dimensional data (Size = N), can be list or series
    :param fs: Sampling frequency
    :param visualize: Plot or not (Boolean)
    :return: amplitude and the frequency spectrum (Size = N // 2)
    '''
    # Sample points and sampling frequency
    N = sampled_data.size
    fs = fs
    # fft
    print('Scipy.FFT on {} points...'.format(N), end='')
    # take only half of the FFT output because it is a reflection
    # take abs because the FFT output is complex
    # divide by N to reduce the amplitude to correct one
    # times 2 to restore the discarded reflection amplitude
    y_fft = fft(sampled_data)
    y_fft = (2.0/N) * np.abs(y_fft[0: N//2])
    # x-axis - only half of N
    f_axis = np.linspace(0.0, fs/2, N//2)

    if visualize:
        plt.plot(f_axis, y_fft)
        # use sci. notation at the x-axis value
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        # plot only 0Hz to 300kHz
        plt.xlim((0, 300e3))
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude')
        plt.title('Fast Fourier Transform')
        plt.show()
    print('[Done]')
    return y_fft, f_axis


# SPECTROGRAM
def spectrogram_scipy(sampled_data=None, fs=1, visualize=True):
    '''
    :param sampled_data: A one dimensional data (Size = N), can be list or series
    :param fs: Sampling frequency
    :param visualize: Plot Spectrogram or not (Boolean)
    :return: time axis, frequency band and the Amplitude in 2D matrix
    '''
    # There is a trade-off btw resolution of frequency and time due to uncertainty principle
    # Spectrogram split input signal into segments before FFT and PSD on each seg.
    # Adjust nperseg is adjusting segment length. Higher nperseg giv more res in Freq but
    # lesser res in time domain.
    f, t, Sxx = spectrogram(sampled_data,
                            fs=fs,
                            scaling='spectrum',
                            nperseg=10000,  # Now 5kHz is sliced into 100 pcs i.e. 50Hz/pcs
                            noverlap=1000)
    print('\n----------SPECTROGRAM OUTPUT---------')
    print('Time Segment....{}\n'.format(t.size), t)
    print('Frequency Segment....{}\n'.format(f.size), f)
    f_res = fs / (2 * (f.size - 1))
    print('Spectrogram Dim: {}, F-Resolution: {}Hz/Band'.format(Sxx.shape, f_res))
    if visualize:
        plt.pcolormesh(t, f, Sxx)
        plt.ylabel('Frequency [Hz]')
        plt.ylim((0, 300e3))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        plt.xlabel('Time [Sec]')
        plt.show()

    return t, f, Sxx


# ----------------------[DATA IMPORT]-------------------------
ae_dataset_1 = AcousticEmissionDataSet()

# testing
data_test = ae_dataset_1.testing()

# ----------------------[SIGNAL TRANSFORMATION]-------------------------
time_step, f_band, mat = spectrogram_scipy(data_test[0], fs=1e6, visualize=False)





