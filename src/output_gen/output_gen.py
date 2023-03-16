import spacy
import os
import sys
import textract
import re
import nltk
import urllib.request
import numpy as np
import pandas as pd
import math
import heapq
# Library to import pre-trained model for sentence embeddings - installs transformers, torch, torchvision, numpy, scipy, scikit-learn, nltk, huggingface-hubpip
from sentence_transformers import SentenceTransformer
# Calculate similarities between sentences
from sklearn.metrics.pairwise import cosine_similarity
# Visualization library
import seaborn as sns
import matplotlib.pyplot as plt
# package for finding local minimas
from scipy.signal import argrelextrema

from collections import defaultdict
from plantweb.render import render
from spacy.matcher import PhraseMatcher
from dotenv import load_dotenv

load_dotenv()

pd.set_option('max_colwidth', 2000)
pd.options.display.max_rows = 500

# will need downloading only if there's a new installation.
#nltk.download('punkt')
#nltk.download('stopwords')


'''
pip install spacy
pip install pdfminer.six # to replace pdftotext in textract
pip install textract
python -m spacy download en_core_web_sm
pip install plantweb
pip install python-dotenv
Tesseract: https://github.com/UB-Mannheim/tesseract/wiki (for Windows)
pip install sentence_transformers
pip install seaborn

set up .env file with DIR_PATH variable going to the io/input folder in this repo

'''

# https://towardsdatascience.com/from-text-to-knowledge-the-information-extraction-pipeline-b65e7e30273e



# Set the directory path to search
DIR_PATH = os.getenv('DIR_PATH')

nlp = spacy.load('en_core_web_sm')

# Loading a model - 420 MB, will take a while (5 min?) but only on the first run on a new machine so the model files can be downloaded. 
model = SentenceTransformer('all-mpnet-base-v2')

text = ''




def title_gen(contents, num_sentences):
    article_text = contents
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )		
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list = nltk.sent_tokenize(article_text)				#divide text into sentences
    stopwords = nltk.corpus.stopwords.words('english')				

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):			#calculate frequency of each word
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)		#weighted frequency
        
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]		#calculate each sentence value
                
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)		#get top sentences

    summary = ' '.join(summary_sentences)
    return summary



def rev_sigmoid(x:float)->float:
    return (1 / (1 + math.exp(0.5*x)))
    
def activate_similarities(similarities:np.array, p_size=10)->np.array:
        """ Function returns list of weighted sums of activated sentence similarities
        Args:
            similarities (numpy array): it should square matrix where each sentence corresponds to another with cosine similarity
            p_size (int): number of sentences are used to calculate weighted sum 
        Returns:
            list: list of weighted sums
        """
        # To create weights for sigmoid function we first have to create space. P_size will determine number of sentences used and the size of weights vector.
        x = np.linspace(-10,10,p_size)
        # Then we need to apply activation function to the created space
        y = np.vectorize(rev_sigmoid) 
        # Because we only apply activation to p_size number of sentences we have to add zeros to neglect the effect of every additional sentence and to match the length ofvector we will multiply
        activation_weights = np.pad(y(x),(0,similarities.shape[0]-p_size))
        ### 1. Take each diagonal to the right of the main diagonal
        diagonals = [similarities.diagonal(each) for each in range(0,similarities.shape[0])]
        ### 2. Pad each diagonal by zeros at the end. Because each diagonal is different length we should pad it with zeros at the end
        diagonals = [np.pad(each, (0,similarities.shape[0]-len(each))) for each in diagonals]
        ### 3. Stack those diagonals into new matrix
        diagonals = np.stack(diagonals)
        ### 4. Apply activation weights to each row. Multiply similarities with our activation.
        diagonals = diagonals * activation_weights.reshape(-1,1)
        ### 5. Calculate the weighted sum of activated similarities
        activated_similarities = np.sum(diagonals, axis=0)
        return activated_similarities
  

component_map = defaultdict(list)
component_names = []
        
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
            
            # Split text into sentences
            sentences = text.decode('utf-8').split('. ')

            # Get the length of each sentence
            sentence_length = [len(each) for each in sentences]
            # Determine longest outlier
            long = np.mean(sentence_length) + np.std(sentence_length) *2
            # Determine shortest outlier
            short = np.mean(sentence_length) - np.std(sentence_length) *2
            # Shorten long sentences
            text = ''
            for each in sentences:
                if len(each) > long:
                    # let's replace all the commas with dots
                    comma_splitted = each.replace(',', '.')
                else:
                    text+= f'{each}. '
            sentences = text.split('. ')
            # Now let's concatenate short ones
            text = ''
            for each in sentences:
                if len(each) < short:
                    text+= f'{each} '
                else:
                    text+= f'{each}. '

            # Embed sentences
            embeddings = model.encode(sentences)
            print(embeddings.shape)

            # Create similarities matrix
            similarities = cosine_similarity(embeddings)

            # Apply function: for long sentences, 10 or more sentences are recommended.
            activated_similarities = activate_similarities(similarities, p_size=5)

            # Find relative minima of the vector. For all local minima and save them to variable with argrelextrema function
            minima = argrelextrema(activated_similarities, np.less, order=2) # order parameter controls how frequent the splits should be - recommend not changing.

            '''
            # plotting only

            # Create an empty figure for the plot
            fig, ax = plt.subplots()

            # plot the flow of the text with activated similarities
            sns.lineplot(y=activated_similarities, x=range(len(activated_similarities)), ax=ax).set_title('Relative minima');

            # plot vertical lines to see where the split was created
            plt.vlines(x=minima, ymin=min(activated_similarities), ymax=max(activated_similarities), colors='purple', ls='--', lw=1, label='vline_multiple - full height')
            '''

            #Get the order number of the sentences which are in splitting points
            split_points = [each for each in minima[0]]

            # Create empty string
            text = ''

            for num,each in enumerate(sentences):
                # Check if sentence is a minimum (splitting point)
                if num in split_points:
                    # If it is than add a dot to the end of the sentence and a paragraph before it.
                    text+=f'\n\n {each}. '
                else:
                    # If it is a normal sentence just add a dot to the end and keep adding sentences.
                    text+=f'{each}. '

            paragraphs = text.split('\n\n')
            print("num of paragraphs", len(paragraphs))

            titles = []
            for para in paragraphs:
                num_sents = len(para.split('. '))
                titles.append(title_gen(para, 1))

            print("generated titles", titles)

            # Embed paragraphs
            embeddings = model.encode(paragraphs)
            #print(embeddings.shape)

            # Create similarities matrix
            similarities = cosine_similarity(embeddings)
            #print("num of similarities", len(similarities))
            #print(similarities)

            connections = []
            for i in range(len(similarities)):
                p_start = i
                row = np.array(similarities[i])
                idx_one = np.argmax(row)
                decision_row = np.delete(row, idx_one)
                #print(decision_row)
                idx_max = np.argmax(decision_row)
                #print(idx_max)
                if idx_one == idx_max:
                    p_end = idx_max + 1
                else:
                    p_end = idx_max
                #print(p_start, p_end)
                connections.append([p_start, p_end, titles[p_start], paragraphs[p_start]])

        

            # Generate the PlantUML component diagram

            print('@startuml')

            for i in range(len(connections)):
                if len(connections[i]) > 0:
                    node1, node2, title, para = connections[i]
                    print(f'{node1} --> {node2}')

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


            # or instead of UML, use Mermaid to render the diagram and accompanying paragraph text upon clicking on each object in the diagram.
            # This will offer a highly condensed and organized view of all documentation sections and how they relate to the overall project being described by the diagram.

