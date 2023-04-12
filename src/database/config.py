from sqlmodel import create_engine

DATABASE_URL = 'mysql+pymysql://root:password@localhost:32776/blueboard_milestones'
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True)