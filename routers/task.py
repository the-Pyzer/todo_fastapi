from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from models.shema import CreateTaskShema
from database import User,create_task,all_tasks,delete_task
from auth.reglog import get_current_user,find_user
from dependencies import get_db



router = APIRouter()

@router.post('/task/',status_code=status.HTTP_201_CREATED)
def add_task(payload: CreateTaskShema,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    user = find_user(db,current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    new_task = create_task(db,payload,current_user)
    return new_task

@router.get('/tasks/')
def get_tasks(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    return all_tasks(db,current_user)

@router.delete('/task/{task_id}')
def delete_task(task_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return delete_task(db, task_id, current_user)
