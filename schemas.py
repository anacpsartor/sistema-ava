from pydantic import BaseModel

class CursoBase(BaseModel):
    titulo: str
    descricao: str
    carga_horaria: int
    qtd_exercicios: int

class CursoRequest(CursoBase):
    novo_campo: str

class CursoResponse(CursoBase):
    id: int
    active: bool

    class Config:
        from_attributes = True
        orm_mode = True

class AlunoBase(BaseModel):
    nome: str
    sobrenome: str
    email: str
    idade: int
    cpf: str

class AlunoRequest(AlunoBase):
    ...

class AlunoResponse(AlunoBase):
    id: int
    curso: CursoResponse

    class Config:
        orm_mode = True
