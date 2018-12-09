import csv
from diploma_mpls.graph import GraphUtil
import numpy as np
import itertools

gutil = GraphUtil()
unique_routes = gutil.unique_routes
unique_routes_cnt = gutil.unique_routes_cnt
mpls_graph = gutil.graph
ethernet_max_throughput = 125e5  # 100 MB/s


def generate_example_inputs(g, util):
    util.init_network_load()

    sample = []
    sample.append(np.random.choice(list(range(8))))
    sample.append(gutil.source)
    sample.append(gutil.target)

    threads = [round(np.random.uniform(3, 8), 2) for _ in range(15)]
    for k in gutil.tunnels_load:
        sample.append(k)
    for thread in threads:
        sample.append(thread)

    return sample


def generate_example_output(sample):
    coses = list(range(8))
    current_cos = sample[0]
    threads = sample[8:]
    cnt = [0] * len(threads)

    # if traffic class >= max tunnel class
    if current_cos >= 2:
        current_cos = 2

    tuns = [t for t in gutil.tunnels if t.cos == current_cos]
    for i in range(len(threads)):
        d = [(t, gutil.tunnels_load[t.index]) for t in tuns]
        # print(gutil.tunnels_load)
        best_tunnel = min(d, key=lambda x: x[1])[0]

        if gutil.add_load(best_tunnel.index, threads[i] / 100).load >= 0.65:
            index = coses.index(best_tunnel.cos)
            if index - 1 != -1:
                index -= 1

            tuns = [t for t in gutil.tunnels if t.cos == coses[index]]
            d = [(t, gutil.tunnels_load[t.index]) for t in tuns]
            best_tunnel = min(d, key=lambda x: x[1])[0]
        cnt[i] = best_tunnel.index
    # print('------------Segment--------------')
    return cnt


def generate_example(util):
    x = generate_example_inputs(mpls_graph, util)
    y = generate_example_output(x)
    return (x, y)


def generate_dataset(m, filename):
    f = open(filename, 'a', newline='')
    for source, dest in gutil.destinations[0]:
        gutil.source = source
        gutil.target = dest
        # inputs = []
        # outputs = []

        for k in range(8):
            i = 0
            while i < m:
                inp, out = generate_example(gutil)
                if inp[0] != k:
                    continue
                sample = []
                for z in itertools.chain(inp, out):
                    sample.append(z)
                writer = csv.writer(f)
                writer.writerow(sample)

                i += 1
    f.close()


generate_dataset(500, 'dataset2.csv')
generate_dataset(500, 'dataset.csv')
