from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'mysql+pymysql://root:password@localhost:32776/blueboard_milestones'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
