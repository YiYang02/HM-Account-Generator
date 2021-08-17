# H&M New Account Generator

Script that automatically creates a new H&M account for user to use. To use, either download the script file or go to https://hm-account-generator.herokuapp.com/. 

## Description

Selenium script that goes to the H&M website and registers a brand new account for you. Utilizes the GuerillaMail and PasswordRandom APIs to retrieve unique emails and passwords
respectively. Then, uploads the email and password onto a Flask frontend which users can click to access in the terminal after running the script. 

## Getting Started

### Dependencies

Must have Chrome Driver installed.
Dependencies can be found in the requirements.txt file.

### Installing

Clone the project and place it in a directory of your choosing.
Must comment out line 39 and uncomment line 40. For line 40, pass in the file path of the Chrome Driver 
into the argument "executable_path".

### Executing program

```
python hmdiscountbot.py
```
Click on the proxy that appears in the terminal to launch Flask app.

## Authors

Yi Yang
Bowdoin College
17 Aug 2021

## Version History

* 0.1
    * Initial Release
