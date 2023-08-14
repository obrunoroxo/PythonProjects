# Libraries commum imports
import os
from pathlib import Path

# Extra libraries imports
from dotenv import load_dotenv

# Loading .env file
load_dotenv(os.getenv("ENV_FILE"))

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = os.getenv("SAMPLE_RANGE_NAME")