from datetime import datetime

today = datetime.now()

# print(today.time() < datetime.strptime('15:30:00', '%H:%M:%S'))
# print(today.hour)

print(today.hour < 15 or (today.hour == 15 and today.minute <= 30))