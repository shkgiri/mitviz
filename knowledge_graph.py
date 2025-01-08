import networkx as nx
import holoviews as hv
from holoviews import opts
import panel as pn

# Initialize HoloViews with Bokeh backend
hv.extension('bokeh')

def create_knowledge_graph():
    """
    Creates an interactive knowledge graph with expandable/collapsible nodes.

    Returns:
        hv.DynamicMap: The interactive graph visualization.
    """

    # Create a sample graph
    G = nx.Graph()
    G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])
    G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E')])

    # Define node visibility (initially all visible)
    nx.set_node_attributes(G, {node: True for node in G.nodes()}, 'visible')

    def update_graph(node_name, x=None, y=None):
        """
        Toggles the visibility of a node and its neighbors.

        Args:
            node_name (str): The name of the node to toggle.
            x (optional): Not used in this case.
            y (optional): Not used in this case.
        """
        G.nodes[node_name]['visible'] = not G.nodes[node_name]['visible'] 
        for neighbor in G.neighbors(node_name):
            G.nodes[neighbor]['visible'] = G.nodes[node_name]['visible']

    # Create a dynamic graph that updates on node selection
    graph = hv.DynamicMap(
        update_graph,  # Include x and y arguments with default values
        streams=[hv.streams.Tap()]
    )

    # Style the graph
    graph.opts(
        opts.Graph(
            tools=['tap', 'box_select'],
            node_size=20,
            node_color='lightblue',
            edge_color='gray',
            width=600,
            height=400,
            xaxis=None,
            yaxis=None,
            node_hover_fill_color='red',
            edge_hover_line_color='red',
            edge_hover_line_width=3
        )
    )

    # Connect tap events to the update function
    graph.events('tap').adjoin(hv.streams.Stream.from_callback(
        lambda x: update_graph(x['x0']),
        streams=[graph.tap]
    ))

    return graph

# Create and display the graph
knowledge_graph = create_knowledge_graph()

# Create a Panel app
app = pn.Column(
    pn.pane.Markdown("# Interactive Knowledge Graph"),
    pn.pane.Markdown("Click on nodes to expand/collapse"),
    knowledge_graph
)

# Show the app
app.servable()