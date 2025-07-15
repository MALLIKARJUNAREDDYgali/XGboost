# download_dataset.py

import os
import requests

def download_churn_dataset():
    """
    Downloads the Telco Customer Churn dataset and saves it into the explainxg/data/ folder.
    """
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    save_folder = "explainxg/data"
    save_path = os.path.join(save_folder, "telco_churn.csv")

    try:
        # Create directory if it doesn't exist
        os.makedirs(save_folder, exist_ok=True)

        # Download the CSV file
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Save the file
        with open(save_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Dataset successfully downloaded at: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download dataset: {e}")

if __name__ == "__main__":
    download_churn_dataset()
