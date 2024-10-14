from fastapi import FastAPI, Request ,Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .models import Project, SessionLocal, engine
from pydantic import BaseModel
from fastapi import UploadFile, File, HTTPException ,Form
import shutil
import os

app = FastAPI()

templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root(request: Request ,db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return templates.TemplateResponse("index.html", {"request": request ,"projects": projects})


@app.get("/projects_read")
async def read_projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})


@app.get("/projects")
async def get_projects(db: Session = Depends(get_db)):
    """Get all projects from the database."""
    projects = db.query(Project).all()
    return projects


@app.get("/about")
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/contact")
async def read_contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})




UPLOAD_DIR = "./static/images/"

@app.post("/projects")
async def create_project(name: str = Form(...),role: str = Form(...),description: str = Form(...),
    link: str = Form(...), technologies: str = Form(...), image: UploadFile = File(...)  ,db: Session = Depends(get_db)
    ):
    """Create a new project and save it to the database."""

    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are allowed.")
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    new_project = Project(
        name=name,
        image_url=image_path,  # Store the image path in the database
        role=role,
        description=description,
        link=link,
        technologies= technologies
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project