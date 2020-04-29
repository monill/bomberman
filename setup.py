import os
import pygame

from setuptools import setup

pygamedir = os.path.split(pygame.base.__file__)[0]

NAME = "bomberman"
VERSION = "1.0"

plist = dict(
    CFBundleIconFile=NAME,
    CFBundleName=NAME,
    CFBundleShortVersionString=VERSION,
    CFBundleGetInfoString=' '.join([NAME, VERSION]),
    CFBundleExecutable=NAME,
    CFBundleIdentifier='org.pygame.monil.bomberman',
)

setup(
    data_files=[
        'fonts',
        'images',
        'levels',
        'net',
        'sounds',
        os.path.join(pygamedir, pygame.font.get_default_font())
    ],

    app=[
        dict(script="main.py", plist=plist)
    ]
)
