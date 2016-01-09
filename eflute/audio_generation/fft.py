import numpy as np
import pandas as pd


def _fft_numpy(data, sampling_frequency):
    try:
        tmp_data = data.values
    except AttributeError:
        tmp_data = data

    # Normalize Data
    tmp_data = tmp_data / (2.0 ** 15)

    # Calculate FFT
    data_fft = np.fft.fft(tmp_data)
    data_angles = np.angle(data_fft)
    data_spec = np.abs(data_fft)

    # Calculate last frequency before Nyquist limit
    N = len(tmp_data)
    data_samples_before_nyquist = np.ceil((N + 1) / 2.0)
    data_fft = data_fft[0:int(data_samples_before_nyquist)]

    # Normalize Spectrum
    data_fft = data_fft / float(N)

    # Calculate output values
    spec = np.abs(data_fft)
    power_spec = 20 * np.log10(spec)
    angle = np.angle(data_fft)
    frequencies = np.arange(0, data_samples_before_nyquist) * (1.0 * sampling_frequency / N)

    result_df = pd.DataFrame(np.transpose([frequencies, spec, power_spec, angle]),
                             columns=["Frequency", "FFT", "FFT_Power", "Angle"])
    return result_df


def fft(data):
    frame_rate = data["frame_rate"].mean()
    return _fft_numpy(data["left"], frame_rate)


def get_windowed_data(sound_data, delta=2500):
    size = len(sound_data)
    for x in xrange(0, size, delta):
        data_middle = sound_data[x:x + delta]
        data_left = 0.5 * sound_data[x-delta:x]
        data_right = 0.5 * sound_data[x+delta:x+2*delta]

        data = pd.concat([data_left, data_middle, data_right])

        fft_data = fft(data)
        tmp = fft_data[["Frequency", "FFT_Power"]].copy()
        tmp["x"] = x
        yield tmp


def heatmap(sound_data, n_cuts_frequency=50, n_cuts_time=30, max_frequency=2500):
    number_of_datapoints = len(sound_data)
    windowed_data = get_windowed_data(sound_data, int(1.0 * number_of_datapoints / n_cuts_time))
    tmp = pd.concat(list(windowed_data))
    tmp["Frequency_short"] = pd.cut(tmp.Frequency, np.arange(0, max_frequency, 1.0 * max_frequency/n_cuts_frequency))

    return tmp.groupby(["Frequency_short", "x"]).mean()["FFT_Power"].unstack()