from dataclasses import dataclass, field
from typing import Annotated
import typing

from arcaflow_plugin_sdk import validation


@dataclass
class StoreDocumentRequest:
    url: str = field(
        metadata={
            "name": "url",
            "description": """The URL for the Elasticsearch instance.""",
        }
    )

    index: Annotated[str, validation.min(1)] = field(
        metadata={
            "name": "index",
            "description": """Name of the Elasticsearch index that will """
            """receive the data. """,
        }
    )

    data: typing.Dict[str, typing.Any] = field(
        metadata={
            "name": "data",
            "description": """Data to upload to your Elasticsearch """
            """index.""",
        }
    )

    username: Annotated[str, validation.min(1)] = field(
        default=None,
        metadata={
            "name": "username",
            "description": """A username for"""
            """an authorized user for the given Elasticsearch instance.""",
        }
    )

    password: str = field(
        default=None,
        metadata={
            "name": "password",
            "description": """The password for the given user.""",
        }
    )


@dataclass
class SuccessOutput:
    """This is the output data structure for the success case."""

    message: str


@dataclass
class ErrorOutput:
    """This is the output data structure in the error case."""

    error: str
