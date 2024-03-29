import networkx as nx
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
import numpy as np

Tunnel = namedtuple('MPLSTunnel', 'index, cos, route invroute load')


class GraphUtil:
    SOURCE = 7
    TARGET = 10

    def __init__(self):
        self.graph = nx.Graph()
        self.__init_destination()
        self.__init_edges()
        self.__init_tunnels()
        self.init_network_load()

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, value):
        self._graph = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def unique_routes(self):
        route = []
        forward, backward = self.destinations

        for i in range(self.tunnels_cnt):
            temp = []
            if (self.source, self.target) in forward:
                to = self.routes(self.source, 8)
                if not to:
                    to.append(self.source)
                else:
                    to = to[0]
                temp.append(list(itertools.chain(
                    to, self.tunnels[i].route[1:])))

                if self.target != self.tunnels[i].route[-1]:
                    route_to_target = self.routes(
                        self.tunnels[i].route[-1], self.target)
                    for node in route_to_target[0][1:]:
                        temp[0].append(node)

            else:
                to = self.routes(self.source, 11)
                if not to:
                    to.append(self.source)
                else:
                    to = to[0]
                temp.append(list(itertools.chain(
                    to, self.tunnels[i].invroute[1:])))

                if self.target != self.tunnels[i].invroute[-1]:
                    route_to_target = self.routes(
                        self.tunnels[i].route[-1], self.target)
                    for node in route_to_target[0][1:]:
                        temp[0].append(node)

            route.append(temp[0])
            temp.clear()
        return route

    def routes(self, s, t):
        unique_routes = list(nx.all_simple_paths(
            self.graph, source=s, target=t))
        unique_routes.sort(key=len)
        return unique_routes

    @property
    def unique_routes_cnt(self):
        return len(self.unique_routes)

    @property
    def tunnels(self):
        return self.tuns

    @property
    def tunnels_cnt(self):
        return 5

    @property
    def tunnels_load(self):
        return [round(tun.load, 2)
                for tun in self.tunnels]

    def add_load(self, index, load):
        tunnel = self.tunnels[index]
        tunnel = Tunnel(tunnel.index, tunnel.cos,
                        tunnel.route, tunnel.invroute,
                        tunnel.load + load)
        self.tuns[index] = tunnel
        return self.tuns[index]

    @property
    def destinations(self):
        forward = [
            (7, 11),
            (7, 10),
            (6, 11),
            (6, 10),
            (5, 11),
            (5, 10),
            (8, 11),
            (8, 10),
        ]
        backward = [(dest[1], dest[0]) for dest in forward]
        return forward, backward

    def nodes_to_edges(self, node_route):
        edges = []
        y = node_route[0]
        for i in range(1, len(node_route)):
            x = y
            y = node_route[i]
            edge = (x, y)
            edges.append(edge)
        return edges

    def __init_edges(self):
        self.graph.add_nodes_from(list(range(1, 16)))

        edges = [
            (5, 6),
            (5, 8),
            (6, 1),
            (6, 8),
            (1, 7),
            (7, 2),
            (2, 8),
            (8, 9),
            (8, 12),
            (8, 15),
            (8, 13),
            (12, 4),
            (4, 11),
            (11, 3),
            (3, 10),
            (15, 13),
            (13, 11),
            (13, 9),
            (15, 14),
            (14, 13)
        ]
        for start, end in edges:
            self.graph.add_edge(start, end)

    def __init_tunnels(self):
        s = 8
        t = 11
        tunnel1 = Tunnel(
            0, 0, self.routes(s, t)[0], self.routes(s, t)[0][:: -1], 0)
        tunnel2 = Tunnel(
            1, 0, self.routes(s, t)[1], self.routes(s, t)[1][:: -1], 0)
        tunnel3 = Tunnel(
            2, 1, self.routes(s, t)[2], self.routes(s, t)[2][:: -1], 0)
        tunnel4 = Tunnel(
            3, 1, self.routes(s, t)[3], self.routes(s, t)[3][:: -1], 0)
        tunnel5 = Tunnel(
            4, 2, self.routes(s, t)[4], self.routes(s, t)[4][:: -1], 0)

        tunnel6 = Tunnel(5, tunnel1.cos, tunnel1.invroute, tunnel1.route, 0)
        tunnel7 = Tunnel(6, tunnel2.cos, tunnel2.invroute, tunnel2.route, 0)
        tunnel8 = Tunnel(7, tunnel3.cos, tunnel3.invroute, tunnel3.route, 0)
        tunnel9 = Tunnel(8, tunnel4.cos, tunnel4.invroute, tunnel4.route, 0)
        tunnel10 = Tunnel(9, tunnel5.cos, tunnel5.invroute, tunnel5.route, 0)

        self.tuns = []
        self.tuns.append(tunnel1)
        self.tuns.append(tunnel2)
        self.tuns.append(tunnel3)
        self.tuns.append(tunnel4)
        self.tuns.append(tunnel5)
        self.tuns.append(tunnel6)
        self.tuns.append(tunnel7)
        self.tuns.append(tunnel8)
        self.tuns.append(tunnel9)
        self.tuns.append(tunnel10)

    def init_network_load(self):
        self.clear_edges_load()
        while True:
            for tun in self.tunnels[0:5]:
                self.add_load(tun.index, round(
                    np.random.uniform(0.04, 0.2), 2))

            if max(self.tunnels_load) >= 0.2:
                self.clear_edges_load()
                continue

            for i in range(self.tunnels_cnt):
                tunnel = self.tunnels[i]
                tunnel = Tunnel(tunnel.index, tunnel.cos,
                                tunnel.route, tunnel.invroute,
                                self.tunnels_load[i])
                self.tuns[i] = tunnel

            for i in range(5, 10):
                tunnel = self.tunnels[i]
                tunnel = Tunnel(tunnel.index, tunnel.cos,
                                tunnel.route, tunnel.invroute,
                                self.tuns[i-5].load)
                self.tuns[i] = tunnel

            break

    def __init_destination(self):
        self.source = self.SOURCE
        self.target = self.TARGET

    def clear_edges_load(self):
        for i in range(10):
            tun = self.tunnels[i]
            tun = Tunnel(tun.index, tun.cos, tun.route, tun.invroute, 0.0)
            self.tuns[i] = tun

    def show_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos, node_size=300)

        nx.draw_networkx_edges(self.graph, pos,
                               width=1,
                               alpha=0.6, edge_color='b', style='solid')

        # labels
        nx.draw_networkx_labels(
            self.graph, pos, font_size=14, font_family='sans-serif')

        plt.axis('off')
        plt.savefig("Graph.png", format="PNG")
        plt.show()
