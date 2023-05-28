from typing import Annotated
from fastapi import FastAPI, UploadFile, File, Form
from models import Todo, session, Images
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from uuid import uuid4 as uuid
import os

app = FastAPI()

# Configuración CORS
origins = ["http://localhost","http://localhost:5000","http://localhost:3000"]

app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

folder = 'imagenes'
folder_path = os.path.join(os.getcwd(), folder)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

class Todo_demo(BaseModel):
    text: str
    is_done: bool = False
    

@app.post("/create")
async def create_todo(todo_demo: Todo_demo):
    tarea = Todo(text = todo_demo.text, is_done = todo_demo.is_done)
    session.add(tarea)
    session.commit()
    session.close()
    
    return todo_demo.text


@app.get("/")
async def get_all_todos():
    todos_query = session.query(Todo)
    return todos_query.all()

@app.get("/done")
async def list_done_todos():
    todos_query = session.query(Todo)
    done_todos_query = todos_query.filter(Todo.is_done==True)
    return done_todos_query.all()

@app.put("/update/{id}")
async def update_todo(
    id: int,
    new_text: str = "",
    is_complete: bool = False
):
    todo_query = session.query(Todo).filter(Todo.id==id)
    todo = todo_query.first()
    if new_text:
        todo.text = new_text
    todo.is_done = is_complete
    session.add(todo)
    session.commit()

@app.delete("/delete/{id}")
async def delete_todo(id: int):
    todo = session.query(Todo).filter(Todo.id==id).first() # Todo object
    session.delete(todo)
    session.commit()
    return {"todo deleted": todo.text}


class Image(BaseModel):
    file: UploadFile = File(...)

@app.post("/upload-image/")
async def upload_image(image: Image):
    image.file.filename
    print(image.file.filename)
    return {"filename": image.file.filename}

@app.post('/upload')
async def create_upload(texto: str, file: UploadFile = File(...)):
    contents = await file.read()
    with open(f"{texto}.{(file.filename).split('.')[-1]}", "wb") as f:
        f.write(contents)
    return file.filename

@app.post("/files/")
async def create_file(
    file: UploadFile = File(...),
    fileb: UploadFile = File(...),
    token: str = Form(...),
):
    image1 = str(uuid())
    image2 = str(uuid())
    
    token_db = Images(name = token, image_name1 = image1, image_name2 = image2)
    session.add(token_db)
    session.commit()
    session.close()
    # Guardar la primera imagen
    with open(f"{folder_path}/{image1}.{(file.filename).split('.')[-1]}", "wb") as first_image_file:
        first_image_file.write(await file.read())

    # Guardar la segunda imagen
    with open(f"{folder_path}/{image2}.{(fileb.filename).split('.')[-1]}", "wb") as second_image_file:
        second_image_file.write(await fileb.read())
        
    return {"message": "Imágenes guardadas exitosamente"}

# Ruta para servir archivos estáticos (imágenes)
app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes")