import csv
import codecs
import json

from fastapi import UploadFile, File, Query, Depends
from sqlmodel import Session
from app.database.config import engine

class CommonActions():

    @staticmethod
    async def get_session():
        with Session(engine) as session:
            yield session

    @staticmethod
    def make_username(first, last):
        first = first.lower()
        last = last.lower()
        return f"{first}{last}"
    
    @staticmethod
    async def process_csv(csv_file: UploadFile = File(...)):
            csv_reader = csv.DictReader(codecs.iterdecode(csv_file.file, 'utf-8'))
            csv_items = []
            for row in csv_reader:
                csv_items.append(json.loads(json.dumps(row)))
            return csv_items
