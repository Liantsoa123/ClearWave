class ClearWaveAudio:
    def __init__(self):
        self.header = {}
        self.samples = []
        self.bits_per_sample = 0
        self.max_value = 0
    
    def read_wav_file(self, filename):
        """Read and parse a WAV file"""
        with open(filename, 'rb') as file:
            # Read RIFF header
            riff = file.read(4)
            if riff != b'RIFF':
                raise ValueError("Not a valid WAV file")
            
            # Read file size (minus 8 bytes)
            file_size = int.from_bytes(file.read(4), byteorder='little')
            
            # Read WAVE format
            wave = file.read(4)
            if wave != b'WAVE':
                raise ValueError("Not a valid WAV file")
            
            # Read fmt chunk
            fmt = file.read(4)
            if fmt != b'fmt ':
                raise ValueError("Not a valid WAV file")
            
            # Read chunk size
            chunk_size = int.from_bytes(file.read(4), byteorder='little')
            
            # Read audio format
            audio_format = int.from_bytes(file.read(2), byteorder='little')
            
            # Read number of channels
            channels = int.from_bytes(file.read(2), byteorder='little')
            if channels != 1:
                print("Warning: This file is not mono. Only the first channel will be processed.")
            
            # Read sample rate
            sample_rate = int.from_bytes(file.read(4), byteorder='little')
            
            # Read byte rate
            byte_rate = int.from_bytes(file.read(4), byteorder='little')
            
            # Read block align
            block_align = int.from_bytes(file.read(2), byteorder='little')
            
            # Read bits per sample
            bits_per_sample = int.from_bytes(file.read(2), byteorder='little')
            
            # Skip any extra parameters in fmt chunk
            if chunk_size > 16:
                file.read(chunk_size - 16)
            
            # Look for data chunk
            while True:
                chunk_id = file.read(4)
                if not chunk_id:
                    raise ValueError("No data chunk found")
                
                if chunk_id == b'data':
                    break
                
                # Skip this chunk
                chunk_size = int.from_bytes(file.read(4), byteorder='little')
                file.read(chunk_size)
            
            # Read data size
            data_size = int.from_bytes(file.read(4), byteorder='little')
            
            # Read audio data
            audio_data = file.read(data_size)
            
            # Convert to samples
            samples = []
            bytes_per_sample = bits_per_sample // 8
            for i in range(0, len(audio_data), bytes_per_sample * channels):
                sample = int.from_bytes(audio_data[i:i+bytes_per_sample], byteorder='little', signed=True)
                samples.append(sample)
            
            self.header = {
                'channels': channels,
                'sample_rate': sample_rate,
                'bits_per_sample': bits_per_sample,
                'byte_rate': byte_rate,
                'block_align': block_align
            }
            self.samples = samples
            self.bits_per_sample = bits_per_sample
            self.max_value = 2**(bits_per_sample - 1) - 1
            self.min_value = -2**(bits_per_sample - 1)
            
            print(f"Loaded WAV file: {len(samples)} samples, {sample_rate}Hz, {bits_per_sample}-bit")