#!/usr/bin/env python3

import unittest
import opensearch_plugin
from arcaflow_plugin_sdk import plugin


class StoreTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            opensearch_plugin.StoreDocumentRequest(
                url="OPENSEARCH_URL",
                username="OPENSEARCH_USERNAME",
                password="OPENSEARCH_PASSWORD",
                index="another-index",
                data={
                    "key1": "interesting value",
                    "key2": "next value",
                },
            )
        )

        plugin.test_object_serialization(
            opensearch_plugin.SuccessOutput(
                "successfully uploaded document for index another-index"
            )
        )

        plugin.test_object_serialization(
            opensearch_plugin.ErrorOutput(
                "Failed to create OpenSearch document: BadRequestError(400,"
                " 'mapper_parsing_exception','failed to parse')"
            )
        )


if __name__ == "__main__":
    unittest.main()
