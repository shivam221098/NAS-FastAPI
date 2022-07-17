from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from starlette import status
import shutil
import os
from typing import List
import webbrowser
import socket
import re

app = FastAPI()

templates = Jinja2Templates(directory="templates")
received_path = "D:/NAS/Received"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "username": "Network Attached Storage",
                                                    "laptop_name": socket.gethostname()})


@app.post("/submitform")
async def upload_file(request: Request, uploaded_files: List[UploadFile] = File(...)):
    filenames = []
    for uploaded_file in uploaded_files:
        filenames.append(uploaded_file.filename)
        with open(f"D:/NAS/Received/{uploaded_file.filename}", "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

    return templates.TemplateResponse("greetings.html", {"request": request, "filenames": filenames,
                                                         "length": len(filenames), "deleted": ""})


@app.get("/downloads", response_class=HTMLResponse)
async def download_page(request: Request):
    filelist = os.listdir(received_path)
    return templates.TemplateResponse("filelist.html", {"request": request, "filelist": filelist})


@app.get("/download/{name}")
async def download_file(name: str):
    file_path = received_path + "/" + name
    return FileResponse(path=file_path, filename=name, media_type="application/octet-stream")


@app.post("/delete/{name}")
async def delete_file(name: str, request: Request):
    filepath = received_path + "/" + name
    os.remove(filepath)
    filelist = os.listdir(received_path)
    return templates.TemplateResponse("filelist.html", {"request": request, "filelist": filelist,
                                                        "deleted": name})


@app.post("/openpage")
async def share_page(request: Request, link: str = Form(...)):
    url_pattern = re.compile("((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)", re.IGNORECASE)
    if re.search(url_pattern, link) is not None:
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new_tab(link)
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)
