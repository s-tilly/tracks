from tracks.tools import *

# Type de back
DRUM = "drum" # + section associée
FULL = "full"
ZETA = "zeta"
ZETA_INSTRUMENTS = ("guitar", "voice")



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


def drum(c, b_track):
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


def back(c, b_track, instrument):
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

def zeta(c, b_track):
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

def full(c, b_track):
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
