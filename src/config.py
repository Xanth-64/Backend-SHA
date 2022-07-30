# -*- coding: utf-8 -*-
"""General Configuration Params
"""
from os import getpid, path

import firebase_admin
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

# Firebase Admin Configuration
try:
    firebase_admin.initialize_app(name=f"firebase-admin {getpid()}")
except ValueError:
    print("Duplicate Process Detected")
    firebase_admin.get_app(name=f"firebase-admin {getpid()}")
