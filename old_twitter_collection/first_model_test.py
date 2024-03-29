import numpy as np
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

alpha_tests = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]

best_alpha = 0
best_score = 0
best_cod_average = 100

for alphas in alpha_tests:
    min_score_dist = 100
    min_score = 10
    this_cod = 0
    for i in range(100):
        x_train, x_test ,y_train, y_test = train_test_split(all_nft_parameters, response_variable, test_size=0.20)

        clf = linear.Lasso(alpha = alphas, max_iter = 10000, fit_intercept=False, positive=True)
        clf.fit(x_train, y_train)
        scores = clf.score(x_test, y_test)
        if (1 - scores) < min_score_dist:
            min_score = scores
            min_score_dist = (1 - scores)
        this_cod+=scores
    #print("this_alpha", alphas)
    #print("best thing", min_score, "and", min_score_dist)
    avg_cod = this_cod/100
    #print("average", avg_cod)
    if abs((1-best_cod_average)) > abs(1-avg_cod):
        best_alpha = alphas
        best_cod_average = avg_cod
        best_clf = clf
    if abs(1-best_score) > abs(1-min_score):
        best_score = min_score
#print("my_alpha", best_alpha)
print("accuracy_score:", best_score)
#print("my_best_average_cod", best_cod_average)
