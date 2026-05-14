# Project Plan

## 1. Goal

This plan defines the next-step roadmap for improving the current project in a controlled way.

The overall target is:

1. keep `Force-only` as the stable primary prediction backbone
2. improve multimodal branches where they add real value
3. upgrade the current lightweight explanation layer into a stronger LLM-assisted decision module
4. improve deployment, demo quality, and final presentation readiness

The project should move from:

- multiple baselines + lightweight explanation

to:

- stable prediction + auxiliary multimodal reasoning + stronger LLM explanation + deployable demo

---

## 2. Current Baseline

Current project status:

- `Force-only` is the strongest and most stable predictive model
- multimodal baselines exist, but their gains are unstable
- local rule-engine explanation works
- ONNX export and CPU benchmark are already available
- minimal Gradio demo is available

Current weakness:

- multimodal fusion is not yet strong enough to be the main result
- the LLM layer is still lightweight and mostly rule-guided
- the demo is functional but not yet polished enough for strong presentation

---

## 3. Improvement Strategy

The improvement direction should follow this priority:

1. strengthen LLM and knowledge-grounded explanation
2. refine multimodal modeling without forcing weak claims
3. polish the demo and system integration
4. improve deployment presentation and documentation

This means:

- do not spend unlimited time chasing weak multimodal regression gains
- instead, build a stronger system-level story

---

## 4. LLM Plan

### 4.1 Target

Upgrade the current explanation layer from:

- `rules + JSON knowledge base + template report`

to:

- `rules + retrieval + structured generation + optional DeepSeek backend`

### 4.2 Backend Choice

Planned model:

- `deepseek-v4-flash`

Planned API key variable:

- `DEEPSEEK_API_KEY`

Planned base URL variable:

- `DEEPSEEK_BASE_URL`

Recommended later environment configuration:

```env
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

Note:

- the key will be filled in later by the user
- before the key is added, the system should continue to support local `template` mode

### 4.3 Concrete Tasks

#### Phase L1: Knowledge Base Upgrade

- expand `knowledge_base.json`
- add richer fields such as:
  - `applicable_conditions`
  - `risk_level`
  - `recommended_action`
  - `evidence_type`
  - `case_tag`

Expected result:

- better structured evidence for retrieval and generation

#### Phase L2: Retrieval Upgrade

- upgrade retriever from pure `rule_id -> item` lookup
- support:
  - rule-based filtering
  - keyword-based matching
  - optional similarity ranking

Expected result:

- explanation reports grounded in a richer evidence set

#### Phase L3: Structured Output

- first generate a structured JSON-like result:
  - diagnosis
  - risk level
  - evidence
  - action
  - replacement suggestion
- then render it into human-readable Chinese report text

Expected result:

- better controllability
- easier demo rendering

#### Phase L4: DeepSeek Integration

- add a `deepseek` report mode
- support:
  - `template`
  - `openai`
  - `deepseek`
- use environment variables for credentials

Expected result:

- stronger and more natural LLM-generated explanation

### 4.4 LLM Success Criteria

The LLM module will be considered improved if:

- it supports local fallback mode
- it supports a real external backend
- reports become more natural and evidence-grounded
- the demo can display both rule evidence and generated explanation

---

## 5. Multimodal Model Plan

### 5.1 Target

Do not force multimodal to replace `Force-only` as the primary regression model.

Instead, the improved multimodal strategy should be:

- `Force-only` for main prediction
- multimodal models for:
  - auxiliary classification
  - richer context
  - better explanation support

### 5.2 Concrete Tasks

#### Phase M1: Data Cleanup

- isolate bad vibration files cleanly
- document skipped cycles explicitly
- make consistent train/val subset handling

Expected result:

- cleaner experimental comparisons

#### Phase M2: Image Branch Improvement

- enable pretrained visual features if feasible
- if not, add stronger augmentation and lighter fine-tuning
- validate whether image features help classification or explanation

Expected result:

- more meaningful image modality contribution

#### Phase M3: Vibration Feature Improvement

- expand beyond simple statistics where practical
- candidate directions:
  - RMS
  - peak-to-peak
  - skew/kurtosis
  - energy bands
  - FFT-based summary features

Expected result:

- stronger vibration/sound classification support

#### Phase M4: Fusion Reframing

- avoid over-optimizing regression-only fusion
- focus multimodal fusion on:
  - classification support
  - interpretability support
  - context enrichment

Expected result:

- a more honest and technically coherent multimodal story

### 5.3 Multimodal Success Criteria

The multimodal side will be considered good enough if:

- it contributes usefully to classification or explanation
- it strengthens system completeness
- it provides interpretable auxiliary evidence

It does **not** need to beat `Force-only` on every metric.

---

## 6. Deployment Plan

### 6.1 Target

Strengthen the existing deployment story around the primary model.

### 6.2 Concrete Tasks

#### Phase D1: Keep Force-only as Deployment Target

- maintain `Force-only` ONNX export as the main deployment path
- keep benchmark results updated

#### Phase D2: Improve Reporting

- clearly report:
  - model size
  - average latency
  - input dimension
  - runtime backend

#### Phase D3: Demo Exposure

- surface deployment benchmark in the Gradio demo
- make deployment evidence visible in presentation materials

### 6.3 Deployment Success Criteria

- export works reliably
- benchmark numbers are documented
- deployment is visible in demo and README

---

## 7. Demo Plan

### 7.1 Target

Turn the current demo from “functional” into “presentation-ready”.

### 7.2 Concrete Tasks

#### Phase UI1: Better Information Layout

- separate:
  - input sample
  - model prediction
  - rule evidence
  - retrieved knowledge
  - final report

#### Phase UI2: Mode Switching

- allow report mode switching:
  - `template`
  - `deepseek`

#### Phase UI3: Result Context

- show:
  - prediction vs ground truth
  - model type used
  - deployment benchmark

### 7.3 Demo Success Criteria

- one-click sample inference
- readable system output
- strong enough for live demonstration

---

## 8. Documentation Plan

### 8.1 Target

Make the repository easy to understand and presentation-ready.

### 8.2 Concrete Tasks

#### Phase DOC1: Keep README Updated

- reflect final model positioning
- reflect explanation backend choices
- reflect deployment capability

#### Phase DOC2: Experiment Table

- maintain one official experiment report
- avoid scattered result interpretation

#### Phase DOC3: System Workflow

- keep a concise workflow description ready for PPT reuse

---

## 9. Recommended Execution Order

The best next-step order is:

1. expand and normalize the knowledge base
2. add `deepseek-v4-flash` backend support with env-based configuration
3. improve retriever and structured output
4. polish demo to expose explanation evidence and backend mode
5. if time remains, improve image branch or vibration features further

---

## 10. Final Recommended Narrative

The final project should be presented as:

- a tool wear monitoring prototype with a reliable `Force-only` prediction backbone
- multimodal auxiliary signals used for richer analysis and interpretability
- an LLM-assisted explanation layer that converts predictions into maintenance guidance
- a lightweight deployment path validated through ONNX benchmark

This is stronger and more defensible than insisting that the multimodal branch must dominate every predictive metric.
