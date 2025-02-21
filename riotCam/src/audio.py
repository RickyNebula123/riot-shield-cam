import wave
import sys
import pyaudio

p = pyaudio.PyAudio()
target_device_name: str = 'USB PnP Sound'

def find_mic_index() -> int:
    for i in range(p.get_device_count()):
        if p.get_device_info_by_index(i)['name'].startswith(target_device_name):
            return i
        
    raise ValueError('No recording device found!')

def bg_record():
    CHUNK: int = 1024
    FORMAT: int = pyaudio.paInt16
    CHANNELS: int = 1
    RATE: int = 44100
    
    FILENAME: str = 'background.wav'
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
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
    
    # Keep recording until a key is pressed
    input('Recording in the background... Press any key to stop.')
    
    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    
    print(f'Recording saved as: [{FILENAME}]')
           
def test():
    CHUNK: int = 1024
    FORMAT: int = pyaudio.paInt16
    CHANNELS: int = 1
    RATE: int = 44100
    RECORD_SECONDS: int = 5

    with wave.open('output.wav', 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
        
        print('Recording...')
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))
        print('Done')
        
        stream.close()
        p.terminate()
    
    
bg_record()    
    
    
    
    

