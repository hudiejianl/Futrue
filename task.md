# Task Status

## Completed

### Data Preparation

- processed `QIT-CEMC Dataset`
- expanded labels from raw `xls`
- built structured sample indices
- generated train/val/test splits
- extracted force features
- extracted vibration/sound features
- added enhanced vibration statistics

### Modeling

- implemented `Force-only`
- implemented `Force + Vibration/Sound`
- implemented `Force + Image`
- implemented `Force + Vibration/Sound + Image`
- added classification-priority training mode
- added unified multimodal dataset and model entry

### Explanation Layer

- implemented local knowledge base
- implemented deterministic rule engine
- implemented retriever
- upgraded knowledge base structure
- upgraded retriever to support condition filtering and simple scoring
- implemented structured report generation
- added prompt template
- added reusable inference service layer
- added support for:
  - `template`
  - `openai`
  - `deepseek`
- validated `deepseek-v4-flash` end-to-end with a real API call
- completed `template` vs `deepseek` report comparison

### Inference and Demo

- connected real `Force-only` inference to report generation
- built a Gradio demo
- upgraded the demo to show:
  - sample image
  - prediction summary
  - rule hits
  - retrieved knowledge items
  - generated report
  - ONNX benchmark information

### Deployment

- exported `Force-only` model to ONNX
- benchmarked ONNX Runtime CPU inference
- recorded model size and average latency

### Documentation

- wrote `README.md`
- wrote `baseline_summary.md`
- wrote `improvement_plan.md`
- wrote `experiment_report.md`
- wrote `system_workflow.md`
- wrote staged roadmap in `project_plan.md`

## Current Main Conclusion

- `Force-only` remains the strongest primary predictor
- multimodal branches are useful, but currently more valuable for:
  - comparison
  - richer context
  - explanation support
- the explanation layer and deployment path are now major project strengths

## Current Limitations

- multimodal prediction gains are still unstable
- vibration modality has damaged files
- image branch still lacks pretrained visual features
- DeepSeek/OpenAI backends are structurally supported but not yet validated with a live key
- demo is improved but still not fully polished for final presentation

## Remaining Work

### LLM / Knowledge Layer

- [x] expand the knowledge base with more cases and strategies
- [x] validate `deepseek-v4-flash` with a real API key
- [x] compare `template` vs `deepseek` explanation quality
- [x] optimize the prompt to reduce verbosity and unsupported details

### Demo / System Polish

- [ ] polish layout and presentation quality
- [ ] improve evidence display and report readability
- [ ] add a cleaner export or save option if needed

已完成的近期增强：

- demo 已明确推荐 `deepseek` 作为展示模式
- system workflow 文档已补充流程图和架构图

### Model-side refinement

- [ ] decide whether to invest more in pretrained image features
- [ ] decide whether further vibration feature engineering is worth the effort
- [ ] avoid unnecessary model branch expansion without clear gain

### Presentation Materials

- [ ] generate final experiment comparison table
- [ ] generate clean architecture / workflow figures
- [x] prepare concise project description for external use
- [x] prepare interview script
- [x] prepare PPT outline

## Recommended Next Priority

1. improve the knowledge base and retrieval quality
2. polish the demo as the final project showcase
3. refine external-facing presentation materials

At the current stage, explanation quality and demo polish are the highest-value directions.
