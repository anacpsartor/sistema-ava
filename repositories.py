from sqlalchemy.orm import Session
from models import Aluno, Curso
from fastapi import HTTPException, status

class CursoRepository:
    @staticmethod
    def find_all(db: Session) -> list[Curso]:
        return db.query(Curso).filter(Curso.active == True).all()

    @staticmethod
    def save(db: Session, curso: Curso) -> Curso:
        if curso.id:
            db.merge(curso)
        else:
            db.add(curso)
        db.commit()
        return curso

    @staticmethod
    def find_by_id(db: Session, id: int) -> Curso:
        return db.query(Curso).filter(Curso.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Curso).filter(Curso.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        curso = db.query(Curso).filter(Curso.id == id).first()
        if curso is not None:
            db.delete(curso)
            db.commit()

class AlunoRepository:
    @staticmethod
    def create(db: Session, aluno: Aluno) -> Aluno:
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
        return aluno

    @staticmethod
    def find_all(db: Session) -> list[Aluno]:
        return db.query(Aluno).all()

    @staticmethod
    def find_by_id(db: Session, id: int) -> Aluno:
        return db.query(Aluno).filter(Aluno.id == id).first()

    @staticmethod
    def update(db: Session, id: int, aluno_data: dict) -> Aluno:
        db.query(Aluno).filter(Aluno.id == id).update(aluno_data)
        db.commit()
        return db.query(Aluno).filter(Aluno.id == id).first()

    @staticmethod
    def find_by_cpf(db: Session, cpf: str) -> Aluno:
        return db.query(Aluno).filter(Aluno.cpf == cpf).first()

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        aluno = db.query(Aluno).filter(Aluno.id == id).first()
        if aluno is not None:
            if aluno.curso and aluno.curso.active:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Não foi possível excluir o aluno, pois ele está vinculado a um curso ativo.")
            db.delete(aluno)
            db.commit()