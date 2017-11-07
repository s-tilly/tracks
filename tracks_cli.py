import sys
import argparse

from tracks.tools import *
from tracks.configparser import TracksConfigParser, TracksConfigParserException, set_configparser
from tracks.backingtrack import BackingTrack, drum, back, zeta, full, DRUM

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

    config_filename = args.backing_track_config
    if not args.list: print_msg("Parsing config file " + blue(config_filename) + ": ")
    try:
        c = set_configparser(config_filename)
    except TracksConfigParserException as e:
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
            drum(c, b_track)
        except Exception as e:
            pass
        for instrument in avalaibles:
            back(c, b_track, instrument)
        full(c, b_track)
        zeta(c, b_track)
        sys.exit(0)
    if args.full:
        full(c, b_track)
    if args.zeta:
        zeta(c, b_track)
    if args.drum:
        drum(c, b_track)
    if args.back_type:
        back(c, b_track, instrument=args.back_type)
