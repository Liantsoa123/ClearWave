import sys

from ClearWave import ClearWaveAudio

def main():
    if len(sys.argv) < 3:
        print("Usage: python ClearWaceAudio.py input.wav output.wav")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    processor = ClearWaveAudio()
    
    try:
        processor.read_wav_file(input_file)
        max_sample = max(abs(min(processor.samples)), abs(max(processor.samples)))
        print(f"Maximum sample value before processing: {max_sample}")
        # Apply processing chain
        #processor.amplify(2)                 # Moderate amplification
        processor.anti_distortion(0.5)       # Anti-distortion
        processor.write_wav_file(output_file)
        print("ClearWave processing completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()