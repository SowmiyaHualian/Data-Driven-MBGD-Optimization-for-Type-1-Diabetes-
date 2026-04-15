# Ensemble Model Integration Guide

## Overview
Your T1D Diabetes Risk Prediction system now uses an **Ensemble approach** combining:
- **MBGD Logistic Regression**: Fast, interpretable linear model
- **Artificial Neural Network (ANN)**: Captures complex non-linear patterns

## What Changed

### New Files Created
1. **`src/ann_model.py`** - ANN implementation with ReLU hidden layers
2. **`src/ensemble.py`** - Ensemble class that combines both models

### Modified Files
1. **`src/train_model.py`** - Now trains both MBGD and ANN separately, then combines
2. **`src/predict.py`** - Uses ensemble for predictions, shows individual model outputs
3. **`backend/api.py`** - Loads and uses ensemble model, returns model insights

## How the Ensemble Works

### Training Phase
```
1. Load data with preprocessing
2. Train MBGD Logistic Regression on training set
3. Train ANN (64 hidden units) on same training set
4. Save both model weights separately
```

### Prediction Phase
```
1. Input data is scaled using the scaler
2. MBGD predicts probability: P_mbgd
3. ANN predicts probability: P_ann
4. Ensemble probability = 0.5 × P_mbgd + 0.5 × P_ann
5. Final prediction = (ensemble_prob ≥ 0.5) ? 1 : 0
```

### Model Storage
- **`models/mbgd_model.npz`** - MBGD weights + bias + scaler parameters
- **`models/ann_model.npz`** - ANN weights (W1, b1, W2, b2) + hidden_units

## API Response Changes

The `/api/predict` endpoint now returns:
```json
{
  "risk_probability": 0.75,
  "prediction": 1,
  "risk_level": "High",
  "rehabilitation_plan": [...],
  "model_insights": {
    "mbgd_probability": 0.72,
    "ann_probability": 0.78,
    "ensemble_method": "Weighted Average (50% MBGD + 50% ANN)"
  }
}
```

## Usage Instructions

### Train New Ensemble Models
```bash
cd src
python train_model.py
```

This will:
- Train both MBGD and ANN on the diabetes dataset
- Display accuracy metrics for each model individually
- Display ensemble accuracy
- Save both models to `models/` folder

### Test Ensemble Predictions
```bash
cd src
python predict.py
```

This will show individual and ensemble predictions on a sample input.

### Run the API
```bash
python main.py
```

The API will automatically load both models and create ensemble predictions.

## Performance Considerations

**ANN Training**: Takes longer than MBGD but captures non-linear patterns
- Hidden layer: 64 units
- Activation: ReLU (hidden) + Sigmoid (output)
- Optimization: MBGD with variable batch sizes

**Ensemble Benefits**:
✓ More robust predictions (reduces overfitting)
✓ Combines linear and non-linear decision boundaries
✓ Better generalization to unseen data
✓ Individual model insights for model interpretability

## Customization

### Adjust Ensemble Weights
In `src/ensemble.py`, modify initialization:
```python
ensemble = EnsembleModel(mbgd_weight=0.6, ann_weight=0.4)  # Give MBGD more weight
```

### Modify ANN Architecture
In `src/train_model.py`, change:
```python
self.ann_model = ANN(hidden_units=128, lr=0.01, epochs=500)  # More hidden units
```

### Adjust Hyperparameters
- **Learning rate**: Lower = slower but more accurate training
- **Epochs**: More epochs = longer training but potentially better accuracy
- **Batch size**: Larger batches = faster training but less stable gradients
