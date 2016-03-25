from jinja2 import Environment, FileSystemLoader
import pandas as pd

import os
import glob
import datetime
from config import csv_field_mapping as f_map
import logging


#Test URl = /Users/jnordling/projects/emammal-csv-manifest/output/L-HTL11-A01B.xml


directory = '/Users/jnordling/projects/emammal-csv-manifest/sample-data'
output_directory = '/Users/jnordling/projects/emammal-csv-manifest/output'

date_format ='%Y-%m-%d-%H+%M:%S.%f'
DEPLOYMENT_FILE = "Deployment.csv"
IMAGE_FILE = "Image.csv"
PROJECT_FILE = "Project.csv"

fields = f_map.fields # Fields mapping from config
required_files = [DEPLOYMENT_FILE, IMAGE_FILE, PROJECT_FILE]

logging.basicConfig(filename='error.log',filemode='w', level=logging.DEBUG)
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('manifest_template.xml')



def get_dir_to_process_way():
    return [os.path.join(directory, x) for x in os.listdir(directory) if os.path.isdir(os.path.join(directory, x))]

def validate_required_files(directory):
    all_csv_files = glob.glob(directory+'/'+'*.csv')
    is_valid = True
    for csv in all_csv_files:
        if not os.path.basename(csv) in required_files:
            return False
    return is_valid


def set_deployment_values(folder, deployment):
    success = True
    data = pd.read_csv(os.path.join(folder, DEPLOYMENT_FILE), dtype=str)
    data = data[pd.notnull(data['Camera Deployment ID'])]
    data['Camera Deployment Begin Date'] = pd.to_datetime(data['Camera Deployment Begin Date'])
    data['Camera Deployment End Date'] = pd.to_datetime(data['Camera Deployment End Date'])

    data['Camera Deployment End Date'] = data['Camera Deployment End Date'].index.map(lambda x: datetime.datetime.strftime(data['Camera Deployment End Date'][x], '%Y-%m-%d'))
    data['Camera Deployment Begin Date'] = data['Camera Deployment Begin Date'].index.map(lambda x: datetime.datetime.strftime(data['Camera Deployment Begin Date'][x], '%Y-%m-%d'))
    # data['Camera Deployment Begin Date'] = data['Camera Deployment Begin Date']
    # data['Camera Deployment End Date'] = data['Camera Deployment End Date']
    if len(data.index) != 1:
        success = False
        return success
    try:

        for i in fields["deployment"]:
            csv_mapped_name = fields['deployment'][i]
            if not pd.isnull(data[csv_mapped_name]).tolist()[0]:
                deployment[i] = data[csv_mapped_name].tolist()[0]
            else:
                deployment[i] = None
    except Exception as e:
        success = False

    # return the success of setting the function
    return success


def set_project_values(folder, deployment):
    success = True
    data = pd.read_csv(os.path.join(folder, PROJECT_FILE), dtype=str)
    data = data[pd.notnull(data['Project ID'])]
    data['Publish Date'] = pd.to_datetime(data['Publish Date'])
    # data['Publish Date'] = data['Publish Date'][0].strftime('%Y-%m-%dT%H:%M:%SZ')
    data['Publish Date'] = data['Publish Date'].index.map(lambda x: datetime.datetime.strftime(data['Publish Date'][x], '%Y-%m-%d'))
    if len(data.index) != 1:
        success = False
        return success
    try:
        for i in fields['project']:
            csv_mapped_name = fields['project'][i]
            if not pd.isnull(data[csv_mapped_name]).tolist()[0]:
                deployment[i] = data[csv_mapped_name].tolist()[0]
            else:
                deployment[i] = None
        if deployment['project_owner_email'] == None:
            deployment['project_owner_email'] = deployment['principal_investigator_email']
    except Exception as e:
        success = False

    # return the success of setting the function
    return success

def write_oufile(dir,deployment):
    output = template.render(deployment=deployment)
    out_file = open(os.path.join(output_directory, os.path.basename(dir)+".xml"),'w')
    out_file.write(output)
    out_file.close()


def create_sequences(folder, deployment):
    sequences = []
    data = pd.read_csv(os.path.join(folder,IMAGE_FILE), dtype=str)
    data = data[pd.notnull(data['Image ID'])]
    data['Date_Time'] = pd.to_datetime(data['Date_Time'])
    data = data.sort(['Date_Time'], ascending=True)
    count = 0
    while not data.empty:
        start_date = data.ix[data.head(1)["Date_Time"].index.tolist()[0]]["Date_Time"]
        end_date = start_date + datetime.timedelta(seconds=60)
        mask = data[(data['Date_Time'] >= start_date) & (data['Date_Time'] <= end_date)]
        mask = mask.sort(['Date_Time'], ascending=True)
        sequence_start_data = datetime.datetime.strftime(mask["Date_Time"][mask["Date_Time"].index.tolist()[0]],'%Y-%m-%dT%H:%M:%S')
        sequence_end_data = datetime.datetime.strftime(mask["Date_Time"][mask["Date_Time"].index.tolist()[0]],'%Y-%m-%dT%H:%M:%S')

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
            index = i[0]
            ## researcher_identifications
            r_indent["iucn_id"] = [mask["IUCN ID"][index] if not pd.isnull(mask["IUCN ID"][index]) else None][0]
            r_indent["sn"] = [mask["Genus Species"][index] if not pd.isnull(mask["Genus Species"][index]) else None][0]
            r_indent["age"] = [mask["Age"][index] if not pd.isnull(mask["Age"][index]) else None][0]
            r_indent["sex"] = [mask["Sex"][index] if not pd.isnull(mask["Sex"][index]) else None][0]
            r_indent["individual_id"] = [mask["Individual ID"][index] if not pd.isnull(mask["Individual ID"][index]) else None][0]
            r_indent["animal_recognizable"] = [mask["Animal recognizable"][index] if not pd.isnull(mask["Animal recognizable"][index]) else None][0]
            r_indent["individual_animal_notes"] = [mask["Individual Animal Notes"][index] if not pd.isnull(mask["Individual Animal Notes"][index]) else None][0]
            sequence["researcher_identifications"].append(r_indent)

            # Images
            image = {}
            access_constraints_array.append(mask['IUCN Status'][index])
            image["image_id"] = [mask["Image ID"][index] if not pd.isnull(mask["Image ID"][index]) else None][0]
            image["file_name"] = [mask["Image File Name"][index] if not pd.isnull(mask["Image File Name"][index]) else None][0]
            image["date_time_original"] = datetime.datetime.strftime([mask["Date_Time"][index] if not pd.isnull(mask["Date_Time"][index]) else None][0],'%Y-%m-%dT%H:%M:%S')
            image["image_order"] = image_count
            image["digital_origin"] = [mask["Digital Origin"][index] if not pd.isnull(mask["Digital Origin"][index]) else None][0]
            image["photo_type"] = [mask["Photo Type"][index] if not pd.isnull(mask["Photo Type"][index]) else None][0].lower()
            image["photo_type_identified_by"] = [mask["Photo Type Identified by"][index] if not pd.isnull(mask["Photo Type Identified by"][index]) else None][0]
            image["count"] = [mask["Count"][index] if not pd.isnull(mask["Count"][index]) else None][0]
            image['restrictions_on_access'] = [mask["Restrictions on Access"][index] if not pd.isnull(mask["Restrictions on Access"][index]) else None][0]
            image['embargo_period_end_date'] = [mask["Embargo Period"][index] if not pd.isnull(mask["Embargo Period"][index]) else None][0]
            image['image_use_restrictions'] = [mask["Image Use Restrictions"][index] if not pd.isnull(mask["Image Use Restrictions"][index]) else None][0]

            image["iucn_id"] = [mask["IUCN ID"][index] if not pd.isnull(mask["IUCN ID"][index]) else None][0]
            image["sn"] = [mask["Genus Species"][index] if not pd.isnull(mask["Genus Species"][index]) else None][0]
            image["age"] = [mask["Age"][index] if not pd.isnull(mask["Age"][index]) else None][0]
            image["sex"] = [mask["Sex"][index] if not pd.isnull(mask["Sex"][index]) else None][0]
            image["individual_id"] = [mask["Individual ID"][index] if not pd.isnull(mask["Individual ID"][index]) else None][0]
            image["animal_recognizable"] = [mask["Animal recognizable"][index] if not pd.isnull(mask["Animal recognizable"][index]) else None][0]
            image["individual_animal_notes"] = [mask["Individual Animal Notes"][index] if not pd.isnull(mask["Individual Animal Notes"][index]) else None][0]
            sequence["images"].append(image)
            image_count = image_count + 1

        access_constraints_array = list(set(access_constraints_array))
        if 'US' in access_constraints_array:
            deployment['access_constraint'] = 'US'
        elif 'CR' in access_constraints_array:
            deployment['access_constraint'] = 'CR'
        elif 'EN' in access_constraints_array:
            deployment['access_constraint'] = 'EN'
        else:
            deployment['access_constraint'] = access_constraints_array[0]


        sequences.append(sequence)

        ## Set new data val
        data = data[data['Date_Time'] > end_date]
        count = count + 1
    deployment["sequences"] = sequences


def main():
    # Check if the directory given is valid
    if not os.path.isdir(directory):
        logging.error('Invalid Directory ' + directory)
        raise Exception('ERROR >> Invalid Directory', directory)

    for dir in get_dir_to_process_way():
        # Reset Deployment
        deployment = {}
        # Check that this directory has all required files
        if not validate_required_files(dir):
            logging.error('Error Processing not all required files : ' + dir)
            print 'Error Processing ', dir
            continue  # Something went wrong continue to other dir
        # Process deployment
        print 'processing ', dir
        project_values = set_project_values(dir, deployment)

        deployment_values = set_deployment_values(dir, deployment)
        sequence_values =  create_sequences(dir,deployment)
        # Ckeck if the setting projects failed
        if not project_values or not deployment_values:
            logging.error("Could not set project values for" + dir)
            continue  # Something went wrong continue to other dir
        write_oufile(dir,deployment)



if __name__ == '__main__':
    main()