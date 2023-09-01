import threading
import json
import shutil
import os
import datetime
import glob
import time
from logger import logger
import environment

def backup_json_file(json_file_path, backup_folder):
    backup_file_name = os.path.basename(json_file_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file_name = f"{backup_file_name}_{timestamp}.json"
    backup_file_path = os.path.join(backup_folder, backup_file_name)
    shutil.copyfile(json_file_path, backup_file_path)
    logger.info(f"Backup performed: {backup_file_name}")

def cleanup_old_backups(backup_folder, num_backups_to_keep):
    backup_files = sorted(glob.glob(os.path.join(backup_folder, "*.json")), reverse=True)
    num_backups = len(backup_files)
    if num_backups > num_backups_to_keep:
        backups_to_delete = backup_files[num_backups_to_keep:]
        for backup_file in backups_to_delete:
            os.remove(backup_file)

def run_backup_periodically(json_file_path, backup_folder):
    backup_json_file(json_file_path, backup_folder)
    while True:
        time.sleep(int(environment.BACKUP_FREQUENCY))
        backup_json_file(json_file_path, backup_folder)
        cleanup_old_backups(backup_folder, int(environment.BACKUP_QUANTITY))

def start_backup_thread(json_file_path, backup_folder):
    logger.info(f"Backup settings: Frequency={environment.BACKUP_FREQUENCY} seconds, Quantity={environment.BACKUP_QUANTITY}")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    backup_thread = threading.Thread(target=run_backup_periodically, args=(json_file_path, backup_folder))
    backup_thread.daemon = True
    backup_thread.start()