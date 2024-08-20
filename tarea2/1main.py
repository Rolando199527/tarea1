from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URI = 'mysql+mariadb://usuario:contraseña@localhost/nombre_de_base_de_datos'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Definición del modelo de Receta
class Receta(Base):
    __tablename__ = 'recetas'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    ingredientes = Column(String(1000), nullable=False)
    pasos = Column(String(1000), nullable=False)

# Crear todas las tablas
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()
