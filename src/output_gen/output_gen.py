import spacy
import sys
from collections import defaultdict
from plantweb.render import render
import opennre
model = opennre.get_model('wiki80_cnn_softmax')

# https://towardsdatascience.com/from-text-to-knowledge-the-information-extraction-pipeline-b65e7e30273e

import pandas as pd
pd.set_option('max_colwidth', 2000)
pd.options.display.max_rows = 500

nlp = spacy.load('en_core_web_lg')

# Read the text file
doc = nlp(open('example.txt', encoding="utf8").read())


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Named Entity Recognition
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# Get the entities, labels and explaination to the labels
table = []
for ent in doc.ents:
    table.append([ent.text,ent.label_,spacy.explain(ent.label_)])

# Create a dataframe from the list created above
df2 = pd.DataFrame(table, columns=['Entity', 'Label','Label_Description']).sort_values(by=['Label'])
#print(df2)

entities = []
relations = []

for ent in doc.ents:
    entities.append((ent.text, ent.label_))

print('entities', entities)
for token in doc:
    if token.dep_ in ["nsubj"]: # "amod", "compound"]:
        relations.append((token.head.text, token.dep_, token.text))
    elif token.dep_ in ["prep"]: #, "pobj", "dobj"]:
        prep = token.text
        for child in token.children:
            if child.dep_ == "pobj":
                relations.append((token.head.text, prep, child.text))

component_map = defaultdict(list)
component_names = set() #entities #set()

# Parse the output from the dependency parsing code
for line in relations:
    #line = line.strip()
    if line:
        head, rel, tail = line # .split('\t')
        if rel in ["nsubj"]: # "amod", "compound"]:
            #print('add to names', line)
            component_names.add(head)
        else: # rel in ["prep", "pobj", "dobj"]: #rel == 'prep': # and tail.startswith('n'):
            #print('add to map', line)
            component_map[head].append(tail)

# Generate the PlantUML component diagram

print('@startuml')

for component in component_names:

    if len(component_map[component]) > 0:
        #print(f'component {component} {{')
        #print(f'{component_map[component]}')
        #print('}')
        for connection in component_map[component]:
            print(f'{component} --> {connection}')

print('@enduml')


'''
CONTENT = """
actor Foo1
boundary Foo2
control Foo3
entity Foo4
database Foo5
Foo1 -> Foo2 : To boundary
Foo1 -> Foo3 : To control
Foo1 -> Foo4 : To entity
Foo1 -> Foo5 : To database
"""

output = render(
        CONTENT,
        engine='plantuml',
        format='svg',
        cacheopts={
            'use_cache': False
        }
    )
'''
print('==> OUTPUT:')
#print(output)