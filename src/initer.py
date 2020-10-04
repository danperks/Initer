import sys
import os
import webbrowser
from urllib.request import urlopen
import subprocess
import time
import shutil
import zipfile
from distutils.dir_util import copy_tree

ver = "0.2"

def checkUpdate():
    if connected():
        latest = urlopen("https://raw.githubusercontent.com/danperks/Initer/master/version").read().decode()
        if latest != ver:
            print("initer: message: initer has a newer version, update to " + latest + " at https://github.com/danperks/Initer")
    else:
        print("initer: warning: initer could not check for updates, created a file named .noupdate in the base directory to stop update checks")

def connected():
    try:
        urlopen('https://raw.githubusercontent.com/danperks/Initer/master/version', timeout=1)
        return True
    except:
        return False

def printVersion():
    print(ver)

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
        return "usage: initer [-l] [-x] [-h] [-v] name template {github,heroku}"
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
            - -l, --list      Lists the available templates and credentials
            - -x, --command     Runs a specified command, see commands section
            - -h, --help     Show this help message and exit
            - -v, --version   Outputs the latest version to the terminal
            
            commands - for use with -x:
            - `open {base, temp[lates], global, cred[entials]}` - Opens the relevant folder/file, defaults to base
            - `import [.init file location]` - Import a template from an .init file
            - `export [name] {path}` - Export a template in a .init file, defaults to deskop if no path is provided
            - `install` - Installs the necessary folders and files for Initer to work
            - `uninstall` - Removes all of Initer's program files, does not delete Initer.exe

            For full usage instructions, go to https://github.com/danperks/initer
            """)
    
def install():
    print("initer: message: initer is about to be (re)installed to: " + getPath())
    sure = input("initer: warning: are you sure you want to do this (y/n): ")
    if sure.lower() == "y":
        path = str(getPath()).strip()
        if not os.path.isdir(path):
            os.mkdir(path)
            changes = True
        folder = path + r"\templates"
        creds = path  + r"\creds.ini"
        glob = path  + r"\global.bat"
        if not os.path.isdir(folder):
            os.mkdir(folder)
            changes = True
        if not os.path.isfile(creds):
            with open(creds, "w+") as f:
                f.write("this is the creds file")
            changes = True
        if not os.path.isfile(glob):
            with open(glob, "w+") as g:
                g.write(":: This file runs after each init - add your post-init code below\n\n")
            changes = True
        if not os.path.isdir(folder + r"\flask"):
            os.mkdir(folder + r"\flask")
            with open(folder + r"\flask\hello.py", "w") as f:
                if connected:
                    text = (urlopen(r"https://raw.githubusercontent.com/miguelgrinberg/flask-examples/master/01-hello-world/hello.py").read().decode('utf-8'))
                else:
                    text = 'print("Hello World!")'
                f.write(text)
            changes = True
        if changes:
            input("initer: message: initer was (re)installed successfully")
        else:
            input("initer: message: initer was already installed, no changes were made")
    else:
        input("initer: message: initer was not installed")

def upgrade():
    pass # get update script online and run

def uninstall():
    print("initer: warning: initer is about to be uninstalled, this will delete all your projects and credentails")
    sure = input("initer: warning: are you sure you want to do this (y/n): ")
    if sure.lower() == "y":
        path = str(getPath()).strip()
        if os.path.isdir(path):
            shutil.rmtree(path)
            print("initer: message: initer is now uninstalled, delete initer.exe to complete remove Initer")
        else:
            print("initer: message: initer was not yet installed, delete initer.exe to complete remove Initer")
    else:
        input("initer: message: initer was not uninstalled")


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

def runCommand(args):
    if args[1] == "exit":
        return []
    elif args[1] == "import":
        archive = args[2]
        if os.path.isfile(archive):
            if archive[-5:] == ".init":
                name = archive.split(r"\ ".strip())[-1].split(".")[0]
                if name in next(os.walk(str(getPath()).strip() + r"\templates"))[1]:
                    print("initer: error: template " + name + " already exists")
                else:
                    with zipfile.ZipFile(archive, 'r') as zip_ref:
                        outpath = getPath() + r"\templates\ " .strip() + str(name) + r"\ ".strip()
                        zip_ref.extractall(outpath)
                    print("initer: message: template " + name + " successfully imported")
            else:
                print("initer: error: file to import is not a .init archive")
        else:
            print("initer: error: file at path '" + archive + "' does not exsist")
    elif args[1] == "export":
        name = args[2]
        path = (getPath() + r"\templates\ ".strip() + name)
        print(path)
        if os.path.isdir(path):
            print()
            zipf = zipfile.ZipFile((os.path.join(os.environ["HOMEPATH"], "Desktop") + r"\ ".strip() + name + '.init'), 'w', zipfile.ZIP_DEFLATED)
            for x in os.walk(path):
                for file in x[2]:
                    zipf.write(os.path.join(x[0], file), arcname=file)
            zipf.close() 
        else:
            print("initer: error: '" + name + "' is not a valid template")
    elif args[1] == "install":
        install()
    elif args[1] == "upgrade":
        upgrade()
    elif args[1] == "uninstall":
        uninstall()
    elif args[1] == "open":
        if len(args) < 2:
            openDir()
        elif args[2] == "base":
            openDir()
        elif args[2] == "temp" or args[2] == "templates" :
            openTemps()
        elif args[2] == "global":
            openGlobal()
        elif args[2] == "cred" or args[2] == "credentials":
            openCreds()
        else:
            print("initer: error: unknown file/folder, check your syntax and try again")
    else:
        print("initer: error: unknown command, check your syntax and try again")
    

def init():
    args = sys.argv[1:]
    if args == []:
        print(getUsage())
        print("initer: error: no arguments were given")
        return []
    elif args[0] == "-v" or args[0] == "--version": printVersion()
    elif args[0] == "-l" or args[0] == "--list": listOptions()
    elif args[0] == "-h" or args[0] == "--help": printHelp()
    elif args[0] == "-x" or args[0] == "--command": runCommand(args)
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
    name = args[0].replace("/","\\")
    template = args[1]
    service = ""
    output = True
    if os.path.isfile(getPath() + r"\.noout"):
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
            os.makedirs(path)
            if output: print("initer: message: folder generated successfully")
            if not os.path.isfile(getPath() + r"\templates\ ".strip() + template + r"\.nogit"):
                result = subprocess.Popen(['git', 'init'], cwd=path, stdout=subprocess.PIPE)
                result = result.communicate()[0].decode("UTF-8")
                if result[:12] == "Initialized ":
                    if output: print("initer: message: git initalised successfully")
                else:
                    print("initer: error: failed to initalise the git repository - git will be ignored")
                    service == ""
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
            if not os.path.isfile(getPath() + r"\templates\ ".strip() + template + r"\.noglobal"):
                command = getPath() + r'\global.bat"' 
                dir = os.getcwd() + r"\ ".strip() + name
                os.chdir(dir)
                os.system(command)
            else:
                if output: print("initer: message: global.bat creaignoredted as per .noglobal file")
            if os.path.isfile(getPath() + r"\templates\ ".strip() + template + r"\init.bat"):
                    os.system(getPath() + r"\templates\ ".strip() + template + r"\init.bat")
    else:
        print("initer: error: '" + template + "' is not a valid template - do 'initer -t' to create it")
        
if not os.path.isfile(getPath() + r"\.noglobal"):
    checkUpdate()
        
        
# todo:
# - add github / heroku integration