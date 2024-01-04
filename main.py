import json
import os
import connection.connect as connect
import view.write_to_csv as write_to_csv
import datetime

# Global variables
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(ROOT_DIR, 'reports')
CONFIG_FILE = os.path.join(ROOT_DIR, 'configuration', 'config.json')


def analyze_objects(backup_objects: list[dict], cluster_datacenter: str):
    # Defining track variables
    objects_out_of_compliance = []
    objects_in_compliance = []
    cluster_compliance_count = {
        "Cluster Name": cluster_datacenter,
        "OK": 0,
        "NOK": 0,
        "SQL_OK": 0,
        "SQL_NOK": 0,
        "Oracle_OK": 0,
        "Oracle_NOK": 0,
    }

    for backup_object in backup_objects:
        # Adding Cluster Datacenter to backup_object dictionary
        backup_object.update({"cluster": cluster_datacenter})

        # Getting database type (Oracle or SQL)
        object_type = backup_object["databaseType"]

        # This fields might be non-numerical
        try:
            log_backup_frequency = 2 * datetime.timedelta(
                seconds=backup_object["logBackupFrequency"])
        except:
            log_backup_frequency = datetime.timedelta(minutes=0)
        try:
            log_delay = datetime.timedelta(
                seconds=backup_object["logBackupDelay"])
        except:
            log_delay = datetime.timedelta(minutes=0)

        # Check if the delay is greater than the frequency, therefor out of compliance
        if log_delay > log_backup_frequency:
            object_type_key = object_type + "_NOK"

            cluster_compliance_count["NOK"] += 1
            cluster_compliance_count[object_type_key] += 1
            objects_out_of_compliance.append(backup_object)
        else:
            object_type_key = object_type + "_OK"

            cluster_compliance_count["OK"] += 1
            cluster_compliance_count[object_type_key] += 1
            objects_in_compliance.append(backup_object)

    return cluster_compliance_count, objects_in_compliance, objects_out_of_compliance


if __name__ == '__main__':
    # Getting list of Rubrik clusters from JSON
    with open(CONFIG_FILE, 'r') as json_file:
        config_parse = json.load(json_file)

    overall_log_compliance_status = []
    backup_objects_in_compliance = []
    backup_objects_out_of_compliance = []

    # Looping through clusters to perform daily check
    for cluster in config_parse['clusters']:
        try:
            # Establish connection with Rubrik CDM and Cluster name
            rubrik_conn = connect.connect_to_cluster(
                cluster['cluster_address'], cluster['api_token'])
            cluster_datacenter = cluster['cluster_dc']

            # Get Rubrik CDM name
            print(f"Querying API for {cluster_datacenter}")
            limit = 30000
            log_report = rubrik_conn.get(
                'v1', f'/database/log_report?limit={limit}', timeout=600)

            # Check if data is not null
            if not log_report["data"]:
                continue

            cluster_compliance_count, objects_in_compliance, objects_out_of_compliance = analyze_objects(
                log_report["data"], cluster_datacenter)

            overall_log_compliance_status.append(cluster_compliance_count)
            backup_objects_in_compliance += objects_in_compliance
            backup_objects_out_of_compliance += objects_out_of_compliance
        except:
            print(f"Unable to collect data for {cluster['cluster_dc']}")
            continue

    # Send data somewhere
    print("Writing to file")
    write_to_csv.create_file(REPORT_PATH, overall_log_compliance_status,
                             backup_objects_in_compliance, backup_objects_out_of_compliance)
