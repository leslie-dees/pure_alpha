import numpy as np
import make_full_dataset
from sklearn import linear_model as linear
from sklearn.model_selection import train_test_split
import warnings
from sklearn.exceptions import ConvergenceWarning
import csv

warnings.simplefilter("ignore", category=ConvergenceWarning)
        

my_path = input("Insert datapath: ")

with open(my_path, 'r') as csv_file:
    csv_reader = csv.reader()
    list_of_rows = list(csv_reader)
    list_of_rows = np.array(list_of_rows)

response_variable = list_of_rows[1, :]
all_nft_parameters = list_of_rows[2:, :]

x_train, x_test ,y_train, y_test = train_test_split(all_nft_parameters, response_variable, test_size=0.20)

clf = linear.Ridge(alpha = 1, max_iter= 100000, fit_intercept=False, positive = True)
clf.fit(x_train, y_train)
score = clf.score(x_test, y_test)
print(score)