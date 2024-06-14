from connection.wrapper import request
from graphql import queries
import data.data_operation as data
from model.cluster import Cluster
from model.database import Database


def _get_all_cluster_info(access_token: str) -> list[Cluster]:
    clusters_information = []

    # Gather clusters information
    query, variables = queries.all_cluster_info_query()

    try:
        response = request(access_token, query, variables)
    except Exception:
        raise LookupError("Unable to collect clusters data!")

    if not response["data"]:
        return []

    # Process cluster information
    for item in response["data"]["allClusterConnection"]["nodes"]:
        cluster = data.create_cluster_from_data(item)
        if cluster:
            clusters_information.append(cluster)

    return clusters_information


def _parse_databases_from_cluster(access_token: str, cluster: Cluster) -> list[Database]:
    offset = 0
    limit = 1000
    has_more = True
    databases_info_at_cluster = []

    while has_more:
        query, variables = queries.get_log_backup_status_by_cluster(
            cluster_id=cluster.id,
            offset=offset,
            limit=limit)

        try:
            response = request(access_token, query, variables)
        except Exception:
            print(f"Unable to collect database data for {cluster.name}!")
            continue

        if not response["data"]:
            continue

        for item in response["data"]["databaseLogReportForCluster"]["data"]:
            cluster = data.create_cluster_from_data(item)
            if cluster:
                databases_info_at_cluster.append(cluster)

        has_more = response["data"]["databaseLogReportForCluster"]["hasMore"]
        offset += limit

    return databases_info_at_cluster


def get_all_databases_info(access_token: str) -> list[Database]:
    databases_information = []

    clusters = _get_all_cluster_info(access_token=access_token)

    for cluster in clusters:
        databases_information += _parse_databases_from_cluster(
            access_token=access_token,
            cluster=cluster)

    return databases_information


