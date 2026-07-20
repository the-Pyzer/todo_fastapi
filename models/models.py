from sqlalchemy import  ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    tasks: Mapped[list['Task']] = relationship(back_populates='user')

class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[bool]  = mapped_column(nullable=False,default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='tasks')

