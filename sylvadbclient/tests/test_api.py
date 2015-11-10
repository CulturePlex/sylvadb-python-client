# -*- coding: utf-8 -*-
import os
import unittest

from sylvadbclient import Graph, API

SYLVADB_TOKEN = os.environ.get("SYLVADB_TOKEN", "default")
SYLVADB_GRAPH = os.environ.get("SYLVADB_GRAPH", None)


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.api = API(token=SYLVADB_TOKEN)
        if not SYLVADB_GRAPH:
            self.slug = self.api.get_graphs()[0]["slug"]
        else:
            self.slug = SYLVADB_GRAPH
        self.api.use(self.slug)
        self.graph = Graph(self.slug, auth=SYLVADB_TOKEN)

    def test_can_list_nodetypes(self):
        nodetypes = self.api.get_nodetypes()
        self.assertTrue(len(nodetypes) > 0)
