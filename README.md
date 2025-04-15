# TheSkullCon - File Converter

<div align="center">
    <img src="app/static/images/logo.png" alt="TheSkullCon Logo" width="200">
</div>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/badge/FastAPI-0.104.0-blue.svg" alt="FastAPI Version">
    <img src="https://img.shields.io/badge/FFmpeg-Required-orange.svg" alt="FFmpeg Required">
</p>

> Developed by [RunawayDevil](https://github.com/RunawayDevil) © 2025

## 📝 Description

TheSkullCon is a modern web application for converting images and videos with a beautiful and intuitive interface. It supports a wide range of formats and provides real-time preview of files.

## ✨ Features

- **Image Conversion**
  - Supported formats: JPG, JPEG, PNG, BMP, TIFF, WebP
  - High-quality conversion
  - Preserves image quality

- **Video Conversion**
  - Supported formats: MP4, AVI, MOV, MKV, GIF
  - Optimized for web playback
  - Maintains video quality

- **Audio Conversion**
  - Supported formats: MP3, WAV, OGG, FLAC, AAC, M4A
  - High-quality audio conversion
  - Preserves audio quality

- **User Experience**
  - Drag and drop interface
  - Real-time file preview
  - Automatic download after conversion
  - Progress bar during conversion
  - Responsive design

## 🛠️ Technologies Used

### Backend
- FastAPI
- FFmpeg
- Pillow
- Python-Magic
- Filetype

### Frontend
- Bootstrap 5
- Font Awesome
- Jinja2 Templates
- JavaScript

## 🚀 Installation

### Requirements
- Python 3.11 or higher
- FFmpeg
- Debian 12 (Bookworm) or compatible system

### Step 1: Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and required packages
sudo apt install -y python3 python3-pip python3-venv ffmpeg

# Install FFmpeg
sudo apt install -y ffmpeg
```

### Step 2: Clone and Setup Project

```bash
# Clone repository
git clone https://github.com/RunawayDevil/TheSkullCon.git
cd TheSkullCon

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
# Start the server
uvicorn app.main:app --reload --port 8012
```

The application will be available at `http://localhost:8012`

## 📁 Project Structure

```
TheSkullCon/
├── app/
│   ├── static/
│   │   ├── images/
│   │   └── uploads/
│   ├── templates/
│   │   └── index.html
│   ├── services/
│   │   └── converter.py
│   ├── __init__.py
│   ├── config.py
│   └── main.py
├── requirements.txt
└── README.md
```

## 🔧 Configuration

The application can be configured by modifying the `app/config.py` file:

```python
# Server settings
HOST = "0.0.0.0"
PORT = 8012
DEBUG = True

# Upload settings
MAX_CONTENT_LENGTH = 300 * 1024 * 1024  # 300MB
CLEANUP_INTERVAL = 3600  # 1 hour in seconds
```

## 🎯 Supported Formats

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

## 🔍 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```bash
   sudo apt install ffmpeg
   ```

2. **Permission denied**
   ```bash
   sudo chmod -R 755 app/static/uploads
   ```

3. **Port already in use**
   ```bash
   # Find process using port 8012
   sudo lsof -i :8012
   
   # Kill the process
   sudo kill -9 <PID>
   ```

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

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Pablo Murad (RunawayDevil)**
  - GitHub: [@RunawayDevil](https://github.com/RunawayDevil)
  - Email: your.email@example.com 