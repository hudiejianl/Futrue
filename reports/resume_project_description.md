# Resume Project Description

## 1. 中文简历版本

### 版本 A：精简版

**面向端边协同部署的刀具磨损监测与大模型辅助决策系统**

- 基于 QIT-CEMC 数据集完成力/扭矩、振动/声音、图像及磨损标签的清洗、对齐与结构化索引构建
- 搭建刀具磨损预测系统，完成 `Force-only` 主模型与多组多模态 baseline 对比，确定主预测骨干并验证辅助模态作用
- 构建规则引擎、知识库检索与 DeepSeek 报告生成链路，实现刀具状态解释、换刀建议输出和最小化 demo 展示
- 将主模型导出为 ONNX 并完成 CPU 端 benchmark，验证模型轻量化与边缘部署可行性

### 版本 B：偏科研版

**面向智能制造的刀具磨损监测、解释与边缘部署系统**

- 面向公开 QIT-CEMC 工业数据集，构建包含力/扭矩、振动/声音、图像及磨损标签的多模态数据处理流程，完成样本索引构建与按 cycle 划分的训练/验证/测试集生成
- 设计并实现 `Force-only`、`Force+Vibration/Sound`、`Force+Image` 与三模态基线模型，完成回归与分类对比实验，分析单模态与多模态在不同任务上的适用性
- 搭建知识库、规则引擎与 DeepSeek(`deepseek-v4-flash`) 解释模块，实现基于预测结果的结构化诊断报告、风险评估和换刀建议生成
- 完成主模型 ONNX 导出与 CPU 推理 benchmark，为端边协同部署和工程演示提供依据

### 版本 C：偏工程版

**刀具磨损监测与智能解释原型系统**

- 将原始工业数据集整理为可训练、可推理、可展示的结构化工程数据资产
- 以 `Force-only` 作为稳定主预测模型，以图像与振动/声音作为辅助信息源，构建完整的刀具状态监测原型
- 实现从预测、解释、报告生成到 demo 展示、ONNX 导出的完整链路

## 2. 英文简历版本

### Version A

**Tool Wear Monitoring and LLM-Assisted Decision Prototype for Edge-Ready Smart Manufacturing**

- Built a structured data pipeline on the QIT-CEMC dataset, covering force/torque, vibration/sound, image, and tool wear labels
- Implemented a stable `Force-only` prediction backbone and multiple multimodal baselines for comparative analysis
- Developed a rule-guided explanation module with knowledge retrieval and DeepSeek-based report generation for maintenance suggestions
- Exported the primary model to ONNX and benchmarked CPU inference latency for edge deployment validation

## 3. 项目亮点关键词

可用于简历中的关键词：

- `智能制造`
- `刀具磨损监测`
- `多模态数据处理`
- `结构化知识库`
- `DeepSeek`
- `可解释决策`
- `ONNX`
- `边缘部署`
- `Gradio Demo`

## 4. 建议保留的最终说法

如果简历空间有限，建议优先保留这三点：

1. 做了数据集处理与主预测模型
2. 做了解释模块与 DeepSeek 诊断报告
3. 做了 ONNX 导出与边缘部署验证
