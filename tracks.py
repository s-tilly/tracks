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


import configparser
import sys
import os
import argparse
import traceback
import shlex
import subprocess
from pprint import pprint

MAIN_SECTION = 'main'
DESTINATION="destination"
TITLE = 'title'
# Ajouté à chaud dans le configParser
MYPATH = "mypath"

# Par instrument
VOLUME = 'volume'
TRACK = 'track'

# Type de back
DRUM = "drum" # + section associée
FULL = "full"
ZETA = "zeta"
ZETA_INSTRUMENTS = ("guitar", "voice")

# Extension
MP3 = ".mp3"

colors = { 'HEADER': '\033[95m',
           'OKBLUE': '\033[94m',
           'OKGREEN': '\033[92m',
           'WARNING': '\033[93m',
           'FAIL': '\033[91m',
           'ENDC': '\033[0m',
           'BOLD': '\033[1m',
           'UNDERLINE': '\033[4m' }

def blue(msg):
    """Juste pour mettre en bleu la string msg
    """
    return colors['OKBLUE'] + msg + colors['ENDC']

def yellow(msg):
    """Juste pour mettre en jaune la string msg
    """
    return colors['WARNING'] + msg + colors['ENDC']

def print_err(msg, error=None, fatal=False):
    """Affiche un message d'erreur

    Le pendant de print_ok. On met un failed en rouge. Si une erreur
    est passé en paramètre, on affiche son message. Si fatal=True, on
    fait un sys.exit(1) à la fin.
    """
    print("[" + colors['FAIL'] + "FAILED" + colors['ENDC'] + "]")
    print(colors['FAIL'] + "<<<<<<<<<<<<<< ERROR <<<<<<<<<<<<<" + colors['ENDC'])
    print(msg)
    if error is not None:
        print(colors['WARNING'] + "%s" % error + colors['ENDC'])
    if fatal:
        print(colors['FAIL'] + "This Error is fatal !")
    print(colors['FAIL'] + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + colors['ENDC'])
    sys.stdout.flush()
    if fatal:
        sys.exit(1)

def print_msg(msg):
    """Affiche un message typique du script

    Une étoile en bleu, le message sans saut de ligne à la
    fin. Typiquement, on appel print_ok() après.
    """
    print(colors['OKBLUE'] + '* ' + colors['ENDC'] + msg, end="")
    #with open('/tmp/log', 'a') as f:
    #    f.write(msg + '\n')
    #    r, o, e = run('ls -ld /usr/local/ansible')
    #    f.write(o + '\n')
    sys.stdout.flush()

def print_ok():
    """Affiche un OK en vert entre crochet.
    """
    print('[' + colors['OKGREEN'] + "OK" + colors['ENDC'] + "]")
    sys.stdout.flush()

def run(command, debug=False):
    """Run shell command

    On retourne le code retour de la fonction, stdout et stderr dans
    une liste (et dans cet ordre)
    """
    args = shlex.split(command)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if debug:
        print()
        print('command: ', command)
        print('Return code :', p.poll())
        print('stdout:\n', stdout)
        print('stderr:\n', stderr)
        sys.stdout.flush()
    return p.poll(), stdout, stderr


class ConfigParserException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class ConfigParser:
    """Parser de fichier de conf pour les backing tracks

    Cette classe permet de remplir une structure de type $params
    depuis un fichier de conf ini. Cette structure est accessible en
    tant que variable de classe
    """

    def set(self, config):
        self.config = config
        self.params = {}
        self.title = ""
        self.destination = ""

    def get_instruments_list(self):
        """Retourne la liste des instruments disponibles dans la configuration

        Pour ça, on enlève MAIN_SECTION.
        """
        sections = self.config.sections()
        sections.remove(MAIN_SECTION)
        return sections

    def get_title(self):
        """Retourne le titre du back, s'il est vide on lance une erreur
        """
        if self.title == "":
            raise ConfigParserException("Please, run " + blue("ConfigParser.parse_main()") + " before get_title()", fatal=TRUE)
        return self.title

    def get_bt_filepath(self, bt_type, extension=MP3):
        """Retourne le filepath du backing track à générer.

        Attention, l'extension détermine le format qui sera généré
        """
        filename = self.get_title() + "-" + bt_type + extension
        full_dir = os.path.join(self.destination, self.get_title())
        if not os.path.isdir(full_dir):
            os.mkdir(full_dir)
        return os.path.join(full_dir, filename)

    def parse_main(self):
        """Parcours de l'entête =MAIN_SECTION= du fichier de conf

        On s'attend à trouver title et destination dans =config=
        """
        # On valide qu'on a bien une section main avec un titre, sans
        # ça on peut rien faire.
        if not self.config.has_section(MAIN_SECTION):
            raise ConfigParserException('config file has no =%s= section' % MAIN_SECTION)
        if not self.config.has_option(MAIN_SECTION, TITLE):
            raise ConfigParserException('config file has no =%s= option in =%s= section' % (TITLE, MAIN_SECTION))
        self.title = self.config.get(MAIN_SECTION, TITLE)
        if self.title == "":
            raise ConfigParserException('=%s= in =%s= section is empty' % (TITLE, MAIN_SECTION))
        if not self.config.has_option(MAIN_SECTION, DESTINATION):
            raise ConfigParserException('config file has no =%s= option in =%s= section' % (DESTINATION, MAIN_SECTION))
        self.destination = os.path.abspath(self.config.get(MAIN_SECTION, DESTINATION))
        if not os.path.isdir(self.destination):
            raise ConfigParserException('the path =%s= is not a valid directory' % self.destination)

    def parse_instruments(self, section):
        """Pour un instrument donné, on parcours les options

        Pour un instrument donnée (=section=), on parcours les options
        dans =config= et on rempli =params=.
        """
        volume = self.config.getfloat(section, VOLUME)
        track = self.config.get(section, TRACK)
        full_path = os.path.join(os.path.dirname(config.get(MAIN_SECTION, MYPATH)), track)
        if not os.path.isfile(full_path):
            raise OSError(TRACK + ' does not exist in filesystem')
        self.params[section] = {VOLUME:volume, TRACK: full_path}

    def parse(self):
        """Parcours le fichier de conf et renseigne les attributs d'objet

        En particulier, on charge la section main, on parcours les
        instruments et on rempli la varibles params.
        """
        self.parse_main()
        for i in self.get_instruments_list():
            try:
                self.parse_instruments(i)
            except Exception as e:
                print_err("Impossible to parse " + blue(i) + " in " + blue(config.get(MAIN_SECTION, MYPATH)) + "\nInstrument won't be added.", error=e)

class BackingTrack:
    """Classe pour la génération du backing track
    """
    def backing_track_cmd(self, tracks_dict, back_filepath):
        """Génère la commande pour faire les backings tracs via l'outil sox

        Pour ça, on a besoin de tracs_dict (équivalent du
        ConfigParser.params et le chemin du back de destination (qu'on
        récupère avec ConfigParser.get_bt_filepath()).

        A la fin on retourne la commande sox qu'on peut lancer dans un
        shell.
        """
        command = "sox "
        # Si on fait un backing track d'une piste, on n'ajoute pas le
        # -m dans la ligne de commande.
        if len(tracks_dict.keys()) > 1:
            command += "-m "
        for track in tracks_dict.keys():
            volume = tracks_dict[track]['volume']
            filename = tracks_dict[track]['track']
            command += "-v %s '%s' " % (volume, filename)
        command += "-c 1 '%s'" % back_filepath
        return command

    def backing_track_only_one_instrument(self, track, back_filepath):
        """Track pour une piste (typiquement drum)

        Ici, le Track qu'on balance est juste un dico avec {'track': 'path/to/track.wav', volume:1},
        mais on ne se sert que du chemin de la piste
        """
        # Cette fonction est en trop. On pourrait construire un dict qui à la forme ci-dessous et appeler directement le backing_track_cmd
        #{'drum': {'track': '/home/stilly/ownCloud/zic-gab-zen/sons/pistes/ain t no ' 'love in the heart of the city/aint_no_love_batt_90.wav',
        # 'volume': 1.2}}
        return "sox '%s' '%s'" % (track['track'], back_filepath)


def main_drum(c, b_track):
    """Un backing track avec la piste drum uniquement
    """
    print_msg("Create " + blue(DRUM) + " backing track: ")
    if not DRUM in c.get_instruments_list():
        print_err("Can't find " + blue(DRUM) + " instrument in config file, skip this one")
        return
    try:
        # Le nom va être [titre]-drum_only.mp3
        bt_filename = c.get_bt_filepath(DRUM + "_only")
    except Exception as e:
        print_err("Error get backing track filename " + blue(bt_filename), error=e, fatal=True)
    # cf commentaire backing_track_only_one_instrument
    p, stdout, stderr = run(b_track.backing_track_only_one_instrument(c.params[DRUM], bt_filename))
    if p != 0:
        print_err("Problem when generating backing track :\n" + blue(stderr.decode("utf-8")))
    else:
        print_ok()


def main_back(c, b_track, instrument):
    """Un backing track moins l'instrument passé en paramètre
    """
    print_msg("Create " + blue(instrument) + " backing track: ")
    bt_filename = ""
    if not instrument in c.get_instruments_list():
        print_err("Can't find "+ blue(instrument) + " instrument in config file !", fatal=True)
        return
    try:
        bt_filename = c.get_bt_filepath(instrument)
    except Exception as e:
        print_err("Error get backing track filename " + blue(bt_filename), error=e, fatal=True)
    wanted_instruments = c.params.copy()
    del wanted_instruments[instrument]
    p, stdout, stderr = run(b_track.backing_track_cmd(wanted_instruments, bt_filename))
    if p != 0:
        print_err("Problem when generating backing track :\n" + blue(stderr.decode("utf-8")))
    else:
        print_ok()

def main_zeta(c, b_track):
    """Un backing track moins voice et guitar

    S'il en manque un des deux, ben ça fait moins voice ou moins
    guitar. Les instruments à enlever sont noté dans ZETA_INSTRUMENTS
    """
    print_msg("Create " + blue(ZETA) + " backing track: ")
    bt_filename = ""
    try:
        bt_filename = c.get_bt_filepath(ZETA)
    except Exception as e:
        print_err("Error get backing track filename " + blue(bt_filename), error=e, fatal=True)
    wanted_instruments = c.params.copy()
    for instrument in ZETA_INSTRUMENTS:
        try:
            del wanted_instruments[instrument]
        except Exception as e:
            print("no " + yellow(instrument) + " found ", end="")
    p, stdout, stderr = run(b_track.backing_track_cmd(wanted_instruments, bt_filename))
    if p != 0:
        print_err("Problem when generating backing track :\n" + blue(stderr.decode("utf-8")))
    else:
        print_ok()

def main_full(c, b_track):
    """Un backing track avec toutes les pistes
    """
    print_msg("Create " + blue(FULL) + " backing track: ")
    bt_filename = ""
    try:
        bt_filename = c.get_bt_filepath(FULL)
    except Exception as e:
        print_err("Error get backing track filename " + blue(bt_filename), error=e, fatal=True)
    p, stdout, stderr = run(b_track.backing_track_cmd(c.params, bt_filename))
    if p != 0:
        print_err("Problem when generating backing track :\n" + blue(stderr.decode("utf-8")))
    else:
        print_ok()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gab & Syl backing tracks generator")
    parser.add_argument('backing_track_config', help="The backing track configuration file")
    parser.add_argument('-b', '--back', required=False, default=None, action='store',
                        dest='back_type', help="Backing track type, precise instrument you DON'T want.")
    parser.add_argument('-d', '--drum', required=False, default=None, action='store_true',
                        dest='drum', help="Generate drum ONLY backing track")

    parser.add_argument('-f', '--full', required=False, default=None, action='store_true',
                        dest='full', help="Generate song with all instruments")
    parser.add_argument('-z', '--zeta', required=False, default=None, action='store_true',
                        dest='zeta', help="Generate song without guitar and voice")
    parser.add_argument('-a', '--all', required=False, default=None, action='store_true',
                        dest='all', help="Generate all backing tracks (drum, all types of backing tracks and full one)")
    parser.add_argument('-l', '--list', required=False, default=None, action='store_true',
                        dest='list', help="List available instruments and exit")
    args = parser.parse_args()

    c = ConfigParser()
    config_filename = args.backing_track_config
    if not args.list: print_msg("Parsing config file " + blue(config_filename) + ": ")
    try:
        config = configparser.ConfigParser()
        config.read_file(open(config_filename))
        config.set(MAIN_SECTION, MYPATH, os.path.abspath(config_filename))
        c.set(config)
        c.parse()
    except ConfigParserException as e:
        print_err("Impossible to parse " + blue("main config file part"), error=e, fatal=True)
    except Exception as e:
        print_err("Error when loading " + blue(config_filename), error=e, fatal=True)
    finally:
        sys.exc_info()
    b_track = BackingTrack()
    if not args.list: print_ok()

    if args.list:
        avalaibles = c.get_instruments_list()
        for a in avalaibles:
            print(a)
        sys.exit(0)
    if args.all:
        avalaibles = c.get_instruments_list()
        # On cherche à enlever la batterie
        try:
            del avalaibles[avalaibles.index(DRUM)]
            # Si on arrive ici, c'est qu'il y a une piste drum, donc un back à faire
            main_drum(c, b_track)
        except Exception as e:
            pass
        for instrument in avalaibles:
            main_back(c, b_track, instrument)
        main_full(c, b_track)
        main_zeta(c, b_track)
        sys.exit(0)
    if args.full:
        main_full(c, b_track)
    if args.zeta:
        main_zeta(c, b_track)
    if args.drum:
        main_drum(c, b_track)
    if args.back_type:
        main_back(c, b_track, instrument=args.back_type)
