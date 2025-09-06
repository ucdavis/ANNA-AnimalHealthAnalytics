# ANNA - AI Animal Health Analytics with Electronic Health Record Data
A Python based Computational Server for analyzing Animal Electronic Health Record Data with machine learning (ML) Classifiers.

School of Veterinary Medicine, University of California Davis

Authors: Chun Yin (Kelvin) Kong, Picasso Vasquez, Makan Farhoodi, Chris Brandt, Titus C. Brown, Krystle L. Reagan, Allison Zwingenberger, Stefan M. Keller

License: GNU Affero General Public License

Last Update: Sept 6 2025

## Table of Content
* [Introduction](#introduction)
* [Publications](#publications)
* [Software Requirement](#software-requirement)
* [Installation](#installation)
    * [Python](#python)
    * [miniconda](#miniconda)
    * [Apache HTTP Server](#apache-http-server)
    * [MySQL Community Server](#mysql-community-server)
    * [Python Packages](#python-packages)
* [Folder Structure](#folder-structure)
* [ML Classifiers](#ml-classifiers)
* [License Notice](#license-notice)

## Introduction

This GitHub repository contains the required source codes to run ANNA.

## Publications

A technical paper discussing ANNA computational infrastructure is available on arXiv preprint server.
- Title: **Enhancing AI Accessibility in Veterinary Medicine: Linking Classifiers and Electronic Health Records**
- DOI: https://doi.org/10.48550/arXiv.2410.14625

## Software Requirement

To impelemnt ANNA, we would need the following software and packages to start with. Our implementation is based on machines running Windows Server Operating System. The software/package/dependencies would be different if the host machine runs with different operating systems.

- Python Version 3.7 and 3.9
- miniconda 
- Apache HTTP Server
- MySQL Community Server (GPL) Version 8.4.2 LTS
- MySQL Workbench (Optional)
      - MySQL Workbench is the GUI of the MySQL Community Server Management System
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

## ML Classifiers

### Leptospirosis Classifier

Reagan KL, Deng S, Sheng J, Sebastian J, Wang Z, Huebner SN, et al. Use of machine-learning algorithms to aid in the early detection of leptospirosis in dogs. J Vet Diagn Invest. 2022;34:612–21. https://doi.org/10.1177/10406387221096781.

[Link to Original GitHub Repo](https://github.com/sf-deng/lepto-classifier)

[Link to Publication](https://doi.org/10.1177%2F10406387221096781)


### Addisons Classifier (TommyPy)

Reagan KL, Reagan BA, Gilor C. Machine learning algorithm as a diagnostic tool for hypoadrenocorticism in dogs. Domest Anim Endocrinol. 2020;72:106396. https://doi.org/10.1016/j.domaniend.2019.106396.

[Link to Original GitHub Repo](https://github.com/krystlereagan/Tommy)

[Link to Publication](https://www.sciencedirect.com/science/article/abs/pii/S0739724019300748?via%3Dihub)

### Portosystemic Shunt Classifier

Farhoodimoghadam M, Reagan KL, Zwingenberger AL. Diagnosis and classification of portosystemic shunts: a machine learning retrospective case-control study. Front Vet Sci. 2024;11:1291318. https://doi.org/10.3389/fvets.2024.1291318.

[Link to Original GitHub Repo](https://github.com/MakanFar/pss_classification)

[Link to Publication](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11024426/)

# License Notice
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
