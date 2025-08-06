# tests/conftest.py
import sys
from pathlib import Path

# Insert project root (one level above tests/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # .../your-repo
sys.path.insert(0, str(PROJECT_ROOT))
