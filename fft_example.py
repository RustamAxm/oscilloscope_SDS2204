import numpy as np
from matplotlib import pyplot as plt
from SDS2204 import SDS2204


def fft_example():

    oscilloscope = SDS2204()

    print('Sample Rate = ', oscilloscope.get_sample_rate())

    for iteration in range(5):
        time, voltage = oscilloscope.get_waveform(channel='C1')

        if iteration == 0:
            fft_data = np.fft.fft(voltage)
            freq = np.fft.fftfreq(len(time)) * oscilloscope.sara
        else:
            fft_data += np.fft.fft(voltage)

    oscilloscope.close_device()

    plt.figure(1)
    freq_show_lims = (0, 5e3)
    plt.subplot(3, 1, 1)
    plt.plot(time, voltage, label='WAVEFORM', color='g')
    plt.grid()
    plt.legend()
    plt.xlabel('time(sec)')
    plt.ylabel('voltage(V)')
    plt.subplot(3, 1, 2)
    plt.plot(freq[:int(len(freq) / 2)], abs(fft_data.real[:int(len(freq) / 2)]), label='FFT_REAL', color='b')
    plt.grid()
    plt.legend()
    plt.xlabel('freq(Hz)')
    plt.xlim(freq_show_lims)
    plt.subplot(3, 1, 3)
    plt.plot(freq[:int(len(freq) / 2)], fft_data.imag[:int(len(freq) / 2)], label='FFT_IMG', color='r')
    plt.grid()
    plt.legend()
    plt.xlabel('freq(Hz)')
    plt.xlim(freq_show_lims)
    plt.show()


if __name__ == '__main__':
    fft_example()
