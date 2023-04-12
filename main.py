
from YoutubeExtractor import startGet

condition = True

while condition:

    link = str(input("Enter Video Link: "))
    try:

            # classifiers menu
        output = int(input("Choose:\n"
                           "1- SVM\n"
                           "2- Naive Bayes\n"
                           "3- Logistic Regression\n"
                           "4- K-Nearest Neighbors\n"
                           "5- Decision Tree\n"
                           "6- Random forest\n"))

        if output == 1:
            choice = "SVM"
        elif output == 2:
            choice = "Naive Bayes (Recommended)"
        elif output == 3:
            choice = "Logistic Regression"
        elif output == 4:
            choice = "KNN"
        elif output == 5:
            choice = "Decision Tree"
        elif output == 6:
            choice = "Random Forest"
        else:
            print("Wrong input")



        recommendation = startGet(link, choice)
        print(recommendation)

    except Exception as e:
        continue

    condition = False