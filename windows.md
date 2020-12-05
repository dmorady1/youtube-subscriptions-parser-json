# Installation under Windows

1.  Download and Install Python
    First download & install python <https://www.python.org/downloads/> you can choose the latest or download and install the version 3.60 (i tested it with 3.6, but newer versions should not be a problem)
    
    here the version i downloaded: <https://www.python.org/downloads/release/python-360/>
    
    I downloaded: `Windows x86 executable installer`
    
    Make sure to install with pip (the recommended version).

2.  Make sure that you have google chrome installed
    <https://www.google.com/chrome/index.html>
    
    (you can deinstall it after you have your json file :) )

3.  Download/ clone the files from this repository into a directory

4.  Go into the folder/directory  where you cloned/download the files


5.  Download the chromedriver from
    https://chromedriver.chromium.org/

    make sure that the chrome version you have installed is matching with the chromedriver you download and install

6.  Start a powershell in this folder/directory by holding `Shift` and right click in the folder, there should be something to start/run `powershell`
    
    first try to check if python is correctly installed:
    type:

    `python --version`

    it should print your python version

7.  Create an virtual environment (similar to the install script but doesn&rsquo;t work on windows)
    
    `python -m venv env`

8.  Then activate the virtual environment
    
    `env/Scripts/activate.bat`

9.  Install the needed packages
    
    `python -m pip install -r requirements.txt`

10.  start the program with

    `python .\youtube-json-parse.py`

