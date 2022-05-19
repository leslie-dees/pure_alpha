from datetime import datetime
from datetime import date
from datetime import timedelta
import csv
import numpy as np
import pytz

<<<<<<< HEAD
with open('Projects - Upcoming Projects.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    list_of_rows = list(csv_reader)
    projects_list = np.array(list_of_rows)
    projects_list = projects_list[1:]

project = projects_list[9]
datez = project[3]
timez = project[4]

timezone = pytz.timezone('America/New_York')

this_datetime_obj = datetime.strptime(datez+timez, '%m/%d/%Y%I:%M %p')
start_time = this_datetime_obj.replace(tzinfo=timezone)
time_rn = datetime.now().astimezone(tz=timezone)

print(start_time)

time_delta = start_time - time_rn
print(time_delta)
=======
print("hello world")
>>>>>>> 878fd4107cb7e57d83edf325114ac0d9d9a802d3
