import wave
import sys
import pyaudio

# Local imports
import helpers

# Package level constants
CHUNK:    int = 1024
FORMAT:   int = pyaudio.paInt16
RATE:     int = 44100
CHANNELS: int = 1  

# Initialize Pyaudio
microphone = pyaudio.PyAudio()
target_device_name: str = 'USB PnP Sound'

def find_mic_index() -> int:
    '''
    This function finds the index of our recording device
    using the pyaudio library.

    Returns:
        int: Index of the sound device.
        
    Raises:
        Value Error: If no recording device is found
    '''
    for i in range(microphone.get_device_count()):
        if microphone.get_device_info_by_index(i)['name'].startswith(target_device_name):
            return i
        
    raise ValueError('No recording device found!')

def record_audio(filename: str) -> tuple[pyaudio.PyAudio.Stream, wave.Wave_write]:
    '''
    Starts recording and writing audio using the globally defined
    pyaudio object microphone.
    
    Returns:
        Tuple containing relevant classes that can
        access the file descriptors.
    '''
    # Open WAV file for writing
    wf = wave.open(filename+'.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(microphone.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    
    # Callback function to write directly to the file
    def audio_callback(in_data, frame_count, time_info, status):
        wf.writeframes(in_data) # Write the chunk directly to the file
        return (in_data, pyaudio.paContinue)
    
    audio_stream = microphone.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=find_mic_index(),
                    stream_callback=audio_callback)
    #Start the stream
    audio_stream.start_stream()
    return (audio_stream, wf)

def stop_recording_audio(stream: pyaudio.PyAudio.Stream, wf: wave.Wave_write):
    # Clean up
    stream.stop_stream()
    stream.close()
    wf.close()