# Author: https://github.com/jnordling
# Description: Smithsonian Emammal Legacy Data Converter
# Name: Emammal Legacy Data Converter

from jinja2 import Environment, FileSystemLoader
import pandas as pd

import os
import glob
import datetime
from config import fields as f_map
import logging

#Test URl = /Users/jnordling/projects/emammal-csv-manifest/output/L-HTL11-A01B.xml


root_directory = '/Users/jnordling/projects/emammal-csv-manifest/sample-data/wcs-sample-data'
output_directory = '/Users/jnordling/projects/emammal-csv-manifest/output'

DEPLOYMENT_FILE = "Deployment.csv"
IMAGE_FILE = "Image.csv"
PROJECT_FILE = "Project.csv"

fields = f_map.fields # Fields mapping from config
required_files = [DEPLOYMENT_FILE, IMAGE_FILE, PROJECT_FILE]

logging.basicConfig(filename='error.log',filemode='w', level=logging.DEBUG)
env = Environment(loader=FileSystemLoader('templates'))

template = env.get_template('manifest_template.xml')

date_time_format ='%Y-%m-%dT%H:%M:%S'
year_month_date_format = '%Y-%m-%d'

def get_dir_to_process_way(directory):
    return [os.path.join(directory, x) for x in os.listdir(directory) if os.path.isdir(os.path.join(directory, x))]




def set_deployment_values(folder, deployment):
    errors = False
    error_message = "Could not process "+os.path.join(folder, DEPLOYMENT_FILE)
    # Config mappings to field names
    camera_deployment_id = fields["deployment"]["camera_deployment_id"]
    camera_deployment_begin_date = fields["deployment"]["camera_deployment_begin_date"]
    camera_deployment_end_date = fields["deployment"]["camera_deployment_end_date"]

    data = pd.read_csv(os.path.join(folder, DEPLOYMENT_FILE), dtype=str)
    data = data[pd.notnull(data[camera_deployment_id])]
    data[camera_deployment_begin_date] = pd.to_datetime(data[camera_deployment_begin_date])
    data[camera_deployment_end_date] = pd.to_datetime(data[camera_deployment_end_date])
    data[camera_deployment_begin_date] = data[camera_deployment_begin_date].index.map(lambda x: datetime.datetime.strftime(data[camera_deployment_begin_date][x], year_month_date_format))
    data[camera_deployment_end_date] = data[camera_deployment_end_date].index.map(lambda x: datetime.datetime.strftime(data[camera_deployment_end_date][x], year_month_date_format))
    if len(data.index) != 1:
        errors = True
        logging.error(error_message)
        return errors
    try:
        for i in fields["deployment"]:
            csv_mapped_name = fields['deployment'][i]
            if not pd.isnull(data[csv_mapped_name]).tolist()[0]:
                deployment[i] = data[csv_mapped_name].tolist()[0]
            else:
                deployment[i] = None
    except Exception as e:
        errors = True
        logging.error(error_message)
        logging.error(e)

    # return the success of setting the function
    return errors


def set_project_values(folder, deployment):
    errors = False
    error_message = "Could not process "+os.path.join(folder, PROJECT_FILE)
    project_id = fields["project"]['project_id']
    publish_date = fields["project"]["publish_date"]
    data = pd.read_csv(os.path.join(folder, PROJECT_FILE), dtype=str)
    data = data[pd.notnull(data[project_id])]
    if len(data.index) != 1:
        errors = True
        logging.error(error_message)
        return errors
    try:
        data[publish_date] = pd.to_datetime(data[publish_date])
        data[publish_date] = data[publish_date].index.map(lambda x: datetime.datetime.strftime(data[publish_date][x], year_month_date_format))
        for i in fields['project']:
            csv_mapped_name = fields['project'][i]
            if not pd.isnull(data[csv_mapped_name]).tolist()[0]:
                deployment[i] = data[csv_mapped_name].tolist()[0]
            else:
                deployment[i] = None

        # If project_owner_email os  null make it the same as principal_investigator_email (Validator requires value)
        if deployment['project_owner_email'] == None:
            deployment['project_owner_email'] = deployment['principal_investigator_email']

    except Exception as e:
        errors = True
        logging.error(error_message)
        logging.error(e)

    # return the success of setting the function
    return errors

def write_deployment(dir,deployment):
    errors = False
    error_message = "Error writing deployment file "+ os.path.join(output_directory, os.path.basename(dir)+".xml")
    try:
        output = template.render(deployment=deployment)
        out_file = open(os.path.join(output_directory, os.path.basename(dir)+".xml"),'w')
        out_file.write(output)
        out_file.close()
    except Exception as e:
        logging.error(error_message)
        errors = True
    return errors


def get_access_constraint(constraints_array):
    if 'US' in constraints_array:
        constraint = 'US'
    elif 'CR' in constraints_array:
        constraint= 'CR'
    elif 'EN' in constraints_array:
        constraint = 'EN'
    else:
        constraint = constraints_array[0]

    return constraint


def create_sequences(folder, deployment):
    errors = False
    error_message ="Could not process sequences"
    try:

        sequences = []
        data = pd.read_csv(os.path.join(folder,IMAGE_FILE), dtype=str)
        data = data[pd.notnull(data[fields["image"]["image_id"]])]
        date_time = fields["image"]["date_time"]
        iucn_status = fields["image"]["iucn_status"]

        data[date_time] = pd.to_datetime(data[date_time])
        data = data.sort_values([date_time], ascending=True)
        count = 0
        while not data.empty:
            start_date = data.ix[data.head(1)[date_time].index.tolist()[0]][date_time]
            end_date = start_date + datetime.timedelta(seconds=60)
            mask = data[(data[date_time] >= start_date) & (data[date_time] <= end_date)]
            mask = mask.sort_values([date_time], ascending=True)
            sequence_start_data = datetime.datetime.strftime(mask[date_time][mask[date_time].index.tolist()[0]],date_time_format)
            sequence_end_data = datetime.datetime.strftime(mask[date_time][mask[date_time].index.tolist()[0]],date_time_format)

            sequence = {}
            sequence["sequence_id"] = deployment["camera_deployment_id"]+"s"+str(count)
            sequence["begin_date_time"] = sequence_start_data
            sequence["end_date_time"] = sequence_end_data
            sequence["researcher_identifications"] = []
            sequence["images"] = []
            access_constraints_array = []

            image_count = 1
            for i in mask.iterrows():
                r_indent = {}
                image = {}
                index = i[0] # int value of which image in seq

                # Set Images & researcher_identifications values
                image["image_order"] = image_count
                for i in fields['image']:
                    csv_mapped_name = fields['image'][i]
                    if not pd.isnull(mask[csv_mapped_name][index]):
                        image[i] = mask[csv_mapped_name][index]
                        r_indent[i] = mask[csv_mapped_name][index]
                    else:
                        image[i] = None
                        r_indent[i] = None
                sequence["researcher_identifications"].append(r_indent)

                ## XML Requires these values to be lower case
                if image["photo_type"]:
                    image["photo_type"] = image["photo_type"].lower()
                if image["date_time"]:
                    image["date_time"] = datetime.datetime.strftime(image["date_time"],date_time_format)

                access_constraints_array.append(mask[iucn_status][index])
                sequence["images"].append(image)
                image_count = image_count + 1

            # End of image loop

            sequences.append(sequence)
            deployment["access_constraint"] = get_access_constraint(list(set(access_constraints_array)))

            ## Set new data val
            data = data[data[date_time] > end_date]
            count = count + 1

        # End of sequences loop

        deployment["sequences"] = sequences
    except Exception as e :
        errors = True
        logging.error(error_message)
        logging.error(e)

    return errors

def validate_required_files(directory):
    errors = False
    error_message = "No CSV file found in " + root_directory

    all_csv_files = glob.glob(directory+'/'+'*.csv')
    if len(all_csv_files) == 0:
        errors = True
        logging.error(error_message)
        print error_message
    for csv in all_csv_files:
        if not os.path.basename(csv) in required_files:
            message = 'Invalid Filename ' + csv + " must match [ " + ", ".join(required_files) + ' ]'
            print message
            logging.error(message)
            errors = True
    return errors

def validate_fields(folder):
    errors = False
    for f in required_files:
        df = pd.read_csv(os.path.join(folder, f), dtype=str)
        headers =  list(df)
        if f == IMAGE_FILE:
            config_fields = fields["image"]
        elif f == PROJECT_FILE:
            config_fields = fields["project"]
        else:
            config_fields = fields["deployment"]

        for i in config_fields:
            if not config_fields[i] in headers:
                print 'Expexting field '+"`"+config_fields[i]+"`" +'in' +os.path.join(folder, f)
                logging.error('Expexting field '+"`"+config_fields[i]+"`" +' in' +os.path.join(folder, f))
                errors = True
    return errors


def main():
    if not os.path.isdir(root_directory):
        logging.error('Invalid Root Directory ' + root_directory)
        return

    for dir in get_dir_to_process_way(root_directory):
        deployment = {}
        errors_in_directories = validate_required_files(dir)
        if errors_in_directories:
            continue

        errors_in_fields_valid = validate_fields(dir)
        if errors_in_fields_valid:
            continue

        errors_project_values = set_project_values(dir, deployment)
        errors_deployment_values = set_deployment_values(dir, deployment)
        errors_sequence_values = create_sequences(dir,deployment)
        errors_write_deployment = write_deployment(dir, deployment)

        if errors_project_values or errors_deployment_values or errors_sequence_values or errors_write_deployment:
            continue



if __name__ == '__main__':
    main()