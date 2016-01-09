from time import sleep

import numpy as np
import pandas as pd
from scipy.io import wavfile


def load_wav(file_name):
    frame_rate, sound_data = wavfile.read(file_name)
    if len(np.shape(sound_data)) == 1:
        sound_data = pd.DataFrame(sound_data, columns=["left"])
    elif len(np.shape(sound_data)) == 2:
        sound_data = pd.DataFrame(sound_data, columns=["left", "right"])
    else:
        raise ValueError("Do not understand wav file.")
    sound_data["frame_rate"] = frame_rate

    return sound_data


def setup_plots():
    import IPython
    IPython.core.getipython.get_ipython().magic(u'matplotlib inline')

    import seaborn as sb
    sb.set_context("poster")

def play_wav(file_name):
    from wave import open as waveOpen
    from ossaudiodev import open as ossOpen
    s = waveOpen(file_name,'rb')
    (nc,sw,fr,nf,comptype, compname) = s.getparams()
    dsp = ossOpen('/dev/dsp','w')
    from ossaudiodev import AFMT_S16_NE
    dsp.setparameters(AFMT_S16_NE, nc, fr)
    data = s.readframes(nf)
    s.close()
    dsp.write(data)
    dsp.close()