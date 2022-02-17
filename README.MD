# BunnyCDN API Wrapper
This is an API wrapper built for using the Bunny.net API in Python.

It currently only supports the Stream API, but I do plan on covering the Edge Storage API and other functionalities soon.

## Getting Started
Install the package from PyPi. (Link: https://pypi.org/project/bunnycdn-api-wrapper/1.0.14/)

    pip install bunnycdn-api-wrapper

Now, you are ready to start using the API. Here are some examples on how to use the API:

    # Libraries
    # Connecting the video libraries.
    from bunny.stream.library import Library
    lib = Library(LIBRARY_ID=12345, API_KEY="abcd1234")

    # Get all videos and collections in a library.
    videos = lib.get_library_videos()
    collections = lib.get_collections()

    # Creating and Uploading a new video to Bunny.
    from pathlib import Path
    lib.create_new_video(title="New Video", filepath=Path("path/to/file.mp4"))


    # Collections
    from bunny.stream.collection import Collection
    your_collection = Collection(library=lib, collection_id="COLLECTION ID") # Getting the collection.
    your_collection.delete() # Delete a collection.

    Collection.get_all_collections(library=lib) # Get all collections in a library.

    Collection.search_collections(library=lib, title="Search term") # Search collections in a library for the "title" specified.

    Collection.create_new_collection(library=lib, collection_name="New Collection") # Creating new collections.


    # Videos
    from bunny.stream.video import Video
    video = Video(library=lib, video_id="VIDEO ID") # Getting video.

    video.rename("Video title updated") # Rename the video.

    video.reencode() # Re-encode the video.

    video.update_thumbnail(thumbnail_url="https://www.images.com/thumbnail.jpg") # Updating video thumbnail.

    video.delete() # Delete video from Bunny.

    # Updating video chapters
    from bunny.stream.chapter import Chapter
    prologue = Chapter("Prologue", start=0, end=60)
    epilogue = Chapter("Epilogue", start=240, end=300)

    chapters = [prologue, epilogue]

    video.update_chapters(chapters) # Update video chapters.

    # Updating video moments
    from bunny.stream.moment import Moment
    moment_1 = Moment("Label", timestamp=225)
    moment_2 = Moment("Label", timestamp=300)

    moments = [moment_1, moment_2]

    video.update_moments(moments) # Update video moments.