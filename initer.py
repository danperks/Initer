import sys
import os
import webbrowser
from urllib.request import urlopen
import subprocess
from distutils.dir_util import copy_tree

def getPath():
    return (os.getenv('LOCALAPPDATA') + r"\Initer")

def checkGit():
    result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE)
    if result.stdout.decode("UTF-8")[:4] == "git ":
        return True
    else:
        return False

def getUsage(full=False):
    if full:
        return "usage: initer [-l] [-h] [-i] [-t] [-c] [-v] name template {github,heroku}"
    else:
        return "usage: initer [--help] name template {github,heroku}"

def printHelp():
    print("\n"*60)
    print(getUsage(full=True))
    print("")
    print("""
            Initalise new projects with a one line command

            positional arguments:
            name               The name for your new project
            template           The template name you want to copy from
            {github,heroku}    The service to initalise a repository and generate a remote for

            optional arguments:
            -h, --help         Show this help message and exit
            -l, --list         Lists the available templates and credentials
            -i, --install      (Re)install Initer without overriding any templates or credentials
            -u, --uninstall    Delete all the files Initer uses
            -t, --temps        Opens the templates folder
            -c, --creds        Opens the credentials.ini file
            -v, --version      Prints the current version

            For full usage instructions, go to https://github.com/danperks/initer
            """)
    
def install():
    print("\n"*60)
    changes = False
    print("INITER - INSTALL/FIX")
    print("This option will install or fix the Initer directories")
    print("")
    path = str(getPath()).strip()
    if not os.path.isdir(path):
        os.mkdir(path)
        print("Base folder created")
        changes = True
    folder = path + r"\templates"
    creds = path  + r"\creds.ini"
    glob = path  + r"\global.bat"
    if not os.path.isdir(folder):
        os.mkdir(folder)
        print("Template folder created")
        changes = True
    if not os.path.isfile(creds):
        with open(creds, "w+") as f:
            f.write("this is the creds file")
        print("Credentials file created")
        changes = True
    if not os.path.isfile(glob):
        with open(glob, "w+") as g:
            g.write(":: This file runs after each init - add your post-init code below\n\n")
        print("Global.bat file created")
        changes = True
    if not os.path.isdir(folder + r"\flask"):
        os.mkdir(folder + r"\flask")
        with open(folder + r"\flask\hello.py", "w") as f:
            text = (urlopen(r"https://raw.githubusercontent.com/miguelgrinberg/flask-examples/master/01-hello-world/hello.py").read().decode('utf-8'))
            f.write(text)
        changes = True
        print("Example template created")
    if changes:
        print("Installation Complete!")
    else:
        print("Initer was already installed, so no changes were made")
    

def openTemps():
    path = str(getPath()).strip()
    path = path + r"\templates"
    
    if os.path.isdir(path):
        webbrowser.open("file:\\" + path)
    else:
        print("initer: error: Initer is not installed correctly. Run 'initer --install' and try again")
    return []

def openDir():
    path = str(getPath()).strip()
    
    if os.path.isdir(path):
        webbrowser.open("file:\\" + path)
    else:
        print("initer: error: Initer is not installed correctly. Run 'initer --install' and try again")
    return []

def openGlobal():
    path = str(getPath()).strip()
    path = path + r"\global.bat"
    
    if os.path.isfile(path):
        webbrowser.open("file:\\" + path)
    else:
        print("initer: error: Initer is not installed correctly. Run 'initer --install' and try again")
    return []

def listOptions():
    path = str(getPath()).strip()
    path = path + r"\templates"
    temps = (next(os.walk(path))[1])
    if len(temps) == 0:
        print("NO TEMPLATES AVAILABLE - Do 'initer -t' to add some")
    else:
        print("AVAILABLE TEMPLATES: ")
        print(", ".join(temps))
    print(" ")
    creds = []
    if len(creds) == 0:
        print("NO CREDENTIALS AVAILABLE  Do 'initer -c' to add some")
    else:
        print("AVAILABLE CREDENTIALS: ")
        print(" ".join(temps))
    

def openCreds():
    path = str(getPath()).strip()
    path = path + r"\creds.ini"
    
    if os.path.isfile(path):
        webbrowser.open("file:\\" + path)
    else:
        print("initer: error: Initer is not installed correctly. Run 'initer --install' and try again")
    return []

def init():
    args = sys.argv[1:]
    if args == []:
        print(getUsage())
        print("initer: error: no arguments were given")
        return []
    elif args[0] == "-i" or args[0] == "--install": install()
    elif args[0] == "-t" or args[0] == "--temps": openTemps()
    elif args[0] == "-c" or args[0] == "--creds": openCreds()
    elif args[0] == "-d" or args[0] == "--dir": openDir()
    elif args[0] == "-g" or args[0] == "--gloabl": openGlobal()
    elif args[0] == "-l" or args[0] == "--list": listOptions()
    elif args[0] == "-h" or args[0] == "--help": printHelp()
    else:
        if len(args) == 1:
            print(getUsage())
            print("initer: error: not enough arguments were given")
            return []
        elif len(args) > 3:
            print(getUsage())
            print("initer: error: too many arguments were given")
            return []
        else:
            return args
    return []
    
args = init()
if args != []:
    print("args", args)
    print("")
    name = args[0]
    template = args[1]
    service = ""
    output = True
    if not os.path.isfile(getPath() + r"\.noout"):
        output = False
    if len(args) > 2:
        if checkGit():
            service = args[2]
        else:
            if output: print("initer: warning: git is not installed, so all git features will be disabled")
    possibTemps = next(os.walk(str(getPath()).strip() + r"\templates"))[1]
    if template in possibTemps:
        cwd = os.getcwd()
        path = cwd + r"\ ".strip() + name
        if os.path.isdir(path):
            print("initer: error: folder '" + name + "' already exists here")
        else:
            os.mkdir(path)
            if output: print("initer: message: folder generated successfully")
            if not os.path.isfile(getPath() + r"\templates\ ".strip() + template + r"\.nogit"):
                result = subprocess.Popen(['git', 'init'], cwd=path, stdout=subprocess.PIPE)
                result = result.communicate()[0].decode("UTF-8")
                if result[:12] == "Initialized ":
                    if output: print("initer: message: git initalised successfully")
                else:
                    print("initer: error: failed to initalise the git repository")
            else:
                if output: print("initer: message: no local git created as per .nogit file")
            copy_tree((getPath() + r"\templates\ ".strip() + template), path)
            if service == "":
                if output: print("initer: message: template '" + template + "' successfully copied")
            else:
                if not os.path.isfile(getPath() + r"\templates\ ".strip() + template + r"\.nogit"):
                    print("initer: error: online git intergration not yet implemented")
                else:
                    if output: print("initer: message: template '" + template + "' successfully copied")
    else:
        print("initer: error: '" + template + "' is not a valid template - do 'initer -t' to create it")