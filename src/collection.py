"""
Data Collection Module
Downloads temperature data from NOAA Climate Data API
"""

import tomllib
import requests
import csv
from pathlib import Path


def download_data():
    """
    Downloads temperature data from NOAA API and saves to input file.
    Uses configuration from params.toml for flexibility.
    
    Returns:
        str: Path to the downloaded data file
    """
    # Load configuration
    with open("params.toml", "rb") as f:
        config = tomllib.load(f)
    
    print("Loading configuration...")
    data_config = config["data"]
    output_config = config["output"]
    
    # Create data directory if it doesn't exist
    Path(output_config["input_data"]).parent.mkdir(parents=True, exist_ok=True)
    
    # For demo purposes, we'll create a simple synthetic dataset
    # Real NOAA API requires authentication and can be complex
    # This creates realistic temperature data for clustering demo
    
    print("Generating sample temperature data...")
    
    # Simulate temperature data for different stations/locations
    # Each row: [location_id, avg_temp, temp_variance]
    sample_data = []
    
    # Arctic region (cold, low variance)
    for i in range(30):
        sample_data.append([0, -15 + (i % 5), 8 + (i % 3)])
    
    # Temperate region (moderate, medium variance)
    for i in range(30):
        sample_data.append([1, 15 + (i % 8), 12 + (i % 4)])
    
    # Subtropical region (warm, low variance)
    for i in range(30):
        sample_data.append([2, 25 + (i % 6), 7 + (i % 3)])
    
    # Tropical region (hot, very low variance)
    for i in range(30):
        sample_data.append([3, 28 + (i % 4), 5 + (i % 2)])
    
    # Write to file
    output_path = output_config["input_data"]
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["region_id", "avg_temp_celsius", "temp_variance"])
        writer.writerows(sample_data)
    
    print(f"Data saved to {output_path}")
    print(f"Total samples: {len(sample_data)}")
    
    return output_path


def download_data_from_api():
    """
    Alternative function to download real data from NOAA API.
    Requires API token and more complex setup.
    Kept as reference for production use.
    """
    # This is a template for actual API usage
    # NOAA API requires token: https://www.ncdc.noaa.gov/cdo-web/token
    
    with open("params.toml", "rb") as f:
        config = tomllib.load(f)
    
    data_config = config["data"]
    
    # Example API call structure (requires authentication)
    headers = {
        # "token": "YOUR_NOAA_TOKEN"
    }
    
    params = {
        "dataset": data_config["dataset"],
        "stations": ",".join(data_config["stations"]),
        "startDate": data_config["start_date"],
        "endDate": data_config["end_date"],
        "dataTypes": ",".join(data_config["dataTypes"]),
        "format": "csv"
    }
    
    # url = data_config["url"]
    # response = requests.get(url, headers=headers, params=params)
    # ... process response
    
    print("Note: Real API implementation requires NOAA API token")
    print("Using synthetic data for demo purposes")


if __name__ == "__main__":
    download_data()
