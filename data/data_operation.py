from typing import Optional
from model.cluster import Cluster
from model.database import Database


def create_cluster_from_data(data) -> Optional[Cluster]:
    try:
        return Cluster(
            id=data["id"],
            name=data["name"],
            connected_state=data["state"]["connectedState"]
        )
    except Exception as e:
        print("Error processing cluster item: ", e)
        return None


def create_database_from_data(data, cluster: Cluster) -> Optional[Database]:
    try:
        return Database(
            id=data["id"],
            name=data["name"],
            location=data["location"],
            database_type=data["databaseType"],
            last_snapshot_time=data["lastSnapshotTime"],
            log_backup_delay=data["logBackupDelay"],
            last_recovery_time=data["latestRecoveryTime"],
            sla_id=data["effectiveSlaDomainId"],
            sla_name=data["effectiveSlaDomainName"],
            log_backup_frequency=data["logBackupFrequency"],
            cluster=cluster
        )
    except Exception as e:
        print("Error processing database item: ", e)
        return None
