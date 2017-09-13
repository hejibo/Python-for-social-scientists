import wave
import numpy
import pygame

# maximal sound amplitude and sampling rate
MAXAMP =  16383
SAMPLERATE = 48000

# mono
NCHANNELS = 1

# sound length (seconds) and frequency (Herz)
SOUNDLEN = 3.0
SOUNDFREQ = 1000

# calculate the total amount of cycles
ncycles = SOUNDLEN * SOUNDFREQ

# calculate the total amount of samples
nsamples = SOUNDLEN * SAMPLERATE
# calculate the number of samples per cycle
spc = nsamples / ncycles

# the stepsize is the distance between samples within a cycle
# (divide the range by the amount of samples per cycle)
stepsize = (2*numpy.pi) / spc
# create a range of numbers between 0 and 2*pi
x = numpy.arange(0, 2*numpy.pi, stepsize)
# make a sine wave out of the range
sine = numpy.sin(x)

# increase the sine wave's amplitude
sine = sine * MAXAMP

# repeat the sine wave!
allsines = numpy.tile(sine, int(ncycles))

# initialise the mixer module
# (it requires the sampling rate and the number of channels)
pygame.mixer.init(frequency=SAMPLERATE, channels=NCHANNELS)

# now create a sound out of the allsines vector
tone = pygame.mixer.Sound(allsines.astype('int16'))

# play the sinusoid sound
tone.play()

# create a series of random numbers
noise = numpy.random.rand(SOUNDLEN * SAMPLERATE)

# correct the value range (-1 to 1)
noise = (noise * 2) - 1

# increase the noise's amplitude
noise = noise * MAXAMP

# turn the noise vector into a sound
whitenoise = pygame.mixer.Sound(noise.astype('int16'))

# play the noise sound
whitenoise.play()

# open new wave file objects
tonefile = wave.open('pure_tone.wav', 'w')
noisefile = wave.open('noise.wav', 'w')

# set parameters for the pure tone
tonefile.setframerate(SAMPLERATE)
tonefile.setnchannels(NCHANNELS)
tonefile.setsampwidth(2)

# set the same parameters for the noise
noisefile.setframerate(SAMPLERATE)
noisefile.setnchannels(NCHANNELS)
noisefile.setsampwidth(2)

# get buffers
tonebuffer = tone.get_buffer()
noisebuffer = whitenoise.get_buffer()
# write raw buffer to the wave file
tonefile.writeframesraw(tonebuffer.raw)
noisefile.writeframesraw(noisebuffer.raw)

# neatly close the wave file objects
tonefile.close()
noisefile.close()