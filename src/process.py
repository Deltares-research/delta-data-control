"""
Processing Module
Runs K-Means clustering on temperature data and stores metrics
"""

import tomllib
import csv
import json
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


def run_kmeans_analysis():
    """
    Performs K-Means clustering on temperature data.
    Stores clustering metrics for evaluation and reproducibility.
    
    Returns:
        dict: Dictionary containing clustering metrics and results
    """
    # Load configuration
    with open("params.toml", "rb") as f:
        config = tomllib.load(f)
    
    print("Loading configuration...")
    clustering_config = config["clustering"]
    output_config = config["output"]
    
    # Load input data
    print(f"Reading data from {output_config['input_data']}...")
    data = []
    with open(output_config["input_data"], "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append([
                float(row["avg_temp_celsius"]),
                float(row["temp_variance"])
            ])
    
    X = np.array(data)
    print(f"Loaded {len(X)} samples with {X.shape[1]} features")
    
    # Run K-Means clustering
    print(f"Running K-Means with {clustering_config['n_clusters']} clusters...")
    kmeans = KMeans(
        n_clusters=clustering_config["n_clusters"],
        random_state=clustering_config["random_state"],
        max_iter=clustering_config["max_iter"],
        n_init=clustering_config["n_init"]
    )
    
    labels = kmeans.fit_predict(X)
    
    # Calculate clustering metrics
    print("Calculating metrics...")
    metrics = {
        "algorithm": "K-Means",
        "n_clusters": clustering_config["n_clusters"],
        "n_samples": int(len(X)),
        "n_features": int(X.shape[1]),
        "random_state": clustering_config["random_state"],
        
        # Quality metrics
        "inertia": float(kmeans.inertia_),
        "silhouette_score": float(silhouette_score(X, labels)),
        "davies_bouldin_score": float(davies_bouldin_score(X, labels)),
        "calinski_harabasz_score": float(calinski_harabasz_score(X, labels)),
        
        # Cluster information
        "cluster_centers": kmeans.cluster_centers_.tolist(),
        "cluster_sizes": [int(np.sum(labels == i)) for i in range(clustering_config["n_clusters"])],
        
        # Labels for visualization
        "labels": labels.tolist(),
        "data_points": X.tolist()
    }
    
    # Save metrics
    metrics_path = output_config["metrics_file"]
    Path(metrics_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\nMetrics saved to {metrics_path}")
    print(f"  - Silhouette Score: {metrics['silhouette_score']:.3f} (higher is better, range: -1 to 1)")
    print(f"  - Davies-Bouldin Score: {metrics['davies_bouldin_score']:.3f} (lower is better)")
    print(f"  - Calinski-Harabasz Score: {metrics['calinski_harabasz_score']:.3f} (higher is better)")
    print(f"  - Inertia: {metrics['inertia']:.2f}")
    
    print(f"\nCluster sizes: {metrics['cluster_sizes']}")
    
    return metrics


if __name__ == "__main__":
    run_kmeans_analysis()
