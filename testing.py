from datetime import date, timedelta


today = f"{date.today()}"
tomorrow = f"{date.today() + timedelta(1)}"

print((today, tomorrow))