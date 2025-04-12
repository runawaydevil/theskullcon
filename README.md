# TheSkullCon - File Converter

<div align="center">
  <img src="https://i.ibb.co/3YR3V6zx/logo-2.png" alt="TheSkullCon Logo" width="200">
</div>

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![FFmpeg Required](https://img.shields.io/badge/FFmpeg-Required-orange.svg)](https://ffmpeg.org/)

A modern web application for converting images, videos, and audio files with an intuitive interface.

> Developed by [RunawayDevil](https://github.com/RunawayDevil) in 2025 under the MIT License.

## Features

- **Image Conversion**
  - Supported formats: JPG, JPEG, PNG, BMP, TIFF, WebP
  - Real-time preview
  - Automatic download after conversion

- **Video Conversion**
  - Supported formats: MP4, AVI, MOV, MKV, GIF
  - Optimized compression
  - Progress bar during conversion
  - Automatic download after conversion

- **Audio Conversion**
  - Supported formats: MP3, WAV, OGG, FLAC, AAC, M4A
  - High-quality conversion
  - Progress bar during conversion
  - Automatic download after conversion

- **General Features**
  - Maximum file size: 300MB
  - Modern and responsive interface
  - Real-time file preview
  - Progress tracking
  - Automatic format detection
  - Secure file handling

## Requirements

- Debian 12 (Bookworm)
- Python 3.11 or higher
- FFmpeg
- Virtual environment (recommended)

## Installation

### System Requirements
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and required packages
sudo apt install -y python3 python3-pip python3-venv ffmpeg

# Install filetype dependencies
sudo apt install -y libmagic-dev
```

### Project Setup
```bash
# Clone repository
git clone https://github.com/RunawayDevil/TheSkullCon.git
cd TheSkullCon

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create upload directory
mkdir -p app/static/uploads
mkdir -p app/static/images
```

### Running the Application
```bash
# Start the server
uvicorn app.main:app --reload --port 8012
```

The application will be available at `http://localhost:8012`

## Project Structure

```
TheSkullCon/
├── app/
│   ├── static/
│   │   ├── uploads/     # Temporary storage for converted files
│   │   └── images/      # Static images (logo, etc)
│   │   └── templates/   # Web interface templates
│   ├── services/
│   │   └── converter.py # File conversion logic
│   ├── config.py        # Configuration settings
│   └── main.py          # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Supported Formats

### Images
- JPG/JPEG
- PNG
- BMP
- TIFF
- WebP

### Videos
- MP4
- AVI
- MOV
- MKV
- GIF

### Audio
- MP3
- WAV
- OGG
- FLAC
- AAC
- M4A

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```bash
   sudo apt install ffmpeg
   ```

2. **Python dependencies not installing**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **File size limit exceeded**
   - Maximum file size is 300MB
   - Compress your file before uploading if necessary

### Running as a Service

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/theskullcon.service
```

Add the following content:
```ini
[Unit]
Description=TheSkullCon File Converter
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/TheSkullCon
ExecStart=/path/to/TheSkullCon/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8012
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable theskullcon
sudo systemctl start theskullcon
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 