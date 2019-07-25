#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Kiotlin
# DATE: 2019/07/24 
# TIME: 23:09:44

# DESCRIPTION: Music files format convertor

import os
from pydub import AudioSegment
from midi2audio import FluidSynth

class Convertor:
    def __init__(self, file):
        self.source_file = file
        self.format = self.source_file.split('.')[-1]
        self.file_name = self.source_file.split('.')[0]

    def convert_to_mp3(self, dir="./export"):
        source_file = AudioSegment.from_file(self.source_file, format=self.format)
        mp3_file = source_file.export(f'{dir}/{self.file_name}.mp3', format="mp3")

    def convert_to_wav(self, dir="./export"):
        source_file = AudioSegment.from_file(self.source_file, format=self.format)
        wav_file = source_file.export(f'{dir}/{self.file_name}.wav', format="wav")

    def convert_to_3gp(self, dir="./export"):
        source_file = AudioSegment.from_file(self.source_file, format=self.format)
        _3gp_file = source_file.export(f'{dir}/{self.file_name}.3gp', format="3gp")
    
    def convert_to_ogg(self, dir="./export"):
        source_file = AudioSegment.from_file(self.source_file, format=self.format)
        ogg_file = source_file.export(f'{dir}/{self.file_name}.ogg', format="ogg")

    def convert_to_aac(self, dir="./export"):
        source_file = AudioSegment.from_file(self.source_file, format=self.format)
        aac_file = source_file.export(f'{dir}/{self.file_name}.aac', format="aac")
    
    def convert_midi_to_audio(self, dir="./export"):
        fs = FluidSynth()
        wav_file = fs.midi_to_audio(self.source_file, f'{dir}/{self.file_name}.wav')

    

if __name__ == '__main__':
    file_ = input('Input a music file: ')
    converter = Convertor(file_)