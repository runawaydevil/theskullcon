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

- Python 3.8 or higher
- FFmpeg
- Python dependencies (listed in `requirements.txt`)

## Detailed Installation Guide

### 1. System Requirements

#### Windows
1. Install Python 3.8+:
   - Download from [Python's official website](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. Install FFmpeg:
   - Download from [FFmpeg official website](https://ffmpeg.org/download.html)
   - Extract the ZIP file
   - Add the FFmpeg `bin` folder to your system's PATH:
     - Search for "Environment Variables" in Windows
     - Under "System Variables", find and select "Path"
     - Click "Edit" → "New"
     - Add the path to FFmpeg's bin folder
     - Click "OK" to save

#### Linux (Ubuntu/Debian)
```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Install FFmpeg
sudo apt install ffmpeg
```

#### macOS
```bash
# Using Homebrew
brew install python
brew install ffmpeg
```

### 2. Project Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/theskullcon.git
cd theskullcon
```

2. Create and activate a virtual environment:

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create uploads directory:
```bash
# Windows
mkdir app\static\uploads

# Linux/macOS
mkdir -p app/static/uploads
```

### 3. Running the Application

1. Verify FFmpeg installation:
```bash
ffmpeg -version
```

2. Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8012
```

3. Access the application:
```
http://localhost:8012
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
   - Ensure the uploads directory has proper write permissions
   - Run the application with appropriate user privileges

3. **Port Already in Use**
   - Change the port in the uvicorn command:
     ```bash
     uvicorn app.main:app --reload --port 8013
     ```

4. **Dependencies Installation Fails**
   - Upgrade pip:
     ```bash
     python -m pip install --upgrade pip
     ```
   - Install dependencies one by one if needed
   - Check Python version compatibility

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 