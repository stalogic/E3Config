#!/usr/bin/python3
import json
from e3config import E3Config

if __name__ == "__main__":
    config = E3Config("config.json").get_config()
    print(json.dumps(config, indent=2))

    config = E3Config("config.json", ["eval"]).get_config()
    print(json.dumps(config, indent=2))

    config = E3Config("config.json", ["v3"]).get_config()
    print(json.dumps(config, indent=2))

    config = E3Config("config.json", ["v3", "train"]).get_config()
    print(json.dumps(config, indent=2))