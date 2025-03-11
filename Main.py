import sys
from ClearWave import ClearWaveAudio

def print_menu():
    print("\nClearWave Audio Processing Options:")
    print("1. Amplification")
    print("2. Anti-distortion")
    print("3. Noise reduction (threshold)")
    print("4. Noise reduction (reference file)")
    print("5. Change playback speed")
    print("6. Save and exit")
    print("0. Exit without saving")
    return input("Choose an option (0-6): ")

def main():
    if len(sys.argv) < 3:
        print("Usage: python ClearWaveAudio.py input.wav output.wav")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    processor = ClearWaveAudio()
    
    try:
        processor.read_wav_file(input_file)
        max_sample = max(abs(min(processor.samples)), abs(max(processor.samples)))
        print(f"Maximum sample value before processing: {max_sample}")
        
        while True:
            choice = print_menu()
            
            if choice == "0":
                print("Exiting without saving...")
                return
            
            elif choice == "1":
                gain = float(input("Enter amplification factor (default=2.0): ") or "2.0")
                limit_choice = input("Apply limiting to prevent clipping? (y/n, default=n): ").lower()
                no_limit = limit_choice != 'y'  # Default to no limiting
                processor.amplify(gain, no_limit)
            
            elif choice == "2":
                threshold = float(input("Enter anti-distortion threshold (0-1, default=0.8): ") or "0.8")
                processor.anti_distortion(threshold)
            
            elif choice == "3":
                threshold_db = float(input("Enter noise reduction threshold in dB (default=-50): ") or "-50")
                processor.reduce_noise(threshold_db)
            
            elif choice == "4":
                noise_file = input("Enter path to noise reference file (WAV): ")
                if not noise_file:
                    print("No file entered. Operation cancelled.")
                    continue
                processor.reduce_noise_with_reference(noise_file)
            
            elif choice == "5":
                speed = float(input("Enter speed factor (e.g., 0.5=slower, 2.0=faster, default=1.0): ") or "1.0")
                processor.change_speed(speed)
            
            elif choice == "6":
                processor.write_wav_file(output_file)
                print("ClearWave processing completed successfully!")
                break
            
            else:
                print("Invalid option. Please choose between 0-6.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()