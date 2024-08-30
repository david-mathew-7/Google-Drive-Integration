import os
from fastapi import APIRouter, Request, HTTPException, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse

from app.services.google_drive_service import list_files, upload_file, download_file, delete_file, get_file_metadata

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# default download directory
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@router.get("/list-files", response_class=HTMLResponse)
async def list_files_route(request: Request):
    credentials_dict = request.session.get('credentials')
    if not credentials_dict:
        raise HTTPException(status_code=403, detail="User not authenticated")

    items = list_files(credentials_dict)

    return templates.TemplateResponse("list_files.html", {"request": request, "items": items})


@router.get("/upload-file", response_class=HTMLResponse)
async def upload_file_form(request: Request):
    # Render upload file form
    return templates.TemplateResponse("upload_file.html", {"request": request})


@router.post("/upload-file", response_class=HTMLResponse)
async def upload_file_route(request: Request, file_path: UploadFile = Form(...), folder_id: str = Form(None)):
    credentials_dict = request.session.get('credentials')
    if not credentials_dict:
        return RedirectResponse(url="/auth/login")

    file_content = await file_path.read()

    upload_file(credentials_dict, file_content, file_path.filename, folder_id)

    return RedirectResponse(url="/drive/list-files", status_code=303)


@router.get("/download-file/{file_id}")
async def download_file_route(file_id: str, request: Request):
    credentials_dict = request.session.get('credentials')
    if not credentials_dict:
        return RedirectResponse(url="/auth/login")

    metadata = get_file_metadata(credentials_dict, file_id)
    original_name = metadata.get('name')
    mime_type = metadata.get('mimeType')
    destination_path = os.path.join(DOWNLOAD_DIR, original_name)
    downloaded_path = download_file(credentials_dict, file_id, destination_path)

    return FileResponse(
        path=downloaded_path,
        filename=original_name,
        media_type=mime_type
    )


@router.post("/delete-file/{file_id}")
async def delete_file_route(file_id: str, request: Request):
    credentials_dict = request.session.get('credentials')
    if not credentials_dict:
        return RedirectResponse(url="/auth/login")
    delete_file(credentials_dict, file_id)
    return RedirectResponse(url="/drive/list-files", status_code=303)