import numpy as np
import make_full_dataset
from sklearn import linear_model as linear
from sklearn.model_selection import train_test_split
import warnings
from sklearn.exceptions import ConvergenceWarning

warnings.simplefilter("ignore", category=ConvergenceWarning)
        

my_data = make_full_dataset.make_full_dataset(path = "nft_tweets\*.csv")
y_data = my_data['Current FP (as of 3/17)']
x_data = my_data.loc[:, my_data.columns !='Current FP (as of 3/17)']
x_data = x_data.loc[:, x_data.columns != 'Twitter']

alpha_tests = np.linspace(0.00000001, 0.001, 10)

best_alpha = 0
best_score = 0
best_cod_average = 100
for alphas in alpha_tests:
    min_score_dist = 100
    min_score = 10
    this_cod = 0
    for i in range(100):
        x_train, x_test ,y_train, y_test = train_test_split(x_data, y_data, test_size=0.20)

        clf = linear.Lasso(alpha = alphas, max_iter = 10000, fit_intercept=False, positive=True)
        clf.fit(x_train, y_train)
        scores = clf.score(x_test, y_test)
        if (1 - scores) < min_score_dist:
            min_score = scores
            min_score_dist = (1 - scores)
        this_cod+=scores
    print("this_alpha", alphas)
    print("best thing", min_score, "and", min_score_dist)
    avg_cod = this_cod/100
    print("average", avg_cod)
    if abs((1-best_cod_average)) > abs(1-avg_cod):
        best_alpha = alphas
        best_cod_average = avg_cod
    if abs(1-best_score) > abs(1-min_score):
        best_score = min_score
print("my_alpha", best_alpha)
print("my_best_score", best_score)
print("my_best_average_cod", best_cod_average)
