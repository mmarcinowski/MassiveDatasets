import numpy as np
import matplotlib.pyplot as plt
from utils.load import convert_to_onehot
from utils.evaluate import scorer_squared_error, scorer_01loss
from utils.load import read_and_convert_pandas_files
import time


def evaluate_accuracy_and_time(classifier, X_train, y_train, X_test, y_test):
    start=time.clock()
    classifier.fit(X_train, y_train)
    end=time.clock()
    training_time = end-start
    scores=[]
    #print("Training time = {0}".format(training_time))

    scorers = [(scorer_01loss, "0/1 loss"), (scorer_squared_error, "squared error")]
    for scorer, scorer_name in scorers:
        a = scorer(classifier, X_train, y_train)
        b = scorer(classifier, X_test, y_test)
        #print("Train {0} = {1}".format(scorer_name, scorer(classifier, X_train, y_train)))
        #print("Test {0} = {1}".format(scorer_name, scorer(classifier, X_test, y_test)))
        scores.append(a)
        scores.append(b)
    #print(scorers[0](classifier, X_train, y_train))
    return [training_time, scores]
