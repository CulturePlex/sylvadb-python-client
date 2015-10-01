# -*- coding: utf-8 -*-
import os
import unittest

from sylvadbclient import Graph, API

SYLVADB_USER = os.environ.get("SYLVADB_USER", "default")
SYLVADB_PASS = os.environ.get("SYLVADB_PASS", "default")
SYLVADB_GRAPH = os.environ.get("SYLVADB_GRAPH", None)


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.api = API(auth=(SYLVADB_USER, SYLVADB_PASS))
        if not SYLVADB_GRAPH:
            self.slug = self.api.get_graphs()[0]["slug"]
        else:
            self.slug = SYLVADB_GRAPH
        self.api.use(self.slug)
        self.graph = Graph(self.slug, auth=(SYLVADB_USER, SYLVADB_PASS))

    def test_can_list_nodetypes(self):
        nodetypes = self.api.get_nodetypes()
        self.assertTrue(len(nodetypes) > 0)
