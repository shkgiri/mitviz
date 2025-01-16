from flask import Flask, render_template
from pyvis.network import Network

app = Flask(__name__)

# Route to generate the graph and serve it as an HTML file
@app.route('/graph')
def graph():
    # Create a PyVis Network object
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Add nodes and edges
    nodes = [
        {"id": "A", "label": "A", "group": "1"},
        {"id": "B", "label": "B", "group": "1"},
        {"id": "C", "label": "C", "group": "2"},
        {"id": "D", "label": "D", "group": "2"},
        {"id": "1", "label": "1", "group": "3"},
        {"id": "2", "label": "2", "group": "3"},
        {"id": "3", "label": "3", "group": "4"},
        {"id": "4", "label": "4", "group": "4"},
    ]
    edges = [
        {"source": "A", "target": "B"},
        {"source": "C", "target": "D"},
        {"source": "B", "target": "1"},
        {"source": "B", "target": "2"},
        {"source": "D", "target": "3"},
        {"source": "D", "target": "4"},
    ]

    # Add nodes and edges to the network
    for node in nodes:
        net.add_node(node["id"], label=node["label"], group=node["group"])

    for edge in edges:
        net.add_edge(edge["source"], edge["target"])

    # Save the graph to an HTML file
    net.set_options("""
    var options = {
      nodes: {
        shape: "dot",
        size: 20,
      },
      edges: {
        color: "#cccccc",
        arrows: { to: { enabled: true } },
      },
      groups: {
        "1": { color: { background: "#1f78b4" } },
        "2": { color: { background: "#33a02c" } },
        "3": { color: { background: "#e31a1c" } },
        "4": { color: { background: "#ff7f00" } },
      },
    }
    """)
    net.show("templates/graph.html")
    return render_template("graph.html")


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
