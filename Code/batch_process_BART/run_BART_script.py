# Import needed libraries
import pandas as pd
import numpy as np
from transformers import pipeline
from transformers.models.auto.modeling_tf_auto import TFAutoModelForSequenceClassification
from transformers.models.bart.modeling_tf_bart import TFBartForSequenceClassification
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import transformers
import torch
import datasets
import time
import pickle
import sys
#from accelerate import Accelerator

# Get start and end index that is passed at run time in CLI
batch_index = sys.argv[1]
if len(batch_index) == 1:
    batch_index = '0' + batch_index
start_index = int(sys.argv[2])
end_index = int(sys.argv[3])

# Define Folder path
folder = '/N/slate/jmonser/dsip_ria/'
# Define Data Types of Columns
ft = datasets.Features({'patent_number': datasets.Value('string'),
                        'patent_text': datasets.Value('string')
                       })
# Load Transformer dataset of patents
ds = datasets.load_dataset('csv', data_files= folder + 'PatentView_Data/2020_h2_patents_processed.csv', features=ft)

# Load NAICS-4 labels
#filepath = folder + 'Project_Patent_Classification/Data/NAICS/2-6 digit_2022_Codes.xlsx'
#naics = pd.read_excel(filepath)
#naics = naics.iloc[:, :3]
#naics.dropna(inplace=True, axis=0, how='all')
#naics4 = naics[naics.iloc[:,1].astype('string').str.match('^\d{4}$')].iloc[:,-1].tolist()
with open(folder + 'naics4_2017.pkl', 'rb') as f:
    naics4 = pickle.load(f)

# Add accelerator for parallel processing
#accelerator = Accelerator()

# Add accelerator device so pipeline knows which GPU to run on via accelerator's instructions
#device = accelerator.device
device = torch.device('cuda:0')

# Create BART classifier
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli",
                      device=device
                     )

# Let accelerator prepare classifier for correct processing
#classifier = accelerator.prepare(classifier)

# Generate NAICS labels for patents in batches
start_temp_index = start_index
end_temp_index = start_index
batch_size = 100
results_list = []
while end_temp_index <= end_index:
    end_temp_index += batch_size
    if end_temp_index >= end_index:
        end_temp_index = end_index
        results = classifier(ds['train']['patent_text'][start_temp_index:end_temp_index], naics4, multi_label=True)
        results_list.extend(results)
        break
    else:
        results = classifier(ds['train']['patent_text'][start_temp_index:end_temp_index], naics4, multi_label=True)
        results_list.extend(results)
    start_temp_index = end_temp_index
    
# Save results to Slate
with open(folder + 'BART_results_' + batch_index + '.pkl', 'wb') as f:
    pickle.dump(results_list, f)
