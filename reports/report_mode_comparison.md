# Report Mode Comparison

## Sample: cycle_03_side_4

### Summary
```json
{"sample_id": "cycle_03_side_4", "cycle_id": "cycle_03", "predicted_wear": 0.17592035233974457, "wear_level": 1, "ground_truth_wear": 0.0957, "ground_truth_level": 0, "primary_model": "force_only", "use_image_context": True, "image_file": "D:\\my\\Future\\QIT-CEMC Dataset\\Image\\03\\side-4.png"}
```

### Template Report
```text
诊断对象：cycle_03
诊断结论：当前刀具磨损等级为轻度磨损，预测磨损值为 0.1759。
风险等级：低
主要依据：
- 主预测模型为力信号模型：当前主预测模型为 Force-only
- 图像模态用于辅助解释：当前启用了图像辅助解释
- 刀具进入轻度磨损阶段：磨损等级为 slight
是否建议换刀：否
建议操作：
- 当前系统以力/扭矩信号模型作为主预测依据，因为其在实验中表现最稳定。
- 图像模态当前主要用于辅助判断刀具表面磨损形态和支持解释输出。
- 提高磨损监测频率，关注后续磨损增长趋势。
```

### DeepSeek Report
```text
诊断对象：cycle_03_side_4 刀具  
诊断结论：刀具处于轻度磨损阶段，预测磨损量 0.176，真实磨损 0.096，磨损等级均为轻度或正常，当前状态安全。  
风险等级：低  
主要依据：结构化预测摘要显示预测 wear_level=1，知识库检索结果中“刀具进入轻度磨损阶段”对应 wear_level=1 且风险等级 low；主模型为力信号模型，图像用于辅助解释。  
是否建议换刀：否  
建议操作：1. 提高磨损监测频率，每完成一个加工循环后检查预测值变化趋势；2. 当前可继续使用，无需降载或换刀。
```

## Sample: cycle_64_side_1

### Summary
```json
{"sample_id": "cycle_64_side_1", "cycle_id": "cycle_64", "predicted_wear": 0.38052666187286377, "wear_level": 3, "ground_truth_wear": 0.6183, "ground_truth_level": 3, "primary_model": "force_only", "use_image_context": True, "image_file": "D:\\my\\Future\\QIT-CEMC Dataset\\Image\\64\\side-1.png"}
```

### Template Report
```text
诊断对象：cycle_64
诊断结论：当前刀具磨损等级为重度磨损，预测磨损值为 0.3805。
风险等级：高
主要依据：
- 主预测模型为力信号模型：当前主预测模型为 Force-only
- 图像模态用于辅助解释：当前启用了图像辅助解释
- 刀具进入重度磨损阶段：磨损等级为 severe
- 预测磨损值较高：预测磨损值 0.3805 > 0.30
是否建议换刀：是
建议操作：
- 当前系统以力/扭矩信号模型作为主预测依据，因为其在实验中表现最稳定。
- 图像模态当前主要用于辅助判断刀具表面磨损形态和支持解释输出。
- 尽快换刀，避免继续加工导致质量恶化或刀具失效。
- 优先考虑换刀或降低切削负载。
```

### DeepSeek Report
```text
诊断对象：cycle_64_side_1

诊断结论：刀具处于重度磨损阶段
风险等级：高

主要依据：
- 预测磨损值0.3805，实际磨损0.6183，磨损等级均为3（重度）
- 知识库中“刀具进入重度磨损阶段”规则命中，建议尽快换刀
- 预测磨损值超过0.30阈值，知识库判定为高磨损风险

是否建议换刀：是

建议操作：
1. 立即换刀，避免继续加工导致工件质量恶化或刀具断裂。
2. 如无法立即换刀，降低切削负载（如降低进给或切削深度），并缩短检查周期。
3. 结合侧-1图像画面辅助确认刀具表面磨损形态，作为换刀决策参考。
```
