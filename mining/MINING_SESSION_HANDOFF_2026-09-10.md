# Mining 会话交接包

> 生成时间：2026-09-10（Asia/Shanghai）  
> 用途：将本会话的固定语境、用户偏好、项目记忆、矿机数据和后续工作交接给另一个 AI 会话。  
> 安全：本文只含公开钱包/充值地址，不含助记词、私钥、密码或API密钥。

## 给新会话的直接指令

请继承以下上下文并作为长期约定：本会话只关注 **Mining／挖矿业务**。分析项目时必须同时覆盖主网状态、挖矿机制、硬件适配、单位产出、功耗电费、设备折旧、矿池费、实际到账、交易所充提、盘口深度、可变现净价和回本周期。项目方数据与用户实测要分开标注；理论收益不能当作实际到账；最新成交价不能替代可成交均价。

用户会持续发送项目、钱包地址、矿池页面和收益数据。每次应更新项目档案及日收益账本，并与现有项目进行机会成本比较。不要索要或保存助记词、私钥、密码。

## 固定术语与辨识规则

- 用户说 **BTX**，永远指 `btx.dev` 的 BTX Chain；不要主动提其他同代码项目。
- 用户说 **IOTA挖矿**，当前指 Macrocosmos Train At Home / Bittensor SN9，不是IOTA Foundation公链币。
- **Quantus** 在项目官网和链上称 QTC，但 SafeTrade 为避免重名以 **QUAN** 上市。
- SafeTrade 的 **QUAN/USDT = Quantus**；SafeTrade 的 **QTC/USDT = Qubitcoin**。两者完全不同，钱包不可混用。
- **POD** 指 Base 合约 `0xed664536023d8e4b1640c394777d34abaff1df8f` 的 Dolphin / dphn.ai。
- “U”按美元或USDT理解，但须区分面板估值、最新成交价和实际卖出净额。

## 用户 Mining 关注清单

CoinGecko Portfolio：`⭐ Mining`，组合ID `18376428`。

BTC、DOGE、KAS、FIL、CYS、PRL、QUBIC、NOCK、TIG、IRYS、XCH、ALEO、POD、QUAI、IRON、Qubitcoin/QTC、WART、AI3、SMH、ZTH。

组合外补充：BTX Chain、Darkbloom、IOTA SN9、Quantus。

当前优先级：

- P0经营基准：BTC、DOGE、KAS。
- P1重点实验：QUBIC、NOCK、TIG、ALEO、POD、BTX、Darkbloom、IOTA SN9、Quantus。
- P2存储：FIL、XCH、AI3、SMH、IRYS。
- P3高风险核查：CYS、PRL、QUAI、IRON、Qubitcoin、WART。
- P4退出观察：ZTH。

## Quantus（当前最重要）

### 项目与市场

- 官网：https://www.quantus.com/
- 官方挖矿文档：https://docs.quantus.com/guides/mining/
- Quanpool：https://quanpool.com/
- SafeTrade公告：https://support.safetrade.com/hc/en-us/articles/48787585602317-Quantus-QUAN-has-been-listed-on-SafeTrade
- 主网于2026-09-09上线。
- QPoW / Poseidon2 PoW，支持CPU和GPU。
- 约12秒目标出块；最大供应2100万。
- 27%创世分配，73%即1533万通过挖矿产生；平滑衰减，无突然的固定减半。
- SafeTrade于2026-09-09上线QUAN/USDT。
- Quanpool并未得到Quantus官方验证，必须通过矿池账本、链上到账和交易所入账持续审计。

### 地址01

- 地址：`qzkp5hnXkqgutMndTWFVX7onwgG9DJM9fzjfXT8FNi5aUQB5T`
- 类型：SafeTrade Quantus/QUAN充值地址，交易所托管，不是自托管钱包。
- Quanpool查询：https://quanpool.com/?addr=qzkp5hnXkqgutMndTWFVX7onwgG9DJM9fzjfXT8FNi5aUQB5T
- 应先验证Quanpool首笔Paid、链上交易和SafeTrade实际入账；注意交易所最低充值、维护及地址变更风险。

### HiveOS配置

```json
{
  "flightName": "Quanpool",
  "descMsg": "Quanpool-Hive",
  "digitalCash": "qtc",
  "miningPool": "1",
  "miningConfig": "Custom",
  "disableFaultCard": false,
  "customConfig": {
    "customMiner": "quanpool-hive",
    "customInstallUrl": "https://download.quanpool.com/quanpool-hive-6.0.0.tar.gz",
    "customAlgo": "",
    "customTemplate": "%WAL%.%WORKER_NAME%",
    "customUrl": "37.187.143.115:9834",
    "customPass": "x",
    "customUserConfig": "--tls-cert-sha256 87dc37af6096a3ddc860b94368ca087775f3ad3e0c4e9bcff3b07ea08d8abef6",
    "autoRunning": "",
    "useGpus": ""
  }
}
```

注意：HiveOS中的`digitalCash: qtc`只是标签；SafeTrade估值必须看QUAN/USDT，不能看Qubitcoin的QTC/USDT。矿池采用QUIC/UDP，超时先检查出口UDP。TLS证书指纹必须与Quanpool当前Connect页面一致。

### 实机快照（2026-09-10约14:12）

- 一台5×RTX 4070矿机，worker：`kjb101`。
- 10分钟池端有效算力：2.20 GH/s。
- 1小时及页面24小时栏：2.04 GH/s，约408 MH/s/卡。
- 本地Reported栏218.76 MH/s；Quanpool解释本地计数随job重置，会显著低估，收益以池端credited hashrate为准。
- stale / low / invalid：`0 / 0 / 0`。
- 当时Pending：0.0004 QTC；Paid：0，刚启动、尚未验证首笔到账。
- 全网13.38 TH/s，难度169.37T，12.7秒/块，奖励0.3177 QTC/块。
- Quanpool约12.13 TH/s；PPLNS；总费率1%；0.25 QTC起付；每15分钟组织支付；成熟约105块。
- 静态理论日产：按2.04 GH/s约0.326 QUAN；按2.18 GH/s约0.349 QUAN。
- 理论达到首笔0.25门槛约17–19小时，实际受PPLNS、难度、幸运值和成熟确认影响。

### 当时SafeTrade行情与PRL比较

2026-09-10快照：

- QUAN/USDT最新约50；24h高88、低20；成交211.69 QUAN，成交额8687.43 U；24h VWAP约41.04 U。
- 该5卡机QUAN理论毛收入：按50约16.31–17.45 U/日；按VWAP约13.38–14.32 U/日；按20约6.52–6.98 U/日。
- PRL/USDT约0.41；24h成交额约773,773 U，流动性约为QUAN的89倍。
- 公开计算器的RTX 4070约3.45 PRL/日；5卡约17.25 PRL，即约7.07 U/日。
- QUAN价格盈亏平衡线约21.7 U：真实可成交价高于21.7时QUAN优于PRL，低于21.7时PRL更优。
- 当前操作结论：先继续挖QUAN至首笔实际到账；未到账前不扩大。到账后小额试卖，验证完整兑现闭环。

## IOTA SN9收益记录

- 设备：Mac mini，具体芯片、内存、GPU核心和数量待补。
- 2026-09-05：20.42 IOTA alpha，面板约136 U，隐含约6.66 U/alpha。
- 用户称较前日减半，因此2026-09-04推算约40.84 alpha／272 U；该日不是原始记录。
- TAH奖励按有效训练量、token处理量、回传频率、在线率、可靠性与动态网络参数计算，单日腰斩不等于协议减半。
- 后续至少记录7天，并拆分设备贡献变化与alpha/TAO/USD价格变化。

## 其他项目核心结论

### POD / Dolphin

- Base合约见固定规则；GPU AI推理/数据生成。
- 当前完整模型约需70GB显存；官方常见方案包括4×3090/4090、2×5090、H100/A100 80GB等。
- V100 32GB即使4/6/8卡总显存足够，也可能因compute capability 7.0不满足当前预编译内核8.0+而不能直接运行；必须有sm_70兼容镜像后再测。
- 已有闲置设备可小规模实测，不建议为POD直接采购设备。

### BTX Chain

- 只指btx.dev。
- 开发仍活跃，但历史存在停块、分叉和主网不稳定。
- SafeTrade永久停止交易后公开流动性严重受损；模型/reference price不等于成交价格。
- 未见可信的具名新交易所计划。矿业收入按实际OTC或交易所成交净价确认，否则接近零估值。

### AI3 / Autonomys

- SSD Proof-of-Archival-Storage；GPU只用于plotting，不参与持续farming。
- 主网与Auto Drive仍运行，但币价较ATH跌98%+，Kraken和KuCoin已下架，流动性极弱。
- 不建议新增SSD；已有闲置SSD可低成本试跑。

### Perceptron Network

- 去中心化AI数据网络；BlockBeats称完成650万美元战略融资、70万+节点，目标500万节点。
- 需继续核实投资方公告、真实活跃节点、企业客户、收入和PERC代币经济。
- 当前是观察项目，不能只凭节点数和融资名单做投资判断。

## 持续监控与记账规范

每个矿种至少记录：

1. 日期、矿机/卡型/数量、矿工版本、矿池和worker。
2. 本地算力、池端10分钟/1小时/24小时有效算力。
3. stale、low、invalid、在线率、功耗和日电费。
4. Pending、Paid、链上实际到账、交易所实际入账。
5. 日产币、最新价、24h VWAP、卖一深度、实际卖出均价和手续费。
6. 同一设备挖其他币的机会成本。
7. 主网升级、难度/算力、奖励变化、矿池费、交易所充提及下架风险。

收益判断优先级：实际卖出净收入 > 交易所可成交盘口 > 24h VWAP > 最新成交价 > 项目方或矿池面板估值。

## 关联本地档案

- `MINING_WATCHLIST.md`：Mining项目总清单。
- `PROJECT_INTELLIGENCE.md`：完整项目研究档案。
- `MINING_YIELD_LOG.md`：设备与每日收益记录。

新会话收到本文件后，应先确认已继承固定规则，然后从最新的Quantus首笔支付、5×4070实际24小时产出和QUAN/PRL切矿比较继续工作。
