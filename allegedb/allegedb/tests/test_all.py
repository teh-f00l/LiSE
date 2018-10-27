# This file is part of allegedb, an object-relational mapper for versioned graphs.
# Copyright (c) Zachary Spector. public@zacharyspector.com
import unittest
from copy import deepcopy
import allegedb


testkvs = [0, 1, 10, 10**10, 10**10**4, 'spam', 'eggs', 'ham',  '💧', '🔑', '𐦖',('spam', 'eggs', 'ham')]
testvs = [['spam', 'eggs', 'ham'], {'foo': 'bar', 0: 1, '💧': '🔑'}]
testdata = []
for k in testkvs:
    for v in testkvs:
        testdata.append((k, v))
    for v in testvs:
        testdata.append((k, v))
testdata.append(('lol', deepcopy(testdata)))


class AllegedTest(unittest.TestCase):
    def setUp(self):
        self.engine = allegedb.ORM('sqlite:///:memory:')
        self.graphmakers = (self.engine.new_graph, self.engine.new_digraph, self.engine.new_multigraph, self.engine.new_multidigraph)


class AbstractGraphTest:
    def setUp(self):
        super().setUp()
        g = self.engine.new_graph('test')
        g.add_node(0)
        self.assertIn(0, g)
        g.add_node(1)
        self.assertIn(1, g)
        g.add_edge(0, 1)
        self.assertIn(1, g.adj[0])
        self.assertIn(0, g.adj[1])
        # TODO: test adding edges whose nodes do not yet exist
        self.engine.turn = 1
        self.assertIn(0, g)
        self.assertIn(1, g)
        self.engine.branch = 'no_edge'
        self.assertIn(0, g)
        self.assertIn(1, g)
        self.assertIn(1, g.adj[0])
        self.assertIn(0, g.adj[1])
        g.remove_edge(0, 1)
        self.assertIn(0, g)
        self.assertIn(1, g)
        self.assertNotIn(0, g.adj[1])
        self.assertNotIn(1, g.adj[0])
        self.engine.branch = 'triangle'
        g.add_node(2)
        self.assertIn(2, g)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 0)
        self.engine.branch = 'square'
        self.engine.turn = 2
        self.assertIn(2, g)
        self.assertIn(2, list(g.node.keys()))
        g.remove_edge(2, 0)
        g.add_node(3)
        g.add_edge(2, 3)
        g.add_edge(3, 0)
        self.engine.branch = 'nothing'
        g.remove_nodes_from((0, 1, 2, 3))
        self.engine.branch = 'trunk'
        self.engine.turn = 0


class AbstractBranchLineageTest(AbstractGraphTest):
    def runTest(self):
        """Create some branches of history and check that allegedb remembers where
        each came from and what happened in each.

        """
        self.assertTrue(self.engine.is_parent_of('trunk', 'no_edge'))
        self.assertTrue(self.engine.is_parent_of('trunk', 'triangle'))
        self.assertTrue(self.engine.is_parent_of('trunk', 'nothing'))
        self.assertTrue(self.engine.is_parent_of('no_edge', 'triangle'))
        self.assertTrue(self.engine.is_parent_of('square', 'nothing'))
        self.assertFalse(self.engine.is_parent_of('nothing', 'trunk'))
        self.assertFalse(self.engine.is_parent_of('triangle', 'no_edge'))
        g = self.engine.graph['test']
        self.assertIn(0, g.node)
        self.assertIn(1, g.node)
        self.assertIn(0, g.edge)
        self.assertIn(1, g.edge[0])
        self.engine.turn = 0

        def badjump():
            self.engine.branch = 'no_edge'
        self.assertRaises(ValueError, badjump)
        self.engine.turn = 2
        self.engine.branch = 'no_edge'
        self.assertIn(0, g)
        self.assertIn(0, list(g.node.keys()))
        self.assertNotIn(1, g.edge[0])
        self.assertRaises(KeyError, lambda: g.edge[0][1])
        self.engine.branch = 'triangle'
        self.assertIn(2, g.node)
        for orig in (0, 1, 2):
            for dest in (0, 1, 2):
                if orig == dest:
                    continue
                self.assertIn(orig, g.edge)
                self.assertIn(dest, g.edge[orig])
        self.engine.branch = 'square'
        self.assertNotIn(0, g.edge[2])
        self.assertRaises(KeyError, lambda: g.edge[2][0])
        self.engine.turn = 2
        self.assertIn(3, g.node)
        self.assertIn(1, g.edge[0])
        self.assertIn(2, g.edge[1])
        self.assertIn(3, g.edge[2])
        self.assertIn(0, g.edge[3])
        self.engine.branch = 'nothing'
        for node in (0, 1, 2):
            self.assertNotIn(node, g.node)
            self.assertNotIn(node, g.edge)
        self.engine.branch = 'trunk'
        self.engine.turn = 0
        self.assertIn(0, g.node)
        self.assertIn(1, g.node)
        self.assertIn(0, g.edge)
        self.assertIn(1, g.edge[0])


class BranchLineageTest(AbstractBranchLineageTest, AllegedTest):
    pass


class StorageTest(AllegedTest):
    def runTest(self):
        """Test that all the graph types can store and retrieve key-value pairs
        for the graph as a whole, for nodes, and for edges.

        """
        for graphmaker in self.graphmakers:
            g = graphmaker('testgraph')
            g.add_node(0)
            g.add_node(1)
            g.add_edge(0, 1)
            n = g.node[0]
            e = g.edge[0][1]
            if isinstance(e, allegedb.graph.MultiEdges):
                e = e[0]
            for (k, v) in testdata:
                g.graph[k] = v
                self.assertIn(k, g.graph)
                self.assertEqual(g.graph[k], v)
                del g.graph[k]
                self.assertNotIn(k, g.graph)
                n[k] = v
                self.assertIn(k, n)
                self.assertEqual(n[k], v)
                del n[k]
                self.assertNotIn(k, n)
                e[k] = v
                self.assertIn(k, e)
                self.assertEqual(e[k], v)
                del e[k]
                self.assertNotIn(k, e)
            self.engine.del_graph('testgraph')


class DictStorageTest(AllegedTest):
    """Make sure the dict wrapper works"""
    def runTest(self):
        for i, graphmaker in enumerate(self.graphmakers):
            self.engine.turn = i
            g = graphmaker('testgraph')
            g.add_node(0)
            g.add_node(1)
            g.add_edge(0, 1)
            n = g.node[0]
            e = g.edge[0][1]
            if isinstance(e, allegedb.graph.MultiEdges):
                e = e[0]
            for entity in g.graph, n, e:
                entity[0] = {'spam': 'eggs', 'ham': {'baked beans': 'delicious'}, 'qux': ['quux', 'quuux'],
                             'clothes': {'hats', 'shirts', 'pants'},
                             'dicts': {'foo': {'bar': 'bas'}, 'qux': {'quux': 'quuux'}}
                             }
            self.engine.turn = i + 1
            for entity in g.graph, n, e:
                self.assertEqual(entity[0]['spam'], 'eggs')
                entity[0]['spam'] = 'ham'
                self.assertEqual(entity[0]['spam'], 'ham')
                self.assertEqual(entity[0]['ham'], {'baked beans': 'delicious'})
                entity[0]['ham']['baked beans'] = 'disgusting'
                self.assertEqual(entity[0]['ham'], {'baked beans': 'disgusting'})
                self.assertEqual(entity[0]['qux'], ['quux', 'quuux'])
                entity[0]['qux'] = ['quuux', 'quux']
                self.assertEqual(entity[0]['qux'], ['quuux', 'quux'])
                self.assertEqual(entity[0]['clothes'], {'hats', 'shirts', 'pants'})
                entity[0]['clothes'].remove('hats')
                self.assertEqual(entity[0]['clothes'], {'shirts', 'pants'})
                self.assertEqual(entity[0]['dicts'], {'foo': {'bar': 'bas'}, 'qux': {'quux': 'quuux'}})
                del entity[0]['dicts']['foo']
                entity[0]['dicts']['qux']['foo'] = {'bar': 'bas'}
                self.assertEqual(entity[0]['dicts'], {'qux': {'foo': {'bar': 'bas'}, 'quux': 'quuux'}})
            self.engine.turn = i
            for entity in g.graph, n, e:
                self.assertEqual(entity[0]['spam'], 'eggs')
                self.assertEqual(entity[0]['ham'], {'baked beans': 'delicious'})
                self.assertEqual(entity[0]['qux'], ['quux', 'quuux'])
                self.assertEqual(entity[0]['clothes'], {'hats', 'shirts', 'pants'})
                self.assertEqual(entity[0]['dicts'], {'foo': {'bar': 'bas'}, 'qux': {'quux': 'quuux'}})
            self.engine.del_graph('testgraph')


class ListStorageTest(AllegedTest):
    """Make sure the list wrapper works"""

    def runTest(self):
        for i, graphmaker in enumerate(self.graphmakers):
            self.engine.turn = i
            g = graphmaker('testgraph')
            g.add_node(0)
            g.add_node(1)
            g.add_edge(0, 1)
            n = g.node[0]
            e = g.edge[0][1]
            if isinstance(e, allegedb.graph.MultiEdges):
                e = e[0]
            for entity in g.graph, n, e:
                entity[0] = ['spam', ('eggs', 'ham'), {'baked beans': 'delicious'}, ['qux', 'quux', 'quuux'],
                             {'hats', 'shirts', 'pants'}]
            self.engine.turn = i + 1
            for entity in g.graph, n, e:
                self.assertEqual(entity[0][0], 'spam')
                entity[0][0] = 'eggplant'
                self.assertEqual(entity[0][0], 'eggplant')
                self.assertEqual(entity[0][1], ('eggs', 'ham'))
                entity[0][1] = ('ham', 'eggs')
                self.assertEqual(entity[0][1], ('ham', 'eggs'))
                self.assertEqual(entity[0][2], {'baked beans': 'delicious'})
                entity[0][2]['refried beans'] = 'deliciouser'
                self.assertEqual(entity[0][2], {'baked beans': 'delicious', 'refried beans': 'deliciouser'})
                self.assertEqual(entity[0][3], ['qux', 'quux', 'quuux'])
                entity[0][3].pop()
                self.assertEqual(entity[0][3], ['qux', 'quux'])
                self.assertEqual(entity[0][4], {'hats', 'shirts', 'pants'})
                entity[0][4].discard('shame')
                entity[0][4].remove('pants')
                entity[0][4].add('sun')
                self.assertEqual(entity[0][4], {'hats', 'shirts', 'sun'})
            self.engine.turn = i
            for entity in g.graph, n, e:
                self.assertEqual(entity[0][0], 'spam')
                self.assertEqual(entity[0][1], ('eggs', 'ham'))
                self.assertEqual(entity[0][2], {'baked beans': 'delicious'})
                self.assertEqual(entity[0][3], ['qux', 'quux', 'quuux'])
                self.assertEqual(entity[0][4], {'hats', 'shirts', 'pants'})
            self.engine.del_graph('testgraph')


class SetStorageTest(AllegedTest):
    """Make sure the set wrapper works"""

    def runTest(self):
        for i, graphmaker in enumerate(self.graphmakers):
            self.engine.turn = i
            g = graphmaker('testgraph')
            g.add_node(0)
            g.add_node(1)
            g.add_edge(0, 1)
            n = g.node[0]
            e = g.edge[0][1]
            if isinstance(e, allegedb.graph.MultiEdges):
                e = e[0]
            for entity in g.graph, n, e:
                entity[0] = set(range(10))
            self.engine.turn = i + 1
            for entity in g.graph, n, e:
                self.assertEqual(entity[0], set(range(10)))
                for j in range(0, 12, 2):
                    entity[0].discard(j)
                self.assertEqual(entity[0], {1, 3, 5, 7, 9})
            self.engine.turn = i
            for entity in g.graph, n, e:
                self.assertEqual(entity[0], set(range(10)))
            self.engine.del_graph('testgraph')

class CompiledQueriesTest(AllegedTest):
    def runTest(self):
        """Make sure that the queries generated in SQLAlchemy are the same as
        those precompiled into SQLite.

        """
        from allegedb.alchemy import Alchemist
        self.assertTrue(hasattr(self.engine.query, 'alchemist'))
        self.assertTrue(isinstance(self.engine.query.alchemist, Alchemist))
        from json import load
        with open(self.engine.query.path + '/sqlite.json', 'r') as jsonfile:
            precompiled = load(jsonfile)
        self.assertEqual(
            precompiled.keys(), self.engine.query.alchemist.sql.keys()
        )
        for (k, query) in precompiled.items():
            self.assertEqual(
                query,
                str(
                    self.engine.query.alchemist.sql[k]
                )
            )


if __name__ == '__main__':
    unittest.main()
