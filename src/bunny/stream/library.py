from pathlib import Path
from typing import List
from bunny.stream.collection import Collection
from bunny.stream.helpers import handle_status_code, send_bunny_request
from bunny.stream.stream_settings import BASE_URL
from bunny.stream.video import Video
import requests


class Library:
    """
    Represents a Library in the Bunny CDN.
    """
    def __init__(self, LIBRARY_ID: int, API_KEY: str) -> None:
        self.LIBRARY_ID = LIBRARY_ID
        self.API_KEY = API_KEY

        self._videos = []
        self._collections = []

        self._validate()

    def _validate(self):
        """
        Send a request to the Bunny API using the provided Library ID and API Key to check whether both are valid or not.
        """

        url = BASE_URL + f'library/{self.LIBRARY_ID}/videos'
        headers = {"AccessKey": self.API_KEY}

        resp = requests.get(url, headers=headers)
        data = resp.json()

        handle_status_code(resp.status_code)
    
    def get_library_videos(self) -> List[Video]:
        """
        Get all the videos in the library.

        Returns the list of Video objects after getting them.
        """

        url = BASE_URL + f'library/{self.LIBRARY_ID}/videos'
        headers = {"AccessKey": self.API_KEY}

        i = 1
        while True:
            resp = requests.get(url, headers=headers, params={"page": i})
            data = resp.json()

            handle_status_code(resp.status_code)

            if resp.status_code == 200:
                items = data['items']

                i += 1
                if len(items) == 0: # This would mean we've reached the final page.
                    break

                for item in items:
                    video_id = item['guid']
                    title = item['title']
                    views = item['views']
                    date_uploaded = item['dateUploaded']
                    length = item['length']
                    framerate = item['framerate']
                    width = item['width']
                    height = item['height']
                    resolutions = item['availableResolutions'].split(',')
                    encode_progress = item['encodeProgress']
                    size = item['storageSize']
                    collection_id = item['collectionId'] if len(item['collectionId']) > 0 else None # Instead of None, it returns an empty string if the video has no Collection. We account for that here.
                    thumbnail = item['thumbnailFileName']
                    category = item['category']

                    obj = Video(
                        library=self, video_id=video_id, title=title, views=views, date_uploaded=date_uploaded, length=length, framerate=framerate, 
                        width=width, height=height, resolutions=resolutions, encode_progress=encode_progress, size=size, collection_id=collection_id, 
                        thumbnail=thumbnail, category=category
                    )
                    self._videos.append(obj)
        return self._videos

    def get_collections(self) -> List['Collection']:
        """
        Returns all the Collections in the Library.
        """
        return Collection.get_all_collections(library=self)

    def create_new_video(self, title: str, filepath: Path) -> Video:
        """
        Creates a new video based on the video title and the filepath specified.

        <title>: The title of the video.
        <filepath>: A pathlib.Path object that represents the file path of the video.

        Returns:
            A Video object which represents your uploaded video.
        """
        data = send_bunny_request(endpoint=f'library/{self.LIBRARY_ID}/videos', method="POST", access_key=self.API_KEY, json={"title": title})

        video_id = data['guid']

        try:
            with open(filepath, 'rb+') as file:
                print("Uploading file to Bunny. This may take a couple minutes. Please do not close the program during this time..")
                filedata = file.read()
                data = send_bunny_request(endpoint=f"library/{self.LIBRARY_ID}/videos/{video_id}", method="PUT", access_key=self.API_KEY, data=filedata)

            return Video(library=self, video_id=video_id)

        except FileNotFoundError: # Handling and raising the same error may seem weird, but it does abstract away the internal logics in the tracebacks.
            raise FileNotFoundError("No such file or directory:", filepath) 

    def __str__(self) -> str:
        return f"Library - {self.LIBRARY_ID}"