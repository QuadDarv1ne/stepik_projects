# app/config.py
import os
import logging

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./media_platform.db")

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
