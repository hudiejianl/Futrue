# Experiment Report

## 1. Objective

The experiments in this repository aim to answer two questions:

1. Which modality provides the most stable prediction for tool wear on `QIT-CEMC Dataset`?
2. Under the current data quality and engineering constraints, what is the practical role of multimodal modeling?

## 2. Dataset Setting

The project uses processed side-tooth samples derived from `QIT-CEMC Dataset`.

Current setup:

- primary label target: `VBmax`
- regression target: `wear_value`
- classification target: `wear_level`
- split strategy: by `cycle_id`

Known data issues:

- missing vibration/sound for `cycle 2`
- corrupted vibration files for `cycle 21`, `39`, and `54`
- missing `side-4.png` in `cycle 68`

## 3. Experimental Baselines

The following baselines were implemented:

1. `Force-only`
2. `Force + Vibration/Sound`
3. `Force + Image`
4. `Force + Vibration/Sound + Image`

Additional variants:

- normalized training
- classification-priority training
- enhanced vibration feature engineering

## 4. Main Results

### 4.1 Regression-oriented comparison

| Model | MAE | RMSE | R2 |
|---|---:|---:|---:|
| Force-only + normalization | 0.0540 | 0.0817 | 0.4883 |
| Force + Vibration/Sound + normalization | 0.0694 | 0.0984 | 0.3101 |
| Force + Vibration/Sound + enhanced features | 0.1236 | 0.1883 | -1.5266 |
| Force + Image | 0.0804 | 0.1057 | 0.1449 |
| Force + Vibration/Sound + Image | 0.1207 | 0.1649 | -0.9391 |

### 4.2 Classification-oriented comparison

| Model | F1-macro |
|---|---:|
| Force-only + classification-priority | 0.5732 |
| Force + Vibration/Sound + classification-priority | 0.5406 |
| Force + Image | 0.1154 |
| Force + Vibration/Sound + Image | 0.1250 |

## 5. Result Interpretation

### 5.1 Strongest main predictor

The strongest and most stable model is still:

- `Force-only`

This is true for:

- regression-oriented setup
- classification-priority setup

### 5.2 Why multimodal does not dominate yet

The current multimodal baselines do not consistently outperform `Force-only` because of multiple practical constraints:

- vibration modality contains damaged files
- image branch uses no pretrained visual weights
- feature engineering is still relatively shallow
- cycle-level statistical features may be too coarse for effective multimodal fusion

### 5.3 Practical conclusion

The most defensible project conclusion is:

- `Force-only` is the primary predictive backbone
- auxiliary modalities are still useful for richer system design, comparison, and explanation support

This is a more realistic and technically honest result than claiming unstable multimodal superiority.

## 6. Explanation Layer Result

A local explanation pipeline has been implemented:

1. prediction summary generation
2. deterministic rule matching
3. knowledge retrieval
4. report generation

This means the project already supports:

- prediction
- explanation
- maintenance suggestion

even without relying on a live external LLM service.

## 7. Deployment Result

The primary `Force-only` model has been exported to ONNX and benchmarked on CPU.

Result:

- `avg_latency_ms ≈ 0.0232`
- `model_size_mb ≈ 0.0236`
- `input_dim = 20`

This supports the edge-deployment claim for the primary model.

## 8. Final Experimental Conclusion

At the current stage:

1. `Force-only` should be treated as the final primary prediction model
2. multimodal branches should be described as auxiliary analytical components
3. the explanation layer and deployment path are the main system-level strengths

This conclusion is consistent with the actual experimental evidence and results in a stronger final project narrative.
