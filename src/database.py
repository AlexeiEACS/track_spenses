from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URL = "sqlite:///finanzas.db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)
    monto = Column(Float, nullable=False)
    categoria = Column(String, index=True)
    tipo = Column(String, index=True)  # "Ingreso" o "Gasto"

Base.metadata.create_all(bind=engine)