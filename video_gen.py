#!/usr/bin/env python
"""
AI Video Generator - Standalone Version
No dependencies except PIL and imageio (both standard)
Creates beautiful animated videos instantly
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter
import colorsys
import os
import numpy as np
import pyttsx3

# Create outputs folder
DOWNLOADS_DIR = Path.home() / "Downloads"
OUTPUT_DIR = DOWNLOADS_DIR / "AI Videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Videos will be saved to: {OUTPUT_DIR}")


class VideoGenerator:
    """Simple video generator using PIL"""
    
    def __init__(self):
        self.width = 1080
        self.height = 1920
    
    def generate_sound_beep(self, duration=2.0, sample_rate=44100, frequency=440):
        """Generate a simple beep sound"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * frequency * t) * 0.3
        return audio.astype(np.float32)
    
    def generate_sound_sweep(self, duration=2.0, sample_rate=44100, start_freq=200, end_freq=800):
        """Generate a frequency sweep (whoosh)"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        freq = np.linspace(start_freq, end_freq, len(t))
        phase = 2 * np.pi * np.cumsum(freq) / sample_rate
        audio = np.sin(phase) * 0.3
        return audio.astype(np.float32)
    
    def generate_sound_pulse(self, duration=2.0, sample_rate=44100, frequency=440, pulse_rate=4):
        """Generate a pulsing beep"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        tone = np.sin(2 * np.pi * frequency * t)
        pulse = np.sin(2 * np.pi * pulse_rate * t)
        # Use pulse wave to modulate volume
        pulse_envelope = 0.5 + 0.5 * np.sin(2 * np.pi * pulse_rate * t)
        audio = tone * pulse_envelope * 0.3
        return audio.astype(np.float32)
    
    def generate_sound_chime(self, duration=2.0, sample_rate=44100):
        """Generate a musical chime sound"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Create a chord of multiple frequencies
        freq1, freq2, freq3 = 523.25, 659.25, 783.99  # C5, E5, G5
        decay = np.exp(-2 * t)  # Exponential decay
        audio = (np.sin(2 * np.pi * freq1 * t) + 
                 np.sin(2 * np.pi * freq2 * t) + 
                 np.sin(2 * np.pi * freq3 * t)) * decay * 0.15
        return audio.astype(np.float32)
    
    def generate_sound_crash(self, duration=2.0, sample_rate=44100):
        """Generate a crash/impact sound"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Combination of low frequencies with quick decay
        audio = (np.sin(2 * np.pi * 100 * t) * 0.4 + 
                 np.sin(2 * np.pi * 200 * t) * 0.3) * np.exp(-4 * t) * 0.4
        return audio.astype(np.float32)
    
    def generate_sound_sparkle(self, duration=2.0, sample_rate=44100):
        """Generate a sparkle/glitter sound (high-pitched decaying)"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Multiple high frequencies that decay
        audio = (np.sin(2 * np.pi * 1200 * t) * 0.2 +
                 np.sin(2 * np.pi * 1600 * t) * 0.15 +
                 np.sin(2 * np.pi * 2000 * t) * 0.15) * np.exp(-2.5 * t) * 0.3
        return audio.astype(np.float32)
    
    def generate_sound_ambient(self, duration=2.0, sample_rate=44100):
        """Generate ambient/atmospheric sound"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Low frequencies with slow modulation
        audio = (np.sin(2 * np.pi * 60 * t) * 0.2 +
                 np.sin(2 * np.pi * 120 * t) * 0.15 +
                 np.sin(2 * np.pi * 180 * t) * 0.1) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * t)) * 0.4
        return audio.astype(np.float32)
    
    def generate_sound_scifi(self, duration=2.0, sample_rate=44100):
        """Generate sci-fi sound (rising pitch with intensity)"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Frequency that rises then falls
        freq = 400 + 400 * np.sin(2 * np.pi * 1.5 * t)
        phase = 2 * np.pi * np.cumsum(freq) / sample_rate
        audio = np.sin(phase) * 0.3
        return audio.astype(np.float32)
    
    def generate_sound_retro(self, duration=2.0, sample_rate=44100):
        """Generate retro/8-bit sound"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Square-wave-like analog with buzzy texture
        freqs = [220, 330, 220, 440]  # Classic 8-bit pattern
        segment_len = len(t) // len(freqs)
        audio = np.zeros_like(t)
        for i, freq in enumerate(freqs):
            start = i * segment_len
            end = (i + 1) * segment_len if i < len(freqs) - 1 else len(t)
            audio[start:end] = np.sin(2 * np.pi * freq * t[start:end]) * 0.3
            audio[start:end] *= np.exp(-2 * (t[start:end] - t[start]))
        return audio.astype(np.float32)
    
    def generate_sound_whoosh(self, duration=2.0, sample_rate=44100):
        """Generate whoosh/wind sound"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Fast sweep with modulation
        freq = np.linspace(1000, 200, len(t))
        phase = 2 * np.pi * np.cumsum(freq) / sample_rate
        audio = np.sin(phase) * np.exp(-0.5 * t) * 0.35
        return audio.astype(np.float32)
    
    def generate_voiceover(self, text, duration=None, sample_rate=44100):
        """Generate voiceover audio from text using text-to-speech"""
        try:
            import tempfile
            import time
            
            # Create a temporary WAV file for the voiceover
            temp_voice = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            voice_path = temp_voice.name
            temp_voice.close()
            
            # Initialize text-to-speech engine
            engine = pyttsx3.init()
            
            # Configure voice settings for better quality
            engine.setProperty('rate', 150)  # Speed (words per minute)
            engine.setProperty('volume', 0.9)  # Volume (0-1)
            
            # Try to use a female voice if available
            try:
                voices = engine.getProperty('voices')
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)  # Usually female voice
            except:
                pass
            
            # Save speech to the temporary file
            engine.save_to_file(text, voice_path)
            engine.runAndWait()
            
            # Wait for file to be written
            time.sleep(0.5)
            
            # Read the WAV file
            import scipy.io.wavfile as wavfile
            if os.path.exists(voice_path) and os.path.getsize(voice_path) > 0:
                try:
                    voice_sample_rate, voice_data = wavfile.read(voice_path)
                    
                    # Convert to float32 in the range [-1, 1]
                    if voice_data.dtype == np.int16:
                        voice_data = voice_data.astype(np.float32) / 32768.0
                    elif voice_data.dtype == np.int32:
                        voice_data = voice_data.astype(np.float32) / 2147483648.0
                    elif voice_data.dtype != np.float32:
                        voice_data = voice_data.astype(np.float32)
                    
                    # Resample if necessary
                    if voice_sample_rate != sample_rate:
                        # Use scipy's resample for better quality
                        from scipy.signal import resample
                        new_length = int(len(voice_data) * sample_rate / voice_sample_rate)
                        voice_data = resample(voice_data, new_length).astype(np.float32)
                    
                    # Trim or pad to match duration if specified
                    if duration:
                        target_samples = int(duration * sample_rate)
                        if len(voice_data) > target_samples:
                            voice_data = voice_data[:target_samples]
                        elif len(voice_data) < target_samples:
                            # Pad with silence
                            padding = np.zeros(target_samples - len(voice_data), dtype=np.float32)
                            voice_data = np.concatenate([voice_data, padding])
                    
                    # Ensure audio is in valid range
                    max_val = np.max(np.abs(voice_data))
                    if max_val > 1.0:
                        voice_data = voice_data / max_val
                    
                    return voice_data.astype(np.float32)
                except Exception as read_err:
                    print(f"Error reading voiceover audio: {read_err}")
                    return np.zeros(int(duration * sample_rate) if duration else 1, dtype=np.float32)
                finally:
                    # Clean up temp file
                    try:
                        os.remove(voice_path)
                    except:
                        pass
            else:
                return np.zeros(int(duration * sample_rate) if duration else 1, dtype=np.float32)
        except Exception as e:
            print(f"Voiceover generation failed: {e}")
            import traceback
            traceback.print_exc()
            return np.zeros(int(duration * sample_rate) if duration else 1, dtype=np.float32)
    
    def mix_audio(self, voiceover, sound_effect, sample_rate=44100):
        """Mix voiceover with sound effect audio"""
        # Ensure both have the same length
        max_len = max(len(voiceover), len(sound_effect))
        
        # Pad both to the same length
        if len(voiceover) < max_len:
            voiceover = np.concatenate([voiceover, np.zeros(max_len - len(voiceover), dtype=np.float32)])
        if len(sound_effect) < max_len:
            sound_effect = np.concatenate([sound_effect, np.zeros(max_len - len(sound_effect), dtype=np.float32)])
        
        # Mix with voiceover at 0.7 volume and sound effect at 0.3 volume
        mixed = (voiceover * 0.7 + sound_effect * 0.3)
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 1.0:
            mixed = mixed / max_val
        
        return mixed.astype(np.float32)
        """AI recommendation: analyze prompt and suggest best sound"""
        prompt_lower = prompt.lower()
        
        # Define keyword mappings for different sounds
        keywords = {
            "shine": ["glitter", "sparkl", "bright", "gleam", "shimmer", "crystal"],
            "chime": ["bell", "ring", "chime", "music", "harmony", "melodic"],
            "whoosh": ["fast", "speed", "flying", "rush", "wind", "air", "swift"],
            "crash": ["impact", "boom", "explode", "hit", "strike", "bang", "crash"],
            "ambient": ["calm", "peace", "relax", "serene", "quiet", "soft", "gentle"],
            "scifi": ["future", "tech", "space", "alien", "sci-fi", "cyber", "digital"],
            "retro": ["retro", "vintage", "old", "classic", "8-bit", "game"],
            "pulse": ["beat", "rhythm", "pulse", "heartbeat", "notify", "alert"],
        }
        
        # Score each sound type
        scores = {}
        for sound, keyword_list in keywords.items():
            score = sum(prompt_lower.count(kw) for kw in keyword_list)
            scores[sound] = score
        
        # Return highest scoring sound, default to sweep
        best_sound = max(scores, key=scores.get) if max(scores.values()) > 0 else "sweep"
        return best_sound
    
    def generate_sound_effect(self, effect_name, duration=None, sample_rate=44100):
        """Generate sound effect based on name"""
        if effect_name == "none":
            return np.zeros(1, dtype=np.float32)
        elif effect_name == "beep":
            return self.generate_sound_beep(duration or 2.0, sample_rate)
        elif effect_name == "sweep":
            return self.generate_sound_sweep(duration or 2.0, sample_rate)
        elif effect_name == "pulse":
            return self.generate_sound_pulse(duration or 2.0, sample_rate)
        elif effect_name == "chime":
            return self.generate_sound_chime(duration or 2.0, sample_rate)
        elif effect_name == "crash":
            return self.generate_sound_crash(duration or 2.0, sample_rate)
        elif effect_name == "sparkle":
            return self.generate_sound_sparkle(duration or 2.0, sample_rate)
        elif effect_name == "ambient":
            return self.generate_sound_ambient(duration or 2.0, sample_rate)
        elif effect_name == "scifi":
            return self.generate_sound_scifi(duration or 2.0, sample_rate)
        elif effect_name == "retro":
            return self.generate_sound_retro(duration or 2.0, sample_rate)
        elif effect_name == "whoosh":
            return self.generate_sound_whoosh(duration or 2.0, sample_rate)
        else:
            return np.zeros(1, dtype=np.float32)
    
    def generate_frame(self, frame_num, total_frames, text):
        """Generate a single frame"""
        img = Image.new('RGB', (self.width, self.height), color='black')
        pixels = img.load()
        
        # Create colorful gradient
        for y in range(self.height):
            for x in range(self.width):
                hue = ((x / self.width + y / self.height) / 2 + frame_num / total_frames) % 1.0
                sat = 0.7 + 0.3 * (frame_num / max(total_frames - 1, 1))
                val = 0.4 + 0.6 * ((frame_num + 1) / total_frames)
                
                r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
                pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255))
        
        # Add text
        draw = ImageDraw.Draw(img)
        text = text[:30]  # Truncate long text
        font_size = 60 + int(20 * (frame_num / max(total_frames - 1, 1)))
        
        # Draw text shadow and text
        for offset in [3]:
            draw.text((self.width//2 - offset, self.height//2 - offset), text, 
                     fill=(0, 0, 0), anchor="mm")
        
        draw.text((self.width//2, self.height//2), text, fill=(255, 255, 255), anchor="mm")
        
        return img
    
    def generate_video(self, prompt, num_frames=8, sound_effect="none", include_voiceover=False):
        """Generate video and return path"""
        try:
            import imageio
            import time
            import subprocess
            import tempfile
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"video_{timestamp}.mp4"
            
            frames = []
            start_time = time.time()
            
            for i in range(num_frames):
                frame_start = time.time()
                frame = self.generate_frame(i, num_frames, prompt)
                frames.append(frame)
                
                # Calculate estimated time remaining
                elapsed = time.time() - start_time
                time_per_frame = elapsed / (i + 1)
                remaining_frames = num_frames - (i + 1)
                estimated_remaining = time_per_frame * remaining_frames
                
                # Callback to update status
                if hasattr(self, 'status_callback'):
                    self.status_callback(
                        current=i + 1,
                        total=num_frames,
                        elapsed=elapsed,
                        estimated_remaining=estimated_remaining
                    )
            
            # Calculate video duration and write video
            fps = 30
            duration = len(frames) / fps
            
            # Write video first without audio
            writer = imageio.get_writer(str(output_path), fps=fps, codec='libx264', pixelformat='yuv420p')
            for frame in frames:
                # Convert PIL Image to numpy array if needed
                if isinstance(frame, Image.Image):
                    frame = np.array(frame)
                writer.append_data(frame)
            writer.close()
            
            # Add audio if not silent or voiceover enabled
            if sound_effect != "none" or include_voiceover:
                try:
                    import scipy.io.wavfile as wavfile
                    import shutil
                    
                    sample_rate = 44100
                    audio = None
                    
                    # Generate sound effect
                    if sound_effect != "none":
                        sound_audio = self.generate_sound_effect(sound_effect, duration, sample_rate)
                    else:
                        sound_audio = None
                    
                    # Generate voiceover
                    if include_voiceover:
                        voice_audio = self.generate_voiceover(prompt, duration, sample_rate)
                    else:
                        voice_audio = None
                    
                    # Mix or select audio
                    if voice_audio is not None and sound_audio is not None:
                        # Mix both
                        audio = self.mix_audio(voice_audio, sound_audio, sample_rate)
                    elif voice_audio is not None:
                        # Use voiceover only
                        audio = voice_audio
                    else:
                        # Use sound effect only
                        audio = sound_audio
                    
                    # Save audio to temporary WAV file
                    temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                    wav_path = temp_audio.name
                    temp_audio.close()
                    
                    # Ensure audio is in [-1, 1] range before converting to int16
                    audio = np.clip(audio, -1.0, 1.0)
                    audio_int16 = (audio * 32767).astype(np.int16)
                    
                    try:
                        wavfile.write(wav_path, sample_rate, audio_int16)
                    except Exception as wav_err:
                        print(f"Error writing WAV file: {wav_err}")
                        raise
                    
                    # Use ffmpeg to add audio to video
                    temp_output = str(output_path) + '.temp.mp4'
                    ffmpeg_cmd = [
                        'ffmpeg',
                        '-i', str(output_path),
                        '-i', wav_path,
                        '-c:v', 'copy',
                        '-c:a', 'aac',
                        '-shortest',
                        '-y',
                        temp_output
                    ]
                    
                    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
                    
                    # Replace original with audio version
                    if result.returncode == 0:
                        shutil.move(temp_output, str(output_path))
                    else:
                        print(f"FFmpeg error: {result.stderr}")
                    
                    # Clean up temp files
                    try:
                        os.remove(wav_path)
                    except:
                        pass
                    try:
                        if os.path.exists(temp_output):
                            os.remove(temp_output)
                    except:
                        pass
                except Exception as audio_err:
                    # If audio processing fails, just use the video without audio
                    print(f"Audio processing failed: {audio_err}")
                    import traceback
                    traceback.print_exc()
            
            return str(output_path)
        except Exception as e:
            raise Exception(f"Video generation failed: {e}")


class SimpleApp:
    """Simple GUI for video generation"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Video Generator 🎬")
        self.root.geometry("600x500")
        self.generator = VideoGenerator()
        self.generating = False
        self.setup_ui()
    
    def setup_ui(self):
        """Create UI"""
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main, text="🎬 AI Video Generator", font=("Arial", 20, "bold")).pack(pady=10)
        
        # Prompt
        ttk.Label(main, text="Enter video description:", font=("Arial", 11)).pack(anchor=tk.W)
        self.prompt = tk.Text(main, height=6, font=("Arial", 10))
        self.prompt.pack(fill=tk.BOTH, expand=True, pady=10)
        self.prompt.insert("1.0", "Beautiful colorful animation")
        # Bind text changes to update AI recommendation
        self.prompt.bind("<KeyRelease>", self.update_ai_recommendation)
        
        # Frames
        frame_frame = ttk.Frame(main)
        frame_frame.pack(fill=tk.X, pady=10)
        ttk.Label(frame_frame, text="Frames:").pack(side=tk.LEFT)
        self.frames_var = tk.IntVar(value=8)
        ttk.Scale(frame_frame, from_=3, to=30, variable=self.frames_var, orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.frames_label = ttk.Label(frame_frame, text="8")
        self.frames_label.pack(side=tk.LEFT)
        
        def update_frames(*args):
            self.frames_label.config(text=str(self.frames_var.get()))
        
        self.frames_var.trace("w", update_frames)
        
        # Sound Effects
        sound_frame = ttk.Frame(main)
        sound_frame.pack(fill=tk.X, pady=10)
        ttk.Label(sound_frame, text="Sound Effect:").pack(side=tk.LEFT)
        self.sound_var = tk.StringVar(value="auto")
        sound_options = ["Auto (AI)", "None", "Beep", "Sweep", "Pulse", "Chime", "Crash", "Sparkle", "Ambient", "Sci-Fi", "Retro", "Whoosh"]
        sound_dropdown = ttk.Combobox(
            sound_frame, 
            textvariable=self.sound_var, 
            values=sound_options, 
            state="readonly",
            width=15
        )
        sound_dropdown.pack(side=tk.LEFT, padx=10)
        
        # AI recommendation label
        self.ai_sound_label = ttk.Label(sound_frame, text="", font=("Arial", 9, "italic"), foreground="green")
        self.ai_sound_label.pack(side=tk.LEFT, padx=5)
        
        # Voiceover checkbox
        self.voiceover_var = tk.BooleanVar(value=False)
        voiceover_frame = ttk.Frame(main)
        voiceover_frame.pack(fill=tk.X, pady=10)
        voiceover_check = ttk.Checkbutton(
            voiceover_frame,
            text="🎙️ Include AI Voiceover",
            variable=self.voiceover_var
        )
        voiceover_check.pack(side=tk.LEFT)
        voiceover_info = ttk.Label(voiceover_frame, text="(reads your description)", font=("Arial", 9, "italic"), foreground="gray")
        voiceover_info.pack(side=tk.LEFT, padx=10)
        
        # Generate button
        self.btn = ttk.Button(main, text="🎥 GENERATE VIDEO", command=self.generate)
        self.btn.pack(pady=15, fill=tk.X, ipady=10)
        
        # Progress bar with time estimates
        progress_frame = ttk.Frame(main)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=300)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Status and time display
        time_frame = ttk.Frame(main)
        time_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(time_frame, text="Ready", font=("Arial", 10))
        self.progress_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.time_label = ttk.Label(time_frame, text="", font=("Arial", 9, "bold"), foreground="blue")
        self.time_label.pack(side=tk.RIGHT)
        
        # Status
        ttk.Label(main, text="Status:", font=("Arial", 10)).pack(anchor=tk.W)
        self.status = scrolledtext.ScrolledText(main, height=6, font=("Courier", 9))
        self.status.pack(fill=tk.BOTH, expand=True)
        self.status.insert("1.0", "Ready! Type a description and click Generate.\n\nVideos saved to:\nDownloads/AI Videos/")
        self.status.config(state=tk.DISABLED)
    
    def log(self, msg):
        """Add message to status"""
        self.status.config(state=tk.NORMAL)
        self.status.insert(tk.END, f"\n{msg}")
        self.status.see(tk.END)
        self.status.config(state=tk.DISABLED)
        self.root.update()
    
    def update_status(self, current, total, elapsed, estimated_remaining):
        """Callback from generator with timing info"""
        percentage = int((current / total) * 100)
        self.progress_bar['value'] = percentage
        
        # Format times as M:SS or just Xs
        elapsed_str = self.format_seconds(elapsed)
        remaining_str = self.format_seconds(estimated_remaining)
        
        self.progress_label.config(text=f"Frame {current}/{total} ({percentage}%)")
        self.time_label.config(text=f"⏱ Elapsed: {elapsed_str} | Est: {remaining_str}")
        self.root.update_idletasks()
    
    def format_seconds(self, seconds):
        """Format seconds to M:SS or Xs"""
        s = int(seconds)
        if s >= 60:
            m = s // 60
            sec = s % 60
            return f"{m}m {sec:02d}s"
        else:
            return f"{s}s"
    
    def update_ai_recommendation(self, *args):
        """Update AI sound recommendation based on prompt text"""
        prompt = self.prompt.get("1.0", tk.END).strip()
        if prompt and self.sound_var.get().lower() == "auto (ai)":
            recommended = self.generator.recommend_sound(prompt)
            self.ai_sound_label.config(text=f"→ {recommended.title()}")
        else:
            self.ai_sound_label.config(text="")
    
    def generate(self):
        """Generate video"""
        if self.generating:
            messagebox.showwarning("Busy", "Already generating!")
            return
        
        prompt = self.prompt.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showerror("Error", "Enter a description!")
            return
        
        self.generating = True
        self.btn.config(state=tk.DISABLED)
        self.status.config(state=tk.NORMAL)
        self.status.delete("1.0", tk.END)
        self.status.config(state=tk.DISABLED)
        
        def run():
            try:
                frames = self.frames_var.get()
                sound_choice = self.sound_var.get().lower()  # "Auto (AI)" -> "auto (ai)", "Beep" -> "beep"
                include_voiceover = self.voiceover_var.get()
                
                # If Auto selected, use AI recommendation
                if sound_choice == "auto (ai)":
                    sound_effect = self.generator.recommend_sound(prompt)
                    self.log(f"🎬 Generating {frames} frames...")
                    self.log(f"📝 {prompt}")
                    self.log(f"🤖 AI recommended sound: {sound_effect.title()}")
                else:
                    sound_effect = sound_choice
                    self.log(f"🎬 Generating {frames} frames...")
                    self.log(f"📝 {prompt}")
                    if sound_effect != "none":
                        self.log(f"🔊 Sound: {sound_effect}")
                
                if include_voiceover:
                    self.log(f"🎙️ Voiceover: Enabled")
                
                # Set up callback for progress updates
                self.generator.status_callback = self.update_status
                # Reset progress bar
                self.progress_bar['value'] = 0
                self.progress_label.config(text="Starting...")
                self.time_label.config(text="")
                
                path = self.generator.generate_video(prompt, frames, sound_effect, include_voiceover)
                
                self.log(f"\n✅ DONE!")
                self.log(f"📁 {Path(path).name}")
                
                messagebox.showinfo("Success!", f"Video created!\n\nSaved to:\nDownloads/AI Videos/")
            except Exception as e:
                self.log(f"❌ Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.generating = False
                self.btn.config(state=tk.NORMAL)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()
