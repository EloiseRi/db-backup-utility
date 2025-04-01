from abc import ABC, abstractmethod

class IDatabase(ABC):
    def __init__(self, config):
        self.config = config
        self.database = self.config.get("database", {})
        self.conn = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def backup(self, backup_type, output_path):
        pass

    @abstractmethod
    def restore(self, backup_file):
        pass
