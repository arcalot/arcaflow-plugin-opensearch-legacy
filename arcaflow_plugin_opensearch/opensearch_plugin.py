#!/usr/bin/env python3

import sys
import typing

from opensearchpy import OpenSearch

from arcaflow_plugin_sdk import plugin
from opensearch_schema import ErrorOutput, SuccessOutput, StoreDocumentRequest


def split_arrays(data) -> typing.Dict:
    type_of_val = type(data)
    if type_of_val == list:
        new_dict = {}
        for i, v in enumerate(data):
            new_dict[i] = split_arrays(v)
        return split_arrays(new_dict)
    elif type_of_val == dict:
        result = {}
        for k in data:
            result[split_arrays(k)] = split_arrays(data[k])
        return result
    elif isinstance(type_of_val, type(None)):
        return str("")
    else:
        return data


@plugin.step(
    id="opensearch",
    name="OpenSearch",
    description="Load data into opensearch compatible instance",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def store(
    params: StoreDocumentRequest,
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    if params.split_arrays:
        data = split_arrays(params.data)
    else:
        data = params.data

    if params.username:
        os = OpenSearch(
            hosts=params.url, basic_auth=[params.username, params.password]
        )
    # Support for servers that don't require authentication
    else:
        os = OpenSearch(hosts=params.url)

    try:
        os.index(index=params.index, body=data)

        return "success", SuccessOutput(
            f"Successfully uploaded document for index '{params.index}' to "
            f"'{params.url}'"
        )
    except Exception as ex:
        return "error", ErrorOutput(
            f"Failed to create OpenSearch document: {ex}"
        )


if __name__ == "__main__":
    sys.exit(plugin.run(plugin.build_schema(store)))
