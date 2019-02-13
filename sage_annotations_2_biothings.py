import os
import json

from schema_explorer import SchemaExplorer
import pprint as pp
from graphviz import Source


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

# skip 'not applicable'

se = SchemaExplorer()

# add adhoc classes; TODO: this should be generated based on a metadata model schema

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


# load existing Synapse annotations and convert them to BioThings
# augmenting existing BioThings schema

annotations_file = "experimentalData.json"

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


full_schema = se.full_schema_graph()
full_schema.engine = "fdp"
full_schema.render(filename=os.path.join(annotations_path, annotations_file + "schema.gv.pdf"), view = True)

partial_schema = se.sub_schema_graph(source="Assay", direction="down")
partial_schema.engine = "circo"
partial_schema.render(filename=os.path.join(annotations_path, annotations_file + "partial_schema.gv.pdf"), view = True)

se.export_schema(os.path.join(annotations_path, annotations_file + "ld"))
