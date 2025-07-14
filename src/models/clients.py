from sqlalchemy import (Date, Column, String,
                        Boolean, Text)
from sqlalchemy.dialects.postgresql import UUID

from src.config import ApplicationConfig
from src.common.ulid import CustomUlid

from .base import BaseModel

config_app = ApplicationConfig()

class Clients(BaseModel):
    __tablename__ = "clients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=CustomUlid.ulid_to_uuid)
    nome = Column(Text)
    __table_args__ = (
        {"schema": config_app.DB_SCHEMA},
    )


    @property
    def __name(self):
        return self.name

    @__name.setter
    def __name(self, value):
        self.name = value

    def __set_params(self, params):
        self.__name = params.get("name", self.__name)

    def add(self, params):
        self.__set_params(params)

    def add_bulk(self, params):
        self.id = CustomUlid.ulid_to_uuid()
        self.name = params.get("name")

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "report_id": str(self.id),
            "name": self.__name,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
        }
