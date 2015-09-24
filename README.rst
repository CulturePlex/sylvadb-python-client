SylvaDB API - Python Client
========================

The SylvaDB API client allows the interaction with the SylvaDB API in an easily and flexible way. The abstraction of all the entire environment is done thanks to an awesome package called slumber.

Installation_
-------------

Coming soon


`Getting started`_
------------------

To start, we need to instance the main class called *SylvadbApiClient*. It takes two parameters, the host where our api is running and the authorization to establish the connection:

.. code:: python

  >>> from sylvadbpythonclient.apiclient import SylvadbApiClient

  >>> api = SylvadbApiClient("http://localhost:8000/api/", ("default", "default"))

Right now, we can interact with the api using the available methods (see the docs). All the responses that we obtain are in JSON format:

.. code:: python

  # We get all the graphs for user "default"
  >>> api.get_graphs()

  # We get the graph called "test"
  >>> api.get_graph("test")

  # We get the graph called "test"
  >>> api.get_graph("test")

  # We get the graph node types
  >>> api.get_nodetypes("test")
