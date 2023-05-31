import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Specify the path to your bot script
BOT_SCRIPT_PATH = 'bot.py'

# Store the process ID of the running bot
running_process = None

class RestartHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            global running_process
            if running_process is not None:
                print(f"Stopping previous bot (PID: {running_process.pid})...")
                running_process.terminate()
                running_process.wait()
            print(f"Restarting bot...")
            running_process = subprocess.Popen(['python3', BOT_SCRIPT_PATH])

def start_watchdog():
    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    print(f"Starting bot...")
    running_process = subprocess.Popen(['python3', BOT_SCRIPT_PATH])
    start_watchdog()