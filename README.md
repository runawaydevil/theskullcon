# TheSkullCon - File Converter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green.svg)](https://fastapi.tiangolo.com/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)](https://ffmpeg.org/)

A modern and intuitive web application for converting images and videos.

> Developed by [RunawayDevil](https://github.com/RunawayDevil) in 2025
> 
> Licensed under the MIT License

## Features

- **Image Conversion**:
  - Supported formats: JPG, JPEG, PNG, BMP, TIFF, WebP
  - Real-time preview
  - Intuitive interface

- **Video Conversion**:
  - Supported formats: MP4, AVI, MOV, MKV, GIF
  - Progress bar
  - Automatic download after conversion

- **Web Interface**:
  - Modern design with Bootstrap 5
  - Simple upload process
  - Image preview
  - Visual progress feedback

## Technologies Used

- **Backend**:
  - FastAPI
  - FFmpeg
  - Pillow
  - Python-Magic

- **Frontend**:
  - Bootstrap 5
  - Font Awesome
  - Jinja2 Templates
  - JavaScript

## Requirements

- Debian 12 (Bookworm)
- Python 3.11 or higher
- FFmpeg
- Python dependencies (listed in `requirements.txt`)

## Detailed Installation Guide for Debian 12

### 1. System Requirements

1. Update your system:
```bash
sudo apt update
sudo apt upgrade -y
```

2. Install Python and required system packages:
```bash
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip \
    build-essential libffi-dev libssl-dev libjpeg-dev zlib1g-dev \
    libmagic-dev
```

3. Install FFmpeg:
```bash
sudo apt install -y ffmpeg
```

4. Verify FFmpeg installation:
```bash
ffmpeg -version
```

### 2. Project Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/theskullcon.git
cd theskullcon
```

2. Create and activate a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
```

3. Upgrade pip and install wheel:
```bash
python -m pip install --upgrade pip
pip install wheel
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Create uploads directory:
```bash
mkdir -p app/static/uploads
```

### 3. Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8012
```

2. Access the application:
```
http://localhost:8012
```

### 4. Running as a Service (Optional)

1. Create a systemd service file:
```bash
sudo nano /etc/systemd/system/theskullcon.service
```

2. Add the following content:
```ini
[Unit]
Description=TheSkullCon File Converter
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/theskullcon
Environment="PATH=/path/to/theskullcon/venv/bin"
ExecStart=/path/to/theskullcon/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8012
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl enable theskullcon
sudo systemctl start theskullcon
```

## Project Structure

```
theskullcon/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── config.py          # Configuration settings
│   ├── services/
│   │   └── converter.py   # Conversion logic
│   ├── static/
│   │   └── uploads/       # Temporary file storage
│   └── templates/
│       └── index.html     # Web interface
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
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

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Ensure FFmpeg is properly installed
   - Verify it's in your system's PATH
   - Try running `ffmpeg -version` in terminal

2. **Permission Issues**
   - Ensure the uploads directory has proper write permissions:
     ```bash
     sudo chown -R your_username:your_username app/static/uploads
     sudo chmod -R 755 app/static/uploads
     ```

3. **Port Already in Use**
   - Change the port in the uvicorn command:
     ```bash
     uvicorn app.main:app --reload --port 8013
     ```

4. **Dependencies Installation Fails**
   - Ensure all required system packages are installed
   - Try installing dependencies one by one
   - Check Python version compatibility

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 