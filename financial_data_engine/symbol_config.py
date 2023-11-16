import json
import logging
import os


class SymbolConfig:
    FILE_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    CREATE_LIST = os.path.join(FILE_ROOT_PATH, "symbol_list_create.json")
    UPDATE_LIST = os.path.join(FILE_ROOT_PATH, "symbol_list_update.json")
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def validate_file_path(file_path):
        if not os.path.exists(file_path):
            logging.error(f"Configuration file {file_path} does not exist.")
            raise FileNotFoundError(f"Configuration file {file_path} does not exist.")

    def get_symbols_from_config(self, file_path):
        self.validate_file_path(file_path)
        try:
            with open(file_path, "r") as file:
                config = json.load(file)
            symbols = config.get("symbols", [])
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON from {file_path}: {e}")
            symbols = []

        return symbols


# Usage:
# config = Config()
# create_symbols = config.get_symbols_from_config(Config.CREATE_LIST)
# update_symbols = config.get_symbols_from_config(Config.UPDATE_LIST)
