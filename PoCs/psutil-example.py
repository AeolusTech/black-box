#!/usr/bin/env python
import psutil

# gives a single float value
print(psutil.cpu_percent())

# gives an object with many fields
print(psutil.virtual_memory())

# you can convert that object to a dictionary
print(dict(psutil.virtual_memory()._asdict()))

# you can have the percentage of used RAM
print(f'memory usage: psutil.virtual_memory().percent')


# you can calculate percentage of available memory
print(f'free: {psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}')

