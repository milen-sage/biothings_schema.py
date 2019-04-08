import os
import json

from PIL import Image
from schema_explorer import SchemaExplorer
import pprint as pp
from graphviz import Source
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph

def get_descendents_subgraph(G, node_id):

    s = [node_id]
    for v in dict(nx.bfs_successors(G, node_id)).values():
        s += v
    s = set(s)

    return G.subgraph(s)


def topic_node_style(G, node_id):

    G.node[node_id]["shape"] = "tripleoctagon"
    G.node[node_id]["fontsize"] = "52"
    G.node[node_id]["fontname"] = "Arial bold"


def get_class(class_name, description = None, subclass_of = "Thing"):
    
    class_attributes = {
                    '@id': 'bts:'+class_name,
                    '@type': 'rdfs:Class',
                    'rdfs:comment': description if description else "",
                    'rdfs:label': class_name,
                    'rdfs:subClassOf': {'@id': 'bts:' + subclass_of},
                    'schema:isPartOf': {'@id': 'http://schema.biothings.io'}
    }

    return class_attributes

def first_upper(s):
    return s[0].upper() + s[1:] if len(s) > 0 else s


# path to Synapse annotations
annotations_path = "./data"
annotations_file = "sageCommunity.json"
base_schema_org_file = "experimentalData.jsonld"


# instantiate schema explorer
se = SchemaExplorer()
se.load_schema(os.path.join(annotations_path, base_schema_org_file))

# visualize default schema
full_schema = se.full_schema_graph()
full_schema.render(filename=os.path.join(annotations_path, annotations_file + "biothings_schema.gv.pdf"), view = True)


# add adhoc classes; TODO: this should be generated based on a metadata model schema
'''
# experimentalData classes
new_class = get_class("Assay",\
          description = "The technology used to generate the data in this file",\
          subclass_of = "Thing"\
)
se.update_class(new_class)

new_class = get_class("DataEntity",\
          description = "A data derived entity and attributes.",\
          subclass_of = "EvidenceType"\
)
se.update_class(new_class)


new_class = get_class("Data",\
          description = "A piece of data (e.g. from an assay).",\
          subclass_of = "DataEntity"\
)
se.update_class(new_class)

new_class = get_class("BehavioralEntity",\
          description = "Entity and attributes derived from a Behavior",\
          subclass_of = "Thing"\
)
se.update_class(new_class)


new_class = get_class("MetabolicEntity",\
          description = "Entity and attributes derived from molecular metabolics",\
          subclass_of = "MolecularEntity"\
)
se.update_class(new_class)

new_class = get_class("ProteomicEntity",\
          description = "Entity and attributes derived from molecular proteomics",\
          subclass_of = "MolecularEntity"\
)
se.update_class(new_class)

new_class = get_class("ProteomicEntity",\
          description = "Entity and attributes derived from molecular proteomics",\
          subclass_of = "MolecularEntity"\
)
se.update_class(new_class)

class_info = se.explore_class("Device")
edit_class = get_class("Device",\
          description =  class_info["description"],\
          subclass_of = "Assay"\
)
se.edit_class(edit_class)
'''

# load existing Synapse annotations and convert them to BioThings
# augmenting existing BioThings schema

with open(os.path.join(annotations_path, annotations_file), "r") as a_f:
    synapse_annotations = json.load(a_f)

for annotations_entity in synapse_annotations:

    if not "biothingsParent" in annotations_entity:
        continue

    class_name = first_upper(annotations_entity["name"])
    subclass_of = annotations_entity["biothingsParent"]
    description = annotations_entity["description"]

    new_class = get_class(class_name,\
                          description = description,\
                          subclass_of = subclass_of\
    )
    se.update_class(new_class)
    
    if len(annotations_entity["enumValues"]) > 0 and annotations_entity["columnType"] != "BOOLEAN":  

        for nested_entity in annotations_entity["enumValues"]:
            subclass_of = class_name
            if nested_entity["value"] == "Not Applicable": 
                continue

            nested_class_name = first_upper(nested_entity["value"])
            nested_description = nested_entity["description"]
            new_class = get_class(nested_class_name,\
                                  description = nested_description,\
                                  subclass_of = subclass_of\
            )
            se.update_class(new_class)

            if "biothingsParent" in nested_entity:
                subclass_of = nested_entity["biothingsParent"]
                new_class = get_class(nested_class_name,\
                                  description = nested_description,\
                                  subclass_of = subclass_of\
                )
                se.update_class(new_class)



nx.set_node_attributes(se.schema_nx, "red",  "fillcolor")

color1_subgraph = get_descendents_subgraph(se.schema_nx, "Assay")

nx.set_node_attributes(color1_subgraph, "#990000",  "fillcolor")
nx.set_node_attributes(color1_subgraph, "#990000",  "color")
nx.set_edge_attributes(color1_subgraph,"#990000", "color")  
nx.set_node_attributes(color1_subgraph, "32",  "fontsize")

topic_node_style(color1_subgraph, "Assay")


color2_subgraph = get_descendents_subgraph(se.schema_nx, "Platform")

nx.set_node_attributes(color2_subgraph, "#ff9900",  "fillcolor")
nx.set_node_attributes(color2_subgraph, "#ff9900",  "color")
nx.set_edge_attributes(color2_subgraph,"#ff9900", "color")  
topic_node_style(color2_subgraph, "Platform")


color3_subgraph = get_descendents_subgraph(se.schema_nx, "AssayTarget")

topic_node_style(color3_subgraph, "AssayTarget")
#topic_node_style(color3_subgraph, "CellType")

nx.set_node_attributes(color3_subgraph, "#006600",  "fillcolor")
nx.set_node_attributes(color3_subgraph, "#006600",  "color")
nx.set_edge_attributes(color3_subgraph,"#006600", "color")  

display_subgraph = get_descendents_subgraph(se.schema_nx, "Assay")

#topic_node_style(display_subgraph, "AnatomicalEntity")

agraph = to_agraph(display_subgraph)
agraph.graph_attr['overlap']='false'
agraph.node_attr['style'] = "filled"
agraph.layout(prog = "fdp")
agraph.draw("color.pdf")
#img = Image.open('color.png')
#img.show()
'''
full_schema = se.full_schema_graph()
full_schema.engine = "fdp"
full_schema.render(filename=os.path.join(annotations_path, annotations_file + "schema.gv.pdf"), view = True)

partial_schema = se.sub_schema_graph(source="Assay", direction="down")
partial_schema.engine = "circo"
partial_schema.render(filename=os.path.join(annotations_path, annotations_file + "partial_schema.gv.pdf"), view = True)
'''
se.export_schema(os.path.join(annotations_path, annotations_file + "ld"))

