from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.openapi.utils import get_openapi
from models import Curso, Aluno
from database import engine, Base, get_db
from repositories import AlunoRepository, CursoRepository
from schemas import AlunoRequest, AlunoResponse, CursoRequest, CursoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def create_curso(request: CursoRequest, db: Session = Depends(get_db)):
    curso = CursoRepository.save(db, Curso(**request.dict()))
    return CursoResponse.from_orm(curso)

@app.get("/api/cursos", response_model=list[CursoResponse])
def find_all_cursos(db: Session = Depends(get_db)):
    cursos = CursoRepository.find_all(db)
    return [CursoResponse.from_orm(curso) for curso in cursos]

@app.get("/api/cursos/{curso_id}", response_model=CursoResponse)
def find_curso_by_id(curso_id: int, db: Session = Depends(get_db)):
    curso = CursoRepository.find_by_id(db, curso_id)
    if curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado!")
    return CursoResponse.from_orm(curso)

@app.delete("/api/cursos/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_curso(curso_id: int, db: Session = Depends(get_db)):
    if not CursoRepository.exists_by_id(db, curso_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado!")
    CursoRepository.delete_by_id(db, curso_id)
    return {"message": "Curso removido com sucesso!"}

@app.put("/api/cursos/{curso_id}", response_model=CursoResponse)
def update_curso(curso_id: int, request: CursoRequest, db: Session = Depends(get_db)):
    curso = CursoRepository.find_by_id(db, curso_id)
    if curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado!")
    update_curso = CursoRepository.save(db, Curso(**request.dict(), id=curso.id))
    return CursoResponse.from_orm(update_curso)

@app.post("/api/alunos", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def create_aluno(request: AlunoRequest, db: Session = Depends(get_db)):
    cpf_exists = AlunoRepository.find_by_cpf(db, request.cpf)
    if cpf_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado!")

    aluno = Aluno(**request.dict())
    return AlunoRepository.create(db, aluno)

@app.get("/api/alunos/{aluno_id}", response_model=AlunoResponse)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = AlunoRepository.find_by_id(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado!")
    return aluno

@app.put("/api/alunos/{aluno_id}", response_model=AlunoResponse)
def update_aluno(aluno_id: int, request: AlunoRequest, db: Session = Depends(get_db)):
    aluno_data = request.dict()
    updated_aluno = AlunoRepository.update(db, aluno_id, aluno_data)
    if not updated_aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado!")
    return updated_aluno

@app.delete("/api/alunos/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = AlunoRepository.find_by_id(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado!")
    if aluno.curso and aluno.curso.active: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível excluir o aluno, pois ele está vinculado a um curso ativo.")
    
    AlunoRepository.delete_by_id(db, aluno_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/cursos/{curso_id}/ativo", response_model=CursoResponse)
def update_curso_active(curso_id: int, active: bool, db: Session = Depends(get_db)):
    curso = CursoRepository.find_by_id(db, curso_id)
    if curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado!")

    curso.update_active(db, active)
    return CursoResponse.from_orm(curso)
    

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Ambiente Virtual de Aprendizagem",
        version="1.0.0",
        summary="Alunos EAD",
        description="Sistema de Ambiente Virtual de Aprendizagem para auxiliar alunos 100% EAD",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
