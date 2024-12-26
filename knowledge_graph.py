import networkx as nx
import holoviews as hv
from holoviews import opts
import panel as pn

# Initialize HoloViews with Bokeh backend
hv.extension('bokeh')


def create_expandable_graph():

   # Initial graph with base nodes
    G = nx.Graph()

  # Add initial nodes and edges
  # Start with just A and B visible
    G.add_node('A', visible=True)
    G.add_node('B', visible=True)
    G.add_edge('A', 'B', relation='uses', visible=True)

  # Add hidden nodes and edges
    G.add_node('D', visible=False)
    G.add_node('1', visible=False)
    G.add_node('2', visible=False)
    G.add_edge('B', 'D', relation='detects', visible=False)
    G.add_edge('D', '1', relation='mitigates', visible=False)
    G.add_edge('D', '2', relation='mitigates', visible=False)

  # Handle right-click events using selection
    def handle_selection(event):
        if event.element and event.element.node_renderer.data['name'] == 'B':
            G.nodes['D']['visible'] = not G.nodes['D']['visible']
            G['B']['D']['visible'] = not G['B']['D']['visible']
        elif event.element and event.element.node_renderer.data['name'] == 'D':
            G.nodes['1']['visible'] = not G.nodes['1']['visible']
            G.nodes['2']['visible'] = not G.nodes['2']['visible']
            G['D']['1']['visible'] = not G['D']['1']['visible']
            G['D']['2']['visible'] = not G['D']['2']['visible']
        graph.source = G  # Update graph source with modified visibility

    # Create a dynamic graph that updates on selection
    graph = hv.DynamicMap(
        lambda graph: hv.Graph.from_networkx(graph, nx.spring_layout),
        streams=[hv.streams.PointerXY(source=graph)]  # Use the defined graph here
    )

    # Style the graph
    graph.opts(
        opts.Graph(
            tools=['tap', 'box_select'],
            node_size=30,
            node_color='blue',
            edge_color='gray',
            width=800,
            height=400,
            xaxis=None,
            yaxis=None,
            node_hover_fill_color='red',
            edge_hover_line_color='red',
            edge_hover_line_width=3
        )
    )

    # Connect selection events to handle_selection function
    graph.events('selection').subscribe(handle_selection)

    return graph


# Create and display the graph
expandable_graph = create_expandable_graph()

# Create a Panel app
app = pn.Column(
  pn.pane.Markdown("# Interactive Knowledge Graph"),
  pn.pane.Markdown("Right-click on nodes to expand/collapse"),
  expandable_graph
)

# Show the app
app.servable()