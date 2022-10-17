#!/usr/bin/env python3

import os
import sys
import typing

from elasticsearch import Elasticsearch

from arcaflow_plugin_sdk import plugin
from es_schema import (
    ErrorOutput,
    SuccessOutput,
    StoreDocumentRequest
)


def getEnvironmentVariables(envUrl: str, envUser: str, envPassword: str) -> tuple[str, str, str]:
    """
    :return: a tuple [url, user, password] containing the extracted values 
    from the environment variables. 
    """
    return os.environ.get(envUrl), \
        os.environ.get(envUser), \
        os.environ.get(envPassword)


@plugin.step(
    id="elasticsearch",
    name="Elasticsearch",
    description="Load data into elasticsearch instance",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def store(
    params: StoreDocumentRequest
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:
    """
    :return: the string identifying which output it is, as well the output structure
    """

    url, user, password = getEnvironmentVariables(
        params.url, params.username, params.password)

    try:
        es = Elasticsearch(hosts=url, basic_auth=[user, password])
        resp = es.index(index=params.index, document=params.data)
        if resp.meta.status != 201:
            raise Exception(f"response status: {resp.meta.status}")

        return "success", SuccessOutput(f"successfully uploaded document for index {params.index}")
    except Exception as ex:
        return "error", ErrorOutput(
            f"Failed to create Elasticsearch document: {ex}"
        )


if __name__ == "__main__":
    sys.exit(plugin.run(plugin.build_schema(
        store
    )))
