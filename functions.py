################################################
################# Imports ######################
################################################
import numpy as np
import pygame
import wave
################################################
################# Functions ####################
################################################

def customHanning(M, floor):
    """ 
    this is a function to create a custom hanning window with a non-zero floor, specified by the variable 'floor'
    for example floor = 0.2 means creating a hanning window with values between .2 and 1
    """
    a = 0.5 + 0.5*floor
    b = 0.5 - 0.5*floor
    M = int(M)
    hanning_window = [a - b*np.cos(2 * x * np.pi /(M-1)) for x in range(M)]

    return hanning_window

def sine_gen(dur, freq, amp, sr, chans):
    """ 
    dur = duration of tone
    freq = frequency (in Hz)
    amp = amplitude of tone... range of −32,768 to +32,767 range for 16bit
    sr = sample rate in Hz (e.g. 44100 standard)
    chans = stereo (2) or mono (1) (mono: sound played identically in both channels)
    """
    # calculate the total amount of cycles in the SOUNDLEN
    ncycles = dur * freq

    # calculate the total amount of samples per SOUNDLEN
    nsamples = dur * sr

    # calculate samples per cycle
    spc = nsamples / ncycles

    # stepsize: distance between samples within a cycle
    stepsize = (2*np.pi) / spc

    # create a range of numbers between 0 and 2*pi
    x = np.arange(0, 2*np.pi, stepsize)

    # make a sine wave out of the range
    sine = np.sin(x)

    # increase the amplitude
    sine = sine * amp 

    # repeat the sine wave for the length of the tone
    tone = np.tile(sine, int(ncycles))

    return tone


def amp_mod(risefall_ratio, win_floor, tone):
    """ 
    applies amplitude modulation on a sound (default using a custom Hanning Window)
    
    risefall_ratio = ratio between risetime and falltime e.g. value of  10 = 1(rise):10(fall)
    win_floor = amplitude modulation depth e.g. (between 0 and 1)
    tone = the input sound to appply modulation on

    ## note requires function customHanning()
    """

    # calculate asymmetric Hanning vector (22ms rise and 394 fall)
    riseLen = len(tone) / risefall_ratio
    fallLen = len(tone) - riseLen         

    # create Hann vector for rise len * 2
    riseVec = customHanning((riseLen * 2), win_floor)
    # delete second half of vector (after 1.0)... i.e. only want upramp
    riseVec = riseVec[0:int(riseLen)]

    # create Hann vector for fall len * 2
    fallVec = customHanning((fallLen * 2), win_floor)
    # delete first half of vector
    fallVec = fallVec[int(fallLen)-1:]

    # combine vectors
    hannVec = np.concatenate((riseVec, fallVec),)

    if len(hannVec) > len(tone):    # check for rounding problems with hannVec length
       hannVec = hannVec[0:len(tone)]

    # apply Hanning amplitude modulation
    mod_tone = tone * hannVec
    mod_tone = list(mod_tone)
    return mod_tone

def export_wav(filename, tone1, order, sr, chan, bit_depth, tone2=None,tone3=None):
    """
    filename  = e.g. "motorbike" (".wav" gets added automatically)
    tone1     = base level accent tone, tone2 =  2nd level accent, tone3 = 3rd level accent
    order     = vector indicating in what order tones occur in. e.g. [1 0 2]
    sr        = samplerate e.g. 44100
    chan      = 1 = mono, 2 = stereo
    bit_depth = 2 = 16bit depth (e.g. 2 x 8 bit)
    """
    
    tones = (tone1, tone2, tone3)
    # tile tones to the desired length
    seq = [] # initialising
    for i in order:
        seq = seq + tones[i]

    final_output = np.array(seq) # convert to  np.array
    
    #np.tile(meter, int(nTones/2))

    # initialise mixer module (it requires the sampxling rate and num of channels)
    pygame.mixer.init(frequency=sr, channels=chan)

    # create sound out of the allsines vector
    tone = pygame.mixer.Sound(final_output.astype('int16'))

    # open new wave file objects
    tonefile = wave.open(filename + '.wav', 'w')

    # set parameters for pure tone
    tonefile.setframerate(sr)
    tonefile.setnchannels(chan)
    tonefile.setsampwidth(bit_depth) # in units of bytes and 8 bits per byte = 16bit

    # get buffers
    tonebuffer = tone.get_raw()

    # write raw buffer to the wave file
    tonefile.writeframesraw(tonebuffer)

    # close the wave file 
    tonefile.close()

    return None
