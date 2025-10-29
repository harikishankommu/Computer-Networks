# rip.py
import json, networkx as nx, os
INF = 10**9

# -----------------------------
# Load topology and build graph
# -----------------------------
def load_topo(path): 
    return json.load(open(path))

def build_graph(topo):
    G = nx.Graph()
    for n in topo['nodes']: G.add_node(n)
    for l in topo['links']:
        G.add_edge(l['u'], l['v'], cost=l.get('cost',1))
    return G

# -----------------------------
# RIP Simulation (Distance Vector)
# -----------------------------
def rip_sim(G, max_rounds=50):
    dv = {node: {dest: (0, dest) if node == dest else (INF, None) for dest in G.nodes()} for node in G.nodes()}

    for n in G.nodes():
        for m in G.nodes():
            if m not in dv[n]: dv[n][m] = (INF, None)

    for r in range(max_rounds):
        updated = False
        for u in G.nodes():
            for v in G.neighbors(u):
                c_uv = G[u][v]['cost']
                for dest,(c,dnext) in dv[u].items():
                    if c + c_uv < dv[v][dest][0]:
                        dv[v][dest] = (c + c_uv, u if dest!=v else dest)
                        updated = True
        if not updated:
            print("Converged in round", r)
            break
    return dv

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    topo = load_topo("topologies/topo_small.json")
    G = build_graph(topo)
    dv = rip_sim(G)

    # Print routing tables
    for r in sorted(dv.keys()):
        print("Router", r)
        for dest in sorted(dv[r].keys()):
            c, nh = dv[r][dest]
            if c < INF:
                print(f"  to {dest}: cost={c}, next_hop={nh}")

    # -----------------------------
    # Visualize topology with arrows and edge costs
    # -----------------------------
    import matplotlib.pyplot as plt
    os.makedirs("RIP_outputs", exist_ok=True)

    # Convert to directed graph for arrows
    DG = G.to_directed()
    pos = nx.spring_layout(DG)

    # Draw nodes and labels
    nx.draw_networkx_nodes(DG, pos, node_size=700, node_color='skyblue')
    nx.draw_networkx_labels(DG, pos, font_size=12, font_weight='bold')

    # Draw edges with arrows
    nx.draw_networkx_edges(DG, pos, arrowstyle='-|>', arrowsize=20, edge_color='gray', width=2)

    # Draw edge labels (costs)
    edge_labels = nx.get_edge_attributes(DG, 'cost')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels, font_color='red', font_weight='bold')

    plt.axis('off')
    plt.savefig("RIP_outputs/topology.png", dpi=300)
    plt.show()
