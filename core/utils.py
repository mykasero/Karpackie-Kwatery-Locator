import requests
import os
import environ

env = environ.Env()
environ.Env.read_env()

MAILTRAP_API = env("MAILTRAP_API")
# MAILTRAP_SENDER = 