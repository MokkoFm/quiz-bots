import os
import redis
from dotenv import load_dotenv
load_dotenv()


def connect_to_db():
    db_host = os.getenv("REDIS_DB")
    db_password = os.getenv("REDIS_DB_PASSWORD")
    db = redis.Redis(
        host=db_host, port=10513,
        db=0, password=db_password, decode_responses=True)
    return db
