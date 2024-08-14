# ANNA-AnimalHealthAnalytics
A Python based Computational Server for analyzing Animal Health Data with ML Classifiers.

School of Veterinary Medicine, University of California Davis

Authors: Chun Yin (Kelvin) Kong, Picasso Vasquez, Chris Brandt, Krystle Reagan, Stefan M. Keller

## Table of Content
* [Introduction](#introduction)
* [Software Requirement](#software-requirement)
* [Installation](#installation)
    * [Python](#python)
    * [miniconda](#miniconda)
    * [Apache HTTP Server](#apache-http-server)
    * [MySQL Community Server](#mysql-community-server)
    * [Python Packages](#python-packages)
* [Folder Structure](#folder-structure)



## Introduction

## Software Requirement

To impelemnt ANNA, we would need the following software and packages to start with. In the following instructions, we are demostrated based on Windows machines.

- Python Version 3.7 and 3.9
- miniconda 
- Apache HTTP Server
- MySQL Community Server (GPL) Version 8.4.2 LTS
- MySQL Workbench (Optional)
- MATLAB Runtime R2019b (v9.7)
- List of Python Packages specified in the requirement text file.

### Sofrware Description

Python 3.9 is the Python version used in ANNA Main Server and Leptospirosis Flask Server.

Python 3.7 is the Python verison used in TommyPy Flask Server. Our approach is to use miniconda to manage the virtual environment for installing legacy packages. 

## Installation
### Python

Download and install Python 3.7 and Python 3.9 from official site.

> The installation should be done with administrative privileges.

### miniconda

Download and install miniconda from official site.

> The installation should be done with administrative privileges.

### Apache HTTP Server
1. Download Apache HTTP Server source codes.
2. Extract the source codes to each folder starting with `Apache24_`.
3. Edit each Apache's configuration files:
  - The following configurations need to be changed:
  ```
  Define SRVROOT Path
  Listen
  ServerAdmin (Optional)
  ```
  - The following configuration need to be added:
  ```
  LoadFile `Your Python .dll file path`
  LoadModule wsgi_module `Your Python mod_wsgi.pyd file path`
  WSGIPythonHome `Your Python Virtual Environment folder path`
  WSGIApplicationGroup %{GLOBAL}
  ```

4. Install all Apache servers as Windows NT services.
    > Note: For each apache server, it must have different service names, for ANNA Main server, it can be `Apache2.4`, while Leptospirosis Server can be named as `Apache24_Lepto` and TommyPy Server can be named as `Apache24_Tommy`.


### MySQL Community Server
1. Download and install MySQL Community Server (GPL) Version 8.4.2 LTS
2. Download and install MySQL Workbench (Optional)
    > Note: MySQL Workbench is a graphical interface of managing MySQL relational database.
3. Set up at least two SQL users other than `root` user with different user rights.

> Note: We use default port number for MySQL. 

### MATLAB Runtime
1. Download and install MATLAB Runtime R2019b
2. In Windows System Environment Variables, set MATLAB Cache path:
    - Variable: `MCR_CACHE_ROOT`
    - Value: `C:\MATLAB Cache`

### Python Packages

There are two Python requirement lists. 

- `requirement_anna_main.txt` is used in ANNA Main Server and Leptospirosis Flask Server.
- `requirement_anna_tommypy.txt` is used in TommyPy Flask Python environment. Run package installation to the `miniconda` environment.
    - TommyPy requires separate installation: See the original GitHub repo: [Link](https://github.com/krystlereagan/Tommy)


## Folder Structure
```
- Apache24
    - Other Apache Source Code Folders
    - anna_main
        - apps
            - scripts
            - wsgi_scripts
        - assets

- Apache_Lepto
    - Other Apache Source Code Folders
    - anna_lepto
        - apps
            - scripts
            - wsgi_scripts
        - assets
- Apache24_Lepto
    - Other Apache Source Code Folders
    - anna_tommypy
        - apps
            - scripts
            - wsgi_scripts
        - assets
.gitignore
README.md

```