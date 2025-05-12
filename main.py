# Import downloaded modules
import schedule

# Import built-in modules
import os
import time
import subprocess
from datetime import datetime


# Load environment variables
DB_HOST = os.getenv("PGDB_HOST", "localhost")
DB_PORT = os.getenv("PGDB_PORT", "5432")
DB_USER = os.getenv("PGDB_USER", "user")
DB_PASSWORD = os.getenv("PGDB_PASSWORD", "password")
DB_NAME = os.getenv("PGDB_NAME", "pgdb")
BACKUP_DIR = os.getenv("PG_BACKUP_DIR", "backups")

print("Loaded environment")
print(f"Config is following:\n{DB_HOST=}\n{DB_PORT=}\n{DB_USER=}\n{DB_PASSWORD}\n{DB_NAME=}\n{BACKUP_DIR=}")

# Ensure backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)

print("Made backup directory")

def backup_postgresql():
    """Creates a timestamped backup of the PostgreSQL database."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"/{BACKUP_DIR}/backup_{timestamp}.sql"

    # pg_dump command
    command = f'PGPASSWORD="{DB_PASSWORD}" pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} > {backup_file}'

    print(f"Starting backup: {backup_file}")

    try:
        subprocess.run(command, shell=True)
        print(f"Backup completed: {backup_file}")
    except Exception as e:
        print(f"Error during backup: {e}")

# Run the backup script immediately
backup_postgresql()
print("Made immediate backup")

# Schedule backup every 5 minutes
schedule.every(5).minutes.do(backup_postgresql)

print("PostgreSQL backup script running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)