from dataclasses import dataclass
import typing
from arcaflow_plugin_sdk import schema, validation


@dataclass
class StoreDocumentRequest:

    url: typing.Annotated[
        str,
        schema.name("url"),
        schema.description("The URL for the Opensearch-compatible instance."),
    ]

    index: typing.Annotated[
        str,
        validation.min(1),
        schema.name("index"),
        schema.description("Name of the index that will receive the data."),
    ]

    data: typing.Annotated[
        typing.Dict[str, typing.Any],
        schema.name("data"),
        schema.description("Data to upload to your index"),
    ]

    username: typing.Annotated[
        typing.Optional[str],
        validation.min(1),
        schema.name("username"),
        schema.description(
            "A username for an authorized user for the given "
            "Opensearch-compatible instance."
        ),
    ] = None

    password: typing.Annotated[
        typing.Optional[str],
        schema.name("password"),
        schema.description("The password for the given user."),
    ] = None


@dataclass
class SuccessOutput:

    message: str


@dataclass
class ErrorOutput:

    error: str
