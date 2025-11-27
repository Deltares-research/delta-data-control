"""
Visualization Module
Reads clustering metrics and creates visualization
"""

import os
os.environ['MPLBACKEND'] = 'Agg'

import tomllib
import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def visualize_results():
    """
    Reads clustering metrics and creates visualization.
    Generates a comprehensive plot showing clusters, centers, and metrics.
    
    Returns:
        str: Path to the saved visualization
    """
    # Load configuration
    with open("params.toml", "rb") as f:
        config = tomllib.load(f)
    
    print("Loading configuration...")
    output_config = config["output"]
    viz_config = config["visualization"]
    
    # Load metrics
    print(f"Reading metrics from {output_config['metrics_file']}...")
    with open(output_config["metrics_file"], "r") as f:
        metrics = json.load(f)
    
    # Extract data
    X = np.array(metrics["data_points"])
    labels = np.array(metrics["labels"])
    centers = np.array(metrics["cluster_centers"])
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 2, figsize=(viz_config["figure_width"], viz_config["figure_height"]))
    
    # Plot 1: Scatter plot with clusters
    ax1 = axes[0]
    
    scatter = ax1.scatter(
        X[:, 0], X[:, 1],
        c=labels,
        cmap=viz_config["colormap"],
        alpha=0.7,
        s=80,
        edgecolors='w',
        linewidth=0.5
    )
    
    # Plot cluster centers
    ax1.scatter(
        centers[:, 0], centers[:, 1],
        c='red',
        marker='X',
        s=400,
        edgecolors='black',
        linewidth=2.5,
        label='Cluster Centers',
        zorder=10
    )
    
    ax1.set_xlabel('Average Temperature (°C)', fontsize=12)
    ax1.set_ylabel('Temperature Variance', fontsize=12)
    ax1.set_title('K-Means Clustering of Temperature Data', fontsize=14, fontweight='bold', pad=20)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label('Cluster ID', fontsize=10)
    
    # Plot 2: Metrics summary
    ax2 = axes[1]
    ax2.axis('off')
    
    # Create metrics text
    metrics_text = f"""
    CLUSTERING METRICS SUMMARY
    {'='*40}
    
    Algorithm: {metrics['algorithm']}
    Number of Clusters: {metrics['n_clusters']}
    Total Samples: {metrics['n_samples']}
    
    QUALITY METRICS:
    {'─'*40}
    Silhouette Score: {metrics['silhouette_score']:.4f}
      → Range: -1 to 1 (higher is better)
      → Measures cluster cohesion
    
    Davies-Bouldin Score: {metrics['davies_bouldin_score']:.4f}
      → Lower is better
      → Measures cluster separation
    
    Calinski-Harabasz: {metrics['calinski_harabasz_score']:.2f}
      → Higher is better
      → Variance ratio criterion
    
    Inertia: {metrics['inertia']:.2f}
      → Sum of squared distances to centers
    
    CLUSTER DISTRIBUTION:
    {'─'*40}
    """
    
    for i, size in enumerate(metrics['cluster_sizes']):
        center = centers[i]
        metrics_text += f"\n    Cluster {i}: {size} samples"
        metrics_text += f"\n      Center: ({center[0]:.1f}°C, {center[1]:.1f})"
    
    ax2.text(
        0.05, 0.95,
        metrics_text,
        transform=ax2.transAxes,
        fontsize=9,
        verticalalignment='top',
        fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    )
    
    plt.tight_layout()
    
    # Save figure
    output_path = output_config["visualization"]
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(
        output_path,
        dpi=viz_config["dpi"],
        bbox_inches='tight',
        facecolor='white'
    )
    
    print(f"\nVisualization saved to {output_path}")
    print("Done!")
    
    return output_path


if __name__ == "__main__":
    visualize_results()
