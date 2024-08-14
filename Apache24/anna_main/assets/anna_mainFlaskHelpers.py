# Helper Function:
# Import Python Packages
import pandas as pd
import time
import requests
import logging
import traceback
import numpy as np

# Import from SupplementalFunc
from anna_mainFlaskSupplementalFunc import divergent_var_rename, df_merge_string_clean, df_merge
from anna_mainFlaskSupplementalFunc import tommy_result_database_write_sql, lepto_result_database_write_sql
from anna_mainFlaskSupplementalFunc import tommy_url, lepto_url
from anna_mainFlaskSupplementalFunc import process_xml_parallel_date_specific
from anna_mainFlaskSupplementalFunc import failed_prediction_leptospirosis, failed_prediction_tommy_addisons
from anna_mainFlaskSupplementalFunc import tommy_preprocessing, lepto_preprocessing

## ML Classifier Specific Function:
### TommyPy
def tommypy(patient_id, date, sessionid, app_route):
    time_tommy_start = time.perf_counter()
    # End of Import
    if patient_id is not None and date is not None:
        try:
            cbc_raw, chemua_raw = process_xml_parallel_date_specific(patient_id, date, chmua_date_range=True, micro=False, immu=False) #For TommyPy that reduce fetching:
            time_fetch = time.perf_counter()
            logging.info('Session {} - {}: Fetched Date-Specifc Data: Time used: {}s'.format(sessionid, app_route, round(time_fetch - time_tommy_start, 4)))
        except:
            time_fetch = time.perf_counter()
            logging.debug('Session {} - {}: Unable to fetch date-specific data.'.format(sessionid, app_route))
            cbc_raw = None
            chemua_raw = None
    else:
        cbc_raw = None
        chemua_raw = None

    if isinstance(cbc_raw, pd.DataFrame) == True and isinstance(chemua_raw, pd.DataFrame) == True:
        if cbc_raw.shape[0] == 0 and chemua_raw.shape[0] == 0:
            prediction, TestID_cbc, TestID_chem, classifier_timestamp = failed_prediction_tommy_addisons()
        else:
            if 'Species' in chemua_raw.columns:
                species = chemua_raw['Species'].iloc[0]
                if species == 'K9':
                    try:
                        cbc_df = divergent_var_rename(cbc_raw)
                        chemua_df = divergent_var_rename(chemua_raw)
                        merged_df = df_merge(cbc_df, chemua_df, micro_need=False, immu_need=False)
                        merged_df_cleaned = df_merge_string_clean(merged_df)
                        tommy_data, tommy_testids = tommy_preprocessing(merged_df_cleaned)
                        tommy_data_json = tommy_data.to_json()
                        ### Predictions:
                        prediction = requests.post(tommy_url, json=tommy_data_json).json()
                        #pd.Series.to_list()
                        TestID_cbc = np.array(tommy_testids['TestID_cbc']).tolist()
                        TestID_chem = np.array(tommy_testids['TestID_chem']).tolist()
                        Date_cbc = tommy_testids['Date'].to_list()
                        Date_chem = tommy_testids['Date'].to_list()
                        classifier_timestamp = tommy_result_database_write_sql(patient_id, prediction, TestID_cbc, Date_cbc, TestID_chem, Date_chem)
                        time_predicted = time.perf_counter()
                        logging.info('Session {} - {}: Successful Prediction. Time used: {}s.'.format(sessionid, app_route, round(time_predicted - time_fetch, 4)))
                    except:
                        logging.debug('{}'.format(traceback.format_exc()))
                        prediction, TestID_cbc, TestID_chem, classifier_timestamp = failed_prediction_tommy_addisons()
                        time_predicted = time.perf_counter()
                        logging.info('Session {} - {}: Unsuccessful Prediction. Time used: {}s.'.format(sessionid, app_route, round(time_predicted - time_fetch, 4)))
                else:
                    prediction, TestID_cbc, TestID_chem, classifier_timestamp = failed_prediction_tommy_addisons()
                    time_predicted = time.perf_counter()
                    logging.info('Session {} - {}: Incorrect Species. Unsuccessful Prediction. Time used: {}s.'.format(sessionid, app_route, round(time_predicted - time_fetch, 4)))
            else:
                prediction, TestID_cbc, TestID_chem, classifier_timestamp = failed_prediction_tommy_addisons()
                time_predicted = time.perf_counter()
                logging.info('Session {} - {}: No Species data. Unsuccessful Prediction. Time used: {}s.'.format(sessionid, app_route, round(time_predicted - time_fetch, 4)))
##################### This Triggers when CBC and CHMUAEXPORT are Empty (Can not Fetch) ############################       
    else:
        prediction, TestID_cbc, TestID_chem, classifier_timestamp = failed_prediction_tommy_addisons()
        time_predicted = time.perf_counter()
        logging.info('Session {} - {}: No CBC and CHEMUA Data. Unsuccessful Prediction. Time used: {}s.'.format(sessionid, app_route, round(time_predicted - time_fetch, 4)))
    data_return = {'tommyResult': prediction, 'classifierFirstRunDateTime': classifier_timestamp, 'testIDs': {'TestID_cbc': TestID_cbc, 'TestID_chem':TestID_chem}}
    return data_return


### Leptospirosis
def leptospirosis(patient_id, date, sessionid, app_route):
    time_start = time.perf_counter()
    # End of Import
    if patient_id is not None and date is not None:
        try:
            result_dict, url_dict = process_xml_parallel_date_specific(patient_id, date, chmua_date_range=True, micro=True, immu=True)
            time_fetch = time.perf_counter()
            logging.info('Session {} - {}: Fetched Date-Specifc Data: Time used: {}s'.format(sessionid, app_route, round(time_fetch - time_start, 4)))
        except:
            result_dict = None
            logging.debug('{}'.format(traceback.format_exc()))
            time_fetch = time.perf_counter()
            logging.debug('Session {} - {}: Unable to fetch date-specific data.'.format(sessionid, app_route))
    if result_dict is not None:
        try:
            merged_df = df_merge(result_dict, date, micro_need=True, immu_need=True)
            lepto_breed_groups = pd.read_csv("C:/Apache24/anna_common_assets/app_data/Breed_group_stratification.csv")
            lepto_data, lepto_testids = lepto_preprocessing(merged_df, lepto_breed_groups, use_mat=False)
            prediction = requests.post(lepto_url, json=lepto_data.to_json()).json()
            if isinstance(prediction, list) == True:
                logging.info("Raw Lepto Prediction returned from Flask Server: {}".format(prediction))
                TestID_cbc = np.array(lepto_testids['TestID_cbc']).tolist()
                Date_cbc = np.array(lepto_testids['Date_cbc']).tolist()
                TestID_chem = np.array(lepto_testids['TestID_chem']).tolist()
                Date_chem = np.array(lepto_testids['Date_chem']).tolist()
                TestID_ua = np.array(lepto_testids['TestID_ua']).tolist()
                Date_ua = np.array(lepto_testids['Date_ua']).tolist()
                try:
                    TestID_MAT = np.array(lepto_testids['TestID_mat']).tolist()
                    Date_MAT = np.array(lepto_testids['Date_mat']).tolist()
                except:
                    TestID_MAT = ['NoTest' for x in range(len(prediction))]
                    Date_MAT = ['NoTest' for x in range(len(prediction))]
                try:
                    TestID_leptoPCR = np.array(lepto_testids['TestID_leptoPCR']).tolist()
                    Date_leptoPCR = np.array(lepto_testids['Date_leptoPCR']).tolist()
                except:
                    TestID_leptoPCR = ['NoTest' for x in range(len(prediction))]
                    Date_leptoPCR = ['NoTest' for x in range(len(prediction))]
                try:
                    TestID_leptoLF = np.array(lepto_testids['TestID_leptoLF']).tolist()
                    Date_leptoLF = np.array(lepto_testids['Date_leptoLF']).tolist()
                except:
                    TestID_leptoLF = ['NoTest' for x in range(len(prediction))]
                    Date_leptoLF = ['NoTest' for x in range(len(prediction))]
                time_predicted = time.perf_counter()
                logging.info('Session {} - {}: Succcessful Prediction. Time used: {}s.'.format(sessionid, app_route, round(time_predicted - time_fetch, 4)))

                classifier_timestamp = lepto_result_database_write_sql(patient_id, prediction, TestID_cbc, Date_cbc, TestID_chem, Date_chem, TestID_ua, Date_ua, 
                                                    TestID_MAT, Date_MAT, TestID_leptoPCR, Date_leptoPCR, TestID_leptoLF, Date_leptoLF)
            else:
                prediction, TestID_cbc, TestID_chem, TestID_ua, TestID_MAT, TestID_leptoPCR, TestID_leptoLF, classifier_timestamp  = failed_prediction_leptospirosis()
                time_predicted = time.perf_counter()
                logging.info('Session {} - {}: Unsuccessful Prediction. Time used: {}s.'.format(sessionid, app_route, round(time_predicted - time_fetch, 4)))
        except:
            logging.debug('{}'.format(traceback.format_exc()))
            prediction, TestID_cbc, TestID_chem, TestID_ua, TestID_MAT, TestID_leptoPCR, TestID_leptoLF, classifier_timestamp = failed_prediction_leptospirosis()
            time_predicted = time.perf_counter()
            logging.info('Session {} - {}: Unsuccessful Prediction. Time used: {}s.'.format(sessionid, app_route, round(time_predicted - time_fetch, 4)))

    else:
        prediction, TestID_cbc, TestID_chem, TestID_ua, TestID_MAT, TestID_leptoPCR, TestID_leptoLF, classifier_timestamp = failed_prediction_leptospirosis()
        time_predicted = time.perf_counter()
        logging.info('Session {} - {}: Unsuccessful Prediction. Time used: {}s.'.format(sessionid, app_route, round(time_predicted - time_fetch, 4)))
    data_return = {'leptoResult': prediction, 'classifierFirstRunDateTime': classifier_timestamp, 
                   'testIDs': {'TestID_cbc': TestID_cbc, 'TestID_chem': TestID_chem, 'TestID_ua': TestID_ua, 
                               'TestID_leptoMAT': TestID_MAT, 'TestID_leptoPCR': TestID_leptoPCR, 'TestID_leptoLF': TestID_leptoLF}}
    return data_return