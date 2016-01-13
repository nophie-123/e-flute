# functions that implement analysis and synthesis of sounds using the Sinusoidal plus Stochastic Model
# (for example usage check the models_interface directory)

import utilFunctions
import sineModel
import stochasticModel


def sps_model_anal(x, fs, w, N, H, t, minSineDur, maxnSines, freqDevOffset, freqDevSlope, stocf):
    """
    Analysis of a sound using the sinusoidal plus stochastic model
    x: input sound, fs: sampling rate, w: analysis window; N: FFT size, t: threshold in negative dB,
    minSineDur: minimum duration of sinusoidal tracks
    maxnSines: maximum number of parallel sinusoids
    freqDevOffset: frequency deviation allowed in the sinusoids from frame to frame at frequency 0
    freqDevSlope: slope of the frequency deviation, higher frequencies have bigger deviation
    stocf: decimation factor used for the stochastic approximation
    returns hfreq, hmag, hphase: harmonic frequencies, magnitude and phases; stocEnv: stochastic residual
    """

    # perform sinusoidal analysis
    tfreq, tmag, tphase = sineModel.sine_model_anal(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)
    Ns = 512
    xr = utilFunctions.sineSubtraction(x, Ns, H, tfreq, tmag, tphase, fs)  # subtract sinusoids from original sound
    stocEnv = stochasticModel.stochastic_model_anal(xr, H, H * 2, stocf)  # compute stochastic model of residual
    return tfreq, tmag, tphase, stocEnv


def sps_models_synth(tfreq, tmag, tphase, stocEnv, N, H, fs):
    """
    Synthesis of a sound using the sinusoidal plus stochastic model
    tfreq, tmag, tphase: sinusoidal frequencies, amplitudes and phases; stocEnv: stochastic envelope
    N: synthesis FFT size; H: hop size, fs: sampling rate
    returns y: output sound, ys: sinusoidal component, yst: stochastic component
    """

    ys = sineModel.sine_model_synth(tfreq, tmag, tphase, N, H, fs)  # synthesize sinusoids
    yst = stochasticModel.stochastic_model_synth(stocEnv, H, H * 2)  # synthesize stochastic residual
    y = ys[:min(ys.size, yst.size)] + yst[:min(ys.size, yst.size)]  # sum sinusoids and stochastic components
    return y, ys, yst