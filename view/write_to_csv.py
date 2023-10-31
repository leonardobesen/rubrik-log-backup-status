import pandas as pd
import os
from datetime import datetime


def create_file(REPORT_PATH: str, overall_log_compliance_status: list[dict],
                backup_objects_in_compliance: list[dict], backup_objects_out_of_compliance: list[dict]):
    # Get now datetime info formatted
    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

    # Set path and file information
    file_name = 'Rubrik_Log_Compliance_{date}.xlsx'.format(date=now)
    report_name = os.path.join(REPORT_PATH, file_name)

    writer = pd.ExcelWriter(report_name, engine='openpyxl')

    df = pd.DataFrame(overall_log_compliance_status)
    df.to_excel(writer, sheet_name='Objects Status', index=False)

    if backup_objects_in_compliance:
        df = pd.DataFrame(backup_objects_in_compliance)
        df.to_excel(writer, sheet_name="Objects In Compliance", index=False)

    if backup_objects_out_of_compliance:
        df = pd.DataFrame(backup_objects_out_of_compliance)
        df.to_excel(writer, sheet_name="Objects Out of Compliance", index=False)

    writer.close()
    print(f"File saved on {report_name}")
