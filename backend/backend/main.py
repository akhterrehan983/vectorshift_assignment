# main.py


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx

app = FastAPI()

# Allow CORS for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # Allows only requests from your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


class GraphData(BaseModel):
    nodes: list
    edges: list


@app.post("/pipelines/parse")
async def parse_pipeline(data: GraphData):
    try:
        node_ids = [node["id"] for node in data.nodes]
        edges = [(edge["source"], edge["target"]) for edge in data.edges]

        G = nx.DiGraph()
        G.add_nodes_from(node_ids)
        G.add_edges_from(edges)

        print("Received Nodes:", node_ids)  # Debugging output
        print("Received Edges:", edges)  # Debugging output
        print("Graph Edges:", G.edges())  # Debugging output

        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        is_dag = nx.is_directed_acyclic_graph(G)

        return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": is_dag}
    except Exception as e:
        print(f"Error parsing pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error parsing pipeline: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
