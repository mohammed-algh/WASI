import pickle
import pandas as pd
import numpy as np
from Preprocessing import doPreprocessing
import sklearn
import time
# function to count percentage of positive comments
def count_percentage(prediction: np.ndarray):
    positive_count = np.count_nonzero(prediction == 1)
    percentage = (positive_count/ len(prediction)) * 100
    return int(percentage)


# recommendation function return recommendation word with percentage
def recommendation(prediction: np.ndarray,progress_bar):
    percentage = count_percentage(prediction)
    progress_bar.progress(100)
    time.sleep(0.3)
    if percentage < 0 or percentage > 100:
        raise ValueError('Percentage must be between 0 and 100')

    if percentage <= 30:
        return f"Not recommended ({percentage}%)"
    elif percentage <= 50:
        return f"Unlikely to be effective ({percentage}%)"
    elif percentage <= 60:
        return f"Moderately effective ({percentage}%)"
    elif percentage <= 70:
        return f"Recommended ({percentage}%)"
    elif percentage <= 80:
        return f"Highly recommended ({percentage}%)"
    elif percentage <= 100:
        return f"Strongly recommended ({percentage}%)"

# classify function to start predicting
def classify(comments_list:list, choice:str,progress_bar):

    df = pd.DataFrame(comments_list, columns=['comment'])  # Convert comment_list to dataframe
    X = df["comment"] # assign comment column to X variable
    progress_bar.progress(57)
    time.sleep(0.1)
    if len(X) == 0:
        raise ValueError("Not enough comments to analyze the video")


    # SVM
    if choice == "SVM":
        model = pickle.load(open("classifiers/SVM.pkl", "rb"))  # Load SVM classifier from .pkl file
        y = model.predict(X)  # Predict
        progress_bar.progress(90)
        time.sleep(0.1)
        return recommendation(y,progress_bar)

    # Naive Bayes
    elif choice == "Naive Bayes (Recommended)":
        model = pickle.load(open("classifiers/NB.pkl", "rb"))  # Load Naive Bayes classifier from .pkl file
        y = model.predict(X)  # Predict
        progress_bar.progress(90)
        time.sleep(0.1)
        return recommendation(y,progress_bar)

    # Logistic Regression
    elif choice == "Logistic Regression":
        model = pickle.load(open("classifiers/LR.pkl", "rb"))  # Load Logistic Regression classifier from .pkl file
        y = model.predict(X)  # Predict
        progress_bar.progress(90)
        time.sleep(0.1)
        return recommendation(y,progress_bar)

    # K-Nearest Neighbors
    elif choice == "KNN":
        model = pickle.load(open("classifiers/KNN.pkl", "rb"))  # Load K-Nearest Neighbors classifier from .pkl file
        y = model.predict(X)  # Predict
        progress_bar.progress(90)
        time.sleep(0.1)
        return recommendation(y,progress_bar)

    # Decision Tree
    elif choice == "Decision Tree":
        model = pickle.load(open("classifiers/DT.pkl", "rb"))  # Load Decision Tree classifier from .pkl file
        y = model.predict(X)  # Predict
        progress_bar.progress(90)
        time.sleep(0.1)
        return recommendation(y,progress_bar)

    # Random Forest
    elif choice == "Random Forest":
        model = pickle.load(open("classifiers/RF.pkl", "rb"))  # Load Random Forest classifier from .pkl file
        y = model.predict(X)  # Predict
        progress_bar.progress(90)
        time.sleep(0.1)
        return recommendation(y,progress_bar)

    else:
        print("Wrong input")
        progress_bar.progress(0)



