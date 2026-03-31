# demo/safe-config.py
# ✅ SAFE EXAMPLE — uses environment variables (correct practice)
 
import os
 
DATABASE_URL = os.environ.get("DATABASE_URL")
API_KEY      = os.environ.get("API_KEY")
SECRET_TOKEN = os.environ.get("SECRET_TOKEN")
 
print("Config loaded securely from environment variables.")
