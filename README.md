# rubrik-log-backup-status
A Python script that get a snapshot of Log Backup status for all object on each Rubrik Cluster on the enviroment.

## Dependencies

This projects requires the following libraries to work:
- `rubrik_cdm`
- `pandas`
- `openpyxl`

## How to use it.

1- Create a JSON file named `config.json`, inside the folder `configuration`, with your Rubrik Cluster information, like in the example below:
```
{
    "clusters": [
    {
        "cluster_dc": "Datacenter_name_where_you_rubrik_cdm_is_located",
        "cluster_address": "rubrik_cdm_ip_or_hostname",
        "api_token": "api_token_of_rubrik_cdm"
    },
    {
        "cluster_dc": "Datacenter2",
        "cluster_address": "192.158.10.3",
        "api_token": "really_long_api_string"
    },
    {
        "cluster_dc": "YouGetItByNow",
        "cluster_address": "rubrik3.mydomain.com",
        "api_token": "really_long_api_string_2"
    }
    ]
}
```
2- Download this repository and place in a computer or server that has access to your Rubrik CDMs

3- Install dependencies: `pip install -r requirements.txt`

4- Run main.py
