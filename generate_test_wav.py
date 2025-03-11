import wave
import struct
import math

def generate_test_wav(filename="test_mono.wav", duration=2.0, freq=440.0, sample_rate=44100, amplitude=0.5):
    """
    Generate a test mono WAV file with a sine wave
    
    Parameters:
    filename (str): Output filename
    duration (float): Length of the audio in seconds
    freq (float): Frequency of the sine wave in Hz
    sample_rate (int): Sample rate in Hz
    amplitude (float): Amplitude of the sine wave (0.0 to 1.0)
    """
    # Calculate the number of frames
    num_frames = int(duration * sample_rate)
    
    # Create a sine wave
    samples = []
    for i in range(num_frames):
        t = i / sample_rate  # Time in seconds
        # Generate a sine wave
        value = amplitude * math.sin(2 * math.pi * freq * t)
        # Convert to 16-bit PCM
        sample = int(value * 32767)
        samples.append(sample)
    
    # Open a new WAV file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters
        # nchannels, sampwidth, framerate, nframes, comptype, compname
        wav_file.setparams((1, 2, sample_rate, num_frames, 'NONE', 'not compressed'))
        
        # Convert samples to byte data
        sample_data = struct.pack('<' + 'h' * num_frames, *samples)
        wav_file.writeframes(sample_data)
    
    print(f"Created test mono WAV file: {filename}")
    print(f"Duration: {duration} seconds")
    print(f"Frequency: {freq} Hz")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Number of samples: {num_frames}")

# Generate a test mono WAV file
if __name__ == "__main__":
    generate_test_wav()
    
    # You can also generate different test files
    generate_test_wav("low_tone.wav", freq=220.0)
    generate_test_wav("high_tone.wav", freq=880.0)
    generate_test_wav("quiet_tone.wav", amplitude=0.1)
    generate_test_wav("loud_tone.wav", amplitude=0.9)