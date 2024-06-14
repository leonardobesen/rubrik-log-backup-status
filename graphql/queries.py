def all_cluster_info_query() -> tuple[str, dict]:
    variables = {
        "filter": {
            "productFilters": [
                {
                    "productType": "CDM"
                }
            ]
        }
    }

    query = f"""query ListAllClustersInfo($filter: ClusterFilterInput,$sortBy: ClusterSortByEnum = ClusterName){{
      allClusterConnection(filter: $filter, sortBy: $sortBy){{
        nodes{{
          id
          name
          state{{
            connectedState
          }}
        }}
      }}
    }}"""

    return query, variables


def get_log_backup_status_by_cluster(cluster_id: str,
                                     database_type="",
                                     offset=0,
                                     limit=0) -> tuple[str, dict[str, str]]:
    variables = {
        "input": {
            "clusterUuid": cluster_id,
            "databaseType": database_type,
            "sortBy": "V1_QUERY_LOG_REPORT_REQUEST_SORT_BY_LOG_BACKUP_DELAY",
            "sortOrder": "V1_QUERY_LOG_REPORT_REQUEST_SORT_ORDER_DESC",
            "limit": limit,
            "offset": offset
        }
    }

    query = f"""query DatabaseLogReportForClusterQuery($input: QueryLogReportInput!) {{
      databaseLogReportForCluster(input: $input) {{
        data {{
          id
          name
          location
          databaseType
          lastSnapshotTime
          logBackupDelay
          latestRecoveryTime
          effectiveSlaDomainId
          effectiveSlaDomainName
          logBackupFrequency
          primaryClusterId
        }}
        hasMore
      }}
    }}"""

    return query, variables
