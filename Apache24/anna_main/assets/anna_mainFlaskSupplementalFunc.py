## ANNA Supplemental Function Python Scripts:
import pandas as pd
import numpy as np
import platform
from datetime import datetime, timedelta
import os
import concurrent.futures
import xml.etree.ElementTree as ET
import logging
import time
import requests
import traceback
import MySQLdb
import re

# Variables Define
tommy_url = 'http://127.0.0.1:5001/tommy_addisons'
lepto_url = 'http://127.0.0.1:5002/leptospirosis'
tommy_cols = {"Anion Gap" : "float64","Sodium" : "float64","Potassium" : "float64","Chloride" : "float64",
              "HCO3" : "float64","Phosphorus" : "float64","Calcium" : "float64","BUN" : "float64",
              "Creatinine" : "float64","Glucose" : "float64","Total Pr" : "float64","Albumin" : "float64",
              "Globulin" : "float64","ALT" : "float64","AST" : "float64","ALP" : "float64",
              "GGT" : "float64","Cholesterol" : "float64","Bili" : "float64","RBC" : "float64",
              "Hgb" : "float64","Hct" : "float64","MCV" : "float64","MCH" : "float64","MCHC" : "float64",
              "RDW" : "float64","WBC" : "float64","Neut" : "float64","Lymph" : "float64","Mono" : "float64",
              "Eosin" : "float64","Plt" : "float64","MPV" : "float64","Protein" : "float64"}

tommy_vars_order = ['Anion Gap', 'Sodium', 'Potassium', 'Chloride', 'HCO3', 'Phosphorus', 'Calcium', 'BUN', 'Creatinine',
                      'Glucose', 'Total Pr', 'Albumin', 'Globulin', 'ALT', 'AST', 'ALP', 'GGT', 'Cholesterol', 'Bili', 'RBC', 
                      'Hgb', 'Hct', 'MCV', 'MCH', 'MCHC', 'RDW', 'WBC', 'Neut', 'Lymph', 'Mono', 'Eosin', 'Plt', 'MPV', 'Protein']

lepto_d = {'Hgb': 'float64', 
           'Hct': 'float64',
           'MCV': 'float64',
           'WBC': 'float64',
           'Neut': 'float64',
           'Lymph': 'float64',
           'Mono': 'float64',
           'Eosin': 'float64',
           'Plt': 'float64',
           'Bands': 'float64',
           'Albumin': 'float64',
           'ALP': 'float64',
           'ALT': 'float64',
           'AST': 'float64',
           'Bilirubin': 'float64',
           'BUN': 'float64',
           'Calcium': 'float64',
           'Cholesterol': 'float64',
           'Creatinine': 'float64',
           'GGT': 'float64',
           'Globulin': 'float64',
           'Glucose': 'float64',
           'Phosphorus': 'float64',
           'Total Protein': 'float64',
           'Anion Gap': 'float64',
           'Chloride': 'float64',
           'Sodium': 'float64',
           'Potassium': 'float64',
           'Bicarb': 'float64',
           'Weight': 'float64',
           'Sex': 'int64',
           'Breed': 'O',
           'Breed Group': 'O',
           'Urine Specific Gravity': 'float64',
           'Urine Glucose': 'float64',
           'Urine Protein': 'float64'}

# This WBC is actually WBCCorr
lepto_order_cols_with_MAT = ['Weight','Breed', 'Breed Group', 'Sex', 'MAT', 'Anion Gap', 'Sodium', 'Potassium', 'Chloride', 'Bicarb', 
                    'Phosphorus', 'Calcium', 'BUN', 'Creatinine', 'Glucose', 'Total Protein',
                    'Albumin', 'Globulin', 'ALT', 'Prior', 'AST', 'ALP', 'GGT', 'Cholesterol',
                    'Bilirubin', 'Urine Specific Gravity', 'Urine Protein', 'Urine Glucose', 
                    'Hct', 'Hgb', 'MCV', 'WBC', 'Bands', 'Neut', 'Lymph', 'Mono', 'Eosin', 'Plt']
# This WBC is actually WBCCorr
lepto_order_cols_without_MAT = ['Weight', 'Breed', 'Breed Group', 'Sex', 'Anion Gap', 'Sodium', 'Potassium', 'Chloride', 'Bicarb', 
                    'Phosphorus', 'Calcium', 'BUN', 'Creatinine', 'Glucose', 'Total Protein',
                    'Albumin', 'Globulin', 'ALT', 'AST', 'ALP', 'GGT', 'Cholesterol',
                    'Bilirubin', 'Urine Specific Gravity', 'Urine Protein', 'Urine Glucose', 
                    'Hct', 'Hgb', 'MCV', 'WBC', 'Bands', 'Neut', 'Lymph', 'Mono', 'Eosin', 'Plt']

divergent_var_rename_dict = {'CALCIUMx': 'Calcium', 'Creatine_KinaseOld': 'Creatine_Kinase', 
                  'BICARBONATE': 'Bicarb', 'HCO3':'Bicarb', 'Magnesium1': 'Magnesium',
                  'Basophils': 'Baso', 'Nucleated_RBC': 'NRBC', 'Alkaline_Phosphatase': 'ALP', 'Alk Phos': 'ALP',
                  'Bilirubin_Total':'Bili Total', 'Bili': 'Bili Total', 'Bilirubin': 'Bili Total', 'Anion_Gap': 'Anion Gap', 'Total_Protein':'Total Protein', 'Total Pr': 'Total Protein',
                  'SPECIFIC_GRAVITY':'Urine Specific Gravity', 'PROTEIN_URINE':'Urine Protein', 'GLUCOSE_URINE':'Urine Glucose'}


# General
def get_patient_id_n_date(json_data):
    patient_id = json_data['patientId']
    date = json_data['date']
    return patient_id, date

def failed_prediction_leptospirosis():
    prediction = [-1]
    TestID_cbc = ['NA']
    TestID_chem = ['NA']
    TestID_ua = ['NA']
    TestID_leptoMAT = ['NA']
    TestID_leptoLF = ['NA']
    TestID_leptoPCR = ["NA"]
    timestamp = ['NA']
    return prediction, TestID_cbc, TestID_chem, TestID_ua, TestID_leptoMAT, TestID_leptoLF, TestID_leptoPCR, timestamp

def failed_prediction_tommy_addisons():
    prediction = [-1]
    TestID_cbc = ['NA']
    TestID_chem = ['NA']
    classifier_timestamp = ['NA']
    return prediction, TestID_cbc, TestID_chem, classifier_timestamp


# Data Fetch
def fetch_url(url):
    start_time = time.perf_counter()
    responses = requests.get(url)
    end_time = time.perf_counter()
    logging.info('Finished fetching data. Time used: {}s'.format(round(end_time - start_time, 4)))
    return responses.text


def xml_to_df_anna(request):
    rr = request.replace('#', '')
    rr = rr.replace('(', '')
    rr = rr.replace(')', '')
    rr = rr.replace(',', '')
    rr = rr.replace('URINE_P/C_RATIO', 'URINE_PC_RATIO')

    root = ET.fromstring(rr)

    items = []
    for item in root.findall("./item"):
        news = {}

        for child in item:
            news[child.tag] = child.text

        items.append(news)
    df = pd.DataFrame(items)

    if 'Date' in df.columns:
        df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%d%b%y').date())
    if 'AdmsDate' in df.columns:
        df['Date'] = df['AdmsDate'].apply(lambda x: datetime.strptime(x, '%d%b%y').date())
        df.drop(columns=['AdmsDate'], inplace=True)
    if 'DtOfRq' in df.columns:
        df['Date'] = df['DtOfRq'].apply(lambda x: datetime.strptime(x, '%d%b%y').date())
        df.drop(columns=['DtOfRq'], inplace=True)

    if 'Patient' in df.columns:
        df.rename(columns={'Patient': 'PatientID'}, inplace=True)
    if 'PtntNo' in df.columns:
        df.rename(columns={'PtntNo': 'PatientID'}, inplace=True)
    if 'Lab' in df.columns:
        df.rename(columns={'Lab': 'TestID'}, inplace=True)
    if 'Ref' in df.columns:
        df.rename(columns={'Ref': 'TestID'}, inplace=True)
    if 'Visit' in df.columns:
        df.rename(columns={'Visit': 'VisitID'}, inplace=True)
    if 'VisitNo' in df.columns:
        df.rename(columns={'VisitNo': 'VisitID'}, inplace=True)
    if 'Request' in df.columns:
        df.rename(columns={'Request': 'TestID'}, inplace=True)

    mask_procedures = ['<br>7597-Chem Handling FedEx', '<br>7598-Chem Handling Fee']
    if 'Procedures' in df.columns:
        for proc in mask_procedures:
            df['Procedures'] = df['Procedures'].astype(str).apply(lambda x: x.replace(proc, ''))
    # Create rules to filter Report_Status == Final in CBC/CHEM/UA
    if "Collected_Datetime" not in df.columns:
        if "Report_Status" in df.columns:
            df = pd.concat([df[(df['Report_Status'] == 'Final')], df[(df['Report_Status'] == 'FINAL')]], axis=0)
    return df

def process_xml_parallel_date_specific(patientid, date, cbc_date_range=False,chmua_date_range=False, micro=False, immu=False):
    date_date = datetime.strptime(date, '%Y-%m-%d').date()
    date_specific_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d%b%y')
    upper_date = (date_date + timedelta(days=5)).strftime('%y%m%d')
    lower_date = (date_date - timedelta(days=5)).strftime('%y%m%d')
    if cbc_date_range == True:
        cbc_url = os.getenv('QUERY_TO_CBC_DATABASE_DATE_RANGED').format(patientid, lower_date, upper_date)
    else:
        cbc_url = os.getenv('QUERY_TO_CBC_DATABASE').format(patientid, date_specific_date)
    if chmua_date_range == True:
        chemua_url = os.getenv('QUERY_TO_CHEMISTRY_DATE_RANGED').format(patientid, lower_date, upper_date) #Requires
    else:
        chemua_url = os.getenv('QUERY_TO_CHEMISTRY').format(patientid, date_specific_date)
    if micro == True:
        microbiology_url = os.getenv('QUERY_TO_MICROBIOLOGY').format(patientid, lower_date, upper_date)
    else:
        microbiology_url = None
    if immu == True:
        immunology_url = os.getenv('QUERY_TO_IMMUNOLOGY').format(patientid, lower_date, upper_date)
    else:
        immunology_url = None
    
    list_of_url = [cbc_url, chemua_url, microbiology_url, immunology_url]
    url_dict = {cbc_url: 'cbc', chemua_url: 'chemua', microbiology_url: 'micro', immunology_url: 'immunology'}

    #######
    result_dict = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in list_of_url if url is not None}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            result = future.result()
            result_dict[url_dict[url]] = xml_to_df_anna(result).to_dict()
    return result_dict, url_dict

# Data Preprocessing
def divergent_var_rename(data):
    rename_map =  {'CALCIUMx': 'Calcium', 'Creatine_KinaseOld': 'Creatine_Kinase', 
                  'BICARBONATE': 'HCO3', 'Magnesium1': 'Magnesium',
                  'Basophils': 'Baso', 'Nucleated_RBC': 'NRBC'}
    divergent_list = list(rename_map.keys())
    default_list = list(rename_map.values())

    for i in range(len(divergent_list)):
        divergent_term = divergent_list[i]
        default_term = default_list[i]
        if (divergent_term in data.columns) and (default_term not in data.columns):
            data.rename(columns={divergent_term:default_term}, inplace=True)
        elif (divergent_term in data.columns) and (default_term in data.columns):
            temp_var_list = []
            for j in range(len(data)):
                a = data[divergent_term].iloc[j] #Divergent Vars
                b = data[default_term].iloc[j] #Default
                bool_a = bool(pd.isnull(a))
                bool_b = bool(pd.isnull(b))
                if bool_a == True and bool_b == False: #Default has value
                    temp_var_list.append(b)
                elif bool_a == False and bool_b == True: #Divergent has value
                    temp_var_list.append(a)
                else:
                    temp_var_list.append(b)
            data.drop(columns=divergent_term, inplace=True)
            data.drop(columns=default_term, inplace=True)
            data[default_term] = temp_var_list
        elif (default_term in data.columns) and (divergent_term not in data.columns):
            continue
        elif (default_term not in data.columns) and (divergent_term not in data.columns):
            continue
        else:
            continue

    return data

def df_merge_string_clean(input):
    output = input.copy()
    # This function is in use within df_merge(), at the last after getting final_merge:
    pattern = r'[^\d.]'
    meta_cols = ['PatientID', 'Breed', 'Sex', 'Age', 'Weight', 'Date', 'Procedures', 'Procedures_group', 'TestID',
                 'PatientID', 'Breed', 'Sex', 'Age', 'Weight', 'Date', 'Procedures', 'Procedures_group', 'TestID',
                 'Sex', 'Age', 'Weight', 'Date', 'Procedures', 'Procedures_group', 'TestID'] # Not used in here, just for reference.
    
    string_vars_cols = ['Color', 'Clarity','GLUCOSE_URINE', 'KETONES_URINE', 'BILIRUBIN_URINE', 'HEMOPROTEIN_URINE', 
                        'LIPID_LAYER', 'WBC_URINE', 'RBC_URINE', 'CYRSTALS_URINE', 
                        'EPITHELIAL_CELLS_TRANSITIONAL','EPITHELIAL_CELLS_SQUAMOUS', 'EPITHELIAL_CELLS_RENAL',
                        'EPITHELIAL_CELLS_CAUDATE', 'CASTS_HYALINE', 'CAST_GRANULAR',
                        'CAST_WAXY', 'CAST_CELLULAR', 'BACTERIA', 'LIPID_DROPLETS', 'SPERM','OTHER', 'RBC_Morphology', 'Plt_Comment','Result_Comment']
    
    numeric_vars_cols = ['SPECIFIC_GRAVITY', 'PH_URINE', 'PROTEIN_URINE', 'SEDIMENT_VOLUME', 'VOLUME_URINE', 'CREATININE_URINE', 'TP_QUANT_URINE', 'URINE_PC_RATIO'
                         'Albumin', 'Alkaline_Phosphatase', 'ALP', 'ALT', 'AST', 'Bilirubin_Total', 'Bili Total',
                         'BUN', 'Calcium', 'Magnesium', 'Cholesterol', 'Creatine_Kinase', 'Creatine Kinase', 'Creatinine', 'GGT', 'Globulin', 'Glucose', 
                         'Hemolysis_Index', 'Icteric_Index', 'Lipemic_Index', 'Hemolysis Index', 'Icteric Index', 'Lipemic Index',
                         'Phosphorus', 'Total_Protein', 'Protein Total', 'Anion_Gap', 'Anion Gap',
                         'Chloride', 'Sodium', 'Potassium', 'HCO3', 'Folate_Immulite', 'Creatine_KinaseOld',
                         'RBC', 'Hgb', 'Hct', 'MCV', 'MCH', 'MCHC', 'RDW',
                         'WBCCorr', 'WBC', 'Neut', 'Lymph', 'Mono',
                         'Eosin', 'Plt', 'MPV', 'Protein', 'Retic', 'Bands', 'NRBC', 'Baso']

    replace_pattern = r'[^\d.]'

    for j in numeric_vars_cols:
        if j in input.columns:
            new_var_list = []
            for i in range(len(input)):
                string = str(input[j].iloc[i])
                if string == 'nan':
                    new_var_list.append(np.nan)
                else:
                    if bool(re.search(replace_pattern, string)) == True:
                        new_string = re.sub(replace_pattern, "", string)
                        if new_string == '':
                            new_string_out = np.nan
                        elif new_string == 'None':
                            new_string_out = np.nan
                        elif new_string == 'nan':
                            new_string_out = np.nan
                        else:
                            number_of_dots = len(re.findall(r'\.', new_string))
                            if number_of_dots > 1:
                                new_string_temp = re.sub(r'\.', '<DOT>', new_string, 1)
                                new_string_temp = new_string_temp.replace('.', '')
                                new_string_temp = new_string_temp.replace('<DOT>', '.')
                                new_string_out = float(new_string_temp)
                            else:
                                new_string_out = float(new_string)
                        new_var_list.append(new_string_out)
                    else:
                        new_var_list.append(float(string))

            output[j] = new_var_list

        else:
            pass

            
    return output

def micro_immu_procedure_filter(data):
    if isinstance(data, pd.DataFrame) == True:
        if 'Procedures' in data.columns:
            for index, row in data.iterrows():
                string_test = str(row['Procedures'])
                if '8245' in string_test:
                    pass
                elif '8780' in string_test:
                    pass
                elif '8615' in string_test:
                    pass
                else:
                    data.drop(index, inplace=True)
        return data
    else:
        return None

def chem_ua_split(data):
    # based on df_merge_update_v2 (Seemed not working:)
    # Now based on mapping procedure codes
    mapping_csv = pd.read_csv('C:/Apache24/anna_main/assets/Procedures_group_v5.csv')
    mapping = dict(mapping_csv.values)
    
    data["Procedures_group"] = data["Procedures"].replace(mapping)
    # Need to check colunm name:
    chem_cols = ['VisitID', 'TestID', 'Name','Species','Breed','Date','Specimen', 'Procedures','Albumin','Procedures_group',
        'Alkaline_Phosphatase', 'ALT', 'AST', 'Bilirubin_Total', 'BUN', 'CALCIUMx', 'Calcium', 'Magnesium1', 'Magnesium', 
        'Cholesterol', 'Creatine_Kinase', 'Creatinine', 'GGT', 'Globulin', 'Glucose', 
        'Hemolysis_Index', 'Icteric_Index', 'Lipemic_Index', 'Phosphorus', 'Total_Protein', 
        'Anion_Gap', 'Chloride', 'Sodium', 'Potassium', 'BICARBONATE', 'HCO3', 'Folate_Immulite', 'Creatine_KinaseOld', 'SDH-37', 'Report_Status']

    ua_cols = ['TestID','VisitID','Age','Sex','Weight','Procedures','Date', 'Color',
      'Clarity', 'SPECIFIC_GRAVITY', 'Procedures_group','PH_URINE', 'PROTEIN_URINE', 
      'GLUCOSE_URINE', 'KETONES_URINE', 'BILIRUBIN_URINE', 'HEMOPROTEIN_URINE', 'SEDIMENT_VOLUME', 
      'VOLUME_URINE', 'LIPID_LAYER', 'WBC_URINE', 'RBC_URINE', 'CYRSTALS_URINE', 'CREATININE_URINE', 'TP_QUANT_URINE', 'URINE_PC_RATIO',
      'EPITHELIAL_CELLS_TRANSITIONAL', 'EPITHELIAL_CELLS_SQUAMOUS', 'EPITHELIAL_CELLS_RENAL',
        'EPITHELIAL_CELLS_CAUDATE', 'CASTS_HYALINE', 'CAST_GRANULAR', 'CAST_WAXY', 'CAST_CELLULAR',
          'BACTERIA', 'LIPID_DROPLETS', 'SPERM', 'OTHER', 'Report_Status']


    ua_df = data.loc[data['Procedures_group'] == 'ua'][data.columns.intersection(set(ua_cols))]
    if 'Procedures_group' in ua_df.columns:
        ua_df.drop(columns='Procedures_group', inplace=True)
    if len(ua_df) == 0:
        ua_df = None
    chem_df = data.loc[data['Procedures_group'] != 'ua'][data.columns.intersection(set(chem_cols))]
    if 'Procedures_group' in chem_df.columns:
        chem_df.drop(columns='Procedures_group', inplace=True)
    return chem_df, ua_df

def immu_df_split(data):
    if (isinstance(data, pd.DataFrame) == True) and (len(list(data.columns)) != 0):
        df_8780 = pd.DataFrame(columns=data.columns)
        df_8615 = pd.DataFrame(columns=data.columns)
    else:
        data_cols = ["TestID", "VisitID", "Date", "PatientID", "Procedures", "Report_Status", "Collected_Datetime"]
        df_8780 = pd.DataFrame(columns=data_cols)
        df_8615 = pd.DataFrame(columns=data_cols)
    if isinstance(data, pd.DataFrame) == True:
        if 'Procedures' in data.columns:
            for index, row in data.iterrows():
                if '8780' in str(row['Procedures']):
                    df_8780 = pd.concat([df_8780, pd.DataFrame(row).T], axis=0, ignore_index=True)
                elif '8615' in str(row['Procedures']):
                    df_8615 = pd.concat([df_8615, pd.DataFrame(row).T], axis=0, ignore_index=True)
                else:
                    pass
            df_8615['Date'] = df_8615['Date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date() if type(x) == str else x)
            df_8780['Date'] = df_8780['Date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date() if type(x) == str else x)
        else:
            pass
    else:
        pass
    df_8780 = df_8780.add_suffix("_leptoPCR")
    df_8615 = df_8615.add_suffix("_leptoLF")    
    return df_8780, df_8615

# Classifier Specific Data Preprocessing
## TommyPy
def tommy_preprocessing(tommy_df):
    rename_map = {'Anion_Gap': 'Anion Gap', 'Total_Protein': 'Total Pr',
                  'Alkaline_Phosphatase': 'ALP', 'Alk Phos': 'ALP', 
                  'Bilirubin_Total': 'Bili'}
    divergent_list = list(rename_map.keys())
    default_list = list(rename_map.values())
    for i in range(len(divergent_list)):
        divergent_term = divergent_list[i]
        default_term = default_list[i]
        try:
            tommy_df.rename(columns={divergent_term:default_term}, inplace=True)
        except:
            pass

    final_cols = ['Date','TestID_chem','TestID_cbc'] + list(tommy_cols.keys())
    tommy_df_final = tommy_df[final_cols]
    tommy_df_final.dropna(subset=list(tommy_cols.keys()), axis=0, inplace=True)
    tommy_df_testids = tommy_df_final[['TestID_cbc', 'TestID_chem', 'Date']]
    tommy_df_testids = tommy_df_testids.loc[:,~tommy_df_testids.columns.duplicated()].copy()
    tommy_df_final = tommy_df_final[list(tommy_cols.keys())]

    return tommy_df_final, tommy_df_testids

## Lepto
def lepto_preprocessing(lepto_df, lepto_breed_groups, use_mat=False):
    hostname = platform.node()
    basic_cols = ['TestID_cbc','TestID_chem', 'TestID_ua']
    basicdate_cols = ['Date_cbc', 'Date_chem', 'Date_ua']
    plus_cols = {'TestID_mat':'Date_mat', 'TestID_leptoPCR': 'Date_leptoPCR', 'TestID_leptoLF':'Date_leptoLF'}
    testid_cols = []
    testdate_cols = []
    for col in plus_cols.keys():
        if col in lepto_df.columns:
            testid_cols.append(col)
            testdate_cols.append(plus_cols[col])
    if len(testid_cols) > 0:
        testid_cols_final = basic_cols + testid_cols
        lepto_df = lepto_df[lepto_df[testid_cols_final].notnull().all(1)]
    else:
        lepto_df = pd.DataFrame()

    lepto_rename_map = {"Breed_chem":"Breed",'Anion_Gap': 'Anion Gap',
                  'Total_Protein': 'Total Protein', 'Alkaline_Phosphatase': 'ALP', "Bili Total": "Bilirubin",
                  'Bilirubin_Total': 'Bilirubin', 'Bili':'Bilirubin', 'Alk Phos': 'ALP', 'HCO3': 'Bicarb',
                  'Total Pr': 'Total Protein', 'Patient_Weight': 'Weight',
                  'SPECIFIC_GRAVITY': 'Urine Specific Gravity',
                  'GLUCOSE_URINE': 'Urine Glucose', 'PROTEIN_URINE': 'Urine Protein'}
    
    for col in lepto_rename_map.keys():
        if col in lepto_df.columns:
            lepto_df.rename(columns={col:lepto_rename_map[col]}, inplace=True)

    for param in ['Bands']:
        if param in lepto_df.columns:
            lepto_df[param] = lepto_df[param].fillna(0)
        else:
            lepto_df[param] = 0

    drop_cols = [lepto_df.columns.intersection(set(['GGT', 'RBC', 'Plt', 'Neut', 'RDW']))][0]
    lepto_df.dropna(axis=0, subset=drop_cols, inplace=True)
    if 'Plt' in lepto_df.columns:
        lepto_df['Plt'] = lepto_df['Plt'].apply(lambda x: int(float(x)/1000)) #Plt
    if 'GGT' in lepto_df.columns:
        lepto_df['GGT'] = lepto_df['GGT'].apply(lambda x: int(float(str(x).replace('<3', '0')))) #GGT
    if 'Bili' in lepto_df.columns:
        lepto_df['Bili'] = lepto_df['Bili'].apply(lambda x: float(str(x).replace('<', '')))
    if 'Hct' in lepto_df.columns:
        lepto_df['Hct'] = lepto_df['Hct'].apply(lambda x: int(float(x))) #Hct
    if 'Glucose' in lepto_df.columns:
        lepto_df['Glucose'] = lepto_df['Glucose'].apply(lambda x: x.split(';')[0] if isinstance(x, str) else x)
 
    breed_dict = dict(zip(lepto_breed_groups["Name"], lepto_breed_groups["AKC Group"]))
    if 'Breed' in lepto_df.columns:
        lepto_df['Breed'] = lepto_df['Breed'].apply(lambda i: i if i in list(breed_dict.keys()) else 'Other')
        lepto_df["Breed Group"] = lepto_df["Breed"].replace(breed_dict)

    lepto_df.drop(columns=['PatientID_cbc', 'Breed_cbc', 'Procedures','Procedures_group',
                           'PatientID_chem',  'Procedures_chem', 'Procedures_group_chem',
                           'PatientID_ua', 'Breed_ua', 'Procedures_ua', 'Procedures_group_ua',
                           'RBC', 'MCH', 'MCHC', 'RDW', 'RBC_Morphology', 'Plt_Comment', 'MPV', 'Protein',
                           'Result_Comment', 'Retic','Creatine_Kinase', 'Hemolysis_Index', 'Icteric_Index', 'Lipemic_Index',
                           'Creatine_KinaseOld', 'NRBC', 'Baso', 'Unclass', "WBC", 'PH_URINE', 'PROTEIN_URINE','GLUCOSE_URINE', 'KETONES_URINE', 'BILIRUBIN_URINE',
                           'HEMOPROTEIN_URINE', 'SEDIMENT_VOLUME', 'VOLUME_URINE', 'LIPID_LAYER', 'WBC_URINE',
                           'RBC_URINE', 'CYRSTALS_URINE', 'CREATININE_URINE', 'TP_QUANT_URINE', 'URINE_PC_RATIO',
                           'EPITHELIAL_CELLS_TRANSITIONAL','EPITHELIAL_CELLS_SQUAMOUS', 'EPITHELIAL_CELLS_RENAL',
                           'EPITHELIAL_CELLS_CAUDATE', 'CASTS_HYALINE', 'CAST_GRANULAR',
                           'CAST_WAXY', 'CAST_CELLULAR', 'BACTERIA', 'LIPID_DROPLETS', 'SPERM',
                           'OTHER'], inplace=True, errors='ignore')
    
    lepto_df.rename(columns={"WBCCorr":"WBC"}, inplace=True, errors='ignore')

    if 'Sex' in lepto_df.columns:
        lepto_df["Sex"] = lepto_df["Sex"].replace({'Female Spay': 0, 'Female': 0, 'Male': 1, 'Male Castrate': 1 })
    if "Urine Glucose" in lepto_df.columns:
        lepto_df['Urine Glucose'] = lepto_df['Urine Glucose'].apply(lambda x: convert_ua_for_lepto_clf(x, 'Urine Glucose'))
    if "Urine Protein" in lepto_df.columns:
        lepto_df['Urine Protein'] = lepto_df['Urine Protein'].apply(lambda x: convert_ua_for_lepto_clf(x, 'Urine Protein'))

    lepto_cols = list(lepto_d.keys())
    lepto_cols.extend(testid_cols)
    lepto_testid_cols = basic_cols + basicdate_cols + testid_cols + testdate_cols
    present_in_df_columns = [element in list(lepto_df.columns) for element in lepto_cols]
    if all(present_in_df_columns) == True: # Check if all required 
        lepto_df.dropna(axis=0, subset=lepto_cols, inplace=True)
        lepto_testids = lepto_df[lepto_testid_cols]
        lepto_testids = lepto_testids.loc[:,~lepto_testids.columns.duplicated()].copy()
        if use_mat:
            lepto_df = lepto_df[lepto_order_cols_with_MAT]
        else:
            lepto_df = lepto_df[lepto_order_cols_without_MAT]
    else:
        lepto_df = pd.DataFrame()
        lepto_testids = pd.DataFrame()
    return lepto_df, lepto_testids

def convert_ua_for_lepto_clf(value, col):
    if col == 'Urine Glucose':
        try:
            if value is None:
                return None
            elif value == 'neg':
                return 0
            elif value == 'Negative':
                return 0
            elif int(value) == 0:
                return 0
            elif 1 <= int(value) <= 50:
                return 1
            elif 51 <= int(value) <= 100:
                return 2
            elif 101 <= int(value) <= 500:
                return 3
            elif  501 <= int(value):
                return 4
            else:
                print('Unable to determine urine glucose conversion, value given: {}'.format(value))
                return None
        except:
            return None
    elif col == 'Urine Protein':
            try:
                if value is None:
                    return None
                elif value == 'neg':
                    return 0
                elif value == 'Negative':
                    return 0
                elif int(value) == 0:
                    return 0
                elif 1 <= int(value) <= 75:
                    return 1
                elif 76 <= int(value) <= 100:
                    return 2
                elif 101 <= int(value) <= 150:
                    return 3
                elif 151 <= int(value):
                    return 4
                else:
                    print('Unable to determine urine protein conversion, value given: {}'.format(value))
                    return None
            except:
                return None

# Data Merge
def df_merge(result_dict, date, micro_need=False, immu_need=False):
    # This version consider +- 7 days of Lepto MAT Test:
    # Hence the Microbiology is Time-Series
    # This also consider Immunology DatFrame
    # The Preprocessing of Microbiology happens here:
    # Basically Not Merging MICRO at this stage
    hostname = platform.node()
    date = datetime.strptime(date, '%Y-%m-%d').date()
    # Need to check colunm name:
    UA_cols = ['PatientID', 'Breed', 'Sex', 'Age', 'Weight', 'Date', 'Procedures', 'Procedures_group', 'TestID', 
               'Color', 'Clarity', 'SPECIFIC_GRAVITY', 'PH_URINE', 'PROTEIN_URINE',
               'GLUCOSE_URINE', 'KETONES_URINE', 'BILIRUBIN_URINE',
               'HEMOPROTEIN_URINE', 'SEDIMENT_VOLUME', 'VOLUME_URINE', 'LIPID_LAYER', 'WBC_URINE',
               'RBC_URINE', 'CYRSTALS_URINE', 'CREATININE_URINE', 'TP_QUANT_URINE', 'URINE_PC_RATIO',
               'EPITHELIAL_CELLS_TRANSITIONAL','EPITHELIAL_CELLS_SQUAMOUS', 'EPITHELIAL_CELLS_RENAL',
               'EPITHELIAL_CELLS_CAUDATE', 'CASTS_HYALINE', 'CAST_GRANULAR',
               'CAST_WAXY', 'CAST_CELLULAR', 'BACTERIA', 'LIPID_DROPLETS', 'SPERM',
               'OTHER']

    CHEM_cols = ['PatientID', 'Breed', 'Sex', 'Age', 'Weight', 'Date', 'Procedures', 'Procedures_group', 'TestID',
                 'Albumin', 'Alkaline_Phosphatase', 'ALT', 'AST', 'Bilirubin_Total', 'BUN', 'Calcium', 'Magnesium', 'Cholesterol',
                 'Creatine_Kinase', 'Creatinine', 'GGT', 'Globulin', 'Glucose', 'Hemolysis_Index', 'Icteric_Index',
                 'Lipemic_Index', 'Phosphorus', 'Total_Protein', 'Anion_Gap', 'Chloride', 'Sodium', 'Potassium', 'HCO3',
                 'Folate_Immulite', 'Creatine_KinaseOld']

    CBC_cols = ['Sex', 'Age', 'Weight', 'Date', 'Procedures',
                'Procedures_group', 'TestID', 'RBC', 'Hgb', 'Hct', 'MCV', 'MCH',
                'MCHC', 'RDW', 'RBC_Morphology', 'WBCCorr', 'WBC', 'Neut', 'Lymph', 'Mono',
                'Eosin', 'Plt', 'Plt_Comment', 'MPV', 'Protein', 'Result_Comment', 'Retic', 'Bands', 'NRBC', 'Baso']


    chemua_exclude = ['TestID.1', 'Name', 'Species', 'Specimen', 'Clinical_Diagnosis']
    cbc_exclude = ['PatientID', 'Breed', 'Species', 'Specimen', 'Clinical_Diagnosis']


    ### CBC
    cbc_df = pd.DataFrame.from_dict(result_dict['cbc'])
    if len(cbc_df) == 0:
        cbc_df = pd.DataFrame()
    else:
        cbc_df = cbc_df.loc[:, ~cbc_df.columns.isin(cbc_exclude)]
        cbc_df = cbc_df[cbc_df.columns.intersection(set(CBC_cols))]
        rename_cols_cbc = {"Breed":"Breed_cbc", "VisitID":"VisitID_cbc", "TestID":"TestID_cbc", 
                           "Procedures":"Procedures_cbc", "Sex":"Sex_cbc", "Weight":"Weight_cbc",
                           "Age":"Age_cbc",	"Species": "Species_cbc", "Report_Status":"Report_Status_cbc",
                           "Date":"Date_cbc"}
        for col in rename_cols_cbc.keys():
            if col in cbc_df.columns:
                cbc_df.rename(columns={col:rename_cols_cbc[col]}, inplace=True)

    ### CHEMUA
    chem_ua_df = pd.DataFrame.from_dict(result_dict['chemua'])
    if len(chem_ua_df) == 0:
        chem_ua_df = pd.DataFrame()
        chem_df = pd.DataFrame()
        ua_df = pd.DataFrame()
    else:
        chem_ua_df = chem_ua_df.loc[:, ~chem_ua_df.columns.isin(chemua_exclude)]
        chem_df, ua_df = chem_ua_split(chem_ua_df)
        chem_df = chem_df[chem_df['Date'] == date]
        rename_cols_chem = {"Breed":"Breed_chem", "VisitID":"VisitID_chem", "TestID":"TestID_chem", "Procedures":"Procedures_chem", "Sex":"Sex_chem", "Weight":"Weight_chem",
                       "Age":"Age_chem", "Species": "Species_chem", "Report_Status":"Report_Status_chem","Date":"Date_chem", "Bili Total": "Bilirubin"}
        for col in rename_cols_chem.keys():
            if col in chem_df.columns:
                chem_df.rename(columns={col:rename_cols_chem[col]}, inplace=True)
        rename_cols_ua = {"Breed":"Breed_ua", "VisitID":"VisitID_ua", "TestID":"TestID_ua", "Procedures":"Procedures_ua", "Sex":"Sex_ua", "Weight":"Weight_ua",
                           "Age":"Age_ua", "Species": "Species_ua", "Report_Status":"Report_Status_ua","Date":"Date_ua"}
        for col in rename_cols_ua.keys():
            if col in ua_df.columns:
                ua_df.rename(columns={col:rename_cols_ua[col]}, inplace=True)
    ### MICROBIOLOGY
    if micro_need == True:
        micro_df = pd.DataFrame.from_dict(result_dict['micro'])
        if len(micro_df) == 0:
            micro_df = pd.DataFrame()
        else:
            micro_df = micro_immu_procedure_filter(micro_df)
            rename_cols_micro = {"VisitID":"VisitID_mat", "TestID":"TestID_mat", "Procedures":"Procedures_mat",
                            "Report_Status":"Report_Status_mat","Date":"Date_mat",
                            "Collected_Datetime":"Collected_Datetime_mat"}
            for col in rename_cols_micro.keys():
                if col in micro_df.columns:
                    micro_df.rename(columns={col:rename_cols_micro[col]}, inplace=True)
    ### IMMUNOLOGY
    if immu_need == True:
        immu_df = pd.DataFrame.from_dict(result_dict['immunology'])
        if len(immu_df) == 0:
            immu_df = pd.DataFrame()
            immu_df_concat = pd.DataFrame()
        else:
            immu_df = micro_immu_procedure_filter(immu_df)
            df_8780, df_8615 = immu_df_split(immu_df)
            if (len(df_8780) == 0) and (len(df_8615) > 0):
                immu_df_concat = df_8615
            elif (len(df_8780) > 0) and (len(df_8615) == 0):
                immu_df_concat = df_8780
            elif (len(df_8780) == 0) and (len(df_8615) == 0):
                immu_df_concat = pd.DataFrame()
            else:
                immu_df_concat = df_8780.merge(df_8615, how='cross')
            rename_cols_immu = {"VisitID":"VisitID_immu", "TestID":"TestID_immu", "Procedures":"Procedures_mat",
                                "Report_Status":"Report_Status_immu","Date":"Date_immu",
                                "Collected_Datetime":"Collected_Datetime_immu"}
            for col in rename_cols_immu.keys():
                if col in immu_df.columns:
                    immu_df.rename(columns={col:rename_cols_immu[col]}, inplace=True)

    if len(cbc_df) == 0:
        # Only CHEMUA is captured.
        final_merge = chem_df.merge(right=ua_df, left_on='Date_chem', right_on='Date_ua', how='outer')
    if len(chem_ua_df) == 0:
        final_merge = cbc_df
    else:
        cbc_chem = cbc_df.merge(chem_df, left_on="Date_cbc", right_on="Date_chem", how='inner')
        if isinstance(ua_df, pd.DataFrame) and len(ua_df) > 0:
            final_merge = cbc_chem.merge(ua_df, how="cross")
        else:
            final_merge = cbc_chem
        if micro_need == False and immu_need == False:
            pass
        else:
            if (len(micro_df) > 0) and (len(immu_df_concat) == 0):
                micro_immu_df = micro_df
            elif (len(micro_df) == 0) and (len(immu_df_concat) > 0):
                micro_immu_df = immu_df_concat
            elif (len(micro_df) > 0) and (len(immu_df_concat) > 0):
                micro_immu_df = micro_df.merge(immu_df_concat, how='cross')
            else:
                micro_immu_df = pd.DataFrame()

            # Final Merge
            final_merge = final_merge.merge(micro_immu_df, how='cross')


            for col in divergent_var_rename_dict.keys():
                if col in final_merge.columns:
                    final_merge.rename(columns={col:divergent_var_rename_dict[col]}, inplace=True)
            for col in ["Sex_cbc", "Sex_chem", 'Sex_ua']:
                if col in final_merge.columns:
                    final_merge.rename(columns={col:'Sex'}, inplace=True)
            for col in ["Weight_cbc", "Weight_chem", 'Weight_ua']:
                if col in final_merge.columns:
                    final_merge.rename(columns={col:'Weight'}, inplace=True)
            for col in ["Breed_cbc", "Breed_chem", 'Breed_ua']:
                if col in final_merge.columns:
                    final_merge.rename(columns={col:'Breed'}, inplace=True)
            for col in ["Age_cbc", "Age_chem", 'Age_ua']:
                if col in final_merge.columns:
                    final_merge.rename(columns={col:'Age'}, inplace=True)
            final_merge = final_merge.loc[:,~final_merge.columns.duplicated()].copy()
            
    final_merge = df_merge_string_clean(final_merge)
    return final_merge

# MySQL Implementation
def lepto_result_database_write_sql(patientid, prediction, testid_cbc, date_cbc, testid_chem, date_chem, testid_ua, date_ua, testid_mat, date_mat, testid_leptoPCR, date_leptoPCR, testid_leptoLF, date_leptoLF):
    host_ip = "localhost"
    sql_username = os.getenv("ANNA_FULL_SQL_USERNAME")
    sql_password = os.getenv("ANNA_FULL_SQL_PASSWORD")
    
    mydb = MySQLdb.connect(host=host_ip,
                          user=sql_username,
                          password=sql_password,
                          database="classifier_firstrun")
    timenow = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
    # Modify Datetime Object to string
    date_cbc = [x.strftime('%Y-%m-%d') if isinstance(x, datetime.date) else x for x in date_cbc]
    date_chem = [x.strftime('%Y-%m-%d') if isinstance(x, datetime.date) else x for x in date_chem]
    date_ua = [x.strftime('%Y-%m-%d') if isinstance(x, datetime.date) else x for x in date_ua]
    date_mat = [x.strftime('%Y-%m-%d') if isinstance(x, datetime.date) else x for x in date_mat]
    date_leptoPCR = [x.strftime('%Y-%m-%d') if isinstance(x, datetime.date) else x for x in date_leptoPCR]
    date_leptoLF = [x.strftime('%Y-%m-%d') if isinstance(x, datetime.date) else x for x in date_leptoLF]
    classifier_timestamp_list = []
    for i in range(len(prediction)):
        try:
            c=mydb.cursor()
            tmp_testid_cbc = testid_cbc[i]
            tmp_testid_chem = testid_chem[i]
            tmp_testid_ua = testid_ua[i]
            check_int = c.execute("""SELECT * FROM leptospirosis_firstrun WHERE TestID_cbc = %s and TestID_chem = %s and TestID_ua = %s""", 
                                  (tmp_testid_cbc, tmp_testid_chem, tmp_testid_ua))
            if check_int == 0: # return 0 rows of data from SQL statments.
                data = [(timenow, patientid, prediction[i], testid_cbc[i], date_cbc[i], 
                         testid_chem[i], date_chem[i], testid_ua[i], date_ua[i], testid_mat[i], date_mat[i], 
                         testid_leptoPCR[i], date_leptoPCR[i], testid_leptoLF[i], date_leptoLF[i])]
                c.executemany("""INSERT INTO leptospirosis_firstrun 
                              (ClassifierFirstRunDateTime, PatientID, Prediction,
                            TestID_cbc, Date_cbc, TestID_chem, Date_chem, TestID_ua, Date_ua,
                            TestID_mat, Date_mat, TestID_leptoPCR, Date_leptoPCR, TestID_leptoLF, Date_leptoLF) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data)
            
                mydb.commit()
                classifier_timestamp_list.append(timenow)
            else:
                tmp_data = pd.DataFrame(c.fetchall(), columns=[i[0] for i in c.description])
                classifier_timestamp_list.append(tmp_data["ClassifierFirstRunDateTime"].iloc[0])
                # do nothing
        except:
            logging.debug("{}".format(traceback.format_exc()))
        finally:
            c.close()# Close the cursor
    mydb.close() #Close the connection
    return classifier_timestamp_list

def tommy_result_database_write_sql(patientid, prediction, testid_cbc, date_cbc, testid_chem, date_chem):
    host_ip = "localhost"
    sql_username = os.getenv("ANNA_FULL_SQL_USERNAME")
    sql_password = os.getenv("ANNA_FULL_SQL_PASSWORD")

    mydb = MySQLdb.connect(host=host_ip,
                          user=sql_username,
                          password=sql_password,
                          database="classifier_firstrun")
    timenow = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
    date_cbc = [x.strftime('%Y-%m-%d') if isinstance(x, datetime.date) else x for x in date_cbc]
    date_chem = [x.strftime('%Y-%m-%d') if isinstance(x, datetime.date) else x for x in date_chem]
    classifier_timestamp_list = []
    for i in range(len(prediction)):
        try:
            # input is list:
            c=mydb.cursor()
            tmp_testid_cbc = testid_cbc[i]
            tmp_testid_chem = testid_chem[i]
            check_int = c.execute("""SELECT * FROM tommypy_firstrun WHERE Testid_cbc = %s and TestID_chem = %s""",
                                  (tmp_testid_cbc, tmp_testid_chem))
            if check_int == 0: # When there is no matching result from database, meaning it is firstrun:
                data = [(timenow, patientid, prediction[i], testid_cbc[i], date_cbc[i], testid_chem[i], date_chem[i])]
                c.executemany("""INSERT INTO tommypy_firstrun (ClassifierFirstRunDateTime, PatientID, Prediction,
                        TestID_cbc, Date_cbc, TestID_chem, Date_chem) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""", data)
                mydb.commit()
                classifier_timestamp_list.append(timenow)
            else:
                tmp_data = pd.DataFrame(c.fetchall(), columns=[i[0] for i in c.description])
                classifier_timestamp_list.append(tmp_data["ClassifierFirstRunDateTime"].iloc[0])
                # do nothing but to obtain timestamp from MySQL.
        except:
            logging.debug("{}".format(traceback.format_exc()))
        finally:
            c.close()# Close the cursor
    mydb.close() #Close the connection
    return classifier_timestamp_list
