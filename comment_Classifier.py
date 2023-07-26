import pickle
import pandas as pd
import numpy as np
from Preprocessing import doPreprocessing
import sklearn
import time


# function to count percentage of positive comments
def count_percentage(prediction: np.ndarray):
    positive_count = np.count_nonzero(prediction == 1)
    percentage = (positive_count / len(prediction)) * 100
    return int(percentage)


# recommendation function return recommendation word with percentage
def recommendation(prediction: np.ndarray, progress_bar):
    percentage = count_percentage(prediction)
    progress_bar.progress(85)
    time.sleep(0.3)
    if percentage < 0 or percentage > 100:
        raise ValueError('النسبة يجب ان تكون بين 0% و 100%')

    if percentage <= 30:
        return f"غير موصى به على الإطلاق({percentage}%)", percentage
    elif percentage <= 50:
        return f"يرجّح عدم مشاهدة هذا المقطع ({percentage}%)", percentage
    elif percentage <= 60:
        return f"محتوى المقطع محايد ({percentage}%)", percentage
    elif percentage <= 70:
        return f"موصى به ({percentage}%)", percentage
    elif percentage <= 80:
        return f"موصى به للغاية ({percentage}%)", percentage
    elif percentage <= 100:
        return f"موصى به بشدة ({percentage}%)", percentage


# classify function to start predicting
def classify(comments_list: list, choice: str, progress_bar):
    df = pd.DataFrame(comments_list, columns=['comment'])  # Convert comment_list to dataframe
    X = df["comment"]  # assign comment column to X variable
    progress_bar.progress(57)
    time.sleep(0.1)
    if len(X) <= 20:
        raise ValueError("Not enough comments to analyze the video")

    # SVM
    if choice == "SVM":
        model = pickle.load(open("classifiers/SVM.pkl", "rb"))  # Load SVM classifier from .pkl file
        y = model.predict(X)  # Predict
        df["prediction"] = y
        progress_bar.progress(75)
        time.sleep(0.1)
        recommend, percentage = recommendation(y, progress_bar)
        return recommend, percentage, df

    # Naive Bayes
    elif choice == "Naive Bayes":
        model = pickle.load(open("classifiers/NB.pkl", "rb"))  # Load Naive Bayes classifier from .pkl file
        y = model.predict(X)  # Predict
        df["prediction"] = y
        progress_bar.progress(75)
        time.sleep(0.1)
        recommend, percentage = recommendation(y, progress_bar)
        return recommend, percentage, df

    # Logistic Regression
    elif choice == "Logistic Regression":
        model = pickle.load(open("classifiers/LR.pkl", "rb"))  # Load Logistic Regression classifier from .pkl file
        y = model.predict(X)  # Predict
        df["prediction"] = y
        progress_bar.progress(75)
        time.sleep(0.1)
        recommend, percentage = recommendation(y, progress_bar)
        return recommend, percentage, df

    # K-Nearest Neighbors
    elif choice == "KNN":
        model = pickle.load(open("classifiers/KNN.pkl", "rb"))  # Load K-Nearest Neighbors classifier from .pkl file
        y = model.predict(X)  # Predict
        df["prediction"] = y
        progress_bar.progress(75)
        time.sleep(0.1)
        recommend, percentage = recommendation(y, progress_bar)
        return recommend, percentage, df

    # Decision Tree
    elif choice == "Decision Tree":
        model = pickle.load(open("classifiers/DT.pkl", "rb"))  # Load Decision Tree classifier from .pkl file
        y = model.predict(X)  # Predict
        df["prediction"] = y
        progress_bar.progress(75)
        time.sleep(0.1)
        recommend, percentage = recommendation(y, progress_bar)
        return recommend, percentage, df

    # Random Forest
    elif choice == "Random Forest":
        model = pickle.load(open("classifiers/RF.pkl", "rb"))  # Load Random Forest classifier from .pkl file
        y = model.predict(X)  # Predict
        df["prediction"] = y
        progress_bar.progress(75)
        time.sleep(0.1)
        recommend, percentage = recommendation(y, progress_bar)
        return recommend, percentage, df

    else:
        print("Wrong input")
        progress_bar.progress(0)
