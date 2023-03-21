import spacy
import os
import sys
import textract
import re
import urllib.request
from collections import defaultdict
from plantweb.render import render
from spacy.matcher import Matcher
from dotenv import load_dotenv

load_dotenv()


'''
pip install spacy
pip install pdfminer.six # to replace pdftotext in textract
pip install textract
python -m spacy download en_core_web_sm
pip install plantweb
pip install python-dotenv
Tesseract: https://github.com/UB-Mannheim/tesseract/wiki (for Windows)


set up .env file with DIR_PATH variable going to the io/input folder in this repo

'''

# https://towardsdatascience.com/from-text-to-knowledge-the-information-extraction-pipeline-b65e7e30273e

import pandas as pd
pd.set_option('max_colwidth', 2000)
pd.options.display.max_rows = 500

# Set the directory path to search
DIR_PATH = os.getenv("DIR_PATH")

nlp = spacy.load('en_core_web_lg')

text = ''

# Loop through all files in the directory
for root, dirs, files in os.walk(DIR_PATH):
    for file in files:
        # Check if the file has a .xls extension
        if file.endswith('.pdf'):

            # Get the full path to the file
            file_path = os.path.join(root, file)
            print(file_path)

            # Extract text from the document using textract
            text = textract.process(file_path, language='en')
            
            # Create a new PDF with reportlab
            #pdf_path = os.path.splitext(file_path)[0] + '.pdf'

            #if os.path.exists(pdf_path): os.remove(pdf_path) 


# Download the document from the URL
#url = 'https://www.example.com/document.pdf'
#urllib.request.urlretrieve(url, 'document.pdf')

# Extract text from the document using textract
#text = textract.process('City of Denver 2021.pdf')

# Find titles using regular expressions
titles = re.findall(r'\n\s*[A-Z][A-Za-z0-9\s]+[.:]', text.decode('utf-8'))
titles = [t.replace("\n", "") for t in titles]
titles = [t.replace("\r", "") for t in titles]
titles = [t.replace("\x0c", "") for t in titles]

# Print the titles
#print(titles)

#title_strs = '|'.join([t for t in titles])
#print(title_strs)

# Define the pattern for section titles
#section_title_pattern = [
#    {"TEXT": {title_strs}}
#]

#print(section_title_pattern)

matcher = Matcher(nlp.vocab)

# Define a pattern to match sentences containing "title"
#pattern = [{"LOWER": {"IN": ["title"]}}, {"IS_PUNCT": True, "OP": "?"}, {"POS": "ADJ", "OP": "*"}, {"POS": "NOUN", "OP": "+"}]

#section_title_pattern = [{"label": "SECTION_TITLE", "pattern": pattern} for pattern in patterns]

# Create a pattern for the matcher using the section titles
#for sent in titles:
patterns = list([{"TEXT": sent} for sent in titles])

print(patterns)
#sys.exit(1)
matcher.add('SENTENCES', patterns)

# Read the text file
#doc = nlp(open('example.txt', encoding="utf8").read())
doc = nlp(text)
matches = matcher(doc)


# Print the section titles and their start and end positions
for match_id, start, end in matches:
    section_title = doc[start:end].text
    print(f"Section title: {section_title}, start: {start}, end: {end}")



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