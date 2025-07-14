from sqlalchemy import (Date, Column, Float, ForeignKeyConstraint, Index,
                        Boolean, Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.config import ApplicationConfig
from src.common.ulid import CustomUlid

from .base import BaseModel

config_app = ApplicationConfig()

class EnergyReadings(BaseModel):
    __tablename__ = "energy_readings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=CustomUlid.ulid_to_uuid)
    contract_id = Column(UUID(as_uuid=True), nullable=False)
    reading_date = Column(Date)
    reading_value = Column(Float)
    contracts = relationship("Contracts")
    __table_args__ = (
        Index("idx_energy_readings_reading_date", reading_date),
        ForeignKeyConstraint(
            [contract_id], ["{}.contracts.id".format(config_app.DB_SCHEMA)]
        ),
        {"schema": config_app.DB_SCHEMA},
    )

    @property
    def __contract_id(self):
        return self.contract_id

    @__contract_id.setter
    def __contract_id(self, value):
        self.contract_id = value

    @property
    def __reading_date(self):
        return self.reading_date

    @__reading_date.setter
    def __reading_date(self, value):
        self.reading_date = value

    @property
    def __reading_value(self):
        return self.reading_value

    @__reading_value.setter
    def __reading_value(self, value):
        self.reading_value = value

    def __set_params(self, params):
        self.__contract_id = params.get("contract_id", self.__contract_id)
        self.__reading_date = params.get("reading_date", self.__reading_date)
        self.__reading_value = params.get("reading_value", self.__reading_value)

    def add(self, params):
        self.__set_params(params)

    def add_bulk(self, params):
        self.id = CustomUlid.ulid_to_uuid()
        self.contract_id = params.get("contract_id")
        self.reading_date = params.get("reading_date")
        self.reading_value = params.get("reading_value")

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "report_id": str(self.id),
            "contract_id": self.__contract_id,
            "reading_date": self.__reading_date,
            "reading_value": self.__reading_value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
