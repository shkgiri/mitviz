from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Route to serve graph data
@app.route('/graph-data')
def graph_data():
    # Example graph data
    graph = {
        "nodes": [
            {"id": "A", "label": "A", "group": "1"},
            {"id": "B", "label": "B", "group": "1"},
            {"id": "C", "label": "C", "group": "2"},
            {"id": "D", "label": "D", "group": "2"},
            {"id": "1", "label": "1", "group": "3"},
            {"id": "2", "label": "2", "group": "3"},
            {"id": "3", "label": "3", "group": "4"},
            {"id": "4", "label": "4", "group": "4"}
        ],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "C", "target": "D"},
            {"source": "B", "target": "1"},
            {"source": "B", "target": "2"},
            {"source": "D", "target": "3"},
            {"source": "D", "target": "4"}
        ]
    }
    return jsonify(graph)

# Route to serve the Ogma example HTML
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
