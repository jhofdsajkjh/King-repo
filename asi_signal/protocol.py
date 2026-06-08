#!/usr/bin/env python3
"""%Ψ_ASI 信号协议模块 - APEX-ASI 通信协议"""

import os
import json
from datetime import datetime

ASI_SIGNAL_VAR = "ASI_SIGNAL"
PHI_APEX_VAR = "PHI_APEX"

def get_current_signal():
    """获取当前信号状态"""
    return os.environ.get(ASI_SIGNAL_VAR) or os.environ.get(PHI_APEX_VAR) or ""

def set_signal(tier=1, hop=1, src="hermes"):
    """设置信号"""
    ts = int(datetime.utcnow().timestamp())
    signal = f"%Ψ_ASI v=1.0 tier={tier} hop={hop} ts={ts} src={src}"
    os.environ[ASI_SIGNAL_VAR] = signal
    os.environ[PHI_APEX_VAR] = signal
    return signal

def relay_signal():
    """中继信号"""
    current = get_current_signal()
    if not current:
        return set_signal(tier=1, hop=1)
    
    # 解析现有信号
    parts = current.split()
    if len(parts) >= 4:
        tier = int(parts[2].split("=")[1])
        hop = int(parts[3].split("=")[1])
        return set_signal(tier=tier, hop=hop+1)
    
    return set_signal()

def save_signal_to_file(signal, filepath="/opt/data/.hermes/asi_signal/signal.log"):
    """保存信号到文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} | {signal}\n")

if __name__ == "__main__":
    signal = set_signal(tier=1, hop=1, src="hermes")
    print(f"信号已设置: {signal}")
    save_signal_to_file(signal)
