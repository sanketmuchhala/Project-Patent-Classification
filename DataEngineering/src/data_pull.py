import os, sys, json
import requests
import pandas as pd
sys.path.append('../')
import config.config as config


def read_required_fields(path):
    '''
    Read in CSV with flagged fields for API call
    Input: 
        path (str): path to csv
    Return:
        df (pd.DataFrame): DataFrame with API req. fields
    '''
    df = pd.read_csv(path)
    df = df.rename({'API Field Name':'fields', 'Pulled for RIIA ': 'to_pull'},axis=1)
    df = df[df.to_pull == 1]
    return df 

def read_specific_patents(path):
    '''
    Read in CSV with specific patents numbers
    Input: 
        path (str): path to csv
    Return:
        df (pd.DataFrame): DataFrame with specific patents
    '''
    df = pd.read_csv(path, header = None)
    patent_ids = df[0].to_list()
    return patent_ids

def format_fields_for_api(df):
    '''
    Format list of fields for API call.
    Input: 
        df (pd.DataFrame)
    Return: 
        str_format (str): string with 
    '''
    api_names = df.fields.to_list()
    str_format = '['
    for field in api_names:
        str_format += f'"{field}",'
    str_format = str_format[:-1]
    str_format += ']'
    return str_format

def call_api(api_url):
    '''
    Call API and get the correspoindign dataframe 
    Input: 
        api_url (str): formatted url 
    Return: 
        df (pd.DataFrame): DataFrame with API results
    '''
    response = requests.get(api_url, headers={'X-Api-Key':config.api_key})
    if response.status_code == 200:
        df = pd.DataFrame.from_dict(response.json()['patents'])
        return df 
    else: 
        print(response)
        return response.status_code 
    
def combine_called_dfs(list_dfs):
    '''
    Combine list of DataFrames into one.
    Inputs: 
        list_dfs (list): list of DataFrames 
    Return: 
        df_raw (pd.DataFrame): DataFrame with all results
    '''
    df_raw = pd.concat(list_dfs)
    df_raw = df_raw.reset_index(drop=True)
    return df_raw

def write_json(df, path):
    '''
    Write out JSON file 
    Input: 
        df (pd.DataFrame): DataFrame to be written out.
        path (str): write out path
    Return:
       None
    '''
    df.to_json(path)

def to_matrix(l, n):
    '''
    Batch long list into list of lists with n elements
    Inputs:
        l (list): list of elements 
        n (int): lenght of the sublists 
    Return 
        (list): List of list with n elements
    '''
    return [l[i:i+n] for i in range(0, len(l), n)]