import sys
import wave
import pyaudio

# Package level constants
CHUNK:    int = 1024
FORMAT:   int = pyaudio.paInt16
RATE:     int = 48000
CHANNELS: int = 1  

class Microphone():
    def __init__(self):
        self.mic = pyaudio.PyAudio()
        self.stream = None
        self.wave_descriptor = None
        self.target_device_name: str = 'USB PnP Sound'

    def find_mic_index(self) -> int:
        '''
        This function finds the index of our recording device
        using the pyaudio library.

        Returns:
            int: Index of the sound device.
            
        Raises:
            Value Error: If no recording device is found
        '''
        for i in range(self.mic.get_device_count()):
            if self.mic.get_device_info_by_index(i)['name'].startswith(self.target_device_name):
                return i
            
        raise ValueError('No recording device found!')

    def record_audio(self, filename: str):
        '''
        Starts recording and writing audio using the globally defined
        pyaudio object microphone.
        
        Returns:
            Tuple containing relevant classes that can
            access the file descriptors.
        '''
        # Open WAV file for writing
        self.wave_descriptor = wave.open(filename + '.wav', 'wb')
        self.wave_descriptor.setnchannels(CHANNELS)
        self.wave_descriptor.setsampwidth(self.mic.get_sample_size(FORMAT))
        self.wave_descriptor.setframerate(RATE)
        
        # Callback function to write directly to the file
        def audio_callback(in_data, frame_count, time_info, status):
            self.wave_descriptor.writeframes(in_data) # Write the chunk directly to the file
            return (in_data, pyaudio.paContinue)
        
        self.stream = self.mic.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=self.find_mic_index(),
                        stream_callback=audio_callback)
        #Start the stream
        self.stream.start_stream()

    def stop_recording_audio(self):
        # Clean up
        self.stream.stop_stream()
        self.stream.close()
        self.wave_descriptor.close()
