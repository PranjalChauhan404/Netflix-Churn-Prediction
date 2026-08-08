# Netflix Customer Churn Prediction

## Overview
Short explanation of what the project does and why it matters.

## Problem Statement
Explain the business problem: identifying customers likely to churn so retention actions can be taken proactively.

## Objectives
- Predict customer churn
- Identify important churn factors
- Handle class imbalance
- Compare multiple ML models
- Optimize the best model
- Deploy an interactive prediction application

## Dataset
- Number of customers
- Features used
- Target variable: `churned`
- Brief description of important features

## Machine Learning Workflow
1. Data Understanding
2. Data Cleaning
3. Exploratory Data Analysis
4. Feature Engineering / Encoding
5. Train-Test Split
6. Feature Scaling
7. SMOTE
8. SMOTEENN
9. Model Training
10. Model Comparison
11. Hyperparameter Optimization with Optuna
12. Final Model Selection

## Models Tested
- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- Tuned XGBoost

## Model Performance
Include a small table:

| Model | Accuracy | ROC-AUC |
|---|---:|---:|
| Logistic Regression | 87.7% | 0.96 |
| Decision Tree | 97.1% | 0.97 |
| Random Forest | 97.7% | 1.00 |
| XGBoost | 99.5% | 1.00 |
| Tuned XGBoost | 99.3% | 1.00 |

## Final Model
Explain why XGBoost was selected and mention the final performance.

## Streamlit Application
Describe the dashboard:
- Customer input form
- Churn probability
- Risk level
- Risk meter
- Retention recommendation
- Netflix-themed UI

## Project Structure
Show the important files/folders.

## Installation

```bash
git clone <repository-url>
cd Netflix-Churn-Prediction
pip install -r requirements.txt