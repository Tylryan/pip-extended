#!/usr/bin/python3

import os

a = os.getenv("VIRTUAL_ENV").split("/")[-1]
print(a)
