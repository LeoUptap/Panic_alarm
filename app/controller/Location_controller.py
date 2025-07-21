from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from Database import engine
from model.Location import Location
from Database import get_session
from typing import List

router = APIRouter()
##POST Contacto de emergencia
@router.post("/location", response_model=Location)
def post_location(Localizacion: Location):
    with Session(engine) as session:
        session.add(Localizacion)
        session.commit()
        session.refresh(Localizacion)
        return Localizacion
    
###GET Localizaciones asosiadas a un usuario
@router.get("/location/{main_user_id}", response_model=List[Location])
def get_locations(user_id: int, session: Session =Depends(get_session)):
    # Consulta para obtener todos los contactos de emegencia con ese main_user_id
    statement = select(Location).where(Location.user_id ==user_id)
    results = session.exec(statement).all()

    if not results:
        raise HTTPException(status_code=404, detail="No se encontro un historial de ubicaciones")
    
    return results



@router.delete("/location/{num_id}")
def delete_location(loc_id: int, session: Session =Depends(get_session)):
    localizacion = session.get(Location, loc_id)
    if not localizacion:
        raise HTTPException(status_code=404, detail="NO se enco tro la ubicacion buscada")

    session.delete(localizacion)
    session.commit()
    return {"message": f"Se a borrado la evidencia con el id: {loc_id}"}


###PUT (Actualizar) numero
##Porque alguien querria actualizar los datos de ubicacion?

## R: Tiene amante, se escapo de sus padres, le esta preparando una sorpresa a alguien
@router.put("/location/{num_id}")
def update_location(loc_id: int, updated_loc: Location, session: Session = Depends(get_session)):
    loc = session.get(Location, loc_id)
    if not loc:
        raise HTTPException(status_code=404, detail="Number not found")

    # Actualiza solo campos que vienen con valor (opcional)
    loc.lat = updated_loc.lat
    loc.long = updated_loc.long
    loc.day = updated_loc.day
    loc.time = updated_loc.time

    session.add(loc)
    session.commit()
    session.refresh(loc)

    return loc


###GET Localizacion reciente del usuario
@router.get("/location/fresh_location/{main_user_id}", response_model=List[Location])
def get_fresh_locations(user_id: int, session: Session =Depends(get_session)):
    # Consulta para obtener todos los contactos de emegencia con ese main_user_id
    statement = (
        select(Location)
        .where(Location.user_id ==user_id)
        .order_by(Location.day.desc(),Location.time.desc())
        .limit(1)
        )
    results = session.exec(statement).all()

    if not results:
        raise HTTPException(status_code=404, detail="No se encontro una ubicaion para este usuario")
    
    return results

