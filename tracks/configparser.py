import os
import configparser

from tracks.tools import *



TITLE = 'title'
DESTINATION="destination"


# Par instrument
VOLUME = 'volume'
TRACK = 'track'

# Ajouté à chaud dans le configParser
MYPATH = "mypath"

MAIN_SECTION = 'main'

# Extension
MP3 = ".mp3"

class TracksConfigParserException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class TracksConfigParser:
    """Parser de fichier de conf pour les backing tracks

    Cette classe permet de remplir une structure de type $params
    depuis un fichier de conf ini. Cette structure est accessible en
    tant que variable de classe

    @param config: object ConfigPaser
    @param main_section: string avec la section a enlevé pour avoir la liste des instruments
    """

    def set(self, config, main_section=MAIN_SECTION):
        self.config = config
        self.main_section = main_section
        self.params = {}
        self.title = ""
        self.destination = ""

    def get_instruments_list(self):
        """Retourne la liste des instruments disponibles dans la configuration

        Pour ça, on enlève self.main_section (cf constructeur).
        """
        sections = self.config.sections()
        sections.remove(self.main_section)
        return sections

    def get_title(self):
        """Retourne le titre du back, s'il est vide on lance une erreur
        """
        if self.title == "":
            raise TracksConfigParserException("Please, run " + blue("ConfigParser.parse_main()") + " before get_title()", fatal=TRUE)
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
        """Parcours de l'entête =self.main_section= du fichier de conf

        On s'attend à trouver title et destination dans =config=
        """
        # On valide qu'on a bien une section main avec un titre, sans
        # ça on peut rien faire.
        if not self.config.has_section(self.main_section):
            raise TracksConfigParserException('config file has no =%s= section' % self.main_section)
        if not self.config.has_option(self.main_section, TITLE):
            raise TracksConfigParserException('config file has no =%s= option in =%s= section' % (TITLE, self.main_section))
        self.title = self.config.get(self.main_section, TITLE)
        if self.title == "":
            raise TracksConfigParserException('=%s= in =%s= section is empty' % (TITLE, self.main_section))
        if not self.config.has_option(self.main_section, DESTINATION):
            raise TracksConfigParserException('config file has no =%s= option in =%s= section' % (DESTINATION, self.main_section))
        self.destination = os.path.abspath(self.config.get(self.main_section, DESTINATION))
        if not os.path.isdir(self.destination):
            raise TracksConfigParserException('the path =%s= is not a valid directory' % self.destination)

    def parse_instruments(self, section):
        """Pour un instrument donné, on parcours les options

        Pour un instrument donnée (=section=), on parcours les options
        dans =config= et on rempli =params=.
        """
        volume = self.config.getfloat(section, VOLUME)
        track = self.config.get(section, TRACK)
        full_path = os.path.join(os.path.dirname(self.config.get(self.main_section, MYPATH)), track)
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
                print_err("Impossible to parse " + blue(i) + " in " + blue(self.config.get(self.main_section, MYPATH)) + "\nInstrument won't be added.", error=e)

    def __str__(self):
        return "<%s> : %s" % (type(self).__name__, self.params)



def set_configparser(config_filename):
    c = TracksConfigParser()
    config = configparser.ConfigParser()
    config.read_file(open(config_filename))
    config.set(MAIN_SECTION, MYPATH, os.path.abspath(config_filename))
    c.set(config)
    c.parse()
    return c
