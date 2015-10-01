# -*- coding: utf-8 -*-
import os
import unittest

from sylvadbclient import Graph, API

SYLVADB_USER = os.environ.get("SYLVADB_USER", "default")
SYLVADB_PASS = os.environ.get("SYLVADB_PASS", "default")
SYLVADB_GRAPH = os.environ.get("SYLVADB_GRAPH", None)


class GraphTestSuite(unittest.TestCase):

    def setUp(self):
        self.api = API(auth=(SYLVADB_USER, SYLVADB_PASS))
        if not SYLVADB_GRAPH:
            self.slug = self.api.get_graphs()[0]["slug"]
        else:
            self.slug = SYLVADB_GRAPH
        self.api.use(self.slug)
        self.graph = Graph(self.slug, auth=(SYLVADB_USER, SYLVADB_PASS))

    def test_can_read_properties(self):
        self.assertTrue(self.graph.name is not None)
        self.assertTrue(self.graph.description is not None)

    def test_can_pull_properties(self):
        self.graph.pull()
        self.assertTrue(True)

    @unittest.skipIf(True, "TODO: Fix push problems")
    def test_can_push_properties(self):
        self.graph.push()
        self.assertTrue(True)

    @unittest.skipIf(True, "TODO: Fix problem with segmentation fault")
    def test_can_change_properties(self):
        _name = self.graph.name
        _description = self.graph.description
        name = "{} :)".format(self.graph.name)
        description = "{} :)".format(self.graph.description)
        self.graph.name = name
        self.graph.description = description
        self.assertTrue(self.graph.name == name)
        self.assertTrue(self.graph.description == description)
        self.graph.pull()
        self.assertTrue(self.graph.name == _name)
        self.assertTrue(self.graph.description == _description)
        self.graph.name = name
        self.graph.description = description
        self.graph.push()
        self.assertTrue(self.graph.name == name)
        self.assertTrue(self.graph.description == description)
        self.graph.pull()
        self.assertTrue(self.graph.name == name)
        self.assertTrue(self.graph.description == description)
        self.graph.name = _name
        self.graph.description = _description
        self.graph.push()
        self.graph.pull()
        self.assertTrue(self.graph.name == _name)
        self.assertTrue(self.graph.description == _description)

    def test_can_get_node_types(self):
        self.assertTrue(self.graph.nodes.types is not None)

    def test_can_list_all_nodes(self):
        datatype = self.graph.nodes.types[0]
        self.assertTrue(self.graph.nodes[datatype].all())

    def test_can_get_single_node(self):
        datatype = self.graph.nodes.types[0]
        self.assertTrue(self.graph.nodes[datatype].single())

    def test_can_iterate_over_nodes(self):
        datatype = self.graph.nodes.types[0]
        self.assertTrue([n for n in self.graph.nodes[datatype]] is not None)

    def test_can_count_nodes(self):
        datatype = self.graph.nodes.types[0]
        self.assertTrue(len(self.graph.nodes[datatype]) > 0)

    def test_can_get_rel_types(self):
        self.assertTrue(self.graph.rels.types is not None)

    def test_can_list_all_rels(self):
        datatype = self.graph.rels.types[0]
        self.assertTrue(self.graph.rels[datatype].all())

    def test_can_get_single_rel(self):
        datatype = self.graph.rels.types[0]
        self.assertTrue(self.graph.rels[datatype].single())

    def test_can_iterate_over_rels(self):
        datatype = self.graph.rels.types[0]
        self.assertTrue([n for n in self.graph.rels[datatype]] is not None)

    def test_can_count_rels(self):
        datatype = self.graph.rels.types[0]
        self.assertTrue(len(self.graph.rels[datatype]) > 0)
