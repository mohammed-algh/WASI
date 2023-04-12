import pickle
import pandas as pd
import numpy as np
from Preprocessing import doPreprocessing
import sklearn


# function to count percentage of positive comments
def count_percentage(prediction: np.ndarray):
    positive_count = np.count_nonzero(prediction == 1)
    percentage = (positive_count/ len(prediction)) * 100
    return int(percentage)


# recommendation function return recommendation word with percentage
def recommendation(prediction: np.ndarray):
    percentage = count_percentage(prediction)
    if percentage < 0 or percentage > 100:
        raise ValueError('Percentage must be between 0 and 100')

    if percentage <= 30:
        return f"not recommended ({percentage}%)"
    elif percentage <= 50:
        return f"unlikely to be effective ({percentage}%)"
    elif percentage <= 60:
        return f"moderately effective ({percentage}%)"
    elif percentage <= 70:
        return f"recommended ({percentage}%)"
    elif percentage <= 80:
        return f"highly recommended ({percentage}%)"
    elif percentage <= 100:
        return f"strongly recommended ({percentage}%)"

# classify function to start predicting
def classify(comments_list:list, choice:str):

    df = pd.DataFrame(comments_list, columns=['comment'])  # Convert comment_list to dataframe
    X = df["comment"] # assign comment column to X variable
    if len(X) == 0:
        raise ValueError("Not Enough comments to analyze")


    # SVM
    if choice == "SVM":
        model = pickle.load(open("classifiers/SVM.pkl", "rb"))  # Load SVM classifier from .pkl file
        y = model.predict(X)  # Predict
        return recommendation(y)

    # Naive Bayes
    elif choice == "Naive Bayes (Recommended)":
        model = pickle.load(open("classifiers/NB.pkl", "rb"))  # Load Naive Bayes classifier from .pkl file
        y = model.predict(X)  # Predict
        return recommendation(y)

    # Logistic Regression
    elif choice == "Logistic Regression":
        model = pickle.load(open("classifiers/LR.pkl", "rb"))  # Load Logistic Regression classifier from .pkl file
        y = model.predict(X)  # Predict
        return recommendation(y)

    # K-Nearest Neighbors
    elif choice == "KNN":
        model = pickle.load(open("classifiers/KNN.pkl", "rb"))  # Load K-Nearest Neighbors classifier from .pkl file
        y = model.predict(X)  # Predict
        return recommendation(y)

    # Decision Tree
    elif choice == "Decision Tree":
        model = pickle.load(open("classifiers/DT.pkl", "rb"))  # Load Decision Tree classifier from .pkl file
        y = model.predict(X)  # Predict
        return recommendation(y)

    # Random Forest
    elif choice == "Random Forest":
        model = pickle.load(open("classifiers/RF.pkl", "rb"))  # Load Random Forest classifier from .pkl file
        y = model.predict(X)  # Predict
        return recommendation(y)

    else:
        print("Wrong input")



