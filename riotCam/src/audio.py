import wave
import sys
import pyaudio

# Package level constants
CHUNK:    int = 1024
FORMAT:   int = pyaudio.paInt16
RATE:     int = 44100
CHANNELS: int = 1  
FILENAME: str = 'background.wav'

# Initialize Pyaudio
p = pyaudio.PyAudio()
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
    for i in range(p.get_device_count()):
        if p.get_device_info_by_index(i)['name'].startswith(target_device_name):
            return i
        
    raise ValueError('No recording device found!')

def record_audio() -> tuple[pyaudio.PyAudio.Stream, wave.Wave_write]:
    '''
    Starts recording and writing audio using the globally defined
    pyaudio object p.
    
    Returns:
        Tuple containing relevant classes that can
        access the file descriptors.
    '''
    # Open WAV file for writing
    wf = wave.open(FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    
    # Callback function to write directly to the file
    def audio_callback(in_data, frame_count, time_info, status):
        wf.writeframes(in_data) # Write the chunk directly to the file
        return (in_data, pyaudio.paContinue)
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=find_mic_index(),
                    stream_callback=audio_callback)
    #Start the stream
    stream.start_stream()
    
    return (stream, wf)

def stop_recording_audio(stream: pyaudio.PyAudio.Stream, wf: wave.Wave_write):
    # Keep recording until a key is pressed
    input('Recording in the background... Press any key to stop.')
    
    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    
    print(f'Recording saved as: [{FILENAME}]')
    
stream, wf = record_audio()
stop_recording_audio(stream, wf)
    
    
    
    

