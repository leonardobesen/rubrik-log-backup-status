from model.database import Database
from datetime import timedelta
from configuration.configuration import non_compliant_threshold
import data.data_parser as data_parser

database_data = None
threshold = non_compliant_threshold()


def _initialize_database_data(access_token: str):
    global database_data
    if database_data is None:
        database_data = data_parser.get_all_databases_info(
            access_token=access_token)


def get_compliance(access_token: str) -> tuple[list[Database], list[Database]]:
    _initialize_database_data(access_token)
    non_compliance = []
    in_compliance = []

    print("Analyzing compliance...")
    for db in database_data:
        if not db.log_backup_frequency:
            continue

        if not db.log_backup_delay:
            db.log_backup_delay = timedelta(seconds=0)

        if db.log_backup_delay > \
                timedelta(seconds=threshold * db.log_backup_frequency.total_seconds()):
            non_compliance.append(db)
        else:
            in_compliance.append(db)

    return in_compliance, non_compliance


def get_summary_data(in_compliance: list[Database], non_compliance: list[Database]) -> dict:
    summary = {}

    for db in in_compliance:
        cluster = db.cluster.name.lower()
        summary[cluster] = {
            "OK": sum(1 for db in in_compliance if db.cluster.name.lower() == cluster),
            "NOK": sum(1 for db in non_compliance if db.cluster.name.lower() == cluster),
            "SQL_OK": sum(1 for db in in_compliance if db.database_type == "DATABASE_TYPE_SQL" and db.cluster.name.lower() == cluster),
            "SQL_NOK": sum(1 for db in non_compliance if db.database_type == "DATABASE_TYPE_SQL" and db.cluster.name.lower() == cluster),
            "ORACLE_OK": sum(1 for db in in_compliance if db.database_type == "DATABASE_TYPE_ORACLE" and db.cluster.name.lower() == cluster),
            "ORACLE_NOK": sum(1 for db in non_compliance if db.database_type == "DATABASE_TYPE_ORACLE" and db.cluster.name.lower() == cluster)
        }

    return summary
