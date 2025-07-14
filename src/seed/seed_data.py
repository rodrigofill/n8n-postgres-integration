# src/seed/seed_data.py

from random import choice, gauss
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid
from datetime import date, datetime, timedelta

from src.models.energy_readings import EnergyReadings
from src.models.clients import Clients
from src.models.contracts import Contracts
from src.models.base import Base  # includes metadata

from src.config import ApplicationConfig
config = ApplicationConfig()

engine = create_engine(config.connection_string())
Session = sessionmaker(bind=engine)
session = Session()

# Create clients
clients = [
    Clients(id=uuid.uuid4(), nome="Alice Rodrigues"),
    Clients(id=uuid.uuid4(), nome="Bruno Carvalho"),
    Clients(id=uuid.uuid4(), nome="Carla Mendes"),
    Clients(id=uuid.uuid4(), nome="Daniela Souza"),
    Clients(id=uuid.uuid4(), nome="Eduardo Lima"),
]

session.add_all(clients)
session.flush()  # get client IDs before commit

# Create contracts linked to clients
contracts = [
    Contracts(id=uuid.uuid4(), client_id=clients[0].id, active=True),
    Contracts(id=uuid.uuid4(), client_id=clients[1].id, active=True),
    Contracts(id=uuid.uuid4(), client_id=clients[2].id, active=False),
    Contracts(id=uuid.uuid4(), client_id=clients[3].id, active=True),
    Contracts(id=uuid.uuid4(), client_id=clients[4].id, active=False),
]

session.add_all(contracts)
session.commit()

# 3. Seed energy readings for the last 3 months (approx. 90 days)
today = date.today()
days_back = 90

energy_readings = []

for contract in contracts:
    # Base mean consumption per contract, vary by contract
    base_mean = 50 + 20 * (hash(contract.id) % 5)  # Just to add some variation

    for day_offset in range(days_back):
        reading_date = today - timedelta(days=day_offset)

        # Simulate normal reading with some gaussian noise
        reading_value = gauss(base_mean, 5)

        # Introduce outlier randomly with low probability (~2%)
        if choice(range(50)) == 0:
            reading_value *= 3  # big spike as outlier

        energy_readings.append(
            EnergyReadings(
                id=uuid.uuid4(),
                contract_id=contract.id,
                reading_date=reading_date,
                reading_value=round(reading_value, 2),
            )
        )

session.add_all(energy_readings)
session.commit()
print("✅ Seed data inserted successfully")
