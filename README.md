# rubrik-log-backup-status

Python script that generates a point-in-time Excel report (.xlsx) of Log Backup compliance status for all Oracle and SQL databases on each Rubrik Cluster on the enviroment.

## Dependencies

- Python >= 3.11
- requests
- pandas
- google-api-python-client
- google-auth-oauthlib

## How to use it.

1- Create a JSON file named `config.json` with your Rubrik Security Cloud (RSC) and RSC Service Account information like in the example below and add it inside `../rubrik-daily-check/configutarion/` folder:

```
{
	"client_id": "your_client_id",
	"client_secret": "your_client_secret",
	"name": "name_you_gave",
	"access_token_uri": "https://yourdomain.my.rubrik.com/api/client_token",
	"graphql_url": "https://yourdomain.my.rubrik.com/api/graphql",
	"google_drive_upload_folder_id": ["your_drive_folders_ids_here"],
	"tz_info": "America/Sao_Paulo",
  "non_compliance_threshold": 1.5
}
```

_OBS_: `google_drive_upload_folder_id` and `tz_info` are OPTIONAL.

- If `tz_info` is not declared or left blank (`""`) it will use UTC+0
- If `non_compliance_threshold` is not declared or left blank (`""`) it will use `1.0`
- if `google_drive_upload_folder_id` or left blank (`""`) it will **skip** the process that upload the file to Google Drive

2 - _(Skip this step if you did NOT declare `google_drive_upload_folder_id` on `config.json`)_
You must create a file named `google_drive.json` on `../rubrik-daily-check/configutarion/` folder. See the file example below:

```
{
  "installed": {
    "client_id": "your_client_id",
    "project_id": "your_project_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your_client_secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

3- Download this repository and place in a computer or server that has access to your Rubrik CDMs

4- Run main.py

## Log Backup Threshold Multiplier

Log Backup Frequency multiplier that defines when a Log Backup Delay is Non Compliant (Out of Compliance).
The default value is always 1.0, increasing in a factor of 0.5 (to 1.5) will make that the Log Backup Delay has to be 1.5 times higher the Log Backup Frequency to be considered Non Compliant.
