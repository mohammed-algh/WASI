import os
import googleapiclient.discovery
import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
from colorama import Fore, Back, Style


class Youtube:
    def __init__(self, YoutubeLink: str):
        self.YoutubeLink = YoutubeLink
        self.Youtube_API = self.initialFunction()

    def initialFunction(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyD85mxV3uWGQw_JpNuYir4vy_tosjYm_IE"
        Youtube_API = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)
        return Youtube_API

    def getVideoID(self):
        # process the link to return the video id
        if "/shorts/" in self.YoutubeLink:
            videoId = self.YoutubeLink.split("/shorts/")[1]
        else:
            session = requests.Session()
            response = session.head(self.YoutubeLink, allow_redirects=True)
            full_url = response.url
            parsed_url = urlparse(full_url)
            # get the video id from the url
            videoID = parse_qs(parsed_url.query)['v'][0]
        return videoID

    def getVideoMetaData(self):
        # return the array of general data about a YouTube vidoe
        # return (views, likes, dislikes, video publish date, number of comments and any metadata)
        return

    def getVideoComments(self):
        # return the array of general data about a YouTube vidoe
        # return (views, likes, dislikes, video publish date, number of comments and any metadata)
        numofComments=0
        request = self.Youtube_API.commentThreads().list(
            part="snippet",
            maxResults="100",
            videoId=self.getVideoID()
        )
        apiResponse = request.execute()
        arr=[]
        for comments in apiResponse["items"]:
            arr.append(comments["snippet"].get('topLevelComment').get('snippet').get('textOriginal'))
            numofComments=numofComments+1

        while apiResponse.get("nextPageToken") is not None:
            request = self.Youtube_API.commentThreads().list(
                part="snippet",
                maxResults="100",
                videoId=self.getVideoID(),
                pageToken=apiResponse.get("nextPageToken")
            )
            apiResponse = request.execute()
            for comments in apiResponse["items"]:
                arr.append(comments["snippet"].get('topLevelComment').get('snippet').get('textOriginal'))
                numofComments = numofComments + 1

        print(Fore.GREEN+"The number of comments is:",numofComments)
        print(Style.RESET_ALL)
        return arr

    def getLikelySpamComments(self):
        request = self.Youtube_API.commentThreads().list(
            part="snippet",
            maxResults="100",
            videoId=self.getVideoID(),
            moderationStatus="rejected"
        )
        apiResponse=request.execute()
        print(apiResponse.get("items"))
