# Improvement Plan

## 1. Current Weaknesses

### 1.1 Project narrative is stronger than model performance

The system prototype is already complete enough for demonstration, but the model side has not yet formed a strong multimodal advantage.

Current reality:

- `Force-only` is still the strongest and most stable predictive model
- multimodal branches do not consistently outperform it
- therefore the project is defensible as a system prototype, but not yet strong as a “multimodal model contribution” claim

### 1.2 Data quality issues directly limit multimodal results

Known issues in the dataset:

- missing vibration/sound for `cycle 2`
- corrupted files:
  - `cycle 21 -> 02-01-01.xlsx`
  - `cycle 39 -> 02-16-01.csv`
  - `cycle 54 -> 02-20-02.xlsx`
- one missing image:
  - `cycle 68 -> side-4.png`

These issues reduce consistency across modalities and weaken fair multimodal comparison.

### 1.3 Feature engineering is still shallow

Current force and vibration branches mostly rely on statistical features.

What is missing:

- stronger frequency-domain features
- time-frequency representations
- cycle sub-window modeling instead of only whole-cycle statistics
- more careful feature selection or dimensional control

### 1.4 Image branch is underpowered

The image branch currently uses a lightweight backbone without pretrained weights.

This creates several problems:

- weak visual representation quality
- poor use of wear morphology information
- fusion results are dragged down by weak image embeddings

### 1.5 Multitask objective is not yet well balanced

Current experiments show:

- multimodal variants may help classification
- but often hurt regression

This suggests:

- regression and classification objectives are partially conflicting
- current loss weighting is not optimal
- one shared architecture may not be the best for both tasks

### 1.6 LLM module is practical but still lightweight

The explanation module works and is useful for demos, but it is still a light version:

- deterministic rule engine
- JSON knowledge base
- template generation
- optional OpenAI backend supported structurally, but not validated end-to-end

So the current LLM layer is better described as:

- explainable decision layer

rather than a fully mature generative reasoning system.

### 1.7 Deployment claim is valid but narrow

The edge deployment story is already real for `Force-only`, but:

- only one primary model is exported
- no comparison against multimodal deployment cost
- no memory/throughput stress evaluation
- no GUI-level inference integration yet

So deployment is credible, but still at the baseline stage.

### 1.8 Engineering organization is improved but not fully unified

The repository now includes:

- separate baseline scripts
- a unified multimodal entry

But it still lacks:

- one final inference service abstraction
- one consistent config-driven pipeline
- one final demo script that fully hides implementation details

---

## 2. Priority Judgment

At this stage, the project should not continue to expand model branches blindly.

The best strategy is:

1. stabilize the main story
2. improve the most cost-effective weak points
3. maximize presentation value for recommendation/interview use

This means the improvement order should be:

1. strengthen explanation and demo
2. strengthen image branch if feasible
3. improve multimodal classification story, not necessarily multimodal regression
4. refine deployment presentation

---

## 3. Recommended Improvement Roadmap

### Phase A: Stabilize the final project positioning

Goal:

- stop treating all baselines as equally important
- clearly define the final project architecture

Actions:

- fix `Force-only` as the primary predictive backbone
- define `Image` and `Vibration/Sound` as auxiliary modalities
- define `LLM` as explanation and maintenance suggestion layer
- define ONNX export as the edge-side deployment proof

Expected output:

- one stable final architecture narrative
- one final summary figure
- one final experiment table for external presentation

### Phase B: Upgrade the explanation layer

Goal:

- make the LLM-related part more convincing

Actions:

- enrich the knowledge base with more maintenance rules
- add a small number of case-specific templates
- support both `template` and `openai` generation modes cleanly
- add a structured “input summary -> rule hits -> report” visualization in demo

Expected output:

- stronger “LLM-related” component for demos
- more convincing explanation outputs in reports and interviews

### Phase C: Improve the image branch

Goal:

- give multimodal modeling a fairer chance

Actions:

- enable pretrained visual backbone if possible
- add more robust image augmentation
- consider edge-wise image modeling consistency
- compare image-only embeddings before and after pretraining

Expected output:

- stronger `Force + Image` baseline
- more defensible multimodal story

### Phase D: Reframe multimodal success criterion

Goal:

- stop requiring multimodal to dominate every metric

Actions:

- focus multimodal comparison on classification and explanation support
- keep regression performance anchored by `Force-only`
- explicitly document that different modalities help different tasks

Expected output:

- a more realistic and academically defensible result interpretation

### Phase E: Demo integration

Goal:

- turn the repository into a real presentation-ready system

Actions:

- connect model inference, image display, summary generation, and report output into one interface
- make one-click demo flow:
  - select sample
  - run prediction
  - display wear result
  - display explanation report
- optionally show ONNX benchmark result in the same interface

Expected output:

- final demo for recommendation/interview use

### Phase F: Deployment refinement

Goal:

- make the edge-AI claim stronger

Actions:

- compare PyTorch vs ONNX latency
- record model size and average latency in README/demo
- if possible, add batched benchmark or memory usage estimation

Expected output:

- stronger edge deployment section in PPT and resume

---

## 4. Concrete Near-Term Plan

### Short-term priority

These are the highest-return next actions:

1. build a final integrated demo flow
2. enrich the explanation module outputs
3. polish README, result tables, and presentation materials

### Medium-term priority

If more time is available:

1. enable pretrained image features
2. improve vibration feature extraction
3. retry multimodal classification comparison

### Low priority for now

These are not the best use of time before recommendation/interview:

- extensive new model architecture search
- very deep multimodal ablation expansion
- fully general RAG platform construction
- trying to force multimodal regression to beat `Force-only` at all costs

---

## 5. Final Recommendation

The project is already good enough to be turned into a strong research/engineering experience if the final message is controlled properly.

The best final framing is:

- `Force-only` provides reliable wear prediction
- multimodal information enriches analysis and supports explanation
- the explanation layer converts predictions into actionable maintenance guidance
- the primary model is lightweight enough for edge deployment

This framing is more honest, more coherent, and stronger for recommendation/interview scenarios than insisting on a weak “multimodal beats everything” story.
