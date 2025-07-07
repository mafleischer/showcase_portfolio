import os
import time
from datetime import datetime
from sqlite3 import OperationalError

from sqlalchemy import JSON, Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pipeline_logs.db")

MAX_RETRIES = 10
for i in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        break
    except OperationalError:
        print(f"Database not ready, retrying ({i + 1}/{MAX_RETRIES})...")
        time.sleep(2)
else:
    raise Exception("Could not connect to the database after several retries.")

Session = sessionmaker(bind=engine)


class PipelineLog(Base):
    __tablename__ = "pipeline_logs"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    plugin_name = Column(String)
    result_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)
