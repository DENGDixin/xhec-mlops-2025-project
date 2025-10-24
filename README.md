# 🦪 Abalone Age Prediction - MLOps Project

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Managed with UV](https://img.shields.io/badge/managed%20with-uv-blue)](https://github.com/astral-sh/uv)

A complete MLOps project for predicting abalone age using physical measurements. Built with modern ML engineering practices including experiment tracking (MLflow), workflow orchestration (Prefect), web services (FastAPI + Streamlit), and containerization (Docker).

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Training the Model](#training-the-model)
  - [Running Predictions](#running-predictions)
  - [Running the Web Application](#running-the-web-application)
  - [Using Prefect Workflows](#using-prefect-workflows)
- [Docker Deployment](#docker-deployment)
- [Development](#development)
- [Tech Stack](#tech-stack)
- [Author](#author)

## 🎯 Overview

This project predicts the age of abalone (sea snails) based on physical measurements such as length, diameter, height, and various weights. The project demonstrates end-to-end MLOps practices including:

- **Data Processing**: Feature engineering and preprocessing pipelines
- **Model Training**: Ridge regression with outlier handling
- **Experiment Tracking**: MLflow integration for tracking experiments and models
- **Workflow Orchestration**: Prefect for automated training and prediction flows
- **Model Serving**: FastAPI backend and Streamlit frontend for interactive predictions
- **Containerization**: Docker-based deployment
- **Code Quality**: Pre-commit hooks, Ruff linting, and proper documentation

## ✨ Features

- 🔄 **Automated ML Pipeline**: End-to-end training and prediction workflows
- 📊 **Experiment Tracking**: MLflow integration for model versioning and metrics
- 🚀 **REST API**: FastAPI service for programmatic access
- 🎨 **Web Interface**: Interactive Streamlit dashboard for predictions
- 📦 **Containerized**: Docker deployment with both services
- 🛠️ **Modern Tooling**: UV for dependency management, Ruff for linting
- ✅ **Code Quality**: Pre-commit hooks and type annotations
- 📝 **Well Documented**: Comprehensive docstrings and documentation

## 📁 Project Structure

```
xhec-mlops-2025-project/
├── .github/
│   └── workflows/
│       └── ci.yaml                      # CI/CD pipeline
├── assets/
│   ├── automated_pipeline.png
│   ├── deployment_registered.png
│   ├── flow_run_success.png
│   ├── local_objects_output.png
│   └── prefect_dashboard.png
├── bin/
│   └── run_services.sh                  # Startup script for FastAPI + Streamlit
├── data/
│   └── abalone.csv                      # Dataset
├── docs/
│   └── prefect_tutorial.md              # Prefect workflow guide
├── notebooks/
│   ├── eda.ipynb                        # Exploratory data analysis
│   └── modelling.ipynb                  # Model development experiments
├── src/
│   ├── flows/
│   │   └── training_flow.py            # Prefect workflow orchestration
│   ├── modelling/
│   │   ├── __init__.py
│   │   ├── predicting.py               # Prediction logic
│   │   ├── preprocessing.py            # Data preprocessing pipeline
│   │   ├── training.py                 # Model training logic
│   │   └── utils.py                    # Shared utilities
│   └── web_service/
│       ├── lib/
│       │   └── models.py               # Pydantic data models
│       ├── local_objects/
│       │   ├── meta__v0.0.1.json       # Model metadata
│       │   ├── pipeline__v0.0.1.joblib # Trained model pipeline
│       │   └── predictions.csv          # Prediction outputs
│       ├── main.py                     # FastAPI application
│       ├── streamlit_app.py            # Streamlit web interface
│       └── utils.py
├── .gitignore
├── .pre-commit-config.yaml              # Pre-commit hooks configuration
├── .prefectignore
├── abalone_deploy.yaml                  # Prefect deployment configuration
├── Dockerfile.app                       # Docker image definition
├── pyproject.toml                       # Project dependencies & config
├── README.md
└── uv.lock                              # UV dependency lock file
```

## 🚀 Installation

### Prerequisites

- Python 3.11
- [UV](https://github.com/astral-sh/uv)

### Using UV

```powershell
# Install UV if you haven't already
pip install uv

# Clone the repository
git clone https://github.com/DENGDixin/xhec-mlops-2025-project.git
cd xhec-mlops-2025-project

# Install dependencies
uv sync
```


## 💻 Usage

### Training the Model

Train the Ridge regression model with outlier removal and preprocessing:

```powershell
# Using UV
uv run python -m src.modelling.training

# Or directly with Python
python -m src.modelling.training
```

This will:
- Load and preprocess the abalone dataset
- Split data into train/validation sets
- Remove outliers (Height > 0.35) from training data
- Train a Ridge regression model
- Save the pipeline to `src/web_service/local_objects/pipeline__v0.0.1.joblib`
- Generate metadata and evaluation metrics

### Running Predictions

Generate predictions on the dataset:

```powershell
uv run python -m src.modelling.predicting
```

This creates `predictions.csv` with predicted ages for all samples.

### Using Prefect Workflows

Run the complete training and prediction flow with Prefect:

```powershell
# Run the flow directly
uv run python src/flows/training_flow.py

# Or deploy and schedule with Prefect
prefect deploy --name abalone_local -p abalone_deploy.yaml
```

The flow will:
1. Train the model and save artifacts
2. Generate predictions on the dataset
3. Track all steps with Prefect UI

📖 **For detailed Prefect setup and usage instructions, see [Prefect Tutorial](docs/prefect_tutorial.md)**

### Running the Web Application

#### Option 1: Run Services Separately

**Terminal 1 - FastAPI Backend:**
```powershell
uv run uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Streamlit Frontend:**
```powershell
uv run streamlit run src/web_service/streamlit_app.py
```

- FastAPI will be available at: http://localhost:8001
- Streamlit dashboard at: http://localhost:8501
- API documentation at: http://localhost:8001/docs

#### Option 2: Using Docker (Recommended)

See [Docker Deployment](#docker-deployment) section below.

## 🐳 Docker Deployment

Build and run the entire application with Docker:

```powershell
# Build the Docker image
docker build -f Dockerfile.app -t abalone-app .

# Run the container
docker run -p 8001:8001 -p 8501:8501 abalone-app
```

Access the services:
- **FastAPI**: http://localhost:8001
- **Streamlit**: http://localhost:8501

## 🛠️ Development

### Setting Up Development Environment

```powershell
# Install with dev dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

### Code Quality

This project uses Ruff for linting and formatting:

```powershell
# Run pre-commit checks
uv run pre-commit run --all-files

# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

### Running Tests

```powershell
uv run pytest
```

### MLflow Tracking

View experiment tracking and model registry:

```powershell
mlflow ui --port 5000
```

Then navigate to http://localhost:5000
