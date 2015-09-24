# -*- coding: utf-8 -*-
import slumber


class SylvadbApiClient():
    # The idea is that this attr get a default value
    sylvadb_api = None

    # Method to connect to the SylvadbAPI
    def api_connect(self, host, auth):
        self.sylvadb_api = slumber.API(host,
                                       auth=auth)

    # Let's start with the API methods that encapsules the client

    # Graphs methods
    def get_graphs(self):
        return self.sylvadb_api.graphs.get()

    def post_graph(self, params=None):
        # The params available here are:
        # - name
        # - description
        return self.sylvadb_api.graphs.post(params)

    def get_graph(self, graph_slug):
        return self.sylvadb_api.graphs(graph_slug).get()

    def put_graph(self, graph_slug, params=None):
        # The params available here are:
        # - name
        # - description
        # - public
        return self.sylvadb_api.graphs(graph_slug).put(params)

    def patch_graph(self, graph_slug, params=None):
        # The params available here are:
        # - name
        # - description
        # - public
        return self.sylvadb_api.graphs(graph_slug).patch(params)

    def delete_graph(self, graph_slug):
        return self.sylvadb_api.graphs(graph_slug).delete()

    # Schema methods
    def get_nodetypes(self, graph_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes.get())

    def post_nodetypes(self, graph_slug, params):
        # The params available here are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes.get())

    def get_relationshiptypes(self, graph_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships.get())

    def post_relationshiptypes(self, graph_slug):
        # The params available here are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships.get())

    def get_nodetype(self, graph_slug, nodetype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug).get())

    def delete_nodetype(self, graph_slug, nodetype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug).delete())

    def get_nodetype_schema(self, graph_slug, nodetype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.get())

    def put_nodetype_schema(self, graph_slug, nodetype_slug, params=None):
        # The params available here are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.put(params))

    def patch_nodetype_schema(self, graph_slug, nodetype_slug, params=None):
        # The params available here are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.patch(params))

    def get_nodetype_schema_properties(self, graph_slug, nodetype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.properties.get())

    def post_nodetype_schema_properties(self, graph_slug,
                                        nodetype_slug, params=None):
        # The params available here are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.properties.post(params))
