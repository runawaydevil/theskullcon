from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from app.services.converter import VideoConverter
from app.config import Config

app = FastAPI()

# Configure templates
templates = Jinja2Templates(directory="app/templates")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Ensure upload directory exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Initialize converter
converter = VideoConverter()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_file(
    request: Request,
    file: UploadFile = File(...),
    output_format: str = Form(...)
):
    try:
        # Save uploaded file
        file_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Convert file
        output_file = converter.convert_file(file_path, output_format)

        # Return success message with download link
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": "File converted successfully!",
                "output_file": output_file
            }
        )

    except Exception as e:
        # Return error message
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Error converting file: {str(e)}"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 