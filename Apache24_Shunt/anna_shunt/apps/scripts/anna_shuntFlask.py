# Shunt Flask App
# Imports
from flask import Flask, request
import logging
import time
import pandas as pd
import sys

import traceback
import json


app = Flask(__name__)

# Very First Initialization:
sys.path.insert(0,'C:/Apache24_Shunt/anna_shunt')
from assets.ShuntFlask_helpers import log_path, pss_model_path, subcat_model_path

# Logging into
logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.DEBUG)
ch = logging.FileHandler(log_path)
ch.setFormatter(logging.Formatter('%(asctime)s ; %(levelname)s ; %(name)s ; %(threadName)s ; %(message)s'))
logger2.addHandler(ch)

#Initializing Shunt Classifier
time_sys = time.perf_counter()
## Initialization
from assets.pss_classification.script.run import load_model
app.config['ShuntClassifier_pss'] = load_model(pss_model_path)
app.config['ShuntClassifier_subcat'] = load_model(subcat_model_path)
int_cols = ["Breed_Herding","Breed_Hound","Breed_Non-Sporting","Breed_Other","Breed_Sporting","Breed_Terrier","Breed_Toy","Breed_Working",
            "Sex_F","Sex_M"]
time_tommy = time.perf_counter()
logger2.info('Finished Initializing Shunt Modules, time used: {} seconds.'.format(round(time_tommy - time_sys, 4)))

### Need to work on the scripts below.
@app.route('/shunt', methods=['POST'])
def shunt():
    start_time = time.perf_counter()
    json_data = request.json
    try:
        data = pd.DataFrame(json.loads(json_data))
    except:
        data = pd.DataFrame(json.loads(json_data), index=[0])
    
    model_pss = app.config['ShuntClassifier_pss']
    model_subcat = app.config['ShuntClassifier_subcat']
    result = []
    col_list = list(data.columns)
    float_cols = [elem for elem in col_list if elem not in int_cols]
    data[float_cols] = data[float_cols].astype(float)
    data[int_cols] = data[int_cols].astype(int)
    predictions = model_pss.predict(data)
    probabilities = model_pss.predict_proba(data)
    logger2.info("{}".format(predictions))
    logger2.info("{}".format(type(predictions)))
    k = 0
    for prob, pred in zip(probabilities, predictions):
        label = "Positive" if pred == 1 else "Negative"
        if pred == 1:
            sub_data = pd.DataFrame(data.iloc[k]).T.reset_index(drop=True)
            predictions_subcat = model_subcat.predict(sub_data)
            probabilities_subcat = model_subcat.predict_proba(sub_data)
            for prob_subcat, pred_subcat in zip(probabilities_subcat, predictions_subcat):
                if pred_subcat == 0:
                    label = 'Acquired shunt'
                elif pred_subcat == 1:
                    label = 'Extrahepatic'
                elif pred_subcat == 2:
                    label = 'Intrahepatic'
                elif pred_subcat == 3:
                    label = 'No shunt'
                final_prob = prob_subcat.tolist() #ndarray to list
                final_pred = int(pred_subcat)
                final_label = label
                result.append({'probability':final_prob, 'prediction':final_pred, 'prediction_label':final_label})
        else:
            final_prob = prob.tolist()#ndarray to list
            final_pred = int(pred) #int32 to int
            final_label = label
            result.append({'probability':final_prob, 'prediction':final_pred, 'prediction_label':final_label})
        k += 1
    end_time = time.perf_counter()
    logger2.info('Time needed to run prediction: {} seconds'.format(round(end_time - start_time, 4)))
    return json.dumps(result)