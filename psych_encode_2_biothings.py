import os
import json
import pprint
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


def get_property(property_name, property_class_name, description = None, allowed_values = 'Text'):

    new_property = {
                    '@id': 'bts:' + property_name,
                    '@type': 'rdf:Property',
                    'rdfs:comment': description if description else "",
                    'rdfs:label': property_name,
                    'schema:domainIncludes': {'@id': 'bts:' + property_class_name},
                    'schema:rangeIncludes': {'@id': 'schema:' + allowed_values},

                    'schema:isPartOf': {'@id': 'http://schema.biothings.io'},
    }
                    
    #'http://schema.org/domainIncludes':{'@id': 'bts:' + property_class_name},
    #'http://schema.org/rangeIncludes':{'@id': 'schema:' + allowed_values},
    

    return new_property


def first_upper(s):
    return s[0].upper() + s[1:] if len(s) > 0 else s


annotations_path = "./data"
annotations_file = "psychENCODE.json"


# instantiate schema explorer
se = SchemaExplorer()

# visualize default schema
full_schema = se.full_schema_graph()
full_schema.render(filename=os.path.join(annotations_path, "biothings_schema.pdf"), view = True)

'''
# add classes matching psychENCODE manifest specifications to biothings base ontology
# for now we are hard-coding definitions; however, in the future we should have URI for each term and definition used in a dictionary
# e.g. https://schema.org/docs/schema_org_rdfa.html
'''

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


class_info = se.explore_class("Device")
edit_class = get_class("Device",\
          description =  class_info["description"],\
          subclass_of = "Assay"\
)
se.edit_class(edit_class)

new_class = get_class("Organization",\
          description =  "An organization such as a school, NGO, corporation, club, etc." ,\
          subclass_of = "Thing"\
)
se.update_class(new_class)

new_class = get_class("Study",\
          description =  "Grant research unit" ,\
          subclass_of = "Organization"\
)
se.update_class(new_class)

new_class = get_class("Consortium",\
          description =  "Consortium name" ,\
          subclass_of = "Organization"\
)
se.update_class(new_class)

new_class = get_class("Grant",\
          description =  "NIH project number" ,\
          subclass_of = "Study"\
)
se.update_class(new_class)


new_class = get_class("Investigator",\
          description =  "Principal investigator on a project" ,\
          subclass_of = "Person"\
)
se.update_class(new_class)

# set investigator properties
# name; affiliation

new_class = get_class("Individual",\
          description =  "Donor individual" ,\
          subclass_of = "Case"\
)
se.update_class(new_class)

# add individual properties
new_property = get_property("IndividualAccession",\
                            "Individual",\
                            description = "Unique donor ID assigned by DAC.DCC"\
)
se.update_property(new_property)

new_property = get_property("IndividualID",\
                            "Individual",\
                            description = "Donor ID as provided by lab"\
)
se.update_property(new_property)

new_property = get_property("IndividualIDSource",\
                            "Individual",\
                            description = "Brain bank or other repository to which individualID maps"\
)
se.update_property(new_property)

new_property = get_property("Species",\
                            "Individual",\
                            description = "The name of this Individual species"\
)
se.update_property(new_property)

new_property = get_property("ReportedGender",\
                            "Individual",\
                            description = "Gender as reported by brain bank"\
)
se.update_property(new_property)

new_property = get_property("Sex",\
                            "Individual",\
                            description = "SNP Genotype"\
)
se.update_property(new_property)

new_property = get_property("Age",\
                            "Individual",\
                            description = "Age of individual at biospecimen sampling - age of death for postmortem tissue"\
)
se.update_property(new_property)

new_property = get_property("AgeUnits",\
                            "Individual",\
                            description = "The unit of measurement (gestational week or year)"\
)
se.update_property(new_property)

new_property = get_property("Race",\
                            "Individual",\
                            description = "A person’s social group identification"\
)
se.update_property(new_property)


new_property = get_property("RaceDetail",\
                            "Individual",\
                            description = "Hispanic or Latino and Not Hispanic or Latino"\
)
se.update_property(new_property)

new_property = get_property("GenotypeInferredAncestry",\
                            "Individual",\
                            description = "Ancestry inferred from genotype"\
)
se.update_property(new_property)


new_property = get_property("IQ",\
                            "Individual",\
                            description = "Individuals IQ"\
)
se.update_property(new_property)


new_property = get_property("BMI",\
                            "Individual",\
                            description = "Body Mass Index"\
)
se.update_property(new_property)

new_property = get_property("BMI",\
                            "Individual",\
                            description = "Body Mass Index"\
)
se.update_property(new_property)


new_class = get_class("Diagnosis",\
          description =  "Primary psychiatric diagnosis" ,\
          subclass_of = "Case"\
)
se.update_class(new_class)

# add diagnosis properties
# diagnosisDetail
# what about subdiagnosis (e.g. otherDiagnosis)
# familyHistory
# ageOnset

new_class = get_class("Death",\
          description =  "Lack of life" ,\
          subclass_of = "LifeStage"\
)
se.update_class(new_class)

# add death properties
# causeDeath
# mannerDeath

new_class = get_class("Dementia",\
          description =  "A progressive, neurodegenerative disease characterized by loss of function and death of nerve cells in several areas of the brain leading to loss of cognitive function such as memory and language. [EFO:0000249]" ,\
          subclass_of = "Disease"\
)
se.update_class(new_class)

# add dementia properties
# CDR, braak


new_class = get_class("Neuropathology",\
          description =  "Neurological pathology" ,\
          subclass_of = "Procedure"\
)
se.update_class(new_class)

# add neorupathology description
# neuropathDescription

new_class = get_class("PostmortemToxicology",\
          description =  "Toxicology tests performed on post-mortem tissue" ,\
          subclass_of = "Procedure"\
)
se.update_class(new_class)

# add postmortem tox properties
# postmortemToxSource
# medRecTox


new_class = get_class("Organ",\
          description =  "A unique macroscopic (gross) anatomic structure that performs specific functions. It is composed of various tissues. An organ is part of an anatomic system or a body region." ,\
          subclass_of = "Biosample"\
)
se.update_class(new_class)

# add properties
'''
PMI
pH
organWeight
yearAutopsy
RIN
agonalState

requiresIndividual
'''


'''
nx.set_node_attributes(se.schema_nx, "red",  "fillcolor")

color1_subgraph = get_descendents_subgraph(se.schema_nx, "Assay")

nx.set_node_attributes(color1_subgraph, "#990000",  "fillcolor")
nx.set_node_attributes(color1_subgraph, "#990000",  "color")
nx.set_edge_attributes(color1_subgraph,"#990000", "color")  
nx.set_node_attributes(color1_subgraph, "32",  "fontsize")

topic_node_style(color1_subgraph, "Biosample")

agraph = to_agraph(color1_subgraph)
agraph.graph_attr['overlap']='false'
agraph.node_attr['style'] = "filled"
agraph.layout(prog = "fdp")
agraph.draw("colored_model.pdf")
#img = Image.open('colored_model.png')
#img.show()
'''

pp = pprint.PrettyPrinter(indent=4)
class_info = se.explore_class('Individual')
pp.pprint(class_info)

schema_name = annotations_file.split(".")[0] 

full_schema = se.full_schema_graph()
full_schema.engine = "fdp"
full_schema.render(filename=os.path.join(annotations_path, schema_name + "_schema.pdf"), view = True)

"""
partial_schema = se.sub_schema_graph(source="Assay", direction="down")
partial_schema.engine = "circo"
partial_schema.render(filename=os.path.join(annotations_path, schema_name + "_partial_schema.pdf"), view = True)
"""
se.export_schema(os.path.join(annotations_path, schema_name + ".jsonld"))
