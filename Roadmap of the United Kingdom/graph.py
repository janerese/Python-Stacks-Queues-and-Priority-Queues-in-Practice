# Define a custom data type representing a city in the road map

from typing import NamedTuple

# Extend a named tuple to ensure that node objects are hashable, which is required by networkx
class City(NamedTuple):
    name: str
    country: str
    year: int | None
    latitude: float
    longitude: float

    @classmethod
    # The .from_dict() class method takes a dictionary of attributes extracted from a DOT file and returns a new instance of your City class
    def from_dict(cls, attrs):
        return cls(
            name=attrs["xlabel"],
            country=attrs["country"],
            year=int(attrs["year"]) or None,
            latitude=float(attrs["latitude"]),
            longitude=float(attrs["longitude"]),
        )