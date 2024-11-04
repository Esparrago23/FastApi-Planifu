from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register", response_model=schemas.UsuarioCreate)
def register(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = auth.get_password_hash(user.contrasena)
    db_user = models.Usuario(nombre_usuario=user.nombre_usuario, correo=user.correo, contraseña=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully", "user": db_user}

@app.post("/login")
def login(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.correo == user.correo).first()
    if not db_user or not auth.verify_password(user.contrasena, db_user.contraseña):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
   
    return {"message": "Login successful", "user": {"nombre_usuario": db_user.nombre_usuario, "correo": db_user.correo}}

@app.get("/usuarios/", response_model=list[schemas.Usuario])  
def read_usuarios(db: Session = Depends(get_db)):
    db_usuarios = db.query(models.Usuario).all()  
    return db_usuarios

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)  
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
@app.post("/categorias/", response_model=schemas.CategoriaCreate)
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.get("/categorias/", response_model=list[schemas.Categoria])
@app.get("/categorias/{categoria_id}", response_model=schemas.Categoria)
def read_categoria(categoria_id: int = None, db: Session = Depends(get_db)):
    if categoria_id:
        db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
        if db_categoria is None:
            raise HTTPException(status_code=404, detail="Categoria not found")
        return db_categoria
    return db.query(models.Categoria).all() 

@app.put("/categorias/{categoria_id}", response_model=schemas.CategoriaCreate)
def update_categoria(categoria_id: int, categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    
    for key, value in categoria.dict().items():
        setattr(db_categoria, key, value)
    
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.delete("/categorias/{categoria_id}", status_code=204)
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    
    db.delete(db_categoria)
    db.commit()
    return


@app.post("/actividades/", response_model=schemas.ActividadCreate)
def create_actividad(actividad: schemas.ActividadCreate, db: Session = Depends(get_db)):
    db_actividad = models.Actividad(**actividad.dict())
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

@app.get("/actividades/", response_model=list[schemas.Actividad])
@app.get("/actividades/{actividad_id}", response_model=schemas.Actividad)
def read_actividad(actividad_id: int = None, db: Session = Depends(get_db)):
    if actividad_id:
        db_actividad = db.query(models.Actividad).filter(models.Actividad.id == actividad_id).first()
        if db_actividad is None:
            raise HTTPException(status_code=404, detail="Actividad not found")
        return db_actividad
    return db.query(models.Actividad).all() 

@app.put("/actividades/{actividad_id}", response_model=schemas.ActividadCreate)
def update_actividad(actividad_id: int, actividad: schemas.ActividadCreate, db: Session = Depends(get_db)):
    db_actividad = db.query(models.Actividad).filter(models.Actividad.id == actividad_id).first()
    if db_actividad is None:
        raise HTTPException(status_code=404, detail="Actividad not found")
    
    for key, value in actividad.dict().items():
        setattr(db_actividad, key, value)
    
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

@app.delete("/actividades/{actividad_id}", status_code=204)
def delete_actividad(actividad_id: int, db: Session = Depends(get_db)):
    db_actividad = db.query(models.Actividad).filter(models.Actividad.id == actividad_id).first()
    if db_actividad is None:
        raise HTTPException(status_code=404, detail="Actividad not found")
    
    db.delete(db_actividad)
    db.commit()
    return


@app.post("/recordatorios/", response_model=schemas.RecordatorioCreate)
def create_recordatorio(recordatorio: schemas.RecordatorioCreate, db: Session = Depends(get_db)):
    db_recordatorio = models.Recordatorio(**recordatorio.dict())
    db.add(db_recordatorio)
    db.commit()
    db.refresh(db_recordatorio)
    return db_recordatorio

@app.get("/recordatorios/", response_model=list[schemas.Recordatorio])
@app.get("/recordatorios/{recordatorio_id}", response_model=schemas.Recordatorio)
def read_recordatorio(recordatorio_id: int = None, db: Session = Depends(get_db)):
    if recordatorio_id:
        db_recordatorio = db.query(models.Recordatorio).filter(models.Recordatorio.id == recordatorio_id).first()
        if db_recordatorio is None:
            raise HTTPException(status_code=404, detail="Recordatorio not found")
        return db_recordatorio
    return db.query(models.Recordatorio).all() 

@app.put("/recordatorios/{recordatorio_id}", response_model=schemas.RecordatorioCreate)
def update_recordatorio(recordatorio_id: int, recordatorio: schemas.RecordatorioCreate, db: Session = Depends(get_db)):
    db_recordatorio = db.query(models.Recordatorio).filter(models.Recordatorio.id == recordatorio_id).first()
    if db_recordatorio is None:
        raise HTTPException(status_code=404, detail="Recordatorio not found")
    
    for key, value in recordatorio.dict().items():
        setattr(db_recordatorio, key, value)
    
    db.commit()
    db.refresh(db_recordatorio)
    return db_recordatorio

@app.delete("/recordatorios/{recordatorio_id}", status_code=204)
def delete_recordatorio(recordatorio_id: int, db: Session = Depends(get_db)):
    db_recordatorio = db.query(models.Recordatorio).filter(models.Recordatorio.id == recordatorio_id).first()
    if db_recordatorio is None:
        raise HTTPException(status_code=404, detail="Recordatorio not found")
    
    db.delete(db_recordatorio)
    db.commit()
    return
