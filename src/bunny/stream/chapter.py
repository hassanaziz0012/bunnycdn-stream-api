from typing import Dict, List


class Chapter:
    """
    Represents a Chapter in a Video.
    """
    def __init__(self, title: str, start: int, end: int) -> None:
        self.title = title
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'{self.title} - {self.start}:{self.end}'

    def serialize(self) -> dict:
        """
        Serialize the Chapter object into JSON or a Python dictionary.
        """
        return {
            "title": self.title,
            "start": self.start,
            "end": self.end
        }

    @classmethod
    def serialize_all(cls, chapters: List['Chapter']) -> List[Dict]:
        """
        Serialize all given chapters into JSON or a Python dictionary.
        
        <chapters> - List of Chapter objects to be serialized.
        """
        result = []
        for chapter in chapters:
            data = chapter.serialize()
            result.append(data)
        return result