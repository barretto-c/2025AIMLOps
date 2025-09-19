# 2025AIMLOps

This repository contains materials and projects related to AI/ML Ops in 2025.

## Setup

### Virtual Environment

To set up a virtual environment for this project:

1. Create the virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:
   ```bash
   python predict_time_to_respond.py
   ```

## Testing

To run the basic tests for data and model:

1. Install pytest (if not already installed):
   ```bash
   pip install pytest
   ```
2. Run the tests:
   ```bash
   pytest
   ```

## MLflow Tracking

This project uses [MLflow](https://mlflow.org/) to track experiments and model runs.

### How to Use MLflow

1. **Run your experiment script** (e.g., `python predict_time_to_respond.py`).
   - MLflow will automatically log runs to the `mlruns/` directory (unless configured otherwise).

2. **Start the MLflow UI** to view and compare runs:
   ```bash
   mlflow ui
   ```
   By default, this will launch a web server at http://localhost:5000 where you can browse experiment results, metrics, and artifacts.

3. **(Optional) Clean up runs**
   - You can safely delete the `mlruns/` directory to remove all run history.

### Advanced MLflow Tips

- **Log additional artifacts**: You can log plots, data files, or any output using `mlflow.log_artifact()`.
- **Log model parameters and metrics**: Use `mlflow.log_param()` and `mlflow.log_metric()` to track hyperparameters and results.
- **Use remote tracking servers**: Configure MLflow to log runs to a remote server or database for team collaboration.
- **Register and serve models**: Use the MLflow Model Registry to manage model versions and deploy models as REST APIs.
- **Compare runs**: In the MLflow UI, select multiple runs to compare metrics, parameters, and artifacts side by side.
- **Integrate with CI/CD**: Automate experiment tracking and model deployment as part of your development workflow.

For more advanced usage, see the [MLflow documentation](https://mlflow.org/docs/latest/index.html).

## Attribution

This project is created and maintained by Clyde Barretto. If you use or reference this work, please attribute it accordingly.