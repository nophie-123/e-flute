# functions that implement analysis and synthesis of sounds using the Harmonic plus Stochastic Model
# (for example usage check the examples models_interface)

import harmonicModel
import sineModel
import stochasticModel
import utilFunctions


def hps_model_anal(x, fs, w, N, H, t, nH, minf0, maxf0, f0et, harmDevSlope, minSineDur, Ns, stocf):
    """
    Analysis of a sound using the harmonic plus stochastic model
    x: input sound, fs: sampling rate, w: analysis window; N: FFT size, t: threshold in negative dB,
    nH: maximum number of harmonics, minf0: minimum f0 frequency in Hz,
    maxf0: maximim f0 frequency in Hz; f0et: error threshold in the f0 detection (ex: 5),
    harmDevSlope: slope of harmonic deviation; minSineDur: minimum length of harmonics
    returns hfreq, hmag, hphase: harmonic frequencies, magnitude and phases; stocEnv: stochastic residual
    """

    # perform harmonic analysis
    hfreq, hmag, hphase = harmonicModel.harmonic_model_anal(x, fs, w, N, H, t, nH, minf0, maxf0, f0et, harmDevSlope, minSineDur)
    # subtract sinusoids from original sound
    xr = utilFunctions.sineSubtraction(x, Ns, H, hfreq, hmag, hphase, fs)
    # perform stochastic analysis of residual
    stocEnv = stochasticModel.stochastic_model_anal(xr, H, H * 2, stocf)
    return hfreq, hmag, hphase, stocEnv


def hps_model_synth(hfreq, hmag, hphase, stocEnv, N, H, fs):
    """
    Synthesis of a sound using the harmonic plus stochastic model
    hfreq, hmag: harmonic frequencies and amplitudes; stocEnv: stochastic envelope
    Ns: synthesis FFT size; H: hop size, fs: sampling rate
    returns y: output sound, yh: harmonic component, yst: stochastic component
    """

    yh = sineModel.sine_model_synth(hfreq, hmag, hphase, N, H, fs)  # synthesize harmonics
    yst = stochasticModel.stochastic_model_synth(stocEnv, H, H * 2)  # synthesize stochastic residual
    y = yh[:min(yh.size, yst.size)] + yst[:min(yh.size, yst.size)]  # sum harmonic and stochastic components
    return y, yh, yst