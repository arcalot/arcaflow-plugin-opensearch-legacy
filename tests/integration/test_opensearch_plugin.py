#!/usr/bin/env python3

import json
import os
import time
import unittest
import opensearch_plugin
import requests
from requests.auth import HTTPBasicAuth
from arcaflow_plugin_sdk import plugin


class StoreIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        if os.environ.get("OPENSEARCH_URL") == "":
            os.environ["OPENSEARCH_URL"] = "http://localhost:9200"
        if os.environ.get("OPENSEARCH_USERNAME") == "":
            os.environ["OPENSEARCH_USERNAME"] = "username"
        if os.environ.get("OPENSEARCH_PASSWORD") == "":
            os.environ["OPENSEARCH_PASSWORD"] = "topsecret"

    def test_empty_data(self) -> None:
        exitcode = plugin.run(
            s=plugin.build_schema(opensearch_plugin.store),
            argv=[
                "",
                "-f",
                StoreIntegrationTest.build_fixture_file_path(
                    "empty_data.yaml"
                ),
            ],
        )

        self.assertEqual(exitcode, 0)

        expectedData = {}
        self.assertStoredData(expectedData, "empty-data")

    def test_simple_data(self) -> None:
        exitcode = plugin.run(
            s=plugin.build_schema(opensearch_plugin.store),
            argv=[
                "",
                "-f",
                StoreIntegrationTest.build_fixture_file_path(
                    "simple_data.yaml"
                ),
            ],
        )

        self.assertEqual(exitcode, 0)

        expectedData = {
            "keyNo1": "xXx",
            "keyNo2": "Mambo No 5",
        }
        self.assertStoredData(expectedData, "simple-data")

    def test_nested_data(self) -> None:
        exitcode = plugin.run(
            s=plugin.build_schema(opensearch_plugin.store),
            argv=[
                "",
                "-f",
                StoreIntegrationTest.build_fixture_file_path(
                    "nested_data.yaml"
                ),
            ],
        )

        self.assertEqual(exitcode, 0)

        expectedData = {
            "keyNo3": "Mambo No 3",
            "nestedKey": {
                "deeper-nested-1": {
                    "deeper-nested-key": 1,
                    "another-key-deeply-nested": "here I am",
                },
                "deeper-nested-2": "some value",
            },
        }

        self.assertStoredData(expectedData, "nested-data")

    def assertStoredData(self, expectedData: dict, index: str):
        # retry so OpenSearch has enough time to process it
        for i in range(3):
            actualData = StoreIntegrationTest.get_opensearch_data(index)
            self.assertIn("hits", actualData)
            self.assertIn("hits", actualData["hits"])
            if len(actualData["hits"]["hits"]) == 0:
                time.sleep(i + 1)
                continue
            self.assertDictEqual(
                expectedData, actualData["hits"]["hits"][0]["_source"]
            )
            return
        self.fail(f"No documents found for index {index}")

    @staticmethod
    def build_fixture_file_path(fixtureFile: str) -> str:
        currDir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(currDir, "fixtures", fixtureFile)

    @staticmethod
    def get_opensearch_data(sample: str) -> dict:
        url, user, password = opensearch_plugin.getEnvironmentVariables(
            "OPENSEARCH_URL",
            "OPENSEARCH_USERNAME",
            "OPENSEARCH_PASSWORD",
        )
        elastiUrl = f"{url}/{sample}/_search"
        with requests.get(
            elastiUrl, auth=HTTPBasicAuth(user, password)
        ) as resp:
            return json.loads(resp.text)


if __name__ == "__main__":
    unittest.main()
