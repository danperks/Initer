@echo off
where initer >nul 2> nul
IF %ERRORLEVEL% NEQ 0 (
        ECHO Initer needs to be manually installed first 
        ECHO Run 'initer.exe -x open base' and copy initer.exe there
        ECHO Then add that folder to your Path and rerun this script 
        ) ELSE (
        initer -v > tmpFile 
        set /p ver= < tmpFile 
        del tmpFile
        ECHO Initer version %ver% is successfully installed
        Powershell -Command "wget https://raw.githubusercontent.com/danperks/Initer/master/version -OutFile latestver.txt"
        set /p latest=<latestver.txt
        del latestver.txt
        ECHO Initer latest version is %latest%
        if "%ver%" == "%latest%" (
                echo You have the latest version already
        ) else (
                echo You do not have the latest version
                SET /P AREYOUSURE=Do you want to update now [y/n]: 
                IF /I "%AREYOUSURE%" NEQ "Y" ( 
                        echo Starting Update...
                        Powershell -Command "wget https://raw.githubusercontent.com/danperks/Initer/master/version -OutFile latestver.txt"
                        echo Update Complete!
                ) else (
                        echo Not updating.
                        echo You can manually update at https://github.com/danperks/Initer
                        )
                )
)