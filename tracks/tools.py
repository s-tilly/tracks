import sys
import os
import shlex
import subprocess

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

