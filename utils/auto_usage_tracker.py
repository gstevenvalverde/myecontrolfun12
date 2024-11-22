import threading
import time
from models.usage_model import update_user_usage_data
from datetime import datetime

class UsageTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.total_minutes = 0
        self.running = True
        self.today = datetime.now().strftime("%Y-%m-%d")  # Fecha actual

    def add_time(self, minutes):
        self.total_minutes += minutes

    def save_periodically(self):
        while self.running:
            time.sleep(1800)  # 30 minutos
            if self.total_minutes > 0:
                update_user_usage_data(self.user_id, self.today, self.total_minutes)
                print(f"Guardado automáticamente: {self.total_minutes} minutos")
                self.total_minutes = 0

    def start(self):
        thread = threading.Thread(target=self.save_periodically)
        thread.daemon = True
        thread.start()

    def stop(self):
        if self.total_minutes > 0:
            update_user_usage_data(self.user_id, self.today, self.total_minutes)
            print(f"Guardado final: {self.total_minutes} minutos")
        self.running = False
