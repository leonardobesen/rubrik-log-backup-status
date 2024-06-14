class Cluster():
    def __init__(self, id: str,
                 name: str, connected_state: str) -> None:
        self.id = id
        self.name = name.lower()
        self.connected_state = connected_state

    def __str__(self):
        return f"""\nCluster(id={self.id}, 
        name={self.name}, 
        status={self.connected_state})"""
