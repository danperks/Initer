# Initer - Your favourite project initaliser

Initer is a super simple, but feature rich script you can run to setup a new GitHub or Heroku remote (if you want more, make an issue for it).

## Instalation

To install the program for the first time:

- Download the latest initer.exe from [releases](https://github.com/danperks/initer/releases)
- Save it somewhere you won't need to delete it or move it later
- Add the folder for Initer into your Path (learn to do that [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/))
- Run `initer -v` and check it outputs the version you installed
- Run `initer -i` to install the required files and folders

## Usage

### Create a new project

To initalse a new project, use:
> initer *name* *template* {*github*, *heroku*}

The following arguments can be passed:

- name - The name of your project
- template - The template you want your project to start from
- service (optional) - The service, either GitHub or Heroku, that you want to use

### Other functions

Instead of the above arguments, you can do the following:

- -h, --help     Show this help message and exit
- -l, --list      Lists the available templates and credentials
- -i, --install    (Re)install Initer without overriding any templates or credentials
- -u, --uninstall       Delete all the files Initer uses
- -t, --temps     Opens the templates folder
- -d, --dir       Opens the Initer directory
- -c, --creds    Opens the credentials.ini file
- -g, --global    Opens the global .bat script
- -b, --version   Outputs the latest version to the terminal

### Post-init Scripting

Once an initalisation is complete, you have two options for running your own code/scripts to extend the power of Initer.

- Global Scripting
    - These scripts run after every initalisation
    - If it exists, Initer will run 'global.bat' from its base directory
    - The 'global.bat' script can be opened with `initer -g`
    - The script is run from the directory of the new folder, so can be used for additional project based processing

- Template-based Scripting
    - These scripts run after the initalisation of a certain template
    - Add a batch file named 'after.bat' in your template folder and it will be run once the initalisation is complete
    - The script is run from the directory of the new folder, so can be used for additional project based processing

This is useful for opening your your usual text editor. For example, add `code` to your script to open VS Code or this could be used for running Node.js commands for a web server.

### Reduced Output

If you prefer a cleaner console, put a empty file called '.noout' in the base directory of Initer (%localappdata%/Initer) and no info messages will be displayed. Program-breaking errors will still be displayed.

## Frequent Issues

### 'initer' is not recognized as an internal or external command, operable program or batch file. 

This error suggests the initer.exe file is not in the path
Read on how to add initer.exe to the path [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/). If this does not fix it, create an issue for help with diagnosis.

### More common errors to be added soon