# Report Mode Comparison

## Summary

Current observation:

- `template` mode is more stable and controllable
- `deepseek` mode produces more natural and richer reports
- `deepseek` is better for demo presentation
- `template` is better for strict consistency and deterministic behavior

Recommended usage:

- use `template` mode as safe fallback
- use `deepseek` mode for final demo and presentation

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
**诊断对象**：cycle_03_side_4（刀具侧面，cycle_03）  

**诊断结论**：刀具处于轻度磨损阶段，磨损预测值（0.176）略高于真实测量值（0.096），但均未达到需立即干预的程度。  

**风险等级**：低  

**主要依据**：  
- 预测模型（力信号）输出磨损值 0.176，对应 wear_level = 1（轻度磨损）  
- 真实测量磨损值 0.0957，对应 ground_truth_level = 0（正常）  
- 知识库中“刀具进入轻度磨损阶段”条目确认 wear_level=1 风险等级为 low，建议提高监测频率  
- 主预测模型为力信号模型，稳定性较高；图像模态仅用于辅助解释  

**是否建议换刀**：否  

**建议操作**：  
1. 提高当前刀具的磨损监测频率（如每加工50件执行一次检查）  
2. 关注后续 cycles 的磨损增长趋势，若连续两次预测值超过 0.25 则重新评估换刀必要性  
3. 可结合图像数据（当前 cycle_03_side-4.png）辅助确认表面形态是否出现明显磨损带
```

## Overall Conclusion

For the current project:

1. `template` mode should remain the default fallback
2. `deepseek-v4-flash` should be used as the primary showcase mode
3. future prompt optimization should focus on:
   - reducing verbosity
   - improving structural consistency
   - reducing unsupported extra assumptions

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
好的，已收到您的输入。以下是基于所提供数据生成的诊断报告。

---

**诊断对象：** cycle_64（刀具侧面 1）

**诊断结论：** 刀具已进入重度磨损阶段，存在较高的加工质量风险和失效可能性。

**风险等级：** 高

**主要依据：**
- **磨损预测值高：** 模型预测磨损值为 0.3805，超过 0.30 的高风险阈值（知识库条目 `high_wear_value`）。
- **磨损等级为重度：** 预测磨损等级和实际磨损等级均为 3（重度）（知识库条目 `wear_severe`）。
- **实际磨损值高：** 实际磨损值为 0.6183，远高于预测值，表明刀具实际状态比模型预测更差。

**是否建议换刀：** 是

**建议操作：**
1.  **立即换刀：** 为避免因刀具失效导致工件报废或设备损坏，建议立即停机并更换刀具。
2.  **降载备选：** 如无法立即换刀，必须将切削负载（如进给率、切削深度）降低至少 30%，并密切监控加工状态。
3.  **后续验证：** 换刀后，建议对已加工零件表面质量进行检查，以评估本次加工造成的潜在影响。
4.  **图像复核：** 请参考提供的刀具侧面图像（`side-1.png`），确认刀具磨损形态是否与诊断结论一致，作为历史记录存档。
```
