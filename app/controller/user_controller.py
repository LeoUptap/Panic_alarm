from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from model.user import User
from app.database import get_session

router = APIRouter()


##POST user
@router.post("/users", response_model=User)
def crear_usuario(usuario: User):
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario


##GET users
@router.get("/users", response_model=list[User])
def listar_usuarios():
    with Session(engine) as session:
        return session.exec(select(User)).all()
    


###GET user con id
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = get_session()):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    


# DELETE user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = get_session()):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": f"User {user_id} deleted successfully"}