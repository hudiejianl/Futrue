# ToolWear Multimodal

A tool wear monitoring and decision-support prototype for smart manufacturing, built on the `QIT-CEMC Dataset`.

This repository currently includes:

- data preprocessing and structured indexing for the raw dataset
- a stable `Force-only` primary prediction model
- multiple multimodal baselines for comparison
- a lightweight explanation module with rules, knowledge retrieval, and report generation
- ONNX export and CPU benchmark for edge deployment
- a minimal Gradio demo entry

## 1. Project Positioning

The goal of this project is not to force multimodal models to outperform every single-modality baseline.  
Instead, the project is positioned as a practical system prototype with four layers:

1. sensor-based tool wear prediction
2. multimodal auxiliary analysis with vibration/sound and image inputs
3. explanation and decision support using a rule-guided LLM-style module
4. lightweight deployment for edge-side inference

At the current stage, the project has converged to the following engineering strategy:

- `Force-only` is the main predictive backbone
- `Vibration/Sound` and `Image` are retained as auxiliary modalities
- the explanation module turns predictions into human-readable maintenance suggestions
- deployment is centered on the lightweight `Force-only` model

## 2. Dataset

The project uses the public `QIT-CEMC Dataset`, which contains:

- force and torque signals
- vibration and sound signals
- tool images
- tool wear labels

The original dataset has already been transformed into a structured training-ready format.

Key processed files:

- `data/processed/index/side_samples_all.csv`
- `data/processed/index/side_samples_complete.csv`
- `data/processed/splits/train.csv`
- `data/processed/splits/val.csv`
- `data/processed/splits/test.csv`

## 3. Repository Structure

```text
toolwear_multimodal/
  app/                # Gradio demo entry
  data/processed/     # processed labels, indices, and dataset splits
  deploy/             # ONNX export and benchmark scripts
  llm/                # knowledge base, rule engine, report generation
  outputs/            # training outputs for all baselines
  reports/            # summaries, benchmark reports, generated diagnostics
  scripts/            # preprocessing, training, inference scripts
  src/datasets/       # dataset definitions
  src/models/         # model definitions
  task.md             # task tracking
```

## 4. Implemented Modules

### 4.1 Data Processing

Core scripts:

- `scripts/prepare_qit_cemc_dataset.py`
- `scripts/extract_force_features.py`
- `scripts/extract_vibration_features.py`

These scripts are responsible for:

- parsing the original `tool wear.xls`
- expanding side-tooth and end-tooth labels
- aligning sensor files, image folders, and labels
- generating train/val/test splits
- extracting force and vibration statistics

### 4.2 Baseline Models

Implemented baselines:

- `Force-only`
- `Force + Vibration/Sound`
- `Force + Image`
- `Force + Vibration/Sound + Image`

Related scripts:

- `scripts/train_force_baseline.py`
- `scripts/train_force_vibration_baseline.py`
- `scripts/train_force_image_baseline.py`
- `scripts/train_force_vibration_image_baseline.py`

### 4.3 Unified Multimodal Entry

The repository now also includes a more unified engineering entry:

- dataset: `src/datasets/multimodal_dataset.py`
- model: `src/models/multimodal_fusion_model.py`
- training entry: `scripts/train_multimodal.py`

This unified path is intended as the formal structure for future multimodal extension.

### 4.4 Explanation Module

The explanation module is implemented in:

- `llm/knowledge_base.json`
- `llm/rule_engine.py`
- `llm/retriever.py`
- `llm/report_generator.py`
- `llm/prompt_template.txt`

The current explanation layer supports two backends:

- `template` mode: fully local, deterministic, no external API needed
- `openai` mode: optional OpenAI-based report generation through a prompt template

Prompt template:

- `llm/prompt_template.txt`

Inference entry:

- `scripts/infer_force_and_report.py`

Reusable service layer:

- `src/engine/force_inference_service.py`

### 4.5 Deployment

Implemented deployment scripts:

- `deploy/export_force_onnx.py`
- `deploy/benchmark_force_onnx.py`

Exported model:

- `deploy/force_only.onnx`

## 5. Baseline Results

### Main regression-oriented result

The strongest and most stable regression baseline is:

- `Force-only + normalization`

Best validation result:

- `MAE = 0.0540`
- `RMSE = 0.0817`
- `R2 = 0.4883`

### Classification-priority result

The strongest classification-oriented result is also:

- `Force-only + classification-priority training`

Best validation result:

- `F1-macro = 0.5732`

### Multimodal comparison summary

| Baseline | MAE | RMSE | R2 | F1-macro |
|---|---:|---:|---:|---:|
| Force-only + normalization | 0.0540 | 0.0817 | 0.4883 | 0.4536 |
| Force-only + classification-priority | - | - | - | 0.5732 |
| Force + Vibration/Sound + normalization | 0.0694 | 0.0984 | 0.3101 | 0.3239 |
| Force + Vibration/Sound + enhanced features | 0.1236 | 0.1883 | -1.5266 | 0.4880 |
| Force + Vibration/Sound + classification-priority | - | - | - | 0.5406 |
| Force + Image | 0.0804 | 0.1057 | 0.1449 | 0.1154 |

Detailed discussion is available in:

- `reports/baseline_summary.md`
- `reports/improvement_plan.md`
- `reports/experiment_report.md`
- `reports/system_workflow.md`
- `project_plan.md`

## 6. Current Technical Conclusion

The experimental results clearly indicate:

- `Force-only` is currently the most reliable primary predictor
- multimodal branches do not consistently improve the main predictive metrics
- therefore, the most defensible narrative is:
  - `Force-only` for core prediction
  - `Image` and `Vibration/Sound` for auxiliary analysis and explanation
  - explanation module for risk reporting and maintenance suggestion

This is a stronger and more honest project story than forcing a weak multimodal performance claim.

## 7. Explanation Workflow

The current explanation pipeline works as follows:

1. the main model outputs:
   - `predicted_wear`
   - `wear_level`
2. a structured summary is created
3. the rule engine evaluates deterministic rules
4. the retriever maps matched `rule_id`s to knowledge items
5. the report generator produces a diagnosis report

Example outputs:

- `reports/demo_report.txt`
- `reports/force_infer_report.txt`

## 8. Deployment Result

The current main model has already been exported and benchmarked.

Benchmark file:

- `reports/force_onnx_benchmark.json`

Current ONNX CPU result:

- `avg_latency_ms ≈ 0.0232`
- `model_size_mb ≈ 0.0236`
- `input_dim = 20`

This provides a clear basis for the “edge-side deployable model” claim.

## 9. How to Run

### 9.1 Data preprocessing

```bash
python scripts/prepare_qit_cemc_dataset.py
python scripts/extract_force_features.py
python scripts/extract_vibration_features.py --cycle-file data/processed/splits/train_val_cycles.txt --output data/processed/index/vibration_cycle_features_train_val_v2.csv
```

### 9.2 Train the primary model

```bash
python scripts/train_force_baseline.py --output-dir outputs/force_baseline_cls --reg-weight 0.2 --cls-weight 1.0 --select-metric f1_macro
```

### 9.3 Run prediction + report generation

```bash
python scripts/infer_force_and_report.py --report-mode template
```

If you want to switch to the OpenAI backend:

```bash
set OPENAI_API_KEY=your_key
python scripts/infer_force_and_report.py --report-mode openai
```

### 9.4 Export ONNX and benchmark

```bash
python deploy/export_force_onnx.py
python deploy/benchmark_force_onnx.py
```

### 9.5 Launch demo

```bash
python app/gradio_demo.py
```

The current demo shows:

- selected sample image
- structured prediction summary
- matched rules
- retrieved knowledge items
- generated diagnostic report
- ONNX benchmark result

## 10. Current Limitations

The project is already a complete prototype, but several limitations remain:

### 10.1 Multimodal gains are unstable

- current multimodal variants do not consistently outperform `Force-only`
- multimodal results currently provide more comparison and analysis value than direct predictive gain

### 10.2 Vibration modality has broken files

Confirmed problematic files:

- `cycle 21 -> 02-01-01.xlsx`
- `cycle 39 -> 02-16-01.csv`
- `cycle 54 -> 02-20-02.xlsx`

These issues limit the consistency of vibration-based experiments.

### 10.3 Image branch is weak

- the current image backbone uses no pretrained weights
- visual representation quality is therefore limited
- this is a major reason why `Force + Image` remains weak

### 10.4 Feature engineering is still shallow

- current force and vibration branches mainly use statistical features
- richer spectral, time-frequency, or wavelet features are not yet fully integrated

### 10.5 Explanation module is still lightweight

- current implementation is `rules + knowledge base + report generation`
- the OpenAI backend is structurally supported, but not yet validated in end-to-end use

## 11. Recommended Next Steps

At the current stage, the highest-value next steps are:

1. finalize the project presentation narrative around `Force-only + explanation + deployment`
2. improve the demo experience
3. prepare PPT and resume-ready project descriptions
4. if more time is available:
   - introduce pretrained image features
   - upgrade vibration features
   - validate the OpenAI generation backend

## 12. Current Project State

The project already has:

- a trainable and deployable primary model
- multiple baseline comparisons
- a local explanation pipeline
- a real inference-to-report chain
- ONNX export and benchmark
- a minimal demo entry

At this point, it is already a strong system prototype for pre-recommendation / interview presentation, and future work should focus more on presentation quality and system polish than on endlessly extending model variants.
