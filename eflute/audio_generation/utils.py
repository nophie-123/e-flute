import pandas as pd
from scipy.io import wavfile


def load_wav(file_name):
    frame_rate, sound_data = wavfile.read(file_name)
    sound_data = pd.DataFrame(sound_data, columns=["left", "right"])
    sound_data["frame_rate"] = frame_rate

    return sound_data


def setup_plots():
    import IPython
    IPython.core.getipython.get_ipython().magic(u'matplotlib inline')

    import seaborn as sb
    sb.set_context("poster")
