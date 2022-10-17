from dataclasses import dataclass, field
from typing import Annotated
import typing

from arcaflow_plugin_sdk import validation, schema


@dataclass
class StoreDocumentRequest:
    url: str = field(
        metadata={
            'name': 'url',
            'description': """Name of the environment variable containing """
            """the URL for the Elasticsearch instance."""
        }
    )

    username: Annotated[str, validation.min(1)] = field(
        metadata={
            'name': 'username',
            'description': """Name of the environment variable containing """
            """an authorized user for the given Elasticsearch instance."""
        }
    )

    password: str = field(
        metadata={
            'name': 'password',
            'description': """Name of the environment variable containing the"""
            """password for the given user."""
        }
    )

    index: Annotated[str, validation.min(1)] = field(
        metadata={
            'name': 'index',
            'description': """Name of the Elasticsearch index that will receive the data. """
        }
    )

    data: typing.Dict[str, typing.Any] = field(
        metadata={
            'name': 'data',
            'description': """Data to upload to your Elasticsearch index."""
        }
    )


@dataclass
class SuccessOutput:
    """
    This is the output data structure for the success case.
    """
    message: str


@dataclass
class ErrorOutput:
    """
    This is the output data structure in the error case.
    """
    error: str
