
import json
import os
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""
    API_KEY: str = os.environ.get('API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.url = f'https://www.youtube.com/channel/' + self.channel['items'][0]['id']
        self.description = self.channel['items'][0]['snippet']['description']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=os.getenv('API_KEY'))

    def to_json(self, filename):
        channel_info = {"title": self.title,
                        "channel_id": self.channel_id,
                        "description": self.description,
                        "url": self.url,
                        "subscriber_count": self.subscriber_count,
                        "video_count": self.video_count,
                        "view_count": self.view_count}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_info, file, indent=4, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel))
