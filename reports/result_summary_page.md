# Result Summary Page

## Final Positioning

This project is best presented as a **tool wear monitoring and explanation prototype** rather than a pure multimodal accuracy project.

## Main Findings

### 1. Best Primary Predictor

`Force-only` is the strongest and most stable main model.

Best regression result:

- `MAE = 0.0540`
- `RMSE = 0.0817`
- `R2 = 0.4883`

Best classification result:

- `F1-macro = 0.5732`

### 2. Multimodal Outcome

Multimodal branches did **not** consistently outperform `Force-only`.

However, they still provide value for:

- richer comparative analysis
- auxiliary context
- explanation support

### 3. Explanation Capability

The project already includes:

- rule engine
- structured knowledge base
- retrieval layer
- template generation
- DeepSeek-based report generation

DeepSeek (`deepseek-v4-flash`) has been validated end-to-end.

### 4. Deployment Capability

The primary model has been exported to ONNX and benchmarked on CPU:

- latency: `0.0232 ms`
- size: `0.0236 MB`

This gives the project a clear edge-deployment story.

## Final System Story

The strongest final narrative is:

1. `Force-only` for robust prediction
2. multimodal inputs for auxiliary analysis
3. DeepSeek-assisted explanation for maintenance recommendation
4. ONNX export for edge-side deployment validation

## Recommended External Message

Do **not** over-claim multimodal superiority.

Instead, present the project as:

- a realistic end-to-end industrial AI prototype
- integrating prediction, explanation, and deployment
