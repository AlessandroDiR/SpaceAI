from datetime import datetime, timedelta
import random
import sys
import os
from humanize import Humanize

class SentencesGenerator:

    ASSETS = ["sala riunioni", "auditorium", "sala meeting", "ufficio A", "ufficio B", "desk 18", "desk 40"]

    def __init__(self, seed: int | None = None):
        """Keyword arguments:

        seed -- the seed for random generation\n
        """
        random.seed(seed)

    def __get_random_asset__(self):
        return random.choice(self.ASSETS)
    
    def __get_random_date_time_range__(self) -> tuple[datetime, datetime]:
        """Generate random start and random end datetimes starting from the current day"""
        start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        random_days = random.randint(0, 90)  # Within 3 months
        random_hours_start = random.randint(8, 20) # Similar to a working day
        random_minutes_start = random.randrange(0, 60, step=15) # Random quart of hour
        random_duration_hours = random.randint(0, 4)  # Up to 4 hours
        random_duration_minutes = random.randrange(15, 59, step=15)
        start = start_date + timedelta(days=random_days, hours=random_hours_start, minutes=random_minutes_start)
        end = start + timedelta(hours=random_duration_hours, minutes=random_duration_minutes)
        return start, end

    def run(self, count = 2000, datetime_as_duration: bool = False) -> tuple[list, list]:
        """Generate sentences
        
        Args:\n
        count -- the number of sentences to generate (default 2000)\n
        datetime_as_duration -- if date range must be humanized with date and time durations
        """
        sentences = []
        keys = []
        for _ in range(count):
            asset = self.__get_random_asset__()
            start, end = self.__get_random_date_time_range__()
            humanized_range = Humanize.humanize_datetime_range(start, end, as_duration=datetime_as_duration)
            sentences.append(f"prenota {asset} {humanized_range}")
            keys.append({
                "asset": asset, 
                "start": start.isoformat(timespec="seconds"), 
                "end": end.isoformat(timespec="seconds")
            })
        
        return sentences, keys

if __name__ == "__main__":
    generator = SentencesGenerator(seed=42)
    sentences, kkss = generator.run(datetime_as_duration=True)
    for sentence, keys in zip(sentences, kkss):
        print(f"[\"{sentence}\", {keys}]")
