# Pearl 浮点算法升级与 CMP50HX / RTX4070 兼容性研究

核查日期：2026-09-11，北京时间。对象为 Pearl / PRL；结合本项目 CMP50HX 五卡、每卡160W设置及 RTX4070、4070 SUPER 现有矿机。本文为公开资料研究，没有更改矿机、钱包或矿池配置。

## 判断

**升级方向有官方依据，但“50HX已经不能挖”“低于某个显存容量一律淘汰”不成立。** Pearl Team 的 PIP-3 草案提出将整数矩阵计算改为浮点计算，其中使用 FP8，并指定 Hopper、Blackwell 架构的计算结果必须能够被精确复现。如果按这一方向落实，50HX面临严重兼容性与能效风险；4070和4070 SUPER也不能当作已经获得支持。目前没有在该提案中公布激活日期、区块高度或统一的最低显存容量、带宽数值。[官方PIP-3](https://pearl-research-labs.github.io/pips/pip-0003/)

这不是已经确定的停矿通知。PIP网站说明，发布提案不代表获得共识或即将采用；Draft仍在编辑，Proposed才表示内容完整、进入更广泛评审，Final代表已部署的标准变更。[官方提案流程](https://pearl-research-labs.github.io/pips/)

## 一、已实施规则和未来提案必须分开

| 项目 | 查到的证据 | 对现有矿机的意义 |
|---|---|---|
| 当前第三方 pearlhash 矿工 | WildRig 0.51.0发布说明明确优化RTX2000/3000/4000及CMP40HX/50HX | 50HX仍被当前矿工支持，不能称已淘汰 |
| 已发布V3证书 | 官方代码说明是V2布局加盐化噪声种子派生 | 不是把所有矿机切成FP8 |
| 已实施盐化种子分叉 | 官方指南设置主网高度99,000，要求更新矿工和节点 | 旧程序可能报算力却提交无效份额，属于软件规则不匹配 |
| 拟议FP协议 | PIP-3，2026-07-30创建，状态Draft | 未来兼容性需要重新测试 |

来源：[WildRig 0.51.0](https://github.com/andru-kun/wildrig-multi/releases/tag/0.51.0)、[现行CertificateV3代码](https://raw.githubusercontent.com/pearl-research-labs/pearl/master/node/wire/certificate_v3.go)、[盐化种子升级指南](https://raw.githubusercontent.com/pearl-research-labs/pearl/master/docs/salted-seed-fork-upgrade-guide.md)、[PIP-3](https://pearl-research-labs.github.io/pips/pip-0003/)。WildRig页面显示9月5日发布；页面时间未换算北京时间。

**一个重要的文档冲突：** PIP-3把拟议浮点证书也编号为V3，但现行代码的V3已用于盐化种子。两者含义不同，因此不能用看到“V3”“requiredcertversion:3”证明FP8已经激活。后续正式方案需要解决编号或文档的一致性。这个判断直接来自提案与代码交叉核对，不依赖社区传言。[PIP-3](https://pearl-research-labs.github.io/pips/pip-0003/)、[现行证书代码](https://raw.githubusercontent.com/pearl-research-labs/pearl/master/node/wire/certificate_v3.go)

本次读取的主网参数列出了MoE、DenseOnly、RankPenalty、SaltedSeed等高度，RequiredCertVersion选择的V3是SaltedSeed分支；没有在该选择逻辑中发现FP8激活分支。此结论仅覆盖所核查的公开代码，不代表不存在内部实验或未合并开发分支。[主网参数与证书选择](https://raw.githubusercontent.com/pearl-research-labs/pearl/master/node/chaincfg/params.go)

## 二、PIP-3具体改变什么

当前整数方案把矩阵元素放在INT8存储中，留一位余量，按INT7值参与计算。拟议FP协议的核心流程是：输入BF16矩阵，经过尚未定稿的预量化，提交矩阵承诺，生成噪声，再量化到FP8 E4M3，执行FP8矩阵乘法并以FP32累加，从结果中的矩阵块生成获奖票据。目的在于适配浮点AI工作负载并降低附加计算开销。[官方PIP-3](https://pearl-research-labs.github.io/pips/pip-0003/)

INT8与FP8虽然都可以用8位存一个元素，但数值表示、运算指令和结果规则不同。能快速做INT8的卡，不会因此自动拥有FP8原生硬件加速。

浮点计算还涉及不同GPU、不同指令和累加顺序产生不同末位结果的问题。区块验证需要确定结果，提案因此要求事先声明硬件和规定计算流程，草案列出的架构是Hopper与Blackwell，配置中的device分别为0和1。不能仅看“我的显卡支持FP8”就判断新份额会被接受。[官方PIP-3的Hardware Dependence与Commitment部分](https://pearl-research-labs.github.io/pips/pip-0003/)

这里也有一个不能过度推断的边界：提案要求计算结果可在指定硬件上逐位复现，不能据此证明其他硬件在数学上永远不可能模拟出相同结果。Pearl官方研究目录本身介绍了在CPU上精确复现GPU矩阵计算的Hawkeye研究。但“可以复现”不等于“已经有兼容矿工”，更不等于在旧GPU上速度、功耗仍有竞争力。本次没有核实到PIP-3下50HX或4070的公开有效份额与收益基准。[Pearl Labs](https://pearlresearch.ai/labs)

## 三、对你现有显卡的影响

下表的未来判断是根据草案和硬件架构作出的风险评估，并非已发布的矿工兼容清单。

| 显卡 | 架构与标准显存 | 当前PRL | 按现有FP8草案评估 |
|---|---|---|---|
| CMP50HX | Turing；标准10GB GDDR6 | 当前矿工支持；项目历史代表算力约61TH/s/卡 | 不在草案列出的架构中，缺少原生FP8 Tensor路径，兼容与能效风险高 |
| RTX4070 | Ada；12GB | 当前可挖；项目历史代表值约112TH/s/卡 | Ada有FP8能力，但草案没有列Ada；仍需适配与验证 |
| RTX4070 SUPER | Ada；12GB GDDR6X | 项目有在产设备 | 同样不能直接视为升级后安全；不能套用普通4070算力 |
| Hopper / Blackwell设备 | 草案指定架构 | 需按具体型号与矿工判断 | 方向匹配，但仍需要最终实现、型号支持、内存与有效份额实测 |

硬件依据：[NVIDIA把CMP50HX归类为Turing](https://developer.nvidia.com/nvidia-development-tools-solutions-err-nvcmpgpu-devtools-does-not-support-crypto-mining-processor)、[MSI 50HX规格](https://www.msi.com/Graphics-Card/MSI-NVIDIA-CMP-50HX-MINER/Specification)、[NVIDIA Turing Tensor运算说明](https://docs.nvidia.com/cuda/turing-tuning-guide/)、[NVIDIA Ada FP8说明](https://docs.nvidia.com/cuda/ada-tuning-guide/)、[4070系列官方规格](https://www.nvidia.com/en-eu/geforce/graphics-cards/40-series/rtx-4070-family/)。项目算力是历史运行基线，不是本次新测，也不是未来FP8算力。

**4070的原生FP8能力让它与50HX的处境有所区别，但不能代替协议兼容性证据。** 同理，只因RTX50系列也叫Blackwell，就认定所有型号都已满足草案参考实现，是过早推断。需要看最终支持的具体GPU、计算路径和测试向量。

50HX的现有驱动解锁、提高功耗上限或加显存，不能把Turing芯片变为Hopper，也不能凭空增加原生FP8 Tensor硬件。今后软件可能选择转换、模拟或其他兼容实现，但损失多少性能目前没有可靠实测，不能编造下降百分比。

## 四、显存容量与带宽到底有没有门槛

目前核查到的PIP-3没有给出“至少16GB/24GB/80GB”“至少1TB/s”这样的统一门槛。预量化格式、参考实现、测试向量、实验结果和部署计划仍有待定项。因此不存在可据此宣布“10GB刚好被淘汰、12GB刚好合格”的官方数值界线。[PIP-3](https://pearl-research-labs.github.io/pips/pip-0003/)

实际限制应分为三层：

1. **协议结果是否合格。** 使用什么数字格式、计算流程，是否满足精确验证。
2. **具体程序是否跑得起来。** 内核是否支持该GPU，任务矩阵、缓存、证明或推理工作负载能否装入可用显存。
3. **跑起来之后是否划算。** 有效吞吐、拒绝率、实际功耗、全网竞争和币价共同决定收益。

容量与带宽影响后两层，但不自动解决第一层。

MSI标准50HX给出10GB、320bit、14Gbps，由此计算理论显存带宽：14×320÷8＝**560GB/s**。这是依据厂商规格计算的理论值，不是本项目实测值。它说明50HX并不是简单的“显存带宽很低所以不能挖”。本项目改卡、超频、锁频后的实际数值应另测。[MSI官方规格](https://www.msi.com/Graphics-Card/MSI-NVIDIA-CMP-50HX-MINER/Specification)

显存带宽是GPU读写本地显存的速度，PCIe带宽是显卡与主机或其他设备通信的速度，两者也不要混淆。尤其不能把五张10GB卡直接当作一张50GB卡；普通每卡独立运行的矿工不会自动合并显存。多GPU模型分片需要软件明确支持，并承担通信开销。

另一个常见误读是把“运行完整大模型”要求当成“所有PRL挖矿”要求。官方vLLM矿工是模型推理集成，README示例包含模型、上下文长度和显存利用率参数；它的资源消耗依赖具体模型与配置。当前第三方矿工明确支持50HX，这是不能把某个大模型的显存占用泛化成全网显卡门槛的直接现实依据。[官方vLLM矿工README](https://raw.githubusercontent.com/pearl-research-labs/pearl/master/miner/vllm-miner/README.md)、[WildRig发布说明](https://github.com/andru-kun/wildrig-multi/releases/tag/0.51.0)

## 五、升级时间与仍未解决的问题

截至本次核查，官方PIP-3的状态仍是Draft，Deployment写TBD。参考矿工承诺在升为Proposed前提供，测试向量和实验结果也未在该提案中给出。因此本报告不把社区月份猜测、路线图方向或演讲预期写成确定主网切换日。[官方PIP-3](https://pearl-research-labs.github.io/pips/pip-0003/)

能够改变本报告判断的证据包括：正式激活高度/日期；更新后的完整协议；GPU具体型号兼容清单；参考矿工和公开测试向量；WildRig或其他开发者明确发布新协议支持；矿池接受该协议份额的测试结果。即使先发布支持代码，也需要确认主网是否已激活。

尚不能回答的量化问题包括：50HX能否以模拟方式有效提交、4070能否逐位满足规定运算、具体最低可用显存、每卡升级后有效算力、全网算力构成变化、升级后的PRL净收入。缺少这些输入，不能用芯片理论TOPS计算可靠回本周期。

## 六、本项目的应对判断

**现有设备：** 继续按当前有效份额和实际到账判断运行情况。没有证据支持因该草案立即停止所有50HX或4070。此前排查到的驱动/矿工配置异常应按各自故障处理，不能归因于尚未确认激活的FP8升级。

**新增投入：** 在PRL用途的回本测算中，把算法兼容期作为明确不确定因素。按现有草案，50HX有较高失去竞争力或无法直接运行新矿工的风险，4070也有未解决的架构适配风险；仅按今天收益长期外推不可靠。这个判断不意味着建议立刻采购Hopper或Blackwell，后者也需要完整成本与实际挖矿收益验证。

**替代收益：** 本项目已有50HX的QUAN试挖与PRL比较，但历史报告的价格、难度和收益代理口径都带有时间限制。PRL切换算法后，应重新测量两个项目的有效收益和整机电耗，不沿用旧百分比，也不把不同算法的TH/s、GH/s直接相除比较。[已有50HX比较报告](./CMP50HX_5GPU_COMPARISON_2026-09-11.md)

**正式支持发布后的测试顺序：** 先分别用一台50HX、一台4070或4070 SUPER验证启动、矿池接受份额、拒绝率与稳定性，再累计至少一个完整日的产出和整机电耗。需要排除矿池成熟/付款延迟影响；仅有矿工界面算力或短时收益估计不足以证明兼容和盈利。这里是建议的验收流程，本次没有下发测试或批量升级。

判断门槛应是“新协议下的有效份额＋可重复性能＋实际收益”，而不是只看显存GB数、矿工显示正常或芯片宣传算力。

## 证据范围

核心判断使用官方PIP、Pearl公开代码、矿工开发者发布记录和显卡厂商技术文档交叉核查。PIP-3原文采用CC0。网页与master分支可能后续更新，本文结论以2026-09-11获取的内容为准。未联系开发者、未读取未公开路线图、未运行未来协议矿工，因此所有升级后兼容性与收益判断均保留相应条件。
