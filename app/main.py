from fastapi import FastAPI
from database import engine,create_db_and_tables
from sqlmodel import SQLModel

from controller.user_controller import router as user_router
#from controller.location_controller import router as location_router
#from controller.emergency_controller import router as emergency_router

app = FastAPI()

create_db_and_tables()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Registrar routers
app.include_router(user_router, prefix="/users", tags=["Users"])
#app.include_router(location_router, prefix="/locations", tags=["Locations"])
#app.include_router(emergency_router, prefix="/emergencies", tags=["Emergency Numbers"])
