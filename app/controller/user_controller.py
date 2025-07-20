from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import engine
from model.user import User
from database import get_session
from typing import List


router = APIRouter()


##POST user
@router.post("/users", response_model=User)
def crear_usuario(usuario: User):
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

    


###GET user con id
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

###GET user asosiados a un usuario
@router.get("/users/by-main/{main_user_id}", response_model=List[User])
def get_sub_users(main_user_id: int, session: Session =Depends(get_session)):
    # Consulta para obtener todos los usuarios con ese main_user_id
    statement = select(User).where(User.main_user_id == main_user_id)
    results = session.exec(statement).all()

    if not results:
        raise HTTPException(status_code=404, detail="No users found for given main_user_id")
    
    return results


# DELETE user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session =Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": f"User {user_id} deleted successfully"}