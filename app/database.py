#https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql#create-the-sqlalchemy-parts

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# sql db url format : postgresql://<username>:<password>@<ip-address/hostname>/<database_name>
SQL_ALCHEMY_DB_URL='postgresql://postgres:password@localhost/fastapi'

engine=create_engine(SQL_ALCHEMY_DB_URL)

#session for talking/communicate with sql
sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)


#Base class 
Base = declarative_base()

# Dependency
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


