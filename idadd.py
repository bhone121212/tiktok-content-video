from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create SQLAlchemy engine
# database_url = "postgresql://fbs:yah7WUy1Oi8G@172.32.253.129:5432/fbs"
# engine = create_engine(database_url)
#engine = create_engine('postgresql://fbs:yah7WUy1Oi8G@172.32.253.129:5432/fbs')
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/dbtiktok"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fbs:yah7WUy1Oi8G@172.32.253.129:5432/fbs" #yah7WUy1Oi8G

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Create base class for declarative class definitions
Base = declarative_base()

# Define your table class
class AllContent(Base):
    __tablename__ = 'all_content'
    
    id = db.Column(Integer, primary_key=True)
    content_id = db.Column(Integer)
    network_id = db.Column(Integer)

# Create all tables defined in the models
with app.app_context():
    db.create_all()

    # Create session
    # Session = sessionmaker(bind=db.engine)
    # session = Session()

    # Insert content IDs from 1 to 6000 with network ID 5
    for content_id in range(1, 6001):
        db.session.add(AllContent(content_id=content_id, network_id=5))

    # Commit the session to insert data into the database
    db.session.commit()

    # Close session
    db.session.close()
