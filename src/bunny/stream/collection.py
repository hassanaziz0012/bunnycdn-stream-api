from typing import List
from bunny.stream.helpers import send_bunny_request

class Collection:
    """
    Represents a Collection in Bunny.
    """
    def __init__(self, library, collection_id: str) -> None:
        self.library = library
        self.collection_id = collection_id
        self._get_attributes()

    def _get_attributes(self) -> None:
        """
        Validates the Collection to make sure it exists, and also assigns the attributes from the Get Collection request.
        """
        endpoint = f"library/{self.library.LIBRARY_ID}/collections/{self.collection_id}"
        data = send_bunny_request(endpoint=endpoint, method="GET", access_key=self.library.API_KEY, error_message_404="Invalid Collection ID or Library specified.")
        
        self.name = data['name']
        self.video_count = data['videoCount']
        self.total_size = data['totalSize']

    @staticmethod
    def _get_all_collections(library, search_term: str = None) -> List["Collection"]:
        """
        The private method to get all collections or to search for them in a given library.
        
        Since both the Collection.get_all_collections() and the Collection.search_collections() methods use the same logic and the same endpoint, 
        the logic has been extracted to this method and both methods now just call this method for results.

        <library> - The library from which Collections will be returned.
        <search_term> - Optional argument. If sent, only matching Collections will be returned.

        Returns:
            A list of Collection objects.
        """
        endpoint = f"library/{library.LIBRARY_ID}/collections"

        page = 1
        while True:
            if search_term:
                params = {'page': page, 'search': search_term}
            else:
                params = {'page': page}
                
            data = send_bunny_request(endpoint=endpoint, method="GET", access_key=library.API_KEY, params=params)
            items = data["items"]

            if len(items) == 0:
                break

            for item in items:
                library._collections.append(Collection(library=library, collection_id=item["guid"]))
            page += 1

        return library._collections

    @classmethod
    def get_all_collections(cls, library) -> List['Collection']:
        """
        Gets all the Collections in a given Library.
        
        <library> - The Library object that is being searched.

        Returns:
            A list of the Collection objects found.
        """
        return cls._get_all_collections(library)

    @classmethod
    def search_collections(cls, library, title: str) -> List['Collection']:
        """
        Searches the Collections in a specified Library for a given title.
        
        <library> - A stream.library.Library object that represents the library to be searched.
        <title> - The search term to be searched.
        
        Returns:
            A list of the matching Collection objects.
        """
        return cls._get_all_collections(library, title)

    @staticmethod
    def create_new_collection(library, collection_name: str) -> 'Collection':
        """
        Creates a new Collection in Bunny.

        <library> - A stream.library.Library object that represents the Library this Collection will belong to.
        <collection_name> - The name of the new Collection.
        """
        endpoint = f"library/{library.LIBRARY_ID}/collections"
        data = send_bunny_request(endpoint=endpoint, method="POST", access_key=library.API_KEY, json={"name": collection_name})
        return Collection(library=library, collection_id=data['guid'])

    def delete(self) -> bool:
        """
        Deletes the Collection from Bunny.
        
        Returns a Boolean True/False based on whether the deletion was successfull or not.
        """
        endpoint = f"library/{self.library.LIBRARY_ID}/collections/{self.collection_id}"
        data = send_bunny_request(endpoint=endpoint, method="DELETE", access_key=self.library.API_KEY)
        if data['success'] == True:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f'{self.name} - Collection in Library {self.library.LIBRARY_ID}'

    def __repr__(self) -> str:
        return f'{self.name} - Collection in Library {self.library.LIBRARY_ID}'
        