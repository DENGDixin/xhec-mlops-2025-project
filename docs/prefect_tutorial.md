# Prefect Tutorial: Training Flow Deployment Guide

## Objective
Build, run, and deploy the **Abalone Training Flow** using Prefect. This guide walks you through running Prefect locally, registering deployments, starting workers, and triggering flows via the Prefect UI.

---

## Prerequisites

1. **Navigate to repository root:**
   ```bash
   cd path\to\xhec-mlops-2025-project
   ```

2. **Update `abalone_deploy.yaml`:**
   - Open `abalone_deploy.yaml` in the root directory
   - Locate the `path` field (around line 33) and change it to your local repository path:
     ```yaml
     storage: null
     path: D:\Desktop\HEC\Courses\08-ml-ops-artefact\xhec-mlops-2025-project  # ← Change this
     entrypoint: src/flows/training_flow.py:training_flow
     ```
   - **Windows:** Use backslashes (`\`)
   - **macOS/Linux:** Use forward slashes (`/`)

3. **Configure Prefect API connection (one-time setup):**
   ```bash
   uv run prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
   ```

---

---

## Step 1: Start Prefect Server (Terminal 1)

Launch the Prefect UI in your first terminal:
```bash
uv run prefect server start
```

**Important:** Keep this terminal **open** throughout the process.

Access the dashboard at:
👉 [http://127.0.0.1:4200](http://127.0.0.1:4200)

---

## Step 2: Test Flow Locally (Terminal 2)

Open a second terminal and test the training flow:
```bash
uv run python -m src.flows.training_flow
```

**Expected output:**
```
Flow run 'abalone-training-flow' started
Task 'train_model' succeeded
Flow run completed successfully
```

Verify the flow run in the Prefect UI under **Flow Runs**.

---

## Step 3: Register Deployment (Terminal 2)

### 3.1 Create a Work Pool (One-Time Setup)
```bash
uv run prefect work-pool create --type process default-pool
```

### 3.2 Apply Deployment Configuration
```bash
uv run prefect deploy abalone_deploy.yaml
```

**Verification:**
Navigate to **Prefect UI → Deployments** and confirm that `abalone_local` is listed.

---

## Step 4: Start Worker (Terminal 3)

Open a third terminal and start the worker:
```bash
uv run prefect worker start -p "default-pool" -q "default"
```

**Expected output:**
```
Worker started, listening on pool 'default-pool', queue 'default'
```

**Note:** Keep this terminal running to process flow runs.

---

## Step 5: Trigger Flow from UI

In the Prefect UI:
1. Navigate to **Deployments → abalone_local**
2. Click **Quick Run**
3. Monitor Terminal 3 for execution logs

**Success Indicators:**
- Prefect UI displays: `Flow run succeeded ✅`
- New artifacts appear in:
  ```
  src/web_service/local_objects/
    ├── pipeline__v0.0.1.joblib
    ├── meta__v0.0.1.json
    └── predictions.csv
  ```

---

## Step 6: Schedule Automatic Runs

To enable automated retraining:

1. Go to **Deployments → abalone_local** in the Prefect UI
2. Click **Add Schedule**
3. Select schedule type: **Interval → Every 1 day** (adjust as needed)

Prefect will now automatically retrain the model on your defined schedule.

---

## Visual Examples

- [x] **Screenshot 1:** Prefect UI showing successful flow run
  ![flow_run_success](../assets/flow_run_success.png)

- [x] **Screenshot 2:** Deployments tab displaying `abalone_local`
  ![deployment_registered](../assets/deployment_registered.png)

- [x] **Screenshot 3:** Generated artifacts in `src/web_service/local_objects/`
  ![local_objects_output](../assets/local_objects_output.png)

- [x] **Screenshot 4:** Prefect dashboard overview
  ![prefect_dashboard](../assets/prefect_dashboard.png)

- [x] **Screenshot 5:** Automated training pipeline visualization
  ![automated_pipeline](../assets/automated_pipeline.png)

---

## 📚 Quick Reference

| Task | Terminal | Command |
|------|----------|---------|
| Start Prefect Server | 1 | `uv run prefect server start` |
| Test Flow Locally | 2 | `uv run python -m src.flows.training_flow` |
| Create Work Pool | 2 | `uv run prefect work-pool create --type process default-pool` |
| Register Deployment | 2 | `uv run prefect deployment apply abalone_deploy.yaml` |
| Start Worker | 3 | `uv run prefect worker start -p default-pool -q default` |
| Trigger Flow | Browser | Prefect UI → Deployments → Quick Run |

---

## 🌐 Helpful URLs
- Prefect UI Dashboard: [http://127.0.0.1:4200](http://127.0.0.1:4200)
- Prefect Docs: [https://docs.prefect.io](https://docs.prefect.io)

---

**Author:** Project Group (Jialong Xu et al.)
**Branch:** `3/use_prefect_fix`
**Last Updated:** October 2025
