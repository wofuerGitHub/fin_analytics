"""config module"""

#!/usr/bin/python3

""" {
    "database": {
      "host": "127.0.0.1",
      "schema": "fmg",
      "user": "fmg",
      "password": "fmg"
    },
    "fmg": {
      "apiKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "speed": 1
    },
    "file": {
      "log": "./fin_suite4.log",
      "debug": "./fin_suite4_debug.log",
      "speedControl": "./fmg_speed.ctl"
    },
    "debug":true
  } """

import json

def load_config(file = "config.json"):

    with open(file, "r") as f:
        config = json.load(f)
    return config

def get_database_host(config = None):
    if config:
        pass
    else:
        config = load_config()
    return config['database']['host']

def get_database_schema():
    config = load_config()
    return config['database']['schema']

def get_database_user():
    config = load_config()
    return config['database']['user']

def get_database_password():
    config = load_config()
    return config['database']['password']

# ---

def get_fmg_api_key():
    config = load_config()
    return config['fmg']['apiKey']

def get_fmg_speed():
    config = load_config()
    return config['fmg']['speed']

# ---

def get_file_log():
    config = load_config()
    return config['file']['log']

def get_file_debug():
    config = load_config()
    return config['file']['debug']

def get_file_speed_control():
    config = load_config()
    return config['file']['speedControl']

# ---

def get_debug():
    config = load_config()
    return config['debug']