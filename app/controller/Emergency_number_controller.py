from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from Database import engine
from model.Emergency_number import Emergency_number
from Database import get_session
from typing import List

router = APIRouter()
##POST Contacto de emergencia
@router.post("/emergency_num", response_model=Emergency_number)
def crear_contacto(contacto: Emergency_number):
    with Session(engine) as session:
        session.add(contacto)
        session.commit()
        session.refresh(contacto)
        return contacto
    
###GET Contactos asosiados a un usuario
@router.get("/emergency_num/{main_user_id}", response_model=List[Emergency_number])
def get_nums(main_user_id: int, session: Session =Depends(get_session)):
    # Consulta para obtener todos los contactos de emegencia con ese main_user_id
    statement = select(Emergency_number).where(Emergency_number.user_id == main_user_id)
    results = session.exec(statement).all()

    if not results:
        raise HTTPException(status_code=404, detail="No users found for given main_user_id")
    
    return results



@router.delete("/emergency_num/{num_id}")
def delete_user(num_id: int, session: Session =Depends(get_session)):
    num = session.get(Emergency_number, num_id)
    if not num:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(num)
    session.commit()
    return {"message": f"Emergency num {num_id} deleted successfully"}


###PUT (Actualizar) numero
@router.put("/emergency_num/{num_id}")
def update_user(num_id: int, updated_num: Emergency_number, session: Session = Depends(get_session)):
    num = session.get(Emergency_number, num_id)
    if not num:
        raise HTTPException(status_code=404, detail="Number not found")

    # Actualiza solo campos que vienen con valor (opcional)
    num.name = updated_num.name
    num.phone_number = updated_num.phone_number

    session.add(num)
    session.commit()
    session.refresh(num)

    return num

