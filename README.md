# Delta Data Control

A demonstration project showcasing version-controlled machine learning experiments using DVC (Data Version Control) with k-means clustering on temperature data.

## 📖 Introduction

This is an example project demonstrating best practices for reproducible machine learning workflows. The focus is on **tooling and workflow reproducibility** rather than scientific complexity. The project uses real climate data from NOAA weather stations to perform k-means clustering on temperature patterns, illustrating how to version-control experiments, manage data artifacts, and track pipeline execution.

## 🎯 Project Overview

The project implements a three-stage data pipeline:

1. **Data Collection** (`collect_data`) - Fetches historical temperature data from NOAA weather stations
2. **Data Processing** (`process_data`) - Performs k-means clustering on temperature data and computes quality metrics
3. **Visualization** (`visualize_results`) - Creates plots showing climate clusters and performance metrics

All stages are orchestrated through DVC with parameters managed in `params.toml`. The pipeline automatically tracks dependencies, ensuring reproducibility and efficient caching.

### Project Structure

```
delta-data-control/
├── src/
│   ├── collection.py      # Data collection stage
│   ├── process.py         # Clustering and metrics
│   └── visualize.py       # Visualization stage
├── data/
│   ├── input.txt          # Generated temperature data
│   ├── metrics.json       # Clustering quality metrics
│   └── image.png          # Cluster visualization
├── params.toml            # Experiment parameters
├── dvc.yaml               # Pipeline definition
├── dvc.lock               # Pipeline state 
├── pyproject.toml         # Project dependencies
├── uv.lock                # uv lock file
└── README.md              # Documentation
```

## 📋 Requirements

### Package Manager
- **[uv](https://docs.astral.sh/uv/)** - Fast Python package and project manager

### Version Control
- **[Git](https://git-scm.com/)** - Distributed version control for code
- **[DVC](https://dvc.org/)** - Data Version Control for data and model artifacts

## ⚙️ DVC Setup

### Basic Setup

Initialize DVC in the project (already configured):

```cmd
dvc init
```

### Configure Remote Storage (MinIO)

This project uses a self-hosted MinIO bucket for remote storage. To configure it:

#### Step 1: Add DVC remote
```cmd
dvc remote add -d minio s3://field-data-flows/delta-data-control
```

#### Step 2: Configure MinIO endpoint

Replace `{YOUR_MINIO_URL}` with your MinIO server address:
```cmd
dvc remote modify minio endpointurl https://your-minio-server.com:9000
```

**Security Note:** If using an internal/private MinIO instance, be cautious about sharing this URL publicly.


#### Step 3: Add credentials (stored locally, not committed)
```cmd
dvc remote modify --local minio access_key_id {YOUR_ACCESS_KEY}
dvc remote modify --local minio secret_access_key {YOUR_SECRET_KEY}
```

#### Step 4: Configure S3 connection settings
```cmd
dvc remote modify minio ssl_verify false
dvc remote modify --local minio read_timeout 60
dvc remote modify --local minio connect_timeout 60
```

#### Step 5: Test the connection

To actually test the connection to MinIO:
```cmd
dvc push
```

If credentials or connection fails, you'll get an error. If successful (or says nothing to push), your connection is working.

**Credential Storage Options:**
- `.dvc/config.local` - Automatically gitignored (recommended for security)
- `.env` file - Use with `python-dotenv` in scripts (also add to `.gitignore`)
- Windows environment variables - System-wide, persistent

**Never commit credentials to Git or include them in `.dvc/config`.**

## 🚀 Quick Start

### Installation

```cmd
uv sync
```

### Run the Full Pipeline

Execute all stages in sequence:

```cmd
dvc repro
```

This will:
1. Collect synthetic temperature data
2. Run k-means clustering and compute metrics
3. Generate visualization plots

### Run Individual Stages

To run specific stages without executing the full pipeline:

```cmd
# Run only data collection
uv run src/collection.py

# Run only data processing
uv run src/process.py

# Run only visualization
uv run src/visualize.py
```

### View Pipeline Status

```cmd
dvc status      # Check which stages need re-running
dvc dag         # Visualize the pipeline DAG
```

## 📚 More Information

### Configuration Parameters

Edit `params.toml` to modify experiment behavior:

```toml
[data]
# NOAA Climate Data API endpoint
url = "https://www.ncei.noaa.gov/access/services/data/v1"
dataset = "daily-summaries"
# Sample US weather stations
stations = ["USW00094728", "USW00023174", "USW00013874", "USW00012960", "USW00003017"]
start_date = "2023-01-01"
end_date = "2023-12-31"
# Temperature data fields
dataTypes = ["TMAX", "TMIN"]

[clustering]
n_clusters = 3
random_state = 42
max_iter = 300
n_init = 10

[visualization]
# Plot settings
figure_width = 12
figure_height = 8
dpi = 300
colormap = "viridis"

[output]
input_data = "data/input.txt"
metrics_file = "data/metrics.json"
visualization = "data/image.png"
```

After modifying parameters, run `dvc repro` to re-execute affected stages.

**Key Parameters:**
- `stations` - NOAA weather station IDs to fetch data from
- `start_date` / `end_date` - Date range for historical data
- `dataTypes` - Temperature metrics (TMAX, TMIN)
- `n_clusters` - Number of climate clusters for k-means
- `dpi` - Resolution of visualization output

### Pipeline Outputs

- **data/input.txt** - Historical temperature data from NOAA weather stations (TMAX and TMIN for selected date range)
- **data/metrics.json** - Clustering quality metrics (silhouette score, Davies-Bouldin index, etc.)
- **data/image.png** - Cluster visualization showing temperature patterns across regions

### Version Control Strategy

#### What Goes to Git
- ✅ Python scripts (`src/*.py`)
- ✅ Configuration (`params.toml`)
- ✅ Pipeline definition (`dvc.yaml`, `dvc.lock`)
- ✅ DVC metadata (`.dvc/config`, `.gitignore`)
- ✅ Project files (`pyproject.toml`, `README.md`)

#### What Goes to DVC
- ✅ Data files (`data/input.txt`)
- ✅ Metrics and outputs (`data/metrics.json`, `data/image.png`)
- ✅ Large datasets and model artifacts

#### What Gets Ignored
- ❌ Virtual environment
- ❌ Python cache (`__pycache__/`, `*.pyc`)
- ❌ Credentials and secrets (`.dvc/config.local`)

### Experiment Workflow

Follow this exact order to ensure reproducibility:

```cmd
# 1. Modify parameters or code
# Edit params.toml or src/*.py

# 2. Run the pipeline
dvc repro

# 3. Commit changes to Git
git add params.toml dvc.lock src/
git commit -m "Experiment: adjusted clustering parameters"

# 4. Push data to DVC remote (BEFORE git push)
dvc push

# 5. Push code to GitHub
git push
```

**Important:** Always run `dvc push` before `git push`. This ensures data is backed up to MinIO before Git metadata references it.
