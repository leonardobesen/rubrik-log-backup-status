from typing import Optional
from model.cluster import Cluster
from services.converter import iso_to_date, seconds_to_duration


class Database():
    def __init__(self, id: str, name: str, database_type: str, location: str,
                 last_snapshot_time: str, log_backup_delay: Optional[int],
                 last_recovery_time: str, sla_id: str, sla_name: str,
                 log_backup_frequency: Optional[int], cluster: Cluster) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.database_type = database_type
        self.last_snapshot_time = iso_to_date(last_snapshot_time)
        self.log_backup_delay = seconds_to_duration(log_backup_delay)
        self.last_recovery_time = iso_to_date(last_recovery_time)
        self.sla_id = sla_id
        self.sla_name = sla_name
        self.log_backup_frequency = seconds_to_duration(log_backup_frequency)
        self.cluster = cluster

    def __str__(self):
        return f"""\nDatabase(id={self.id}, 
        name={self.name}, 
        status={self.database_type},
        log_delay={self.log_backup_delay})"""
