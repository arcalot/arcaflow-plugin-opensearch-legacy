#!/usr/bin/env python3

import os
import sys
import typing

from opensearchpy import OpenSearch

from arcaflow_plugin_sdk import plugin
from es_schema import ErrorOutput, SuccessOutput, StoreDocumentRequest


@plugin.step(
    id="elasticsearch",
    name="Elasticsearch",
    description="Load data into elasticsearch instance",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def store(
    params: StoreDocumentRequest,
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:
    """
    :return: the string identifying which output it is, as well the output
        structure
    """

    try:
        if params.username:
            es = OpenSearch(hosts=params.url, basic_auth=[params.username, params.password])
        # Support for servers that don't require authentication
        else:
            es = OpenSearch(hosts=params.url)
        resp = es.index(index=params.index, body=params.data)

        return "success", SuccessOutput(
            f"successfully uploaded document for index {params.index}"
        )
    except Exception as ex:
        return "error", ErrorOutput(
            f"Failed to create Elasticsearch document: {ex}"
        )


if __name__ == "__main__":
    sys.exit(plugin.run(plugin.build_schema(store)))
