from model.database import Database
from configuration.configuration import non_compliant_threshold
import data_parser

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

    for db in database_data:
        if not db.log_backup_frequency:
            continue

        if not db.log_backup_delay:
            db.log_backup_delay = 0

        if db.log_backup_delay > (threshold * db.log_backup_frequency):
            non_compliance.append(db)
        else:
            in_compliance.append(db)

    return in_compliance, non_compliance


def get_summary_data(in_compliance: list[Database], non_compliance: list[Database]) -> dict:
    summary = {
        "OK": len(in_compliance),
        "NOK": len(non_compliance),
        "SQL_OK": sum(1 for db in in_compliance if db.database_type == "DATABASE_TYPE_SQL"),
        "SQL_NOK": sum(1 for db in non_compliance if db.database_type == "DATABASE_TYPE_SQL"),
        "ORACLE_OK": sum(1 for db in in_compliance if db.database_type == "DATABASE_TYPE_ORACLE"),
        "ORACLE_NOK": sum(1 for db in non_compliance if db.database_type == "DATABASE_TYPE_ORACLE")
    }

    return summary
