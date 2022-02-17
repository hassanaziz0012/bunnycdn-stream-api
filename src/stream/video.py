from typing import List
import requests
from stream.helpers import send_bunny_request
from stream.chapter import Chapter
from stream.stream_settings import BASE_URL
from stream.moment import Moment


class Video:
    """
    Represents a Video on the Bunny CDN.
    """
    def __init__(self, library, video_id: str, **kwargs) -> None:
        self.video_id = video_id
        self.library = library
        
        # Setting the other variables from kwargs. If these don't exist, we will just fetch them by the library ID and video ID already provided.
        self.title = kwargs.get("title")
        if self.title == None:
            self._get_video_attributes()

        self.views = kwargs.get("views")
        self.date_uploaded = kwargs.get("date_uploaded")
        self.length = kwargs.get("length")
        self.framerate = kwargs.get("framerate")
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.resolutions = kwargs.get("resolutions")
        self.encode_progress = kwargs.get("encode_progress")
        self.size = kwargs.get("size")
        self.collection_id = kwargs.get("collection_id")
        self.thumbnail = kwargs.get("thumbnail")
        self.category = kwargs.get("category")

        if self.collection_id != None:
            print(type(self.collection_id))

    def _get_video_attributes(self):
        """
        Sends a request to the Bunny servers to get all video attributes for this video.
        
        Video title, views, date uploaded, resolutions, size, thumbnail, and other properties.

        Is a private method and not intended for public use. DO NOT use this method directly in your code.
        """
        endpoint = f'library/{self.library.LIBRARY_ID}/videos/{self.video_id}'
        data = send_bunny_request(endpoint=endpoint, method="GET", access_key=self.library.API_KEY)

        self.title = data.get("title")
        self.views = data.get("views")
        self.date_uploaded = data.get("dateUploaded")
        self.length = data.get("length")
        self.framerate = data.get("framerate")
        self.width = data.get("width")
        self.height = data.get("height")
        self.resolutions = data.get("availableResolutions").split(',') if data.get("availableResolutions") else None
        self.encode_progress = data.get("encodeProgress")
        self.size = data.get("storageSize")
        self.collection_id = data.get("collectionId")
        self.thumbnail = data.get("thumbnailFileName")
        self.category = data.get("category")

    def delete_video(self) -> bool:
        """
        Deletes the Video from Bunny.
        """
        endpoint = f'library/{self.library.LIBRARY_ID}/videos/{self.video_id}'
        data = send_bunny_request(endpoint=endpoint, method="DELETE", access_key=self.library.API_KEY)
        if data["success"] == True:
            return True
        else:
            return False

    def rename(self, new_title: str) -> bool:
        """
        Renames the Video title.
        
        <new_title> - The new title for the video.
        """
        endpoint = f"library/{self.library.LIBRARY_ID}/videos/{self.video_id}"
        data = send_bunny_request(endpoint=endpoint, method="POST", access_key=self.library.API_KEY, json={"title": str(new_title)})
        if data['success'] == True:
            return True
        else:
            return False

    def update_chapters(self, chapters: List[Chapter] = None) -> bool:
        """
        This method will update the Chapters in the Video.
        
        <chapters: List[Chapter]>
            A list of stream.chapter.Chapter objects that represent the chapters you want to have in your video.
            This can also be None. If the chapters list is None, then all chapters in the video will be removed.

        Returns:
            A boolean True/False based on whether the request was successfull or not.
        """
        endpoint = f"library/{self.library.LIBRARY_ID}/videos/{self.video_id}"

        if chapters == None:
            data = send_bunny_request(endpoint=endpoint, method="POST", access_key=self.library.API_KEY, json={"chapters": []})
        else:
            serialized_chapters = Chapter.serialize_all(chapters)
            data = send_bunny_request(endpoint=endpoint, method="POST", access_key=self.library.API_KEY, json={"chapters": serialized_chapters})
        
        if data['success'] == True:
            return True
        else:
            return False

    def update_moments(self, moments: List[Moment] = None) -> bool:
        """
        This method will update the Moments in the Video.
        
        <moments: List[Moment]>
            A list of stream.moment.Moment objects that represent the moments you want to have in your video.
            This can also be None. If the moments list is None, then all moments in the video will be removed.

        Returns:
            A boolean True/False based on whether the request was successfull or not.
        """
        endpoint = f"library/{self.library.LIBRARY_ID}/videos/{self.video_id}"

        if moments == None:
            data = send_bunny_request(endpoint=endpoint, method="POST", access_key=self.library.API_KEY, json={"moments": []})
        else:
            serialized_moments = Moment.serialize_all(moments)
            data = send_bunny_request(endpoint=endpoint, method="POST", access_key=self.library.API_KEY, json={"moments": serialized_moments})
        
        if data['success'] == True:
            return True
        else:
            return False

    def update_thumbnail(self, thumbnail_url: str) -> bool:
        """
        Updates the thumbnail image for the Video in Bunny.
        
        <thumbnail_url> - The direct URL pointing to the image that will be used as thumbnail."""
        endpoint = f"library/{self.library.LIBRARY_ID}/videos/{self.video_id}/thumbnail"
        data = send_bunny_request(endpoint=endpoint, method="POST", access_key=self.library.API_KEY, params={"thumbnailUrl": thumbnail_url})
        if data["success"] == True:
            return True
        else:
            return False

    def reencode(self) -> None:
        """
        Re-encodes the video.
        """
        endpoint = f"library/{self.library.LIBRARY_ID}/videos/{self.video_id}/reencode"
        data = send_bunny_request(endpoint=endpoint, method="POST", access_key=self.library.API_KEY)

    def __str__(self) -> str:
        return f"{self.title} - {self.video_id}"

    def __repr__(self) -> str:
        return f"{self.title} - {self.video_id}"