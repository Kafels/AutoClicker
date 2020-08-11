setlocal
cd /d %~dp0

python -m pip install pywin32 
python -m pip install win32\pyHook-1.5.1-cp36-cp36m-win32.whl
python -m pip install PyUserInput
python main.py
