import os
import sys
from pathlib import Path

# Add backend directory to sys.path so app modules are discoverable
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.main import app

app = app
