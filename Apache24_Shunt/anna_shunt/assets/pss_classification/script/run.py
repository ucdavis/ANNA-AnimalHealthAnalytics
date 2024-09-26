import argparse
import pickle
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model(model_path):
    logger.info(f"Loading model from {model_path}...")
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def preprocess_data(data_path):
    logger.info(f"Loading data from {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        logger.error(f"File not found: {data_path}")
        raise
    except Exception as e:
        logger.error(f"Error occurred while loading data: {e}")
        raise

    # Check if all values are numeric
    numeric_columns = df.select_dtypes(include=['number']).columns
    if len(numeric_columns) != len(df.columns):
        logger.error("All values in the data must be numeric (float or int).")
        raise ValueError("All values in the data must be numeric (float or int).")

    return df

def classify(model_type, data_path):
    model_dir = "../trained_models/"
    if model_type == "pss":
        model_path = model_dir + "pss_model.pkl"
    elif model_type == "subcat":
        model_path = model_dir + "subcat_model.pkl"
    else:
        raise ValueError("Invalid model type. Use 'pss' or 'subcat'.")

    model = load_model(model_path)

    logger.info("Loading and preprocessing data...")
    X = preprocess_data(data_path)

    logger.info("Classifying data...")
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    logger.info("Classification Predictions:")
    result = []
    for prob, pred in zip(probabilities, predictions):
        if (model_type == "pss"):
            label = "positive" if pred == 1 else "negative"
        else:
            if pred == 0:
                label = 'Acquired shunt'
            elif pred == 1:
                label = 'Extrahepatic'
            elif pred == 2:
                label = 'Intrahepatic'
            elif pred == 3:
                label = 'No shunt'
        result.append([prob, pred, label])

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diagnosis and classification of portosystemic shunts.")
    parser.add_argument("--model-type", required=True, choices=["pss", "subcat"], help="Type of classification model.")
    parser.add_argument("--data", required=True, help="Path to the data file.")

    args = parser.parse_args()

    try:
        classification_result = classify(args.model_type, args.data)
        print(classification_result)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print("An error occurred. Please check the logs for more details.")
