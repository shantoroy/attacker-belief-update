import pandas as pd
import numpy as np
import networkx as nx
# from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import plotly.graph_objs as go
import streamlit as st

# help source: https://www.kaggle.com/anand0427/network-graph-with-at-t-data-using-plotly

def network_plot(network_df):
    router = ["Router"]
    nodes = network_df["Nodes"].tolist()
    
    node_list = set(router+nodes)

    # Creating the graph
    G = nx.Graph()

    for i in node_list:
        G.add_node(i)

    # adding edges
    for i,j in network_df.iterrows():
        G.add_edges_from([(router[0],j["Nodes"])])

    # getting positions for each node
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    # Adding positions of the nodes to the graph
    for n, p in pos.items():
        G.nodes[n]['pos'] = p

    # Adding nodes and edges to the plotly api
    edge_trace = go.Scatter(
                        x=[],
                        y=[],
                        line=dict(width=0.5,color='#888'),
                        hoverinfo='none',
                        mode='lines')

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
                        x=[],
                        y=[],
                        text=[],
                        mode='markers',
                        hoverinfo='text',
                        marker=dict(
                            showscale=True,
                            colorscale='RdBu',
                            reversescale=True,
                            color=[],
                            size=15,
                            colorbar=dict(
                                thickness=10,
                                title='Node Connections',
                                xanchor='left',
                                titleside='right'
                            ),
                            line=dict(width=0)))

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])


    # Coloring Nodes
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        node_info = adjacencies[0] +' # of connections: '+str(len(adjacencies[1]))
        node_trace['text']+=tuple([[j,k] for j,k in zip( \
                            network_df["OS"].tolist(), network_df["App"].tolist())])


    # preparing the figure
    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                # title='<br>AT&T network connections',
                # titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Network Node",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return fig