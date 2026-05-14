# Baseline Summary

## 1. 已完成实验

### Force-only + 标准化

输出目录：
[force_baseline_norm](D:\my\Future\toolwear_multimodal\outputs\force_baseline_norm)

最佳验证结果：

- `MAE = 0.0540`
- `RMSE = 0.0817`
- `R2 = 0.4883`
- `F1-macro = 0.4536`

### Force-only + 分类优先

输出目录：
[force_baseline_cls](D:\my\Future\toolwear_multimodal\outputs\force_baseline_cls)

最佳验证结果：

- `F1-macro = 0.5732`

### Force + Vibration/Sound + 标准化

输出目录：
[force_vibration_baseline_norm](D:\my\Future\toolwear_multimodal\outputs\force_vibration_baseline_norm)

最佳验证结果：

- `MAE = 0.0694`
- `RMSE = 0.0984`
- `R2 = 0.3101`
- `F1-macro = 0.3239`

### Force + Vibration/Sound + 增强特征

输出目录：
[force_vibration_baseline_v2](D:\my\Future\toolwear_multimodal\outputs\force_vibration_baseline_v2)

最佳验证结果：

- `MAE = 0.1236`
- `RMSE = 0.1883`
- `R2 = -1.5266`
- `F1-macro = 0.4880`

### Force + Vibration/Sound + 分类优先

输出目录：
[force_vibration_baseline_cls](D:\my\Future\toolwear_multimodal\outputs\force_vibration_baseline_cls)

最佳验证结果：

- `F1-macro = 0.5406`

### Force + Image

输出目录：
[force_image_baseline](D:\my\Future\toolwear_multimodal\outputs\force_image_baseline)

最佳验证结果：

- `MAE = 0.0804`
- `RMSE = 0.1057`
- `R2 = 0.1449`
- `F1-macro = 0.1154`

### Force + Vibration/Sound + Image

输出目录：
[force_vibration_image_baseline](D:\my\Future\toolwear_multimodal\outputs\force_vibration_image_baseline)

当前结果偏弱，未超过 `Force-only`。

## 2. 对比结论

### 回归主线

当前最稳、最强的是：

- `Force-only + 标准化`

说明：

- 力/扭矩模态在当前数据条件下是最可靠的主预测信号
- 多模态并未稳定提升回归主指标

### 分类主线

当前最好结果仍然是：

- `Force-only + 分类优先`
- `F1-macro ≈ 0.5732`

说明：

- 即使将训练目标切到分类优先，多模态版本仍未稳定超过单模态

### 多模态作用的真实定位

当前更合理的项目叙事不是“多模态一定更强”，而是：

- `Force-only` 作为稳健主预测模型
- `Vibration/Sound` 和 `Image` 作为辅助模态
- 多模态用于增强系统解释性、辅助分类判断和丰富系统设计

## 3. 反思后的最终主线

建议固定为：

1. `Force-only` 做主预测
2. `Image` 与 `Vibration/Sound` 作为辅助模态保留在系统设计与实验分析中
3. `LLM` 基于预测结果、图像上下文和规则库生成解释与建议
4. 边缘部署优先围绕 `Force-only` 主模型展开

## 4. 解释模块进展

已完成：

- 规则引擎
- 知识库
- 知识检索
- 报告生成
- 真实主模型推理 + 报告生成链路

相关文件：

- [knowledge_base.json](D:\my\Future\toolwear_multimodal\llm\knowledge_base.json)
- [rule_engine.py](D:\my\Future\toolwear_multimodal\llm\rule_engine.py)
- [retriever.py](D:\my\Future\toolwear_multimodal\llm\retriever.py)
- [report_generator.py](D:\my\Future\toolwear_multimodal\llm\report_generator.py)
- [infer_force_and_report.py](D:\my\Future\toolwear_multimodal\scripts\infer_force_and_report.py)
- [force_infer_report.txt](D:\my\Future\toolwear_multimodal\reports\force_infer_report.txt)

## 5. 部署结果

### ONNX 导出

导出文件：
[force_only.onnx](D:\my\Future\toolwear_multimodal\deploy\force_only.onnx)

### ONNX CPU Benchmark

结果文件：
[force_onnx_benchmark.json](D:\my\Future\toolwear_multimodal\reports\force_onnx_benchmark.json)

关键指标：

- `avg_latency_ms ≈ 0.0232`
- `model_size_mb ≈ 0.0236`
- `input_dim = 20`

说明：

- 当前主模型非常轻量
- 已具备明确的边缘部署叙事基础
- 适合写入“端边协同部署”部分

## 6. 当前项目状态

目前项目已经具备：

- 可训练的主模型
- 多组 baseline 对比
- 解释模块
- 真实推理报告链路
- ONNX 导出与 benchmark
- 最小 demo 入口

因此，后续最优方向不再是继续堆模型，而是：

1. 整理对外输出材料
2. 完善 demo 展示
3. 提炼简历和答辩表述
