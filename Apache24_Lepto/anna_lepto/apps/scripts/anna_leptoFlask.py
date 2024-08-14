# UC Davis ANNA Flask Server Script
# Lepto Flask App

from flask import Flask, request
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import pandas as pd
import sys
import traceback
import json

app = Flask(__name__)

# Very First Initialization:
sys.path.insert(0,'C:/Apache24_Lepto/anna_lepto')
from assets.LeptoFlask_helpers import log_path, sample_initialize_path

# Logging into
logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.DEBUG)
ch = TimedRotatingFileHandler(log_path, when='midnight', interval=1, backupCount=30)
ch.setFormatter(logging.Formatter('%(asctime)s ; %(levelname)s ; %(name)s ; %(threadName)s ; %(message)s'))
logger2.addHandler(ch)

#Initializing Leptospirosis Classifier
time_sys = time.perf_counter()
sys.path.insert(0, 'C:/Apache24_Lepto/anna_lepto/assets/lepto-classifier')
from lepto_classifier import LeptoClassifier
from assets.LeptoFlask_helpers import lepto_d, data_dir
app.config['LeptoClassifier'] = LeptoClassifier()
lepto_sample_data = pd.read_csv(sample_initialize_path)
prediction = app.config['LeptoClassifier'].predict(data_path=lepto_sample_data.astype(lepto_d), use_mat=False)
time_lepto = time.perf_counter()
del lepto_sample_data, prediction
lepto_breed_groups = pd.read_csv(data_dir + "Breed_group_stratification.csv")
app.config['LeptoClassifier_lepto_breed_groups'] = lepto_breed_groups
time_tommy = time.perf_counter()
logger2.info('Finished Initializing Leptospirosis Modules, time used: {} seconds.'.format(round(time_tommy - time_sys, 4)))

@app.route('/test_handling', methods=['GET'])
def test_handling():
    try:
        start_time = time.perf_counter()
        clf = app.config['LeptoClassifier']
        lepto_sample_data = pd.read_csv(sample_initialize_path)
        pre = clf.predict(data_path=lepto_sample_data.astype(lepto_d), use_mat=False)
        prediction = [int(pred_int) for pred_int in pre]
        end_time = time.perf_counter()
        logger2.info('Prediction: {}'.format(prediction))
        logger2.info('Time needed to run prediction: {} seconds.'.format(round(end_time - start_time, 4)))
        return 'Successful'
    except:
        return "{}".format(traceback.format_exc())

### Need to work on the scripts below.
@app.route('/leptospirosis', methods=['POST'])
def leptospirosis():
    start_time = time.perf_counter()
    clf = app.config['LeptoClassifier']
    json_data = request.json
    lepto_data = pd.DataFrame(json.loads(json_data))
    try:
        pre = clf.predict(data_path=lepto_data.astype(lepto_d), use_mat=False)
        prediction = [int(pred_int) for pred_int in pre]
    except:
        logger2.debug("{}".format(traceback.format_exc()))
        prediction = -1
    end_time = time.perf_counter()
    logger2.info('Prediction: {}'.format(prediction))
    logger2.info('Time needed to run prediction: {} seconds'.format(round(end_time - start_time, 4)))
    return json.dumps(prediction)