# Final Application Package

## 1. Recommended Project Name

For most recommendation / interview scenarios, the best final project title is:

**面向端边协同部署的刀具磨损监测与大模型辅助决策系统**

Alternative options:

- **智能制造场景下的刀具磨损监测、解释与部署原型**
- **工业刀具磨损监测与可解释决策系统**

## 2. Best Resume Entry

Recommended final version:

**面向端边协同部署的刀具磨损监测与大模型辅助决策系统**

- 基于 QIT-CEMC 工业数据集完成力/扭矩、振动/声音、图像与磨损标签的清洗、对齐和结构化索引构建，形成可训练、可推理的数据资产
- 设计并实现 `Force-only` 主预测模型及多组多模态 baseline，对比分析不同模态在磨损回归、等级分类和系统解释中的作用，确定稳健主骨干
- 构建知识库、规则引擎与 DeepSeek(`deepseek-v4-flash`) 解释链路，实现刀具状态诊断、风险评估与换刀建议生成，并完成真实端到端调用验证
- 将主模型导出为 ONNX 并完成 CPU benchmark，结合 Gradio demo 构建可解释、可展示、可部署的工业智能原型系统

## 3. If Resume Space Is Tight

Use this shorter version:

**刀具磨损监测与大模型辅助决策系统**

- 完成 QIT-CEMC 工业数据集清洗与样本索引构建，训练 `Force-only` 主预测模型并开展多模态对比实验
- 接入 DeepSeek(`deepseek-v4-flash`) 与知识库解释链路，实现刀具磨损诊断报告与换刀建议生成
- 完成主模型 ONNX 导出与 CPU benchmark，构建 Gradio demo 验证系统展示与部署可行性

## 4. Resume Placement Advice

Recommended placement:

- put this project in the main `项目经历` / `科研经历` section
- if you already have a pure course project or Android project, place this one before it
- use this project to represent:
  - industrial AI
  - multimodal experimentation
  - LLM-assisted explanation
  - deployment capability

## 5. Keyword Pack

Recommended keywords for your resume:

- `智能制造`
- `工业AI`
- `刀具磨损监测`
- `多模态数据处理`
- `结构化知识库`
- `DeepSeek`
- `可解释决策`
- `ONNX`
- `边缘部署`
- `Gradio Demo`

## 6. 30-Second Self-Introduction Version

我做的是一个面向智能制造场景的刀具磨损监测与解释原型系统。项目基于 QIT-CEMC 数据集完成了工业多模态数据处理，并以 `Force-only` 作为稳定主预测模型，再结合知识库、规则引擎和 DeepSeek(`deepseek-v4-flash`) 生成刀具状态诊断和换刀建议，同时完成了 ONNX 导出与边缘部署验证。

## 7. 90-Second Interview Version

这个项目的目标不是只做一个模型，而是做一个完整的工业智能原型。我先对 QIT-CEMC 数据集做了清洗和结构化处理，把力/扭矩、振动/声音、图像和磨损标签整理成可训练的数据资产。然后分别做了 `Force-only`、`Force+Vibration/Sound`、`Force+Image` 和三模态 baseline。实验表明，在当前数据质量和工程条件下，`Force-only` 最稳定，所以我把它作为主预测模型。

在此基础上，我补了一层解释模块，包含知识库、规则引擎和 DeepSeek(`deepseek-v4-flash`) 报告生成链路，用来把预测结果转成更自然的诊断报告和换刀建议。最后我把主模型导出成 ONNX，并做了 CPU benchmark，同时用 Gradio 做了一个可展示 demo。这个项目的核心价值在于它覆盖了数据处理、模型实验、解释生成和部署验证的完整链路。

## 8. One-Line Repo Description

An industrial AI prototype for tool wear prediction, DeepSeek-assisted explanation, and edge-ready deployment built on the QIT-CEMC Dataset.

## 9. Final Presentation Message

The project should be presented with this logic:

1. `Force-only` provides robust primary prediction
2. multimodal inputs enrich analysis and comparison
3. DeepSeek converts model outputs into actionable diagnostic reports
4. ONNX export validates deployment feasibility

This message is stronger and more credible than claiming unstable multimodal superiority.
