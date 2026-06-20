import time
#install watchdog in your venv
from multiprocessing import Process
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from presenter.Presenter import GamePresenter

def run_game():
    try:
        game = GamePresenter()
        game.run()
    except Exception as e:
        print(f"\n Game crashed with error:\n{e}")
        print("Fix the error and press save to try again...")

#  checks for file saves and reloads the game
class SaveHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print("\n💾 File change detected! Restarting game...")
            self.restart_callback()

class GameRunner:
    def __init__(self):
        self.process = None

    def start_game_process(self):
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process.join()
        
        self.process = Process(target=run_game)
        self.process.start()

def main():
    runner = GameRunner()
    runner.start_game_process()

    event_handler = SaveHandler(runner.start_game_process)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    print("Watching for file saves. Edit your code and save to see changes live!")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Clean up when you press Ctrl+C in the terminal
        observer.stop()
        if runner.process:
            runner.process.terminate()
    observer.join()

if __name__ == "__main__":
    main()

