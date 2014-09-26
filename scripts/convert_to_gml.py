import sys
import json
import networkx as nx

reload(sys)
sys.setdefaultencoding("utf-8")

GROUP_MAPPING = {
    "Influenced by": "Programming Language",
    "Designed by": "Computer Scientist",
    "Developer": "Foundation",
    "Dialects": "Dialect",
    "Major implementations": "Implementation",
    "Implementation language": "Programming Language",
}

network = {
    "nodes": [],
    "links": []
}


def add_node(label, group):
    node = {
        "name": label,
        "id": len(network["nodes"]),
        "group": group
    }
    network["nodes"].append(node)
    return node


def find_node_by_label(label):
    for node in network["nodes"]:
        if node["name"] == label:
            return node["id"]


def main():
    data = json.load(open("../data/data.json"))

    for language, properties in data.items():

        add_node(language, GROUP_MAPPING["Influenced by"])

        for edge_type, group in GROUP_MAPPING.iteritems():
            if edge_type in properties:
                nodes = properties[edge_type]

                for node in nodes:
                    node_id = find_node_by_label(node)
                    if node_id is None:
                        added_node = add_node(node, group)
                        node_id = added_node["id"]

                    network["links"].append({
                        "source": find_node_by_label(language),
                        "target": node_id,
                        "type": edge_type
                    })

    graph = nx.MultiDiGraph()
    for node in network["nodes"]:
        graph.add_node(node["name"].encode("utf-8"), node)

    for link in network["links"]:
        graph.add_edge(network["nodes"][link["source"]]["name"].encode("utf-8"),
                       network["nodes"][link["target"]]["name"].encode("utf-8"),
                       label=link["type"])

    nx.write_gml(graph, '../data/network.gml')


if __name__ == "__main__":
    main()
