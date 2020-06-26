import numpy
import math
from matplotlib import pyplot
from scipy.signal.windows import hann
from scipy.io.wavfile import write as wav_write

fs = 44100


def signal_ramp(n, percent):
    if percent > 49: percent = 49
    length = int(numpy.floor((n * percent) / 100))
    window = hann(length * 2 + 1)
    window = window - numpy.min(window)
    window = window / numpy.max(window)
    left = window[0:length + 1]
    right = window[length:]
    buffer = numpy.ones(n - 2 * left.size)
    total = numpy.hstack((left, buffer, right))
    return total


def make_pip(duration, frequency):
    pip_samples = math.ceil(fs * duration)
    time_axis = numpy.linspace(0, duration, pip_samples)
    wave = numpy.sin(2 * math.pi * frequency * time_axis)
    window = signal_ramp(pip_samples, 5)
    wave = wave * window
    return wave


pip = make_pip(0.25, 1000)
silence = make_pip(0.1, 0) * 0

sound = numpy.concatenate((pip, silence))
wav_write('pip.wav', fs, sound)
