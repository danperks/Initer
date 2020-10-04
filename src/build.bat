pyminifier -o initer-mini.py src\initer.py
pyinstaller --onefile initer-mini.py
del initer-mini.py
del /s /q build\
rmdir /s /q build\
del initer-mini.spec
set /p Build=<version
mkdir release
copy dist\initer-mini.exe release\initer-%Build%.exe
copy dist\initer-mini.exe release\initer.exe
del /s /q dist\
rmdir /s /q dist\
cls
@echo off
echo.
echo.
echo Done - output to release/initer-%Build%.exe