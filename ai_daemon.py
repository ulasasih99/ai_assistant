import os
import logging
from telegram import Bot
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Config
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
WORKSPACE = "/media/ihwalkhila/01DBB9D3F3FA8080/ServerAI"
LOG_FILE = f"{WORKSPACE}/logs/activity.log"

# Setup
bot = Bot(token=TELEGRAM_TOKEN)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

class AIHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.report(f"📄 File dibuat: {event.src_path}")

    def on_modified(self, event):
        if event.src_path.endswith("command.ask"):
            with open(event.src_path, 'r') as f:
                command = f.read().strip()
            self.execute(command)

    def execute(self, command):
        try:
            if "BUAT_FOLDER:" in command:
                path = command.split(":")[1]
                os.makedirs(f"{WORKSPACE}/{path}", exist_ok=True)
                self.report(f"📂 Folder dibuat: {path}")
            
            elif "BUAT_FILE:" in command:
                filename, content = command.split(":")[1].split("|")
                with open(f"{WORKSPACE}/{filename}", "w") as f:
                    f.write(content)
                self.report(f"📝 File dibuat: {filename}")

            logging.info(f"SUKSES: {command}")
        except Exception as e:
            logging.error(f"GAGAL: {str(e)}")
            self.report(f"❌ Error: {str(e)}")

    def report(self, message):
        bot.send_message(chat_id=CHAT_ID, text=message)
        logging.info(message)

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(AIHandler(), path=WORKSPACE, recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
