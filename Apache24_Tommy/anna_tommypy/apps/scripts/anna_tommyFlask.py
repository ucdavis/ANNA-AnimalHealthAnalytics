#Tommy Flask App
# Imports
from flask import Flask, request
import logging
import time
import pandas as pd
import sys
import json

app = Flask(__name__)

# Very First Initialization:
sys.path.insert(0,'C:/Apache24_Tommy/anna_tommypy')
from assets.TommyFlask_helpers import log_path, sample_initialize_path

# Logging into
logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.DEBUG)
ch = logging.FileHandler(log_path)
ch.setFormatter(logging.Formatter('%(asctime)s ; %(levelname)s ; %(name)s ; %(threadName)s ; %(message)s'))
logger2.addHandler(ch)

#Initializing Tommy Addison Classifier
time_sys = time.perf_counter()
import TommyPy #It should import because the TommyPy is already installed in tommy environment in VM.
analyzer = TommyPy.initialize()
tommy_sample_data = pd.read_csv(sample_initialize_path)
double_values = [float(arg) for arg in tommy_sample_data.loc[0]]
prediction = analyzer.TommyPy(*double_values)
app.config['TommyAddisionClassifier'] = analyzer
time_tommy = time.perf_counter()
del tommy_sample_data, prediction
logger2.info('Finished Importing TommyPy Modules, time used: {} seconds.'.format(round(time_tommy - time_sys, 4)))


@app.route('/tommy_addisons', methods=['POST'])
def tommy_addisons():
    start_time = time.perf_counter()
    analyzer = app.config['TommyAddisionClassifier']
    json_data = request.json
    try:
        tommy_data = pd.DataFrame(json.loads(json_data)) #Restore the whole dataframe. #For More than 1 rows of data:
    except:
        tommy_data = pd.DataFrame(json.loads(json_data), index=[0]) #For only have one data:
    output_list = []
    total_run_iter = len(tommy_data)
    for i in range(total_run_iter):
        logging.info('Running {} out of {} set(s) of data for predictions..'.format(i+1, total_run_iter))
        data = tommy_data.iloc[i]
        if data.isnull().values.any() == True:
            verdict = -1
        else:
            double_values = [float(arg) for arg in data]
            verdict = analyzer.TommyPy(*double_values)
        output_list.append(int(verdict))
        logging.info('Finished TommyPy Prediction.')

    end_time = time.perf_counter()
    logger2.info('Prediction: {}'.format(output_list))
    logger2.info('Time needed to run prediction: {} seconds'.format(round(end_time - start_time, 4)))
    return json.dumps(output_list)
