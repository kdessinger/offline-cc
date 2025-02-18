import pyaudio
import numpy as np
import queue
import threading
import time
import noisereduce as nr
import webrtcvad
from faster_whisper import WhisperModel

# Audio and transcription configuration
FORMAT = pyaudio.paInt16       # 16-bit PCM
CHANNELS = 1                   # Mono audio
RATE = 16000                   # 16kHz sample rate (required by many STT engines)
CHUNK = 1024                   # Frames per buffer
TRANSCRIPTION_FILE = "H:/faster-whisper/live.txt"
SEGMENT_DURATION = 3           # Seconds per segment
BYTES_PER_SAMPLE = 2           # 16-bit = 2 bytes
NUM_SAMPLES_REQUIRED = int(RATE * SEGMENT_DURATION)
REQUIRED_BYTES = NUM_SAMPLES_REQUIRED * BYTES_PER_SAMPLE

# Thread-safe queue for captured audio
audio_queue = queue.Queue()

# Last transcription to prevent unnecessary file updates
last_transcription = ""

def audio_capture():
    """
    Continuously capture audio from the default microphone and put data into the queue.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Live captioning is running. Press Ctrl+C to exit.")
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_queue.put(data)
    except Exception as e:
        print("Audio capture error:", e)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def frame_generator(frame_duration_ms, audio, sample_rate):
    """
    Breaks the audio bytes into frames of duration frame_duration_ms.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * BYTES_PER_SAMPLE)
    offset = 0
    while offset + n <= len(audio):
        yield audio[offset:offset + n]
        offset += n

def contains_speech(audio_bytes, sample_rate, frame_duration_ms=30, threshold=0.5):
    """
    Returns True if the fraction of frames in the audio containing speech exceeds the threshold.
    Uses webrtcvad for speech detection.
    """
    vad = webrtcvad.Vad(2)  # Mode 2: moderately aggressive
    frames = list(frame_generator(frame_duration_ms, audio_bytes, sample_rate))
    if not frames:
        return False
    speech_frames = sum(1 for frame in frames if vad.is_speech(frame, sample_rate))
    return (speech_frames / len(frames)) > threshold

def stt_processing():
    """
    Process audio segments using overlapping windows:
      1. Accumulate a fixed-duration audio buffer.
      2. Process a segment with a specified overlap (e.g., 50%).
      3. Apply VAD, noise reduction, and transcribe using the GPU-accelerated Whisper model.
      4. Update the OBS transcription file if the text changes.
    """
    global last_transcription
    print("Loading STT model on GPU...")
    model = WhisperModel("large-v2", device="cuda", compute_type="float16")
    print("STT model loaded.")
    
    audio_buffer = bytearray()
    OVERLAP_RATIO = 0.5
    overlap_bytes = int(REQUIRED_BYTES * OVERLAP_RATIO)
    
    while True:
        # Accumulate enough audio for one segment.
        while len(audio_buffer) < REQUIRED_BYTES:
            try:
                data = audio_queue.get(timeout=0.2)
                audio_buffer.extend(data)
            except queue.Empty:
                continue
        
        # Extract a segment of REQUIRED_BYTES.
        segment_bytes = audio_buffer[:REQUIRED_BYTES]
        # Slide the window: retain the last "overlap_bytes" and discard the rest.
        audio_buffer = audio_buffer[(REQUIRED_BYTES - overlap_bytes):]
        
        # Optional: Use VAD to check if the segment has enough speech
        if not contains_speech(segment_bytes, RATE):
            continue
        
        # Convert raw bytes into a normalized numpy array.
        audio_np = np.frombuffer(segment_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        
        # Apply noise reduction.
        reduced_audio = nr.reduce_noise(y=audio_np, sr=RATE)
        
        print("Transcribing audio segment...")
        # Unpack the tuple from transcribe; segments is an iterable of transcription segments.
        segments, info = model.transcribe(reduced_audio, beam_size=5, language="en")
        
        # Combine segment text into one string.
        transcription = " ".join(segment.text.strip() for segment in segments).strip()
        
        # Update transcription file only if there's new, non-empty text.
        if transcription and transcription != last_transcription:
            print("Transcription:", transcription)
            try:
                with open(TRANSCRIPTION_FILE, "w", encoding="utf-8") as f:
                    f.write(transcription)
            except Exception as e:
                print("Error writing transcription file:", e)
            last_transcription = transcription
        
        # Brief pause to keep processing responsive.
        time.sleep(0.05)

def main():
    # Start the capture and processing threads.
    capture_thread = threading.Thread(target=audio_capture, daemon=True)
    processing_thread = threading.Thread(target=stt_processing, daemon=True)
    capture_thread.start()
    processing_thread.start()
    
    print("Live captioning is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting... Clearing transcription file.")
        try:
            with open(TRANSCRIPTION_FILE, "w", encoding="utf-8") as f:
                f.write("")  # Clear the file
        except Exception as e:
            print("Error clearing transcription file:", e)

if __name__ == "__main__":
    main()
