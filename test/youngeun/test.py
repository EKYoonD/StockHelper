from datetime import datetime
import time

from pandas._libs.tslibs.timestamps import Timestamp


date = datetime.now()

Timestamp_now = int(time.mktime(date.timetuple()))
print(Timestamp_now)
print(datetime.fromtimestamp(Timestamp_now))
# datetime.date.fromtimestamp(1583644364)