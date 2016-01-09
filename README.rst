======
eflute
======


Project for analysing sound data coming from musical instruments (mostly flutes), generating flute-like tones and connecting to a electric flute instrument to generate an electronic flute-like instrument.


Description
===========

The project has three different parts:

 * Analyse recorded sound data
 * Create sound data (wav files) similar to the recorded ones, but with a mathematical formular/lookup table
 * Connect to a built electronic device

In the following these three points are described in more detail.

Analyse
-------

For starting to analyse recorded sound data (for example the data shipped with this project in `data`), clone into the project and install the package

::

    git clone https://github.com/nophie-123/e-flute
    python setup.py install

After that, you can open an IPython notebook and load the package. For example you can do:

.. code:: python

    from eflute.audio_generation import utils
    from eflute.audio_generation import fft
    from eflute.audio_generation import peak_detect

    utils.setup_plots()

    # (1)
    sound_data = utils.load_wav("data/Flute/c4.wav")

    # (2)
    f = fft.fft(sound_data)
    plt.plot(f.Frequency, f.FFT_Power)
    peaks = peak_detect.peak_detect(f, column="FFT_Power", lookahead=50)

    # (3)
    plt.plot(peaks.Frequency, peaks.FFT_Power, ls="", marker="o")
    plt.xlim(0, 10000)

To load the flute sound data of a c4 note (1), do a FFT of the sound data and plot it (2) and find the peaks in the spectrum and plot them to (3).
You can now go on analysing the peaks of the FFT for your needs. A full description of the included methods can be found in the end of this document.

Implemented methods
===================

TODO


Note
====

This project has been set up using PyScaffold 2.5.2. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
