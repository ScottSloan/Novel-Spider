import os

path = os.path.join(os.getcwd(), "download")

if not os.path.exists(path):
    os.mkdir(path)