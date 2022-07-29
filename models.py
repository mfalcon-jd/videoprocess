import db
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base 


class Metadata(db.Base):
    __tablename__ = 'video_data'

    id = Column(Integer, primary_key=True)
    clip_name = Column(String)
    clip_file_extension = Column(String)
    clip_duration = Column(Integer)
    clip_location = Column(String)
    insert_timestamp = Column(TIMESTAMP)

    def __init__(self, clip_name, clip_file_extension, clip_duration, clip_location, insert_timestamp):
        self.clip_name = clip_name
        self.clip_file_extension = clip_file_extension
        self.clip_duration = clip_duration
        self.clip_location = clip_location
        self.insert_timestamp = insert_timestamp
