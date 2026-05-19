# ToolWear Multimodal

A tool wear monitoring, explanation, and deployment prototype built on the `QIT-CEMC Dataset`.

This repository currently includes:

- structured preprocessing for the raw dataset
- a stable `Force-only` primary model
- multiple multimodal baselines for comparison
- a rule-guided explanation layer with optional external LLM backend support
- ONNX export and CPU benchmark for edge deployment
- a minimal but presentation-oriented Gradio demo

## 1. Project Positioning

This project is not framed as “multimodal must always beat single-modality prediction”.

Instead, the project is positioned as a system prototype with four coordinated layers:

1. reliable wear prediction
2. multimodal auxiliary analysis
3. explanation and maintenance guidance
4. lightweight deployability

The current engineering conclusion is:

- `Force-only` is the best main predictive backbone
- `Vibration/Sound` and `Image` are retained as auxiliary modalities
- the explanation layer turns predictions into actionable maintenance reports
- the primary model is lightweight enough for edge-side deployment

## 2. Dataset

The project uses the public `QIT-CEMC Dataset`, which contains:

- force and torque signals
- vibration and sound signals
- tool images
- tool wear labels

Processed dataset outputs are available under:

- `data/processed/index/`
- `data/processed/labels/`
- `data/processed/splits/`

Important processed files:

- `data/processed/index/side_samples_all.csv`
- `data/processed/index/side_samples_complete.csv`
- `data/processed/splits/train.csv`
- `data/processed/splits/val.csv`
- `data/processed/splits/test.csv`

## 3. Repository Structure

```text
toolwear_multimodal/
  app/                # Gradio demo
  data/processed/     # processed labels, indices, and splits
  deploy/             # ONNX export and benchmark
  llm/                # knowledge base, rules, retrieval, prompt template
  outputs/            # training outputs
  reports/            # summaries and benchmark reports
  scripts/            # preprocessing, training, inference
  src/datasets/       # dataset definitions
  src/engine/         # inference service layer
  src/models/         # baseline and fusion models
  task.md             # task tracking
  project_plan.md     # staged improvement roadmap
```

## 4. Implemented Components

### 4.1 Data Processing

Core scripts:

- `scripts/prepare_qit_cemc_dataset.py`
- `scripts/extract_force_features.py`
- `scripts/extract_vibration_features.py`

Main responsibilities:

- parse raw `xls` wear labels
- align sensor files, image folders, and labels by cycle
- build side-tooth training index
- generate train/val/test splits
- extract force and vibration statistics

### 4.2 Baseline Models

Implemented baselines:

- `Force-only`
- `Force + Vibration/Sound`
- `Force + Image`
- `Force + Vibration/Sound + Image`

Training scripts:

- `scripts/train_force_baseline.py`
- `scripts/train_force_vibration_baseline.py`
- `scripts/train_force_image_baseline.py`
- `scripts/train_force_vibration_image_baseline.py`

### 4.3 Unified Multimodal Entry

To avoid staying with only scattered baseline scripts, the repository now also includes:

- unified dataset:
  - `src/datasets/multimodal_dataset.py`
- unified multimodal fusion model:
  - `src/models/multimodal_fusion_model.py`
- unified training entry:
  - `scripts/train_multimodal.py`

This path is intended as the formal engineering structure for future multimodal refinement.

### 4.4 Explanation Layer

Current explanation-related files:

- `llm/knowledge_base.json`
- `llm/rule_engine.py`
- `llm/retriever.py`
- `llm/report_generator.py`
- `llm/prompt_template.txt`

The current explanation layer supports:

- `template` mode: fully local and deterministic
- `openai` mode: optional OpenAI backend
- `deepseek` mode: optional DeepSeek backend using `deepseek-v4-flash`

### 4.5 Inference Service

Reusable inference service:

- `src/engine/force_inference_service.py`

This service is responsible for:

- loading the primary model
- preparing standardized features
- running inference
- building structured prediction summaries
- invoking rule retrieval and report generation

### 4.6 Deployment

Deployment-related files:

- `deploy/export_force_onnx.py`
- `deploy/benchmark_force_onnx.py`
- exported model:
  - `deploy/force_only.onnx`

## 5. Experimental Summary

### Main regression result

Best stable regression baseline:

- `Force-only + normalization`

Result:

- `MAE = 0.0540`
- `RMSE = 0.0817`
- `R2 = 0.4883`

### Main classification result

Best classification-oriented result:

- `Force-only + classification-priority`

Result:

- `F1-macro = 0.5732`

### Comparison table

| Baseline | MAE | RMSE | R2 | F1-macro |
|---|---:|---:|---:|---:|
| Force-only + normalization | 0.0540 | 0.0817 | 0.4883 | 0.4536 |
| Force-only + classification-priority | - | - | - | 0.5732 |
| Force + Vibration/Sound + normalization | 0.0694 | 0.0984 | 0.3101 | 0.3239 |
| Force + Vibration/Sound + enhanced features | 0.1236 | 0.1883 | -1.5266 | 0.4880 |
| Force + Vibration/Sound + classification-priority | - | - | - | 0.5406 |
| Force + Image | 0.0804 | 0.1057 | 0.1449 | 0.1154 |

Detailed analysis:

- `reports/baseline_summary.md`
- `reports/experiment_report.md`
- `reports/final_experiment_table.md`
- `reports/result_summary_page.md`

## 6. Current Technical Conclusion

The current evidence supports the following interpretation:

- `Force-only` is the strongest main predictor
- multimodal branches are useful for system richness, comparison, and explanation support
- they are not yet strong enough to replace `Force-only` as the final primary model

This makes the final system story more defensible:

- single-modality for robust prediction
- multimodal auxiliary context for richer interpretation
- explanation layer for maintenance recommendations
- ONNX deployment for edge-AI validation

## 7. Explanation Workflow

Current explanation flow:

1. the primary model predicts:
   - `predicted_wear`
   - `wear_level`
2. a structured summary is created
3. the rule engine matches deterministic rules
4. the retriever selects relevant knowledge items
5. the report generator produces the final diagnosis report

Current backends:

- local template generation
- optional OpenAI generation
- optional DeepSeek generation

DeepSeek backend status:

- `deepseek-v4-flash` has now been validated end-to-end with a real API call
- it is currently the recommended showcase mode for demos, while `template` remains the safer fallback mode
- prompt iteration has already reduced verbosity and improved structural consistency

Example outputs:

- `reports/demo_report.txt`
- `reports/force_infer_report.txt`

## 8. Deployment Result

Current ONNX benchmark result:

- `avg_latency_ms ≈ 0.0232`
- `model_size_mb ≈ 0.0236`
- `input_dim = 20`

Report file:

- `reports/force_onnx_benchmark.json`

This provides direct support for the “edge-side deployable model” claim.

## 9. Demo

Current Gradio demo entry:

- `app/gradio_demo.py`

Current demo shows:

- selected sample image
- structured prediction summary
- matched rule hits
- retrieved knowledge items
- generated diagnosis report
- ONNX benchmark information

Recommended presentation mode:

- `deepseek` for final showcase
- `template` as deterministic fallback

## 10. How to Run

### 10.1 Data preprocessing

```bash
python scripts/prepare_qit_cemc_dataset.py
python scripts/extract_force_features.py
python scripts/extract_vibration_features.py --cycle-file data/processed/splits/train_val_cycles.txt --output data/processed/index/vibration_cycle_features_train_val_v2.csv
```

### 10.2 Train the primary model

```bash
python scripts/train_force_baseline.py --output-dir outputs/force_baseline_cls --reg-weight 0.2 --cls-weight 1.0 --select-metric f1_macro
```

### 10.3 Generate explanation report locally

```bash
python scripts/infer_force_and_report.py --report-mode template
```

### 10.4 Use DeepSeek backend later

Fill these environment variables first:

```bash
set DEEPSEEK_API_KEY=your_key
set DEEPSEEK_BASE_URL=https://api.deepseek.com
set DEEPSEEK_MODEL=deepseek-v4-flash
```

Then run:

```bash
python scripts/infer_force_and_report.py --report-mode deepseek
```

### 10.5 Use OpenAI backend optionally

```bash
set OPENAI_API_KEY=your_key
python scripts/infer_force_and_report.py --report-mode openai
```

### 10.6 Export and benchmark ONNX

```bash
python deploy/export_force_onnx.py
python deploy/benchmark_force_onnx.py
```

### 10.7 Launch demo

```bash
python app/gradio_demo.py
```

## 11. Current Limitations

### 11.1 Multimodal gains are unstable

- multimodal baselines do not consistently outperform `Force-only`
- current multimodal value is more system-level than metric-dominant

### 11.2 Vibration modality contains broken files

Confirmed problematic files:

- `cycle 21 -> 02-01-01.xlsx`
- `cycle 39 -> 02-16-01.csv`
- `cycle 54 -> 02-20-02.xlsx`

### 11.3 Image branch is weak

- current image branch uses no pretrained visual weights
- this limits visual representation quality

### 11.4 Feature engineering is still shallow

- current sensor modeling still relies heavily on statistical features
- richer time-frequency features are not yet fully integrated

### 11.5 LLM backend is not fully validated

- local template mode is working
- OpenAI and DeepSeek modes are structurally supported
- DeepSeek has already been validated end-to-end with a live key
- OpenAI mode remains optional and unvalidated in this repository

## 12. Recommended Next Steps

The most valuable next steps are:

1. improve the knowledge base and retrieval quality
2. validate `deepseek-v4-flash` end-to-end after the key is filled
3. polish the demo for presentation use
4. refine project presentation materials rather than blindly adding weak model branches

## 13. Current State

The project already has:

- a usable primary model
- multiple baseline comparisons
- an explanation layer
- a real inference-to-report chain
- ONNX export and benchmark
- a presentation-oriented demo
- a staged project roadmap

Additional presentation materials are now available under `reports/`, including:

- `resume_project_description.md`
- `interview_script.md`
- `ppt_outline.md`
- `final_external_version.md`

At this point, the project is already a strong prototype, and the highest-value work is now system polish and stronger explanation quality, not uncontrolled model expansion.
