# Import downloaded modules
import schedule
from dotenv import load_dotenv

# Import built-in modules
import os
import time
import subprocess
from datetime import datetime


# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_PORT = os.getenv("DB_PORT", "5432")
DB_PORT = '5432'
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "pgdb")

BACKUP_DIR = os.getenv("BACKUP_DIR", "backups")
BACKUP_REMOVAL = {i.split('.')[0]: int(i.split('.')[1]) for i in os.getenv('BACKUP_REMOVAL').split(',')}

BACKUP_INTERVAL_TYPE, BACKUP_INTERVAL_AMOUNT = os.getenv('BACKUP_INTERVAL', 'hours.4').split('.')
BACKUP_INTERVAL_AMOUNT = int(BACKUP_INTERVAL_AMOUNT)

print("Loaded environment")
print(f"""Config is following:
{DB_HOST=}
{DB_PORT=}
{DB_USER=}
{DB_PASSWORD}
{DB_NAME=}
{BACKUP_DIR=}
{BACKUP_REMOVAL=}
{BACKUP_INTERVAL_TYPE=}
{BACKUP_INTERVAL_AMOUNT=}""")

# Ensure backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)

print("Made backup directory")

def remove_old_backups(amount: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
    # Files example
    # 'backup_20250512_165614.sql'
    # 'backup_20250512_171804.sql'
    
    files = os.listdir(f'./{BACKUP_DIR}')
    files.sort()

    if amount:
        # Remove the oldest files until the specified amount is reached
        while len(files) > amount:
            file_to_remove = files.pop(0)
            file_path = os.path.join(BACKUP_DIR, file_to_remove)
            os.remove(file_path)
            print(f"Removed old backup: {file_path}")

    if days:
        # Remove files older than the specified number of days
        for file in files:
            file_path = os.path.join(BACKUP_DIR, file)
            file_time = datetime.strptime(file.split('_', 1)[1][:-4], "%Y%m%d_%H%M%S")
            if (datetime.now() - file_time).days > days:
                os.remove(file_path)
                print(f"Removed old backup: {file_path}")
    
    if minutes:
        # Remove files older than the specified number of minutes
        for file in files:
            file_path = os.path.join(BACKUP_DIR, file)
            file_time = datetime.strptime(file.split('_', 1)[1][:-4], "%Y%m%d_%H%M%S")
            if (datetime.now() - file_time).seconds // 60 > minutes:
                os.remove(file_path)
                print(f"Removed old backup: {file_path}")
    
    if seconds:
        # Remove files older than the specified number of seconds
        for file in files:
            file_path = os.path.join(BACKUP_DIR, file)
            file_time = datetime.strptime(file.split('_', 1)[1][:-4], "%Y%m%d_%H%M%S")
            if (datetime.now() - file_time).seconds > seconds:
                os.remove(file_path)
                print(f"Removed old backup: {file_path}")
    


def backup_postgresql():
    """Creates a timestamped backup of the PostgreSQL database."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"./{BACKUP_DIR}/backup_{timestamp}.sql"
 
    # pg_dump command
    command = f'PGPASSWORD="{DB_PASSWORD}" pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} > {backup_file}'

    print(f"Starting backup: {backup_file}")

    try:
        subprocess.run(command, shell=True)
        print(f"Backup completed: {backup_file}")
        remove_old_backups(**BACKUP_REMOVAL)
    except Exception as e:
        print(f"Error during backup: {e}")

# Run the backup script immediately
backup_postgresql()
print("Made immediate backup")

# Schedule backup every 5 minutes
schedule_type = {
    'seconds': schedule.every(BACKUP_INTERVAL_AMOUNT).seconds,
    'minutes': schedule.every(BACKUP_INTERVAL_AMOUNT).minutes,
    'hours': schedule.every(BACKUP_INTERVAL_AMOUNT).hours,
    'days': schedule.every(BACKUP_INTERVAL_AMOUNT).days
}

schedule_type.get(BACKUP_INTERVAL_TYPE).do(backup_postgresql)

print("PostgreSQL backup script running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)