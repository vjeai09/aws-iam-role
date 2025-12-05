# Python Script: Download and Verify Fraud Detection Datasets from Kaggle
# Author: Grok (xAI) - For FinTech Fraud Ring Detection Use Case
# Date: December 05, 2025
#
# Purpose:
# 1. Download specified Kaggle datasets (requires Kaggle API setup).
# 2. Verify suitability for fraud detection pipeline:
#    - Check shape (rows/cols for scale).
#    - Inspect columns (e.g., sender/receiver/amount/time for graphs).
#    - Check fraud imbalance (% fraud labels).
#    - Sample data quality (nulls, dtypes).
#    - Graph potential (unique accounts, edge density).
#
# Prerequisites:
# - Install: pip install kaggle pandas numpy networkx
# - Kaggle API: pip install kaggle; kaggle.json in ~/.kaggle/ (from Kaggle > Account > API).
# - Run: python fraud_dataset_downloader.py
#
# Datasets (from your list):
# 1. PaySim (primary: synthetic mobile txns, fraud rings).
# 2. Bank Transaction Dataset.
# 3. Financial Fraud Detection.
# 4. Credit Card Fraud (PCA features, no direct graph).
# 5. BAF (if downloadable; else skip).
# 6. USA Banking (search-based; adapt if needed).

import os
import pandas as pd
import numpy as np
import networkx as nx
from kaggle.api.kaggle_api_extended import KaggleApi
import warnings
warnings.filterwarnings('ignore')

# Initialize Kaggle API
api = KaggleApi()
api.authenticate()

# Define datasets: [kaggle_dataset_slug, file_name, expected_cols_snippet]
DATASETS = [
    # 1. PaySim
    ('ealaxi/paysim1', 'PS_20174392719_1491204439457_log.csv', 
     ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 
      'nameDest', 'oldbalanceDest', 'newbalanceDest', 'isFraud']),
    
    # 2. Bank Transaction Dataset
    ('valakhorasani/bank-transaction-dataset-for-fraud-detection', 'bank_transactions.csv',
     ['TransactionID', 'CustomerID', 'TransactionDate', 'Amount', 'TransactionType', 'FraudFlag']),  # Adapt if cols differ
    
    # 3. Financial Fraud Detection
    ('sriharshaeedala/financial-fraud-detection-dataset', 'financial_fraud_dataset.csv',
     ['Unnamed: 0', 'cc_num', 'category', 'amt', 'gender', 'street', 'lat', 
      'long', 'city_pop', 'job', 'dob', 'trans_num', 'unix_time', 'merch_lat', 
      'merch_long', 'is_fraud']),  # Note: 'cc_num' as sender proxy
    
    # 4. Credit Card Fraud
    ('mlg-ulb/creditcardfraud', 'creditcard.csv',
     ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
      'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 
      'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount', 'Class']),
    
    # 5. BAF (Bank Account Fraud) - Download all; use train.csv
    ('feedzai/bank-account-fraud', 'baf_train.csv',  # Or check files post-download
     ['accountID', 'label', 'date', 'transactionID', 'amount', 'transactionType']),  # Hypothetical; inspect after
    
    # 6. USA Banking - Not direct Kaggle slug; skip or manual download. Use PaySim as proxy.
    # For now, omit; add manual if needed.
]

def download_dataset(slug, file_name):
    """Download single dataset/file."""
    try:
        # Download the file (it will be zipped)
        api.dataset_download_file(slug, file_name, path='./data/')
        
        # Unzip manually if needed
        import zipfile
        zip_path = f'./data/{file_name}.zip'
        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('./data/')
            os.remove(zip_path)
        
        print(f"Downloaded: {slug}/{file_name}")
        return True
    except Exception as e:
        print(f"Error downloading {slug}: {e}")
        return False

def load_and_verify(df_path, expected_cols):
    """Load CSV, verify for use case."""
    try:
        df = pd.read_csv(df_path, nrows=1000000)  # Sample 1M for speed; full later
        print(f"\n--- Verifying {df_path} ---")
        print(f"Shape: {df.shape} (Rows: {df.shape[0]:,}, Cols: {df.shape[1]})")
        
        # Cols check
        print(f"Columns: {list(df.columns)}")
        graph_cols = ['sender', 'receiver']  # Adapt names
        if any(col in df.columns for col in ['nameOrig', 'nameDest', 'cc_num', 'CustomerID']):
            graph_cols = ['nameOrig', 'nameDest'] if 'nameOrig' in df.columns else ['cc_num', 'cc_num']  # Proxy
        print(f"Graph Potential: Has account-like cols? {any(c in df.columns for c in ['nameOrig', 'nameDest', 'cc_num', 'CustomerID'])}")
        
        # Fraud label check
        fraud_col = next((col for col in df.columns if 'fraud' in col.lower() or 'class' in col.lower()), None)
        if fraud_col:
            fraud_rate = (df[fraud_col] == 1).sum() / len(df) * 100
            print(f"Fraud Rate: {fraud_rate:.2f}% (Imbalanced: {'Yes' if fraud_rate < 5 else 'No'})")
        else:
            print("Fraud Label: Missing (Add synthetic?)")
        
        # Data Quality
        null_pct = df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100
        print(f"Null %: {null_pct:.2f}%")
        print(f"Dtypes Sample: {df.dtypes.value_counts()}")
        
        # Graph Suitability (Quick Check)
        if len(graph_cols) == 2 and graph_cols[0] in df.columns and graph_cols[1] in df.columns:
            # Build mini graph (sample 10K rows)
            sample_df = df[['amount', graph_cols[0], graph_cols[1]]].head(10000).dropna()
            G = nx.from_pandas_edgelist(sample_df, source=graph_cols[0], target=graph_cols[1], 
                                        edge_attr='amount', create_using=nx.DiGraph())
            print(f"Graph Stats: Nodes {G.number_of_nodes()}, Edges {G.number_of_edges()}")
            avg_degree = np.mean([d for n, d in G.degree()])
            print(f"Avg Degree: {avg_degree:.1f} (Ring Potential: {'High' if avg_degree > 1 else 'Low'})")
        else:
            print("Graph: Limited (No clear sender/receiver; use time/amount for features)")
        
        # Suitability Score (0-10 for use case)
        score = 10
        if fraud_rate > 10: score -= 2  # Too balanced
        if null_pct > 5: score -= 1
        if avg_degree < 1: score -= 2
        if 'time' not in df.columns and 'step' not in df.columns: score -= 1  # No temporal
        print(f"Use Case Fit (Fraud Rings/Graphs): {score}/10")
        print(f"Recommendation: {'Primary (PaySim-like)' if score >= 8 else 'Secondary/Adapt' if score >= 6 else 'Avoid'}")
        
        return df
    except Exception as e:
        print(f"Error loading {df_path}: {e}")
        return None

def main():
    os.makedirs('./data', exist_ok=True)
    
    for slug, file_name, _ in DATASETS:
        if download_dataset(slug, file_name):
            df_path = f'./data/{file_name}'
            if os.path.exists(df_path):
                load_and_verify(df_path, None)  # expected_cols not used here
    print("\nAll done! Check ./data/ for files. Run full load for production.")

if __name__ == "__main__":
    main()