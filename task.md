# Task Status

## 已完成

### 数据准备

- 确认项目数据源为 `QIT-CEMC Dataset`
- 检查并确认数据集真实目录结构
- 确认主要数据问题：
  - 标签文件为 `tool wear.xls`
  - 振动/声音模态缺失 `cycle 2`
  - 图像目录 `68` 缺失 `side-4.png`
- 安装 `xlrd`，使 `.xls` 标签文件可读取
- 编写并运行数据预处理脚本：
  - [prepare_qit_cemc_dataset.py](D:\my\Future\toolwear_multimodal\scripts\prepare_qit_cemc_dataset.py)
- 生成结构化标签文件：
  - `tool_wear_side_long.csv`
  - `tool_wear_end_long.csv`
  - `tool_wear_side_table.csv`
  - `tool_wear_end_table.csv`
- 生成样本索引：
  - `side_samples_all.csv`
  - `side_samples_complete.csv`
- 生成按 `cycle_id` 切分的训练集、验证集和测试集：
  - `train.csv`
  - `val.csv`
  - `test.csv`

### Force-only baseline

- 编写力特征提取脚本：
  - [extract_force_features.py](D:\my\Future\toolwear_multimodal\scripts\extract_force_features.py)
- 生成力统计特征：
  - [force_cycle_features.csv](D:\my\Future\toolwear_multimodal\data\processed\index\force_cycle_features.csv)
- 实现并训练 `Force-only` baseline：
  - [force_feature_dataset.py](D:\my\Future\toolwear_multimodal\src\datasets\force_feature_dataset.py)
  - [force_mlp.py](D:\my\Future\toolwear_multimodal\src\models\force_mlp.py)
  - [train_force_baseline.py](D:\my\Future\toolwear_multimodal\scripts\train_force_baseline.py)
- 完成标准化版本训练：
  - [force_baseline_norm](D:\my\Future\toolwear_multimodal\outputs\force_baseline_norm)
- 完成分类优先版本训练：
  - [force_baseline_cls](D:\my\Future\toolwear_multimodal\outputs\force_baseline_cls)

### Vibration/Sound baseline

- 编写振动/声音特征提取脚本：
  - [extract_vibration_features.py](D:\my\Future\toolwear_multimodal\scripts\extract_vibration_features.py)
- 生成第一版振动特征：
  - [vibration_cycle_features_train_val.csv](D:\my\Future\toolwear_multimodal\data\processed\index\vibration_cycle_features_train_val.csv)
- 增强振动特征工程：
  - 增加 `RMS / peak-to-peak / skew / kurtosis`
- 生成增强版振动特征：
  - [vibration_cycle_features_train_val_v2.csv](D:\my\Future\toolwear_multimodal\data\processed\index\vibration_cycle_features_train_val_v2.csv)
- 实现并训练 `Force + Vibration/Sound` baseline：
  - [force_vibration_feature_dataset.py](D:\my\Future\toolwear_multimodal\src\datasets\force_vibration_feature_dataset.py)
  - [train_force_vibration_baseline.py](D:\my\Future\toolwear_multimodal\scripts\train_force_vibration_baseline.py)
- 已完成的版本：
  - [force_vibration_baseline_norm](D:\my\Future\toolwear_multimodal\outputs\force_vibration_baseline_norm)
  - [force_vibration_baseline_v2](D:\my\Future\toolwear_multimodal\outputs\force_vibration_baseline_v2)
  - [force_vibration_baseline_cls](D:\my\Future\toolwear_multimodal\outputs\force_vibration_baseline_cls)

### Image baseline

- 实现图像数据集：
  - [force_image_dataset.py](D:\my\Future\toolwear_multimodal\src\datasets\force_image_dataset.py)
- 实现图像模型：
  - [force_image_model.py](D:\my\Future\toolwear_multimodal\src\models\force_image_model.py)
- 实现并训练 `Force + Image` baseline：
  - [train_force_image_baseline.py](D:\my\Future\toolwear_multimodal\scripts\train_force_image_baseline.py)
  - [force_image_baseline](D:\my\Future\toolwear_multimodal\outputs\force_image_baseline)

### 三模态 baseline

- 实现三模态数据集：
  - [force_vibration_image_dataset.py](D:\my\Future\toolwear_multimodal\src\datasets\force_vibration_image_dataset.py)
- 实现三模态模型：
  - [force_vibration_image_model.py](D:\my\Future\toolwear_multimodal\src\models\force_vibration_image_model.py)
- 实现并训练最小三模态 baseline：
  - [train_force_vibration_image_baseline.py](D:\my\Future\toolwear_multimodal\scripts\train_force_vibration_image_baseline.py)
  - [force_vibration_image_baseline](D:\my\Future\toolwear_multimodal\outputs\force_vibration_image_baseline)

### 解释模块

- 建立知识库：
  - [knowledge_base.json](D:\my\Future\toolwear_multimodal\llm\knowledge_base.json)
- 实现规则引擎：
  - [rule_engine.py](D:\my\Future\toolwear_multimodal\llm\rule_engine.py)
- 实现知识检索器：
  - [retriever.py](D:\my\Future\toolwear_multimodal\llm\retriever.py)
- 实现报告生成器：
  - [report_generator.py](D:\my\Future\toolwear_multimodal\llm\report_generator.py)
- 实现本地可运行 demo：
  - [demo_llm_report.py](D:\my\Future\toolwear_multimodal\scripts\demo_llm_report.py)
  - [demo_report.txt](D:\my\Future\toolwear_multimodal\reports\demo_report.txt)
- 实现真实主模型推理 + 报告生成链路：
  - [infer_force_and_report.py](D:\my\Future\toolwear_multimodal\scripts\infer_force_and_report.py)
  - [force_infer_report.txt](D:\my\Future\toolwear_multimodal\reports\force_infer_report.txt)
- 实现最小 Gradio demo 入口：
  - [gradio_demo.py](D:\my\Future\toolwear_multimodal\app\gradio_demo.py)
- 升级解释模块为双后端结构：
  - 默认模板生成
  - 可选 OpenAI API 生成
- 增加提示模板：
  - [prompt_template.txt](D:\my\Future\toolwear_multimodal\llm\prompt_template.txt)

### 部署链路

- 安装 `onnx`
- 实现 ONNX 导出脚本：
  - [export_force_onnx.py](D:\my\Future\toolwear_multimodal\deploy\export_force_onnx.py)
- 成功导出主模型：
  - [force_only.onnx](D:\my\Future\toolwear_multimodal\deploy\force_only.onnx)
- 实现 ONNX benchmark 脚本：
  - [benchmark_force_onnx.py](D:\my\Future\toolwear_multimodal\deploy\benchmark_force_onnx.py)
- 生成部署基准结果：
  - [force_onnx_benchmark.json](D:\my\Future\toolwear_multimodal\reports\force_onnx_benchmark.json)

### 统一训练与数据入口

- 实现统一多模态数据集入口：
  - [multimodal_dataset.py](D:\my\Future\toolwear_multimodal\src\datasets\multimodal_dataset.py)
- 实现统一融合模型入口：
  - [multimodal_fusion_model.py](D:\my\Future\toolwear_multimodal\src\models\multimodal_fusion_model.py)
- 实现统一训练脚本：
  - [train_multimodal.py](D:\my\Future\toolwear_multimodal\scripts\train_multimodal.py)

### 文档

- 实验汇总文档：
  - [baseline_summary.md](D:\my\Future\toolwear_multimodal\reports\baseline_summary.md)
- 改进计划文档：
  - [improvement_plan.md](D:\my\Future\toolwear_multimodal\reports\improvement_plan.md)

## 当前结论

- 当前最稳、最强的主预测线是 `Force-only`
- 在当前数据质量与实现条件下，多模态没有稳定提升主指标
- 即使切换到分类优先，`Force-only` 仍然优于当前双模态版本
- 因此后续最合理的项目主线是：
  - `Force-only` 作为主预测模型
  - `Image` 和 `Vibration/Sound` 作为辅助模态保留在系统设计与实验分析中
  - `LLM` 用于基于预测结果、图像上下文和规则库生成解释与建议

## 当前进行中

- 整理最终系统展示形式
- 准备结果汇报材料

## 未完成

### 数据与鲁棒性

- [ ] 检查特征分布是否存在异常值影响
- [ ] 处理或最终跳过振动模态中的坏文件

已确认的坏文件：

- `cycle 21 -> 02-01-01.xlsx`
- `cycle 39 -> 02-16-01.csv`
- `cycle 54 -> 02-20-02.xlsx`

### 实验整理

- [ ] 生成正式实验对比表
- [ ] 生成适合报告/PPT 的结果图
- [ ] 固定最终对外讲述版本

### 系统与部署

- [x] 导出 ONNX
- [x] 编写 benchmark 脚本
- [x] 构建统一推理脚本
- [x] 构建最小 demo 入口

## 建议的后续主线

1. 固定 `Force-only` 为主预测模型
2. 将 `LLM` 解释模块接到统一推理流程
3. 做一个最小 demo
4. 再整理报告、PPT 和简历表述
