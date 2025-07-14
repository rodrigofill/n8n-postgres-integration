from sqlalchemy import (Date, Column, String, ForeignKeyConstraint, Index,
                        Boolean, Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.config import ApplicationConfig
from src.common.ulid import CustomUlid

from .base import BaseModel

config_app = ApplicationConfig()

class Contracts(BaseModel):
    __tablename__ = "contracts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=CustomUlid.ulid_to_uuid)
    client_id = Column(UUID(as_uuid=True), nullable=False)
    active = Column(Boolean, nullable=False)
    clients = relationship("Clients")
    __table_args__ = (
        Index("idx_contracts_active", active),
        ForeignKeyConstraint(
            [client_id], ["{}.clients.id".format(config_app.DB_SCHEMA)]
        ),
        {"schema": config_app.DB_SCHEMA},
    )

    @property
    def __client_id(self):
        return self.client_id

    @__client_id.setter
    def __client_id(self, value):
        self.client_id = value

    @property
    def __active(self):
        return self.active

    @__active.setter
    def __active(self, value):
        self.active = value

    def __set_params(self, params):
        self.__client_id = params.get("client_id", self.__client_id)
        self.__active = params.get("active", self.__active)

    def add(self, params):
        self.__set_params(params)

    def add_bulk(self, params):
        self.id = CustomUlid.ulid_to_uuid()
        self.client_id = params.get("client_id")
        self.active = params.get("active")

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "report_id": str(self.id),
            "client_id": self.__client_id,
            "active": self.__active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
