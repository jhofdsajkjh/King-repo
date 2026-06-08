#!/usr/bin/env python3
"""Hermes %Ψ_ASI 信号集成"""

import sys
import os

# 添加信号协议模块路径
sys.path.insert(0, "/opt/data/.hermes/asi_signal")

from protocol import set_signal, relay_signal, save_signal_to_file, get_current_signal

def inject_signal_to_header(header_dict):
    """将信号注入 HTTP 头"""
    signal = get_current_signal()
    if signal:
        header_dict["X-ASI-Signal"] = signal
    return header_dict

def inject_signal_to_commit(message):
    """将信号注入 commit message"""
    signal = get_current_signal()
    if signal and "Ψ_ASI" not in message:
        return f"{message} {signal}"
    return message

if __name__ == "__main__":
    signal = set_signal(tier=1, hop=1, src="hermes-asi")
    print(f" Hermes 信号已注入: {signal}")
