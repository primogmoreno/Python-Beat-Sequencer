import sys
import time
import wave

import numpy as np
import pyaudio


FRAMERATE = 44100
NCHANNELS = 1


class Player:
    """Opens an audio stream and plays/mixes sounds
    """
    def __init__(self):
        p = pyaudio.PyAudio()
        self.audio = np.empty(0, dtype=np.float32)
        self.stream = p.open(format=pyaudio.paFloat32,
                             channels=NCHANNELS,
                             rate=FRAMERATE,
                             output=True,
                             stream_callback=self._player_callback)

    def _player_callback(self, in_data, frame_count, time_info, status):
        frames = self.audio[:frame_count]
        self.audio = self.audio[frame_count:]
        frames = np.append(frames, np.zeros(frame_count - len(frames))).astype(np.float32)
        return (frames, pyaudio.paContinue)

    def mix_sound(self, sound, at_frame=0):
        """Mix a sound into the audio stream
        """
        n = len(sound.data) - len(self.audio)
        if n > 0:
            self.audio = np.append(self.audio, np.zeros(n))
        self.audio[0:len(sound.data)] += sound.data


class Sound:
    """Base class for holding audio data
    """
    
    def play(self, player):
        """Plays the Sound on the named player
        """
        player.mix_sound(self)
    
    
class SoundFile(Sound):
    """A sound with audio data from a file
    """
    def __init__(self, file):
        """Create a new sound based on file
        file must be 16-bit, 44100Hz, mono .wav
        """
        with wave.open(file, 'rb') as wf:
            buf = wf.readframes(wf.getnframes())
            self.data = (np.frombuffer(buf, dtype=np.int16) / 65535).astype(np.float32)
            
    def trim(self, start=0.0, end=0.0):
        """Remove data from the start and/or end of a file"""
        index_start = start * FRAMERATE
        index_end = len(self.data) - end * FRAMERATE
        self.data = self.data[index_start:index_end]
        
    
class Tone(Sound):
    """Sound with audio data based on mathematical waveforms
    """

    def __init__(self, shape, frequency=440.0, duration=1.0):
        """Creates a new tone
    
        Parameters:
        shape (str): the type of tone to create
        frequency (float): the fundamental frequency of the tone
        duration (float): the length of the tone in seconds
        """
        t = np.linspace(0, duration, int(FRAMERATE * duration))
        if shape == 'sine':
            self.data = (0.5 * np.sin(2 * np.pi * frequency * t))
        elif shape == 'saw':
            self.data = 0.5 * (t * frequency - np.floor(t * frequency + 0.5))
        elif shape == 'square':
            self.data = 0.3 * np.sign(np.sin(2 * np.pi * frequency * t))
        elif tone == 'bass':
            self.data = Sound('sine', frequency, duration).data
            self.apply_adsr(0.0, 0.1, 0.2, 0.3)
        elif tone == 'strings':
            self.data = Sound('saw', frequency, duration).data
            self.apply_adsr(0.3, 0.31, 1, 0.4)
        elif tone == 'vibes':
            self.data = Sound('square', frequency, duration).data
            self.apply_adsr(0.5, 0.5, 1, 0.5)

    def apply_adsr(self, attack, decay, sustain, release):
        """Apply an ADSR amplitude envelope to a tone

        Parameters:
        attack (float): fraction of sound duration to reach max volume
        decay (float): fraction of sound duration to drop from max volume to sustain level
        sustain (float): sustain level as a fraction of max volume
        release (float): fraction of sound duration at which to start decreasing volume to zero
        """
        n = len(self.data)
        env = np.linspace(0, 1, int(attack * n))
        env = np.append(env, np.linspace(1, sustain, int((decay - attack) * n)))
        env = np.append(env, np.full(int((release - decay) * n), sustain))
        env = np.append(env, np.linspace(sustain, 0, int((1.0 - release) * n)))
        if len(env) < n:
            env = np.append(env, np.zeros(n - len(env)))
        self.data *= env[:n]


if __name__ == '__main__':

    print("This is a test. If you hear three zaps, it works!")
    player = Player()
    zap_sound = SoundFile('zap.wav')
    for i in range(3):
        zap_sound.play(player)
        time.sleep(0.5)

