from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_ALL, "it_IT")

class Humanize:
    @staticmethod
    def humanize_date(target_date, reference_date=None, as_duration=False):
        """
        Umanizza una data rispetto a una data di riferimento.
        """
        if reference_date is None:
            reference_date = datetime.now()

        delta = target_date - reference_date
        days_diff = delta.days

        if days_diff == 0:
            return "oggi"
        elif days_diff == 1:
            return "domani"
        elif as_duration:
            if days_diff > 0:
                return f"tra {days_diff} giorni"
            else:
                return f"{abs(days_diff)} giorni fa"
        elif 0 < days_diff <= 7:
            weekday = target_date.strftime("%A")  # Nome del giorno
            return f"il prossimo {weekday}"
        elif days_diff > 7:
            return target_date.strftime("il %d %B")  # Giorno e mese
        elif -7 <= days_diff < 0:
            weekday = target_date.strftime("%A")
            return f"lo scorso {weekday}"
        else:
            return target_date.strftime("il %d %B %Y")  # Giorno, mese e anno

    @staticmethod
    def humanize_time(start_datetime, end_datetime=None, as_duration=False):
        """
        Umanizza un intervallo temporale o un orario con una durata.
        """
        start_time = start_datetime.time()
        end_time = end_datetime.time() if end_datetime else None
        
        if as_duration and end_datetime:
            duration = end_datetime - start_datetime
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            if hours > 0 and minutes > 0:
                return f"dalle {start_time.strftime('%H:%M')} per {hours} ore e {minutes} minuti"
            elif hours > 0:
                return f"dalle {start_time.strftime('%H:%M')} per {hours} ore"
            elif minutes > 0:
                if minutes == 30:
                    return f"dalle {start_time.strftime('%H:%M')} per mezz'ora"
                return f"dalle {start_time.strftime('%H:%M')} per {minutes} minuti"
        elif end_datetime:
            return f"dalle {start_time.strftime('%H:%M')} alle {end_time.strftime('%H:%M')}"
        else:
            return start_time.strftime("alle %H:%M")

    @staticmethod
    def humanize_datetime_range(start_datetime, end_datetime=None, reference_datetime=None, as_duration=False):
        """
        Umanizza un intervallo temporale completo con data e ora.
        """
        if reference_datetime is None:
            reference_datetime = datetime.now()

        date_part = Humanize.humanize_date(start_datetime, reference_datetime, as_duration)
        time_part = Humanize.humanize_time(start_datetime, end_datetime if end_datetime else None, as_duration)

        return f"{date_part} {time_part}"
    

if __name__ == "__main__":
    reference = datetime(2025, 1, 6, 12, 0)  # Riferimento: 6 gennaio 2025, mezzogiorno
    examples = [
        (reference + timedelta(days=1, hours=2), reference + timedelta(days=1, hours=5)),  # Domani dalle 14:00 alle 17:00
        (reference + timedelta(days=7, hours=2), reference + timedelta(days=7, hours=5)),  # Prossimo lunedì
        (reference + timedelta(days=10, hours=2), reference + timedelta(days=10, hours=5)),  # Il 16 gennaio
        (reference + timedelta(hours=3), reference + timedelta(hours=5)),  # Oggi dalle 15:00 alle 17:00
        (reference - timedelta(days=2, hours=2), reference - timedelta(days=2, hours=1)),  # Lo scorso sabato
        (reference, reference + timedelta(hours=2)),  # Oggi dalle 12:00 per 2 ore
        (reference, reference + timedelta(minutes=30)),  # Oggi dalle 12:00 per 15 minuti
    ]

    for start, end in examples:
        print(Humanize.humanize_datetime_range(start, end, reference, as_duration=True))
