# Final Experiment Table

## 1. Regression-Oriented Results

| Model | MAE | RMSE | R2 | F1-macro |
|---|---:|---:|---:|---:|
| Force-only + normalization | 0.0540 | 0.0817 | 0.4883 | 0.4536 |
| Force + Vibration/Sound + normalization | 0.0694 | 0.0984 | 0.3101 | 0.3239 |
| Force + Vibration/Sound + enhanced features | 0.1057 | 0.1397 | -0.3903 | 0.4470 |
| Force + Image | 0.0804 | 0.1057 | 0.1449 | 0.1154 |
| Force + Vibration/Sound + Image | 0.1207 | 0.1649 | -0.9391 | 0.1250 |

## 2. Classification-Priority Results

| Model | F1-macro | Notes |
|---|---:|---|
| Force-only + classification-priority | 0.5732 | strongest classification baseline |
| Force + Vibration/Sound + classification-priority | 0.5406 | close, but still below Force-only |

## 3. Explanation Layer Result

| Component | Status |
|---|---|
| Rule engine | implemented |
| Knowledge retrieval | implemented and expanded |
| Template report generation | implemented |
| DeepSeek backend | validated end-to-end |
| Template vs DeepSeek comparison | completed |

## 4. Deployment Result

| Item | Value |
|---|---:|
| ONNX average latency (CPU) | 0.0232 ms |
| ONNX model size | 0.0236 MB |
| Input dimension | 20 |

## 5. Main Conclusion

### Predictive Backbone

The final primary prediction model should be:

- `Force-only`

### Multimodal Role

Multimodal branches are retained for:

- auxiliary analysis
- richer system context
- explanation support

### Explanation and Deployment

The strongest system-level contribution of the project is:

- prediction + explanation + deployment as one integrated prototype
