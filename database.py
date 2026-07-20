

from sqlalchemy.engine import create_engine
from  sqlalchemy.orm import Session,sessionmaker
from models.models import Base,User,Task
from models.shema import CreateUser,CreateTaskShema
from uuid import uuid4
from pwdlib import PasswordHash
from fastapi import HTTPException,status
engine = create_engine("sqlite:///users_database.db")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def search_user(db: Session, payload: CreateUser):
    user = db.query(User).filter(User.name == payload.name).first()
    return user


def create_user(db: Session, payload: CreateUser):
    hash = hash_password(payload.password)
    new_user = User(name=payload.name,password=hash)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def create_task(db: Session, payload: CreateTaskShema, current_user: User):
    new_task = Task(title=payload.title,status=payload.status,user_id = current_user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def all_tasks(db:Session,current_user: User):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()

    return tasks

def delete_task(db: Session,task_id: int,current_user: User):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if current_user.id != task.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not your task"
        )

    db.delete(task)
    db.commit()

    return all_tasks(db,current_user)