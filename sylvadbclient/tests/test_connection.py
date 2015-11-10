# -*- coding: utf-8 -*-
import os
import unittest

from sylvadbclient import Graph, API

SYLVADB_TOKEN = os.environ.get("SYLVADB_TOKEN", "default")
SYLVADB_GRAPH = os.environ.get("SYLVADB_GRAPH", None)


class ConnectionTesCase(unittest.TestCase):

    def test_can_instatiate_api(self):
        api = API(token=SYLVADB_TOKEN)
        self.assertTrue(api is not None)

    def test_can_list_graphs(self):
        api = API(token=SYLVADB_TOKEN)
        graphs = api.get_graphs()
        self.assertTrue(len(graphs) > 0)

    def test_can_select_a_graph(self):
        api = API(token=SYLVADB_TOKEN)
        slug = api.get_graphs()[0]["slug"]
        api.use(slug)
        self.assertTrue(api._slug is not None)

    def test_can_instantiate_graph(self):
        api = API(token=SYLVADB_TOKEN)
        slug = api.get_graphs()[0]["slug"]
        graph = Graph(slug, auth=SYLVADB_TOKEN)
        self.assertTrue(graph is not None)
