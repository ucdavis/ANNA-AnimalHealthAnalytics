# ANNA MAIN FLASK SCRIPT APP
# Last Updated: Aug 14 2024
# Last Updated By: Kelvin Kong
# Start of Imports

from flask import Flask, request, abort

import logging
import os
import sys
import time
import json
import pandas as pd
from random import randint

# START TIME OF FLASK
time_sys = time.perf_counter()

app = Flask(__name__)

# Import Individual functions required in ANNA
sys.path.append("C:/Apache24/anna_main/assets")
from anna_mainFlaskHelpers import tommypy, leptospirosis # The main function to run ML classifier
from anna_mainFlaskSupplementalFunc import get_patient_id_n_date

# Set Current Working Directory:
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

## ANNA System Logs
logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.DEBUG)
ch = logging.FileHandler('C:/Apache24/logs/anna_mainFlask.log')
ch.setFormatter(logging.Formatter('%(asctime)s ; %(levelname)s ; %(name)s ; %(threadName)s ; %(message)s'))
logger2.addHandler(ch)


# Initializing ANNA
user_ip_csv = pd.read_csv('C:/Apache24/anna_main/assets/SampleApproved_IPs.csv') #use custom Approved_IPs.csv
app.config['UserIPs'] = user_ip_csv
logger2.info('Loaded Approved IP List.')
lepto_bool = True
tommy_bool = True
initialize_time = time.perf_counter()
logger2.info('Finished ANNA Initialization. Time used: {} seconds.'.format(round(initialize_time - time_sys, 4)))



# ANNA URL Constructs
# It will send to separate flask server

# Leptospirosis
@app.route('/ml_classifier_run/leptospirosis', methods=["GET", 'POST'])
def leptospirosis_classifier_flask():
    app_route = 'Lepto_Flask'
    if lepto_bool == False:
        abort(503)
    else:
        sessionid = randint(100001, 999999)
        real_ip = request.environ['HTTP_X_FORWARDED_FOR']
        logger2.info('Session {} - {}: Client IP: {} connection incoming.'.format(sessionid, app_route, real_ip))
        user_ip_csv = app.config['UserIPs']
        user_ip_list = list(user_ip_csv['IP'])
        if real_ip not in user_ip_list:
            logger2.info('Session {} - {}: Client IP {} not recognized. Abort Connection.'.format(sessionid, app_route, real_ip))
            abort(403)
        else:
            username = user_ip_csv['User'].iloc[user_ip_list.index(real_ip)]
            logger2.info('Session {} - {}: Client IP {} connection approved. User: {}'.format(sessionid, app_route, real_ip, username))
            # Importing required Elements:
            logger2.info('Session {} - {}: Classifier started.'.format(sessionid, app_route))
            time_start = time.perf_counter()
            # Extract Data from REST API
            if request.method == "POST":
                json_data = request.json
                try:
                    patient_id, date = get_patient_id_n_date(json_data)
                    logger2.info('Session {} - {}: PatientID: {}, Test Date: {}'.format(sessionid, app_route, patient_id, date))
                except:
                    patient_id = None
                    date = None
                    logger2.debug('Session {} - {}: Unable to fetch date-specific data.'.format(sessionid, app_route))
            else:
                try:
                    patient_id = request.args.get('PatientNum')
                    date = request.args.get('TestDate')
                    logger2.info('Session {} - {}: PatientID: {}, Test Date: {}'.format(sessionid, app_route, patient_id, date))
                except:
                    patient_id = None
                    date = None
                    logger2.debug('Session {} - {}: Unable to fetch date-specific data.'.format(sessionid, app_route))
            # END OF Extract Data from REST API
            data_return = leptospirosis(patient_id, date, sessionid, app_route) # Main Function
            time_end = time.perf_counter()
            logger2.info('Session {} - {}: {}.'.format(sessionid, app_route, data_return))
            logger2.info('Session {} - {}: Request Ended - Total Time Used: {}s.'.format(sessionid, app_route, round(time_end - time_start, 4)))
            return json.dumps(data_return)

# TommyPy
@app.route('/ml_classifier_run/tommy_addisons', methods=['GET', 'POST'])
def tommy_addisons_flask():
    app_route = 'TommyPy_Flask'
    if tommy_bool == False:
        abort(503)
    else:
        sessionid = randint(100001, 999999)
        real_ip = request.environ['HTTP_X_FORWARDED_FOR']
        logger2.info('Session {} - {}: Client IP: {} connection incoming.'.format(sessionid, app_route, real_ip))
        user_ip_csv = app.config['UserIPs']
        user_ip_list = list(user_ip_csv['IP'])
        if real_ip not in user_ip_list:
            logger2.info('Session {} - {}: Client IP {} not recognized. Abort Connection.'.format(sessionid, app_route, real_ip))
            abort(403)
        else:
            username = user_ip_csv['User'].iloc[user_ip_list.index(real_ip)]
            logger2.info('Session {} - {}: Client IP {} connected approved. User: {}'.format(sessionid, app_route, real_ip, username))
            # Importing required Elements:
            logger2.info('Session {} - {}: ML Classifier started.'.format(sessionid, app_route))
            time_start = time.perf_counter()

            if request.method == "POST":
                json_data = request.json
                try:
                    patient_id, date = get_patient_id_n_date(json_data)
                    logger2.info('Session {} - {}: PatientID: {}, Test Date: {}'.format(sessionid, app_route, patient_id, date))
                except:
                    patient_id = None
                    date = None
                    logger2.debug('Session {} - {}: Unable to fetch date-specific data.'.format(sessionid, app_route))
            else:
                try:
                    patient_id = request.args.get('PatientNum')
                    date = request.args.get('TestDate')
                    logger2.info('Session {} - {}: PatientID: {}, Test Date: {}'.format(sessionid, app_route, patient_id, date))
                except:
                    patient_id = None
                    date = None
                    logger2.debug('Session {} - {}: Unable to fetch date-specific data.'.format(sessionid, app_route))

            data_return = tommypy(patient_id, date, sessionid, app_route) # Main Function
            time_end = time.perf_counter()
            logger2.info('Session {} - {}: {}.'.format(sessionid, app_route, data_return))
            logger2.info('Session {} - {}: Request Ended - Total Time Used: {}s.'.format(sessionid, app_route, round(time_end - time_start, 4)))
            return json.dumps(data_return)
           
        