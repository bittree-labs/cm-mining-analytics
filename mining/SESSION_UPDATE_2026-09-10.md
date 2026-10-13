# Mining 接续核验

时间：2026-09-10 14:23–14:25，Asia/Shanghai。原始交接包与三份关联档案已复制到本目录留档；Documents/Trade 原件未修改。本更新优先于旧档案中的过时结论。

## 固定约定

继承 MINING_SESSION_HANDOFF_2026-09-10.md 的术语、公开地址、硬件、配置、关注清单和记账规范。BTX只指btx.dev；IOTA挖矿指SN9；Quantus链上QTC在SafeTrade为QUAN，不能混用Qubitcoin的QTC。理论收益、池端Paid、链上转账和交易所入账分列。

## 实时观察

- 来源：https://quanpool.com/?addr=qzkp5hnXkqgutMndTWFVX7onwgG9DJM9fzjfXT8FNi5aUQB5T
- 地址01，5×RTX 4070，worker kjb101，PPLNS。
- 10min：2.58 GH/s；1h：2.26 GH/s；worker 24h栏：2.26 GH/s，但运行未满24小时，不能视为完整24h样本。
- Reported 1h：219.61 MH/s；stale/low/invalid：0/0/0。
- Pending：0.0025 QTC；Paid：0.00 QTC。个人Account可见block share记录，未见支付记录。未完成链上到账或交易所充值记录核验。
- 页面起付0.25 QTC，费率1%，每15分钟；Next payout估计14.9h，不是承诺到账时间。
- 全网14.78 TH/s、难度170.53T、11.5秒/块、显示区块奖励0.3078 QTC；池端12.56 TH/s。
- 以上为矿池页面自报，非独立链上审计。页面不同统计栏目可能有时间窗口差异。
- SafeTrade：https://safetrade.com/exchange/QUAN-USDT?type=basic 。最新41.98 U、24h成交212.79 QUAN、成交额8733.31 U；由此计算VWAP约41.0419 U。买卖深度未成功显示，不能判定盘口为空。
- SafeTrade市场列表PRL最新0.41 U；17.25 PRL/日仍沿用交接包公开计算器估计，非此次实测。

## 更新比较

QUAN静态日产：2.26/14780 × 86400/11.5 × 0.3078 × 0.99 ≈ 0.35007 QUAN/日，已扣池费，未扣电费、交易费、折旧。按最新价约14.70 U/日；按24h VWAP约14.37 U/日。PRL沿用17.25×0.41=7.0725 U/日。均非已实现收入。

忽略成本差时切矿无差异价约7.0725/0.35007=20.20 U/QUAN。旧21.7 U为旧算力网络快照结果，不是固定阈值。完整公式：QUAN可卖出净单价阈值=(PRL日产×PRL可卖出净单价+QUAN日成本−PRL日成本)/QUAN日产。成本包括各自电费、托管及适用折旧；交易费计入净单价，勿重复扣除。

继续单机验证；首笔Paid后核对交易哈希、链上收款及SafeTrade实际充值，之后由用户完成小额试卖以验证兑现。不据理论领先扩大规模。

## 旧档案纠偏与待补

- “每小时支付”已由实时页面的每15分钟替代。
- “当前未上市”已过时，QUAN/USDT交易页面存在。
- 卖出估值应检查买盘深度，不应以卖一价估算卖出兑现。
- 待补完整24h产出、PRL同机实测、两种算法墙插功耗、电价、设备成本、交易费和充值规则。
- 本次继承监控规则，未创建后台自动监控任务。
