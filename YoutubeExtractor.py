import requests
from googleapiclient.discovery import build
import re
from comment_Classifier import classify
from Preprocessing import clean_youtube
from urllib.parse import urlparse
from urllib.parse import parse_qs


api_key = 'AIzaSyCeOTkJfH0_XNhpzeVg3zrDF3Xetgjbt9w'

all_comments = []

def get_video_id(link:str)->str:

    full_url = unshorten_url(link)
    parsed_url = urlparse(full_url)

    # get the video id from the url
    videoId = parse_qs(parsed_url.query)['v'][0]

    return videoId

# function for unshort urls
def unshorten_url(url:str)->str:
    session = requests.Session()
    response = session.head(url, allow_redirects=True)
    return response.url

# extract comments from video
def get_comments(youtube, video_id, next_view_token):
    global all_comments

    # check for token
    if len(next_view_token.strip()) == 0:
        all_comments = []
    try:
        if next_view_token == '':
            # get the initial response
            comment_list = youtube.commentThreads().list(part = 'snippet', maxResults = 100, videoId = video_id, order = 'relevance').execute()
        else:
            # get the next page response
            comment_list = youtube.commentThreads().list(part = 'snippet', maxResults = 100, videoId = video_id, order='relevance', pageToken=next_view_token).execute()
    except Exception as error:
        if "commentsDisabled" in str(error):
            print("Comment of this video disabled")
            print()
        if "videoNotFound" in str(error):
            print("Video not found")
            print()

    # loop through all comments
    author_ID_List = []
    for comment in comment_list['items']:

        # add comment to list
        if len(clean_youtube(str([comment['snippet']['topLevelComment']['snippet']['textDisplay']]))) >=3 :
            try:
                author_ID = [comment['snippet']['topLevelComment']['snippet']['authorChannelId']['value']]
                author_Comment = [comment['snippet']['topLevelComment']['snippet']['textDisplay']]
            except:
                pass

            # to remove author repeated comments.
            if author_ID not in author_ID_List and not bool(re.search('[a-zA-Z]+', str(author_Comment))):
                author_ID_List.append(author_ID)

                all_comments.append(*author_Comment)


    if "nextPageToken" in comment_list:
        return get_comments(youtube, video_id, comment_list['nextPageToken'])
    else:
        return

def startGet(link:str, choice:str):
    global video_id
    try:
        video_id = get_video_id(link)
    except:
        print("Invalid link\n")
        raise ValueError("Invalid link")

    yt_object = build('youtube', 'v3', developerKey=api_key)

    # get all comments
    get_comments(yt_object, video_id, '')
    recommendation = classify(all_comments, choice)
    return recommendation


