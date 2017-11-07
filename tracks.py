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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from tracks.tools import *
from tracks.configparser import TracksConfigParser, TracksConfigParserException, set_configparser
from tracks.backingtrack import BackingTrack, drum, back, zeta, full


#if __name__ == "__main__":
#
#    config_filename = "./back.ini"
#    #try:
#    c = set_configparser(config_filename)
#    #except TracksConfigParserException as e:
#    #    print_err("Impossible to parse " + blue("main config file part"), error=e, fatal=True)
#    #except Exception as e:
#    #    print_err("Error when loading " + blue(config_filename), error=e, fatal=True)
#    #finally:
#    #    sys.exc_info()
#    b_track = BackingTrack()



class TracksWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Backing Tracks")
        self.set_border_width(10)

        grid = TracksGrid({'intro': {'volume': 1.0, 'track': '/home/stilly/Softs/tracks/wavtracks/intro.wav'}, 'guitar': {'volume': 1.5, 'track': '/home/stilly/Softs/tracks/wavtracks/guitare.wav'}, 'voice': {'volume': 1.0, 'track': '/home/stilly/Softs/tracks/wavtracks/voix.wav'}, 'drum': {'volume': 1.0, 'track': '/home/stilly/Softs/tracks/wavtracks/batt.wav'}, 'bass': {'volume': 1.25, 'track': '/home/stilly/Softs/tracks/wavtracks/bass.wav'}})
        self.add(grid)

class TracksGrid(Gtk.Grid):
    def __init__(self, tracks):
        Gtk.Grid.__init__(self)
        line = 0
        for k in tracks:
            instrument = Gtk.Label()
            instrument.set_text(k)
            self.attach(instrument, 0, line, 1, 1)
            current_vol = Gtk.Label()
            current_vol.set_text("current: %s" % tracks[k]['volume'])
            self.attach(current_vol, 1, line, 1, 1)
            next_vol = Gtk.Label()
            next_vol.set_text("Next volume will be a slider")
            self.attach(next_vol, 2, line, 1, 1)
            path = Gtk.Label()
            path.set_text(tracks[k]['track'])
            self.attach(path, 3, line, 1, 1)
            line += 1

win = TracksWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
