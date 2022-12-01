import datetime
import uuid

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from db.database import Base


class Restaurants(Base):
    __tablename__ = 'restaurants'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(50), nullable=True)
    description = Column(String(50), nullable=True)
    site_url = Column(String(50), nullable=True)
    draw = Column(Integer(), default=0)
    created_time = Column(DateTime(), nullable=False)
    modified_time = Column(DateTime(), nullable=False)
    histories = relationship(
        'Histories',
        backref='restaurants',
        cascade='all,delete'
    )

    def __init__(self, name, description, site_url):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.site_url = site_url
        self.created_time = datetime.datetime.now()
        self.modified_time = datetime.datetime.now()

    def __repr__(self):
        return f"<Restaurant {self.name}>"
