from src.channel import Channel
from googleapiclient.discovery import build
import os

class Video(Channel):
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    id = None
    title = None
    url = None
    count_views = None
    like_count = None
    def __init__(self, uid) -> None:
        try:
            video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=uid
                                                         ).execute()

            self.id = uid
            self.title = video_response['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={uid}"
            self.count_views = video_response['items'][0]['statistics']['viewCount']
            self.count_likes = video_response['items'][0]['statistics']['likeCount']
        except:
            self.id = uid
            self.title = None
            self.url = None
            self.count_views = None
            self.like_count = None

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id, play_list_id):
        super().__init__(video_id)
        youtube = self.get_service()
        self.play_list_id = youtube.playlistItems().list(playlistId=play_list_id,
                                                         part='contentDetails',
                                                         maxResults=50,
                                                         ).execute()