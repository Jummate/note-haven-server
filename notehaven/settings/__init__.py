import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------
# STEP 1 — Locate project base directory
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------
# STEP 2 — Determine environment safely
# ---------------------------------------
environment = os.getenv("ENVIRONMENT")

if not environment:
    # Always default to development
    environment = "development"

    # Warn if production env file exists but ENVIRONMENT not set
    if (BASE_DIR / ".env.production").exists():
        print("Warning: .env.production exists but ENVIRONMENT not set. Defaulting to development for safety.")

environment = environment.lower()

# ---------------------------------------
# STEP 3 — Load corresponding .env file
# ---------------------------------------
env_file = BASE_DIR / f".env.{environment}"

if env_file.exists():
    load_dotenv(env_file)
    print(f"Loaded environment file: {env_file}")
else:
    print(f"Warning: Expected environment file '{env_file}' not found!")

# ---------------------------------------
# STEP 4 — Import the right Django settings
# ---------------------------------------
if environment == "production":
    from .production import *
else:
    from .development import *

print(f"Using Django settings for environment: {environment}")
