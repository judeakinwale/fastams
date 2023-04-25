from datetime import date, timedelta


# some minor changes
today = f"{date.today()}"
tomorrow = f"{date.today() + timedelta(1)}"

print((today, tomorrow))