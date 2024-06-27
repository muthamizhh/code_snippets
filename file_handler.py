import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class SplunkDataHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None

        elif event.src_path.endswith(".json"):
            print(f"New file detected: {event.src_path}")
            self.process_new_file(event.src_path)

    def process_new_file(self, file_path):
        # Trigger the LoadDataToMongoDB task
        subprocess.run([
            "python", "path/to/your_script.py",
            "LoadDataToMongoDB",
            f"--mongodb-host={configuration['mongodb']['host']}",
            f"--mongodb-port={configuration['mongodb']['port']}",
            f"--mongodb-db={configuration['mongodb']['db']}",
            f"--mongodb-collection={configuration['mongodb']['collection']}",
            f"--json-file={file_path}",
            "--local-scheduler"
        ])

if __name__ == "__main__":
    path = "/path/to/splunk_logs"
    event_handler = SplunkDataHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
