# tracks

This project is used for my personal purpose in order to create backing tracks from wav tracks.

The script read config file and generate backing trakcs.

## Licence & restrictions

The script is written for python3 only.

This is under GPLv3 licence.

## Example

```ini
# Ceci est le fichier de configuration de la génération des backing tracks
# chaque catégorie correspond à un instrument (à part [main]).
#
# [drum] : permet la génération des backings uniquement avec la batterie
# [guitar] & [voice] : permette de généré des backs zeta, sans ces instruments
#
# Tous les instruments peuvent avoir un back (à part [drum]).
#
# Il est possible d'ajouter autant d'instrument que souhaité.
[main]
title=temptation
destination=/home/user/backs/

[intro]
track=temptation_intro.wav
volume=1


[guitar]
track=temptation_guitare.wav
volume=1.5

[voice]
track=temptation_voix_95.wav
volume=1

[drum]
track=temptation_batt_95.wav
volume=1

[bass]
track=temptation_bass_95.wav
volume=1.25
```

Using the script :
```bash
python tracks.py -h
usage: tracks.py [-h] [-b BACK_TYPE] [-d] [-f] [-z] [-a] [-l]
                 backing_track_config

Gab & Syl backing tracks generator

positional arguments:
  backing_track_config  The backing track configuration file

optional arguments:
  -h, --help            show this help message and exit
  -b BACK_TYPE, --back BACK_TYPE
                        Backing track type, precise instrument you DON'T want.
  -d, --drum            Generate drum ONLY backing track
  -f, --full            Generate song with all instruments
  -z, --zeta            Generate song without guitar and voice
  -a, --all             Generate all backing tracks (drum, all types of
                        backing tracks and full one)
  -l, --list            List available instruments and exit
```
