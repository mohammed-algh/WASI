import requests
from googleapiclient.discovery import build
import re
from comment_Classifier import classify
from Preprocessing import clean_youtube
from urllib.parse import urlparse
from urllib.parse import parse_qs
import time
from datetime import datetime
import streamlit as st

api_key = st.secrets["YOUTUBE_KEY"]
service_name = 'youtube'
service_version = 'v3'
youtube = build(service_name, service_version, developerKey=api_key)


def get_video_id_no_bar(url):
    if "/shorts/" in url:
        videoId = url.split("/shorts/")[1]
    else:
        full_url = unshorten_url(url)
        parsed_url = urlparse(full_url)
        videoId = parse_qs(parsed_url.query)['v'][0]
    return videoId


def get_video_info(video_id):
    video_info = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
    if video_info['items']:
        video = video_info['items'][0]
        title = video['snippet']['title']
        publish_date_str = video['snippet']['publishedAt']
        publish_date = datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M:%S%z')
        publish_date_str_formatted = publish_date.strftime('%b %d, %Y at %I:%M %p')
        channel_name = video['snippet']['channelTitle']
        comment_count = video['statistics']['commentCount'] if 'statistics' in video and 'commentCount' in video[
            'statistics'] else 0
        return {'title': title, 'publish_date': publish_date_str_formatted, 'channel_name': channel_name,
                'comment_count': comment_count}
    else:
        return None


all_comments = []


def get_video_id(link: str, progress_bar) -> str:
    if "/shorts/" in link:
        videoId = link.split("/shorts/")[1]
    else:
        full_url = unshorten_url(link)
        progress_bar.progress(0)
        parsed_url = urlparse(full_url)
        # get the video id from the url
        videoId = parse_qs(parsed_url.query)['v'][0]
    time.sleep(0.5)
    progress_bar.progress(15)
    time.sleep(0.5)
    return videoId


# function for unshort urls
def unshorten_url(url: str) -> str:
    session = requests.Session()
    response = session.head(url, allow_redirects=True)
    return response.url


# extract comments from video
def get_comments(youtube, video_id, next_view_token):
    global all_comments
    comment_list = None

    # check for token
    if len(next_view_token.strip()) == 0:
        all_comments = []
    try:
        if next_view_token == '':
            # get the initial response
            comment_list = youtube.commentThreads().list(part='snippet', maxResults=100, videoId=video_id,
                                                         order='relevance').execute()
        else:
            # get the next page response
            comment_list = youtube.commentThreads().list(part='snippet', maxResults=100, videoId=video_id,
                                                         order='relevance', pageToken=next_view_token).execute()
    except Exception as error:
        if "commentsDisabled" in str(error):
            raise ValueError("Comment of this video disabled")
        if "videoNotFound" in str(error):
            raise ValueError("Video not found")

    # loop through all comments
    author_ID_List = []
    for comment in comment_list['items']:
        author_ID = None
        author_Comment = None
        # add comment to list
        if len(clean_youtube(str([comment['snippet']['topLevelComment']['snippet']['textDisplay']]))) >= 3:
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


def startGet(link: str, choice: str, progress_bar):
    global video_id
    try:
        video_id = get_video_id(link, progress_bar)
        progress_bar.progress(30)
        time.sleep(0.5)
    except:
        print("Invalid link\n")
        raise ValueError("Invalid link")

    yt_object = build('youtube', 'v3', developerKey=api_key)

    # get all comments
    get_comments(yt_object, video_id, '')

    response = yt_object.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    # Extract video title from response
    video_title = response['items'][0]['snippet']['title']

    progress_bar.progress(50)
    time.sleep(0.3)
    recommendation, percentage, df = classify(all_comments, choice, progress_bar)

    return recommendation, percentage, df, video_title
