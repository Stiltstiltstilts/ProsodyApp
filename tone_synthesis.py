################################################
################# Imports ######################
################################################

import wave
import pygame
import numpy as np
import functions as fun
from word_table_creator import stress_dict, uniques

################################################=
################# Parameters ###################
################################################

AMP1 = 10000 # amplitude of nonaccented tone... −32,768 to +32,767 range for 16bit
AMP2 = 28000 # amplitude of accented tone... −32,768 to +32,767 range for 16bit
SR = 44100  # Hz
NCHAN = 1 # mono: sound played identically in both channels
DUR1 = .15 # durations in seconds
DUR2 = .25 # durations in seconds
FREQ = 333 # Hz... 333 is about Ab in pitch

nTones = 3
finalDuration = DUR1 * nTones


rise_fall_ratio1 = 10  # rise_fall_ratio:1 ratio of rise and fall ramps
rise_fall_ratio2 = 18
window_floor = 0.2 # creating window between .2 and 1

################################################
############## Stimulus creation ###############
################################################

tone1 = fun.sine_gen(DUR1, FREQ, AMP1, SR, NCHAN)
tone1 = fun.amp_mod(rise_fall_ratio1, window_floor, tone1)

tone2 = fun.sine_gen(DUR2, FREQ, AMP2, SR, NCHAN)
tone2 = fun.amp_mod(rise_fall_ratio1, window_floor, tone2)

tone3 = fun.amp_mod(rise_fall_ratio2, window_floor, tone2)


################################################
######### Combination mixing and export ########
################################################

# produce soundfile for all unique stress patterns
for stressi in uniques:
    #filename = ''
    #for i in range(len(stressi)):
    #    filename += str(stressi[i])
    fun.export_wav(stressi[1], tone1, stressi[0], SR, NCHAN, 2, tone2, tone3)

# Done!
