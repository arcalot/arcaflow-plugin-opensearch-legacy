#!/usr/bin/env python3

import os
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
            os = OpenSearch(hosts=params.url, basic_auth=[params.username, params.password])
        # Support for servers that don't require authentication
        else:
            os = OpenSearch(hosts=params.url)
        resp = os.index(index=params.index, body=params.data)
        print(f"==>> resp is {resp}")
        # if resp.meta.status != 201:
        #     raise Exception(f"response status: {resp.meta.status}")

        return "success", SuccessOutput(
            f"successfully uploaded document for index {params.index}"
        )
    except Exception as ex:
        return "error", ErrorOutput(
            f"Failed to create OpenSearch document: {ex}"
        )


if __name__ == "__main__":
    sys.exit(plugin.run(plugin.build_schema(store)))
