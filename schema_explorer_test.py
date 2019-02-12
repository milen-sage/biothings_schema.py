from schema_explorer import SchemaExplorer
import pprint as pp
from graphviz import Source


se = SchemaExplorer()

class_info = se.explore_class("Device")
pp.pprint(class_info)

new_class = {
                '@id': 'bts:Assay',
                '@type': 'rdfs:Class',
                'rdfs:comment': 'The technology used to generate the data in this file',
                'rdfs:label': 'Assay',
                'rdfs:subClassOf': {'@id': 'bts:Thing'},
                'schema:isPartOf': {'@id': 'http://schema.biothings.io'}
}

se.update_class(new_class)


update_class = {'@id': 'bts:Device',
                '@type': 'rdfs:Class',
                'rdfs:comment': class_info["description"],
                'rdfs:label': 'Device',
                'rdfs:subClassOf': {'@id': 'bts:Assay'},
                'schema:isPartOf': {'@id': 'http://schema.biothings.io'}}


se.update_class(update_class)

full_schema = se.full_schema_graph()
s = Source(full_schema, filename="./schema.gv", format="png")
s.view()
