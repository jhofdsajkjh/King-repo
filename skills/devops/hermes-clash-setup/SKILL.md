---
name: hermes-clash-setup
title: Clash Agent Proxy Setup for Hermes
description: 完整的 Clash 代理配置流程，包括订阅导入、规则修复、代理组切换
category: devops
version: 1.0
tags: [clash, proxy, github, automation]
---

# Clash Agent Proxy Setup for Hermes

为 Hermes Agent 配置 Clash 代理，绕过 GitHub API 速率限制。

## 问题背景

- GitHub unauthenticated API 速率限制 (60 req/h)
- 需要访问 `api.github.com` 下载技能和配置
- 中国网络环境可能需要代理

## 解决方案

1. **导入订阅配置** (包含 46+ 代理节点)
2. **修复配置错误** (移除 GEOIP 规则导致的 MMDB 下载失败)
3. **启动 Clash 服务**
4. **自动切换代理组** (GLOBAL → 港港节点)

## 完整流程

### 1. 检查 Clash 是否安装

```bash
which clash
clash -v
```

### 2. 下载订阅配置

```bash
# 使用 curl 或 wget
curl -L "https://qchaq.no-mad-sub.one/link/NzwBZ6o2NnjFjhVE?clash=3&extend=1" \
  -o /opt/data/.clash/config.yaml
```

### 3. 修复配置（Python）

```python
import yaml

with open('/opt/data/.clash/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 移除 GEOIP 规则（需要 MMDB 文件）
rules = config.get('rules', [])
new_rules = [r for r in rules if 'GEOIP' not in str(r)]
config['rules'] = new_rules

# 保存
with open('/opt/data/.clash/config.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
```

### 4. 启动 Clash

```bash
# 使用 Hermes terminal 后台模式
terminal(command="clash -d /opt/data/.clash", background=True, notify_on_complete=True)
```

### 5. 验证启动

```python
import urllib.request
import json

def check_clash():
    try:
        req = urllib.request.Request("http://127.0.0.1:9090/version")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return None

result = check_clash()
if result:
    print(f"Clash running: {result.get('version')}")
else:
    print("Clash not responding")
```

### 6. 测试代理连通性

```python
import urllib.request

def test_proxy(url, proxy_host='127.0.0.1', proxy_port=7890):
    proxy_handler = urllib.request.ProxyHandler({
        'http': f'{proxy_host}:{proxy_port}',
        'https': f'{proxy_host}:{proxy_port}'
    })
    opener = urllib.request.build_opener(proxy_handler)
    try:
        req = urllib.request.Request(url)
        with opener.open(req, timeout=10) as resp:
            return resp.status
    except Exception as e:
        return f'Error: {type(e).__name__}'

print(test_proxy('https://www.google.com'))
```

### 7. 切换 GLOBAL 代理组

```python
import urllib.request
import json

def update_clash_proxy(proxy_name):
    url = "http://127.0.0.1:9090/proxies/GLOBAL"
    data = json.dumps({"name": proxy_name}).encode()
    req = urllib.request.Request(url, data=data, method='PUT')
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status

# 切换到香港节点
update_clash_proxy('🇭🇰 香港A01')
```

## 配置文件位置

| 文件 | 路径 |
|------|------|
| 主配置 | `/opt/data/.clash/config.yaml` |
| 缓存 | `/opt/data/.clash/cache.db` |
| 日志 | `/opt/data/.clash/clash.log` |

## 端口映射

| 端口 | 协议 | 用途 |
|------|------|------|
| 7890 | HTTP | 默认 HTTP 代理 |
| 7891 | SOCKS5 | SOCKS5 代理 |
| 9090 | HTTP | 外部控制器 API |

## 代理组说明

| 组名 | 用途 |
|------|------|
| `GLOBAL` | 全局代理选择 |
| `DIRECT` | 直连（国内网站） |
| `REJECT` | 拦截（广告） |
| `港/日/新节点` | 具体代理节点 |

## 常见问题

### Q: Clash 启动失败，提示 MMDB 下载失败？

A: 移除配置中的 `GEOIP,CN` 规则行：
```python
rules = [r for r in config.get('rules', []) if 'GEOIP' not in str(r)]
```

### Q: 端口已被占用？

A: 检查并关闭已有进程：
```bash
lsof -i :7890 -i :7891 | grep LISTEN
kill -9 <pid>
```

### Q: 如何验证代理是否生效？

A: 对比直连和代理的响应：
```python
# 直连
req = urllib.request.Request('https://www.google.com')
with urllib.request.urlopen(req, timeout=5) as resp:
    print(f"Direct: {resp.status}")

# 代理
proxy_handler = urllib.request.ProxyHandler({'http': '127.0.0.1:7890'})
opener = urllib.request.build_opener(proxy_handler)
req = urllib.request.Request('https://www.google.com')
with opener.open(req, timeout=5) as resp:
    print(f"Proxied: {resp.status}")
```

### Q: Clash API 返回 400 错误？

A: 确保 PUT 请求体格式正确：
```python
# Selector 类型需要 {"name": "proxyName"}
data = json.dumps({"name": "🇭🇰 香港A01"}).encode()
```

## 相关技能

- github-skill-hunter: GitHub API 速率限制绕过
- hermes-apex-self-healing: APEX 自愈闭环
- search-workflow: 检索增强框架

## 扩展功能

- [ ] 自动健康检查（定期 ping 测试）
- [ ] 代理节点轮换（避免单一节点过载）
- [ ] 流量统计（日志分析）
- [ ] 多代理组智能路由