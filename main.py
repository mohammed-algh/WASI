from urllib.parse import urlparse
from urllib.parse import parse_qs
from YoutubeExtractor import unshorten_url, startGet

condition = True

while condition:

    try:

        url = str(input("Enter Youtube link: "))
        urlC = unshorten_url(url)
        parsed_url = urlparse(urlC)

        # get the video id from the url
        videoId = parse_qs(parsed_url.query)['v'][0]

    except:
        print("Invalid link")
        print()
        continue



    try:

            # classifiers menu
        choice = int(input("Choose:\n"
                           "1- SVM\n"
                           "2- Naive Bayes\n"
                           "3- Logistic Regression\n"
                           "4- K-Nearest Neighbors\n"
                           "5- Decision Tree\n"
                           "6- Random forest\n"))

        recommendation = startGet(videoId, choice)
        print(recommendation)

    except Exception as e:
        continue

    condition = False