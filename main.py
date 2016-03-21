import jinja2
import pandas as pd

import os
import glob
import datetime
from config import csv_field_mapping as f_map



directory = '/Users/jnordling/projects/emammal-csv-manifest/sample-data'

DEPLOYMENT_FILE = "Deployment.csv"
IMAGE_FILE = "Image.csv"
PROJECT_FILE = "Project.csv"

fields = f_map.fields # Fields mapping from config
deployment = {}

required_files = [DEPLOYMENT_FILE, IMAGE_FILE, PROJECT_FILE]


def create_sequences():
    data = pd.read_csv('./Images.csv', dtype=str)
    data = data[pd.notnull(data['Image ID'])]
    data['Date_Time Captured'] = pd.to_datetime(data['Date_Time Captured'])
    data = data.sort(['Date_Time Captured'], ascending=True)
    count = 0
    while not data.empty:
        start_date = data.ix[data.head(1)["Date_Time Captured"].index.tolist()[0]]["Date_Time Captured"]
        end_date = start_date + datetime.timedelta(seconds=60)
        mask = data[(data['Date_Time Captured'] >= start_date) & (data['Date_Time Captured'] <= end_date)]
        data = data[data['Date_Time Captured'] > end_date ]
        print count
        count = count + 1

def get_dir_to_process_way():
    return [os.path.join(directory, x) for x in os.listdir(directory) if os.path.isdir(os.path.join(directory, x))]

def validate_required_files(directory):
    all_csv_files = glob.glob(directory+'/'+'*.csv')
    is_valid = True
    for csv in all_csv_files:
        if not os.path.basename(csv) in required_files:
            return False
    return is_valid

def set_project_values(folder):
    is_error = False
    data = pd.read_csv(os.path.join(folder,PROJECT_FILE), dtype=str)
    data = data[pd.notnull(data['Project ID'])]
    print data.isnull()
    ## Checking there is only one row
    if len(data.index) != 1:
        is_error = False
        return is_error

    for i in fields['project']:
        deployment[i] = "hahah"
        csv_mapped_name = fields['project'][i]
        # if data(data[csv_mapped_name]):
        print i,data[csv_mapped_name].tolist()[0]


def main():
    # Check if the directory given is valid
    if not os.path.isdir(directory):
        raise Exception('ERROR >> Invalid Directory', directory)

    for f in get_dir_to_process_way():
        # Check that this directory has all necessary files
        if not validate_required_files(f):
            print 'ERROR >>  Is Not Valid, check CSV File name:', f
            continue
        set_project_values(f)


if __name__ == '__main__':
    main()