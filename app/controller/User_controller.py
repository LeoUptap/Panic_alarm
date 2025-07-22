from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from Database import engine
from model.User import User
from Database import get_session
from typing import List


router = APIRouter()

    
@router.post("/users", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    # Verifica si el username ya existe
    existing_user = session.exec(select(User).where(User.user_name == user.user_name)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe :/")

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    


###GET user con id
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users_name/{user_name}", response_model=User)
def get_user_byusername(user_name: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.user_name == user_name)
    user=session.exec(statement).all()
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


###PUT (Actualizar) user
@router.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Actualiza solo campos que vienen con valor (opcional)
    user.name = updated_user.name
    user.user_name = updated_user.user_name
    user.password = updated_user.password
    user.main_phone_number = updated_user.main_phone_number
    user.type = updated_user.type
    user.main_user_id = updated_user.main_user_id

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
