# Speech-to-Text Live Overlay

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

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/speech-to-text-overlay.git
   cd speech-to-text-overlay
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

