from typing import List


class Moment:
    """
    Represents a Moment in a Video.
    """
    def __init__(self, label: str, timestamp: int) -> None:
        self.label = label
        self.timestamp = timestamp
    
    def serialize(self) -> dict:
        """
        Serializes a Moment object into JSON or a Python Dictionary.
        """
        return {"label": self.label, "timestamp": self.timestamp}

    @classmethod
    def serialize_all(cls, moments: List) -> List[dict]:
        """
        Serializes all given moments into JSON or a Python Dictionary.
        
        <moments> - A list of Moment objects to be serialized.
        """
        result = []
        for moment in moments:
            result.append(moment.serialize())
        return result
