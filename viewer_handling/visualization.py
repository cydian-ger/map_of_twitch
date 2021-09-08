from pyvis.network import Network
import pandas as pd
from tqdm import tqdm


# https://pyvis.readthedocs.io/en/latest/tutorial.html
def generate(csv, streamer_list):
    """
    :param csv:
    :param streamer_list: Streamer list, so that the amount of viewers is connected to the name (used for value)
    :return:
    """
    csv = csv + "_edges.csv"

    got_net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

    # set the physics layout of the network
    got_net.barnes_hut()
    got_data = pd.read_csv(csv)

    sources = got_data['Source']
    targets = got_data['Target']
    weights = got_data['Weight']

    edge_data = zip(sources, targets, weights)

    pbar_2 = tqdm(total=(len(got_data) + len(got_net.nodes)))
    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        got_net.add_node(src, src, title=src)
        got_net.add_node(dst, dst, title=dst)

        if w > 0:
            # Doesnt draw edges on self connect
            got_net.add_edge(src, dst, value=w)
        pbar_2.update(1)

    for node in got_net.nodes:
        link = "https://www.twitch.tv/%s" % str(node['id']).lower()
        node['title'] += '<br><a href="%s">%s</a>' % (link, link)
        node['value'] = len(streamer_list[node['id']])
        pbar_2.update(1)

    got_net.show('map_of_twitch.html')


def generate_u(csv, streamer_list):
    open(csv, "r")
    got_data = pd.read_csv(csv)

    sources = got_data['Source']
    targets = got_data['Target']
    weights = got_data['Weight']

    edge_data = zip(sources, targets, weights)

    return
