import numpy as np
import csv

with open('Projects - Upcoming Projects.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    list_of_rows = list(csv_reader)
    projects_list = np.array(list_of_rows)
    projects_list = projects_list[1:]

listy = projects_list[13:17]
for project in listy:

    if project[3] == 'Locked':
        print("Locked")
    if project[3] == 'Closed':
        print("Closed")
    if project[3] == 'Open':
        print("Open")