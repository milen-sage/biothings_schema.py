import os
import json

from schema_explorer import SchemaExplorer
import pprint as pp
from graphviz import Source
import networkx as nx

def load_schemaorg_model(model_path):

    # instantiate schema explorer
    se = SchemaExplorer()
    se.load_schema(model_path)

    # visualize loaded schema
    full_schema = se.full_schema_graph()
    full_schema.engine = "fdp"
    full_schema.render(filename=os.path.basename("schema.org.model.pdf"), view = True)

    return se


def get_children(se, parent):

    return se.find_child_classes(parent)


def dump_schema_graph(se, path):

    # write out the networkx graph in GML format
    # R igraph should be able to read that
    nx.write_pajek(se.get_nx_schema(), path)

if __name__ == '__main__':


    model_path = './data/csbcContext.jsonld'


    print("Loading model...")
    se = load_schemaorg_model(model_path)


    # get children of a schema.org class/entity
    class_children = get_children(se, "ResourceType")

    # serialize networkx graph into a standard format (Pajek)
    # readable in R igraph package
    serialized_model_path = "./model.net" 
    dump_schema_graph(se, serialized_model_path)
    print("Graph_saved as " + serialized_model_path)
