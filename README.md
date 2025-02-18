# Offline Closed Captions

## Overview

This project is an **offline speech-to-text (STT) system** that takes live microphone input, converts speech to text using faster-whisper by openAI, and displays the transcribed text as an **overlay** via HDMI output. The system is optimized for **low-latency** transcription and designed for **live production events** such as weddings and concerts.

## Features

- **Offline functionality** (No internet required)
- **Low latency** speech-to-text conversion
- **GPU acceleration** for fast processing
- **Censorship feature** to filter inappropriate words
- **Live HDMI output** for integration with OBS & mixers
- **Supports multiple input sources** (USB mic, line-in, etc.)
- **Customizable text overlay**

## Key Points
- Offline STT with GPU Acceleration:
The program uses the faster‑whisper engine with device="cuda" so that transcription is accelerated (Tested with NVidia GeForce RTX 2080 SUPER).

- Real‑Time Audio Input:
PyAudio is used to capture live audio from the USB condenser mic (which must be the system’s default audio input).

- Noise Filtering:
A simple noise reduction is applied via the noisereduce library. In production you may wish to tweak the parameters or integrate a more sophisticated noise suppression algorithm.

- Live OBS Text File:
The transcription is written to H:/faster-whisper/live.txt. OBS Studio can be configured to use this file as a Text (GDI+) source with a green background, black text, and padding as required. Make sure OBS refreshes the file at a high frequency (below 100 ms delay).

- Deployment Considerations:
The program is intended to run offline on Windows based sytems with Python 3.11.7. Ensure all dependencies (PyAudio, NumPy, noisereduce, and faster-whisper) are installed in your offline environment.

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/kdessinger/offline-cc.git
   cd offline0-cc
   ```
2. **Install Dependencies** (Ensure Python 3.11.7 is installed)
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the Application**
   ```sh
   python main.py
   ```

## Usage

- **Start the application** and select the preferred input device.
- The transcribed text will be displayed on the HDMI output.
- OBS Studio is recommended for integrating the overlay with a live video feed.&#x20;
- A GPU is necessary to accelerate the process.

## Configuration

Modify `config.json` to adjust settings like:

- **Input device** selection
- **Font size & color**
- **Censorship settings**

## License

This project is licensed under the GNU General Public License v3.0. See `LICENSE` for details.

## Contributing

Feel free to submit issues or pull requests to improve this project!

## Contact

For questions or feedback, reach out to Kenn Dessinger at **kdessinger@gmail.com**.

