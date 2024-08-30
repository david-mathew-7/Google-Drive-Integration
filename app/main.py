import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from app.routers import auth, drive


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Conditionally mount static files
if os.environ.get("TESTING") != "1":
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Include routers for auth and drive operations
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(drive.router, prefix="/drive", tags=["drive"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if not request.session.get('credentials'):
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("base.html", {"request": request, "message": "Welcome to the Google Drive Integration App"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)