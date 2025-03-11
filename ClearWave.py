import math
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
            
            print(f"Loaded WAV file: {len(samples)} samples, {sample_rate}Hz, {bits_per_sample}-bit, max_value= {self.max_value}, min_value= {self.min_value} ")
            
    def write_wav_file(self, filename):
        """Write the processed audio data to a new WAV file"""
        channels = self.header['channels']
        sample_rate = self.header['sample_rate']
        bits_per_sample = self.header['bits_per_sample']
        
        bytes_per_sample = bits_per_sample // 8
        byte_rate = sample_rate * channels * bytes_per_sample
        block_align = channels * bytes_per_sample
        
        # Convert samples to bytes
        data_bytes = bytearray()
        for sample in self.samples:
            data_bytes.extend(sample.to_bytes(bytes_per_sample, byteorder='little', signed=True))
        
        data_size = len(data_bytes)
        file_size = 36 + data_size
        
        with open(filename, 'wb') as file:
            # Write RIFF header
            file.write(b'RIFF')
            file.write(file_size.to_bytes(4, byteorder='little'))
            file.write(b'WAVE')
            
            # Write fmt chunk
            file.write(b'fmt ')
            file.write((16).to_bytes(4, byteorder='little'))  # Chunk size
            file.write((1).to_bytes(2, byteorder='little'))   # PCM format
            file.write(channels.to_bytes(2, byteorder='little'))
            file.write(sample_rate.to_bytes(4, byteorder='little'))
            file.write(byte_rate.to_bytes(4, byteorder='little'))
            file.write(block_align.to_bytes(2, byteorder='little'))
            file.write(bits_per_sample.to_bytes(2, byteorder='little'))
            
            # Write data chunk
            file.write(b'data')
            file.write(data_size.to_bytes(4, byteorder='little'))
            file.write(data_bytes)
        
        print(f"Written enhanced audio to {filename}")
        
    def amplify(self, gain_factor=2.0):
        """Apply amplification to the audio samples"""
        print(f"Applying amplification with gain factor: {gain_factor}")

        print("Before amplification (first 10 samples):", self.samples[:10])

        amplified = []
        for sample in self.samples:
            # Appliquer le gain et écrêter uniquement si nécessaire
            new_sample = int(sample * gain_factor)
            new_sample = max(min(new_sample, self.max_value), self.min_value)
            amplified.append(new_sample)

        self.samples = amplified

        print("After amplification (first 10 samples):", self.samples[:10])

        return self

    def anti_distortion(self, threshold=0.8):
        """Apply soft clipping to prevent harsh distortion"""
        print(f"Applying anti-distortion with threshold: {threshold}")
        
        print("Before anti-distortion (first 10 samples):", self.samples[:10])
        
        threshold_value = int(self.max_value * threshold)
        
        processed = []
        for sample in self.samples:
            if abs(sample) > threshold_value:
                # Apply soft clipping using a tanh-like function
                sign = 1 if sample > 0 else -1
                # Map to 0-1 range
                normalized = abs(sample) / self.max_value
                # Apply soft curve
                if normalized > threshold:
                    normalized = threshold + (1 - threshold) * math.tanh((normalized - threshold) / (1 - threshold))
                # Map back to sample range
                processed_sample = int(sign * normalized * self.max_value)
                processed.append(processed_sample)
            else:
                processed.append(sample)
        
        self.samples = processed
        
        print("After anti-distortion (first 10 samples):", processed[:10])
        
        return self
    
    def reduce_noise(self, threshold_db=-60):
        """Simple noise gate to reduce background noise"""
        print(f"Applying noise reduction with threshold: {threshold_db}dB")
        
        # Convert threshold from dB to linear
        threshold = self.max_value * (10 ** (threshold_db / 20))
        
        # Calculate noise profile from "silent" portions
        noise_samples = [abs(s) for s in self.samples if abs(s) < threshold]
        if noise_samples:
            noise_floor = sum(noise_samples) / len(noise_samples)
        else:
            noise_floor = 0
        
        print(f"Detected noise floor: {noise_floor}")
        
        # Apply noise reduction
        processed = []
        
        # For a simple version, we'll use a basic noise gate with a release tail
        release_time = int(self.header['sample_rate'] * 0.1)  # 100ms release
        gate_open = False
        remaining_release = 0
        
        for sample in self.samples:
            if abs(sample) > noise_floor * 2:
                # Signal above threshold, open gate
                gate_open = True
                remaining_release = release_time
                processed.append(sample)
            elif gate_open and remaining_release > 0:
                # In release phase
                attenuation = remaining_release / release_time
                processed.append(int(sample * attenuation))
                remaining_release -= 1
            else:
                # Gate closed
                gate_open = False
                # Attenuate but don't completely remove
                processed.append(int(sample * 0.1))
        
        self.samples = processed
        return self
    
    def reduce_noise_with_reference(self, noise_file):
        
        print(f"Applying noise reduction using reference file: {noise_file}")
        
        # Create a temporary ClearWaveAudio instance to load the noise file
        noise_audio = ClearWaveAudio()
        noise_audio.read_wav_file(noise_file)
        
        # Check if the audio formats are compatible
        if (self.header['sample_rate'] != noise_audio.header['sample_rate'] or 
            self.header['bits_per_sample'] != noise_audio.header['bits_per_sample']):
            print("Warning: Noise file has different format than the main audio file")
        
        # Create a noise profile (frequency spectrum) from the noise file
        # For a simple approach, we'll just calculate the average magnitude of noise
        noise_profile = sum(abs(sample) for sample in noise_audio.samples) / len(noise_audio.samples)
        print(f"Calculated noise profile with average magnitude: {noise_profile}")
        
        # Apply spectral subtraction (simplified version)
        # In a real implementation, this would use FFT for frequency-domain processing
        processed = []
        for sample in self.samples:
            # Simple noise reduction: if the sample is below the noise profile threshold,
            # reduce it significantly. If it's above, reduce it by a smaller amount.
            if abs(sample) <= noise_profile * 1.5:
                # Reduce noise significantly (80%)
                new_sample = int(sample * 0.2)
            else:
                # For signal above noise floor, apply gentler reduction
                # The amount of reduction decreases as the signal gets stronger
                ratio = min(1.0, (abs(sample) - noise_profile) / (self.max_value - noise_profile))
                reduction_factor = 0.2 + (0.8 * ratio)
                new_sample = int(sample * reduction_factor)
            
            processed.append(new_sample)
        
        self.samples = processed
        print(f"Noise reduction complete using '{noise_file}' as reference")
        return self