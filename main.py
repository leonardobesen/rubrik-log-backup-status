import json
import os
import connection.connect as connect
import view.write_to_csv as write_to_csv
import datetime

# Global variables 
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(ROOT_DIR, 'reports')
CONFIG_FILE = os.path.join(ROOT_DIR, 'configuration', 'config.json')

def count_objects(backup_objects: list[dict], cluster_name: str):
    # Defining track variables
    objects_out_of_compliance = []
    cluster_compliance_count = {
        "Cluster Name": cluster_name,
        "OK"          : 0,
        "NOK"         : 0,
        "SQL"         : {"OK": 0, "NOK": 0},
        "Oracle"      : {"OK": 0, "NOK": 0},
    }

    print(f"Processing object for {cluster_name}")
    for backup_object in backup_objects:
        # This fields might not be returned by the API response
        try:
            log_backup_frequency = datetime.timedelta(seconds=backup_object["logBackupFrequency"])
            log_delay = datetime.timedelta(seconds=backup_object["logBackupDelay"])
            object_type = backup_object["databaseType"]
        except:
            continue

        # Add to count
        if log_delay > log_backup_frequency:
            cluster_compliance_count["NOK"] += 1
            cluster_compliance_count[object_type]["NOK"] += 1
            objects_out_of_compliance.append(backup_object)
        else:
            cluster_compliance_count["OK"] += 1
            cluster_compliance_count[object_type]["OK"] += 1

    return cluster_compliance_count, objects_out_of_compliance
    

if __name__ == '__main__':
    # Getting list of Rubrik clusters from JSON
    with open(CONFIG_FILE, 'r') as json_file:
        config_parse = json.load(json_file)

    overall_log_compliance_status = []
    backup_objects_out_of_compliance = []

    # Looping through clusters to perform daily check
    for cluster in config_parse['clusters']:
        # Establish connection with Rubrik CDM and Cluster name
        rubrik_conn = connect.connect_to_cluster(cluster['cluster_address'], cluster['api_token'])
        cluster_name = cluster['cluster_dc']

        # Get Rubrik CDM name
        print(f"Querying API for {cluster_name}")
        limit = 30000
        log_report = rubrik_conn.get('v1', f'/database/log_report?limit={limit}')

        # Check if data is not null
        if not log_report["data"]:
            print(f"No log backups found for {cluster_name}")
            continue
        
        cluster_compliance_count, objects_out_of_compliance = count_objects(log_report["data"], cluster_name)

        overall_log_compliance_status.append(cluster_compliance_count)
        backup_objects_out_of_compliance += objects_out_of_compliance

    # Send data somewhere
    print("Writing to file")
    write_to_csv.create_file(REPORT_PATH, overall_log_compliance_status, backup_objects_out_of_compliance)
