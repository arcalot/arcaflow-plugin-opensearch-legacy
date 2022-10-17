#!/usr/bin/env python3

import unittest
import es_plugin
from arcaflow_plugin_sdk import plugin


class StoreTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            es_plugin.StoreDocumentRequest(
                url="ELASTICSEARCH_URL",
                username="ELASTICSEARCH_USERNAME",
                password="ELASTICSEARCH_PASSWORD",
                index="another-index",
                data={
                    "key1": "interesting value",
                    "key2": "next value", }
            )
        )

        plugin.test_object_serialization(
            es_plugin.SuccessOutput("successfully uploaded document for index another-index")
        )

        plugin.test_object_serialization(
            es_plugin.ErrorOutput(
                'Failed to create Elasticsearch document: BadRequestError(400, \'mapper_parsing_exception\',\'failed to parse\')')
        )

if __name__ == '__main__':
    unittest.main()
