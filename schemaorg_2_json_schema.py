import os
import json

from schema_explorer import SchemaExplorer
import pprint as pp
from graphviz import Source
import matplotlib.pyplot as plt
import networkx as nx

def load_schemaorg_model(model_path):

    # instantiate schema explorer
    se = SchemaExplorer()
    se.load_schema(model_path)

    '''
    # visualize loaded schema
    full_schema = se.full_schema_graph()
    full_schema.engine = "fdp"
    full_schema.render(filename=os.path.basename("schema.org.model.pdf"), view = True)
    '''
    return se


def get_children(se, parent):

    return se.find_child_classes(parent)


def dump_schema_graph(se, path):

    # ensure node properties are not NULL
    G = se.get_nx_schema()
    for node in G.nodes(data = True):
        for attribute, value in node[1].items():
            if not value or value == "null":
                value = "Not defined"
                node[1][attribute] = value
                
    # write out the networkx graph in GML format
    # R igraph should be able to read that

    nx.write_gml(G, path)

def get_requirements_graph(se, requirements_type = ["requiresChild"]):

    G = se.get_nx_schema()

    req_subgraph = set()
    for node in G.nodes(data = True):
        for attribute, value in node[1].items():
            print(attribute)
            if "sms:"+attribute in requirements_type and value == "true":
                req_subgraph.add(node[0])

    return G.subgraph(req_subgraph) 



if __name__ == '__main__':


    model_path = './data/csbcContext.jsonld'


    print("Loading model...")
    se = load_schemaorg_model(model_path)


    # get children of a schema.org class/entity
    class_children = get_children(se, "ResourceType")

    print(class_children)

    #req_subgraph = get_requirements_graph(se)
    
    #print(list(req_subgraph.nodes()))

    #nx.spring_layout(req_subgraph) 

    #plt.show()

    # serialize networkx graph into a standard format (Pajek)
    # readable in R igraph package
    serialized_model_path = "./model.gml" 
    dump_schema_graph(se, serialized_model_path)
    print("Graph_saved as " + serialized_model_path)
