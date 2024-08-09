# ANNA-AnimalHealthAnalytics
A Python based Computational Server for analyzing Animal Health Data with AI

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
- MATLAB Runtime R2019b (v9.7)
- List of Python Packages specified in the requirement text file.

## Installation

### Python

### miniconda

### Apache HTTP Server
1. Download Apache HTTP Server source codes.
2. Extract the source codes to each folder starting with `Apache24_`.
3. Edit each Apache's configuration files:
  - The following configurations need to be changed:
    - Define SRVROOT Path
    - Listen
    - ServerAdmin (Optional)
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

### MATLAB Runtime

### Python Packages

## Folder Structure
