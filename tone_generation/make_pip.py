import numpy
import math
from matplotlib import pyplot
from scipy.signal.windows import hann
from scipy.io.wavfile import write as wav_write
from scipy.signal import butter, lfilter

fs = 44100

class HighPassFilter:
    def __init__(self, cutoff, fs, order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        self.b, self.a = butter(order, normal_cutoff, btype='high', analog=False)

    def run(self, signal):
        y = lfilter(self.b, self.a, signal)
        return y



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


def make_burst(duration):
    pip_samples = math.ceil(fs * duration)
    #wave = (numpy.random.random(pip_samples) * 2) - 1
    wave = numpy.random.normal(size=pip_samples)
    window = signal_ramp(pip_samples, 5)
    wave = wave * window
    return wave


repeats = 10
silence = make_pip(0.25, 0) * 0
hp_filter = HighPassFilter(3000, fs, 6)
parts = []
for i in range(repeats):
    burst = make_burst(0.5)
    burst = hp_filter.run(burst)
    parts.append(burst)
    parts.append(silence)

sound = numpy.concatenate(parts)

pyplot.plot(sound)
pyplot.show()

wav_write('pip.wav', fs, sound)

# pip = make_pip(0.25, 1000)

#
#sound = numpy.concatenate((pip, silence))

