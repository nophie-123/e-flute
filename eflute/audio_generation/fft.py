import numpy as np


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
    fft_left = _fft_numpy(data["left"], frame_rate)
    fft_right = _fft_numpy(data["right"], frame_rate)

    fft_joined = fft_left.join(fft_right, lsuffix="_left", rsuffix="_right", how="inner")
    fft_joined["Frequency"] = 0.5 * (fft_joined["Frequency_left"] + fft_joined["Frequency_right"])
    del fft_joined["Frequency_left"]
    del fft_joined["Frequency_right"]

    return fft_joined


def heatmap(sound_data):
    def loader(size, delta=2500):
        for x in xrange(0, size, delta):
            data = sound_data[x:x + delta]
            fft_data = fft(data)
            tmp = fft_data[["Frequency", "FFT_Power_left"]].copy()
            tmp["x"] = x
            yield tmp

    number_of_datapoints = len(sound_data)
    tmp = pd.concat(list(loader(number_of_datapoints, int(number_of_datapoints/30.0))))

    tmp["Frequency_short"] = pd.cut(tmp.Frequency, np.arange(0, 2500, 50))

    return tmp.groupby(["Frequency_short", "x"]).mean()["FFT_Power_left"].unstack()