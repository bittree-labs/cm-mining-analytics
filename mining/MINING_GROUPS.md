# 挖矿业务分组规范（mining-01/02/03）

> 建立：2026-10-08（用户定义）。挖矿业务项目按运营阶段分三级，直接对着区块链挖矿项目。

## 分组定义

| 组 | 含义 | 判据 |
|---|---|---|
| **mining-01** | 运营中 | 当前在挖、**随时要切换**的项目 |
| **mining-02** | 关注 | 以前挖过、现在挖、未来可能挖（还未挖/未上主网） |
| **mining-03** | 未使用 | 以前挖过、可预见时间内不挖、或已下线 |

> **mining-01 是 mining-02 的子集**（运营中的项目必然也在关注范围内）。

## 项目归属（2026-10-08）

### mining-01 运营中（随时切换）

| 币 | 全名 | 算法 | 挖矿方式 | 价格 U | 说明 |
|---|---|---|---|---|---|
| **QUANTUS** | Quantus | QPoW（Poseidon） | GPU | 157.40 | 现役主力，kj102/103/204 挖 |
| **PRL** | Pearl | 矩阵 PoW（pearlhash） | GPU | 1.45 | 现役主力，ya2/ya3 集群挖 |
| **NOID** | ParanO1d | Poseidon2b PoW | GPU（RTX30/40/50） | 0.117 | 随时切换候选（实测：30HX 1.84 / 50HX 4.66 / 4070TiS 35.46 MH/s） |

### mining-02 关注（含 01 + 观察对象）

| 币 | 全名 | 算法 | 挖矿方式 | 价格 U | 状态 |
|---|---|---|---|---|---|
| TSC | TensorCash | 待确认 | GPU | 6.63 | 关注 |
| QTC | Qubitcoin | Qhash | GPU | 0.6998 | 关注 |
| NOCK | Nockchain | 待确认 | GPU | 0.0207 | 关注 |
| QUBIC | Qubic | QubicHash（AI 训练） | CPU | 0.0000006 | 关注 |
| CMFD | Common Foundry | ForgeMatrix（INT8 矩阵） | GPU | 未上币 | Devnet 测试网，主网未启动 |

> 另见 `MINING_WATCHLIST.md`（CoinGecko Portfolio 20 币的宽泛关注清单，含 BTC/DOGE/KAS/FIL/CYS 等 ASIC/存储/ZK 项目，不在此详列）。

### mining-03 未使用（下线/停挖）

| 币 | 全名 | 状态 |
|---|---|---|
| BTX | BitTree?（btxchain/btx） | 链间歇停块，SafeTrade 维护停牌，无兼容锄头 |
| ZTH | Zether | CoinGecko 已标记 Inactive |

## ⚠️ 关键认知纠正（2026-10-08）

- **QTC ≠ Quantus**。`QTC` 是 **Qubitcoin**（Qhash 算法，独立币）；Quantus 的交易对是 `QUANTUS/USDT`（=QUAN）。两者在 SafeTrade 是独立币、价格差 225 倍。旧文档「QTC 为矿池对 Quantus 的记号」是错的。

## NOID 实测（2026-10-08，真机 benchmark noid-gpu-miner 1.4.0）

**⚠️ 实时全网数据（suprnova API，2026-10-08）**：全网算力 **388.78 GH/s**（10-05 是 165.6，**涨 2.35 倍**）、区块奖励 **45 NOID**（从 50 降 10%）、高度 199942 → **每 MH/s 日产 0.50 NOID（比 10-05 快照缩水 2.6 倍）**。此前用 165.6 GH/s 快照算的收益全部作废。

| 卡 | 实测算力 | 功耗 | 日净利(NOID) | vs 现役 |
|---|---:|---:|---:|---|
| 30HX（TU116） | 1.84 MH/s | 80W | **−0.09 U** | 挖 QUAN 0.60 U |
| 50HX（TU102） | 4.66 MH/s | 160W | **−0.13 U** | 挖 QUAN 1.38 U |
| 4070TiS 开源矿机 | 35.46 MH/s | 275W | 1.25 U | 挖 PRL 4.94 U |
| 4070TiS gb矿机（估） | ~48 MH/s | 275W | 2.05 U | 挖 PRL 4.94 U |

**结论：三张卡都不值得切 NOID，全部维持现役。**
- 30HX/50HX 挖 NOID 已转**亏损**（全网算力涨 2.35 倍后收益归零）。
- 4070TiS 即使用专有 gb-parano1d-miner（比开源高 36%，5070Ti: 107 vs 78.6 MH/s），日净利也就 2~5 U，仍**不超过 PRL 的 4.94 U**。
- 核心教训：**NOID 价格涨 85%，但全网算力涨 2.35 倍，单位算力产出反而缩水 2.6 倍**——涨价的矿币必须同时盯全网算力，否则"涨价就切"会踩空。
- 钱包 vip0-noid-safe01 = o1nh3g…（SafeTrade 充值地址）；矿机走 fallback kernel 全过正确性校验。

## 币价监控（影响收益第一变量）

SafeTrade 是主交易场所，拿价走 API（`cm-crypto-trading/safetrade/safetrade_client.py`）：

```bash
./venv/bin/python3 safetrade_client.py ticker <market>
# market id: quantususdt / prlusdt / noidusdt / tscusdt / qtcusdt / nockusdt / qubicusdt
```

本组币价波动极大（QUAN 单日 100→183→157，NOID 三天涨 3.7 倍），**收益测算必须每次拿实时价 + 实时难度，不沿用旧快照**。

## 待办

- [ ] 补 TSC（TensorCash）算法 + 矿池 + 硬件门槛
- [ ] 补 NOCK（Nockchain）算法 + 矿池 + 硬件门槛
- [ ] 确认 QTC（Qubitcoin）是否已从 maintenance 恢复交易
- [ ] 各币在 30HX/4070TiS/5070Ti 的实测算力（有实测再上收益测算）
- [ ] CMFD 主网激活 + 上币监控（触发后再评估）
