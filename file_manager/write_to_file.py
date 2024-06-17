import pandas as pd
import os
from enum import Enum
from datetime import datetime
from configuration.configuration import get_root_dir
from services.formatter import format_timedelta
from model.database import Database


class Sheets(Enum):
    SUMMARY = 'Object Status'
    INCOMPLIANCE = 'Objects In Compliance'
    NONCOMPLIANCE = 'Objects Out of Compliance'


def create_empty_file() -> str:
    # Get current datetime formatted
    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
    file_name = f'Rubrik_Log_Backup_Compliance_{now}.xlsx'
    report_path = os.path.join(get_root_dir(), 'reports', file_name)

    return report_path


def generate_report(summary: dict, in_compliance: list[Database], non_compliance: list[Database]) -> str:
    REPORT_FILE = create_empty_file()

    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl')

    writer = write_summary_data(
        writer, summary)
    writer = write_compliance_data(
        writer, in_compliance, in_compliance=True)
    writer = write_compliance_data(
        writer, non_compliance, in_compliance=False)

    writer.close()

    return REPORT_FILE


def write_summary_data(writer: pd.ExcelWriter, summary: dict) -> pd.ExcelWriter:
    writer.book.create_sheet(title=Sheets.SUMMARY.value)

    df_summary = pd.DataFrame([{
        'Cluster': cluster,
        'OK': summary[cluster]["OK"],
        'NOK': summary[cluster]["NOK"],
        'SQL OK': summary[cluster]["SQL_OK"],
        'SQL NOK': summary[cluster]["SQL_NOK"],
        'Oracle OK': summary[cluster]["ORACLE_OK"],
        'Oracle NOK': summary[cluster]["ORACLE_NOK"]
    } for cluster in summary])
    df_summary.to_excel(writer, sheet_name=Sheets.SUMMARY.value, index=False)

    return writer


def write_compliance_data(writer: pd.ExcelWriter, db_list: list[Database], in_compliance: bool = True) -> pd.ExcelWriter:
    if in_compliance:
        sheet_name = Sheets.INCOMPLIANCE.value
    else:
        sheet_name = Sheets.NONCOMPLIANCE.value

    writer.book.create_sheet(title=sheet_name)

    df_summary = pd.DataFrame([{
        'Cluster': db.cluster.name,
        'Id': db.id,
        'Name': db.name,
        'Location': db.location,
        'Database Type': db.database_type,
        'Log Backup Frequency': format_timedelta(db.log_backup_frequency),
        'Log Backup Delay': format_timedelta(db.log_backup_delay),
        'Effective SLA Domain': db.sla_name,
        'Last Snapshot Time': db.last_snapshot_time,
        'Last Recovery Time': db.last_recovery_time,
    } for db in db_list])
    df_summary.to_excel(writer, sheet_name=sheet_name, index=False)

    return writer