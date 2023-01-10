#!/usr/bin/env python3

import sys
import typing

from opensearchpy import OpenSearch

from arcaflow_plugin_sdk import plugin
from opensearch_schema import ErrorOutput, SuccessOutput, StoreDocumentRequest


@plugin.step(
    id="opensearch",
    name="OpenSearch",
    description="Load data into opensearch compatible instance",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def store(
    params: StoreDocumentRequest,
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    try:
        if params.username:
            opensearch = OpenSearch(
                hosts=params.url, basic_auth=[params.username, params.password]
            )
        # Support for servers that don't require authentication
        else:
            opensearch = OpenSearch(hosts=params.url)
        resp = opensearch.index(index=params.index, body=params.data)
        if resp["result"] != "created":
            raise Exception(f"Document status: {resp['_shards']}")

        return "success", SuccessOutput(
            f"Successfully uploaded document for index {params.index}"
        )
    except Exception as ex:
        return "error", ErrorOutput(
            f"Failed to create OpenSearch document: {ex}"
        )


if __name__ == "__main__":
    sys.exit(plugin.run(plugin.build_schema(store)))
