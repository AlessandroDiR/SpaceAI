from datetime import datetime, timedelta, timezone
import random

class PhrasesGenerator:
    random.seed(42)

    '''
    Class constants
    '''
    DEFAULT_COUNT = 50
    ACTIONS = ["prenota", "cancella", "modifica"]
    ASSETS = ["sala riunioni", "auditorium", "sala meeting", "ufficio A", "ufficio B", "desk 18", "desk 40"]

    '''
    Class properties
    '''
    count: int

    def __init__(self, count: int = DEFAULT_COUNT):
        self.count = count

    '''
    Convert a datetime into an ISO 8601 format string
    '''
    def to_iso_string(self, dt: datetime) -> str:
        datetime_utc = dt.replace(tzinfo=timezone.utc)
        return datetime_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    '''
    Generate random start, end datetime starting from the current day
    '''
    def random_date_time(self) -> tuple[datetime, datetime]:
        start_date = datetime.today()
        random_days = random.randint(0, 90)  # Within 3 months
        random_hours_start = random.randint(6, 20)
        random_minutes_start = random.randrange(0, 60, step=15)
        random_duration = random.randint(1, 10)  # 1 to 10 hours
        start = start_date + timedelta(days=random_days, hours=random_hours_start, minutes=random_minutes_start)
        end = start + timedelta(hours=random_duration)
        return start, end

    def run(self) -> tuple[str, str]:
        inputs = []
        outputs = []

        for _ in range(self.count):
            phrase = ""
            action = random.choice(self.ACTIONS)
            asset = random.choice(self.ASSETS)
            start, end = self.random_date_time()
            humanized_start, humanized_end = start.strftime("%d/%m/%Y %H:%M"), end.strftime("%d/%m/%Y %H:%M")

            if (action == "prenota"):
                phrase = f"Prenota {asset} per il giorno {humanized_start.split()[0]} dalle {humanized_start.split()[1]} alle {humanized_end.split()[1]}"
            elif action == "cancella":
                phrase = f"Cancella la prenotazione di {asset} per il giorno {humanized_start.split()[0]} dalle {humanized_start.split()[1]} alle {humanized_end.split()[1]}"
            else:
                phrase = f"Modifica la prenotazione di {asset} al giorno {humanized_start.split()[0]} dalle {humanized_start.split()[1]} alle {humanized_end.split()[1]}"

            inputs.append(phrase)
            outputs.append({
                "action": action, 
                "asset": asset, 
                "start": self.to_iso_string(start) , 
                "end": self.to_iso_string(end)
            })
        
        return inputs, outputs



if __name__ == "__main__":
    generator = PhrasesGenerator()
    ins, outs = generator.run()
    
    for i, o in zip(ins, outs):
        print(f"\"{i}\"")
        print(f"Extract: {o}\n")
