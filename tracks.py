#!/usr/bin/env python
"""Script de génération des backing tracks de zic avec Gab

L'objectif est d'avoir un script pour la génération des backing
tracks. Pour ça, on source un fichier de configuration avec les infos
nécessaires (titre du morceau, instrument avec volume associée et la
piste), etc.

| [main]
| title=96_degrees
| destination=/home/stilly/ownCloud/zic-gab-zen/sons/backs/
|
| [guitar]
| track=96_degrees_guit_80_F.wav
| volume=0.4
|
| [voice]
| track=96_degrees_voix_80_F.wav
| volume=1.0
|
| [drum]
| track=96_degrees_bat_hydro_80.wav
| volume=1
|
| [bass]
| track=96_degrees_bass_2F.wav
| volume=1

Pour lancer le script, on lance le binaire avec :
> tracks.py [options] /path/to/initfile.ini
Pour avoir la liste des options, passer un -h
"""

import sys
import os

import traceback

from pprint import pprint

from tracks.tools import *
from tracks.configparser import TracksConfigParser, TracksConfigParserException, set_configparser
from tracks.backingtrack import BackingTrack, drum, back, zeta, full


if __name__ == "__main__":

    config_filename = "./back.ini"
    #try:
    c = set_configparser(config_filename)
    #except TracksConfigParserException as e:
    #    print_err("Impossible to parse " + blue("main config file part"), error=e, fatal=True)
    #except Exception as e:
    #    print_err("Error when loading " + blue(config_filename), error=e, fatal=True)
    #finally:
    #    sys.exc_info()
    b_track = BackingTrack()
    print(c)

