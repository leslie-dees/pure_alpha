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
x_data = x_data.loc[:, x_data.columns != 'Launch date']

print(my_data)

x_train, x_test ,y_train, y_test = train_test_split(x_data, y_data, test_size=0.20)

clf = linear.Lasso(alpha = 1, max_iter= 100000, fit_intercept=False, positive = True)
clf.fit(x_train, y_train)
score = clf.score(x_test, y_test)
print(score)