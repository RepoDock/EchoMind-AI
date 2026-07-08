from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from services.indexing_service import IndexingService
import time


class FileWatcher(FileSystemEventHandler):

    def on_modified(self, event):

        if event.is_directory:
            return

        print("=" * 60)
        print("Modified:", event.src_path)
        service = IndexingService()

        service.index_file(event.src_path)
        print("=" * 60)



class Watcher:

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.observer = Observer()

    def start(self):

        handler = FileWatcher()

        self.observer.schedule(
            handler,
            self.folder_path,
            recursive=True
        )

        self.observer.start()

        print("=" * 60)
        print("Watching:", self.folder_path)
        print("=" * 60)

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()

