# Calling Data from Patent View API

Within the notebook and scripts nested, are the documents needed to pull data from the PatentView API. The `query_api.ipynb` notebook is the primary document to be used in pulling new data. This notebook references scripts in the `src` and  `config` folders. All data being read into the notebook and written out of the notebook are located in the `data` folder.


## Structure for Repositories 

```
utils
│   README.md
│   config   
└────── config.py - file with config information (api key)
│   data
└────── all CSV and JSON files reading in and writing out 
│   src
└────── Scripts being refrenced 
└──query_api.ipynb

```
