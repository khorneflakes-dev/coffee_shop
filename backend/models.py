from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)

class Images(Base):
    __tablename__ = "image_tables"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image_name1 = Column(String)
    image_name2 = Column(String)

Base.metadata.create_all(engine)
