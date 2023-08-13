from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from database import Base

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    qtd_exercicios = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    alunos = relationship('Aluno', back_populates='curso')

    @staticmethod
    def update_active(db: Session, curso_id: int, active: bool):
        curso = db.query(Curso).filter(Curso.id == curso_id).first()
        if curso:
            curso.active = active
            db.commit()
            return curso
        return None
class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    idade = Column(Integer, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    id_curso = Column(Integer, ForeignKey('cursos.id'))
    curso = relationship('Curso', back_populates='alunos') 