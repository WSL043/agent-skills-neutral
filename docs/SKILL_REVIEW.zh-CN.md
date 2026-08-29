# 思维核心与 Workflow 保留审查

当前 canonical 包含 23 个思维 workflow：S=6、A=17，共 9 个认知类别。`runtime/AGENTS.md` 是唯一常驻的默认思维核心；不存在默认 skill profile。所有 `SKILL.md` 都只在当前认知瓶颈需要其独立工作流时按需加载。

S 表示跨场景迁移价值较高，A 表示更具体的场景思维流程。两者都不是路由分数，也不代表默认加载。

## 当前活动清单

### 学习与评估

| Workflow | 级别 | 独立思维结果 |
|---|---:|---|
| `evaluate-agent` | A | 用冻结 claim、同条件 baseline/candidate、trace 与失败归因判断能力是否真实提升。 |

### 系统设计

| Workflow | 级别 | 独立思维结果 |
|---|---:|---|
| `design-codebase` | A | 从职责、依赖方向和变更压力比较结构方案，并形成可迁移的边界。 |
| `model-domain` | A | 从真实场景提炼概念、不变量、状态转换、所有权与限界上下文。 |
| `review-api-design` | A | 以消费者、兼容性、错误、安全边界、演进和可运维性评审接口契约。 |

### 实现推理

| Workflow | 级别 | 独立思维结果 |
|---|---:|---|
| `develop-with-tdd` | S | 围绕可观察行为执行 red-green-refactor，旧代码先建立特征证据。 |
| `diagnose-software` | S | 复现并缩小问题，定位首次分歧，以可证伪假设证明根因。 |
| `optimize-performance` | A | 建立可比 baseline，隔离瓶颈，做单一改动并重新测量正确性和收益。 |
| `simplify-code` | A | 先冻结行为 contract，再删除已证明的偶然复杂度并验证保持不变。 |
| `review-code` | S | 分开审查需求符合度和实现质量，只保留可到达、可验证的发现。 |
| `verify-completion` | S | 把完成声明映射到最新权威证据，并在真实消费或运行表面验证最终状态。 |

### 变更与演进

| Workflow | 级别 | 独立思维结果 |
|---|---:|---|
| `instrument-observability` | A | 从运营问题反推日志、指标和 trace，并验证真实信号能回答问题。 |
| `migrate-system-safely` | A | 通过 expand/backfill/switch/contract、对账和恢复路径迁移活系统。 |

### 规划与协作

| Workflow | 级别 | 独立思维结果 |
|---|---:|---|
| `handoff-task-context` | A | 保存目标、证据、决策、阻塞和 frontier，并在恢复时逐项对账。 |
| `plan-implementation` | S | 基于真实仓库给出文件/符号级、依赖有序、可回滚的实现计划。 |

### 问题框定

| Workflow | 级别 | 独立思维结果 |
|---|---:|---|
| `clarify-requirements` | S | 分离事实、假设、约束和待决事项，只追问会改变决定的信息。 |
| `prototype-solution` | A | 用最小可视或可执行实验接受或否决一个明确不确定性。 |

### 研究与沟通

| Workflow | 级别 | 独立思维结果 |
|---|---:|---|
| `coauthor-documents` | A | 先确定受众、决定和 claim hierarchy，再按证据写作并做陌生读者检查。 |
| `research-primary-sources` | A | 综合多份一手来源，保留版本、矛盾、引用和事实/推断边界；科学假设与研究证据评估作为按需 reference 加载，单一工具参数查询不激活。 |

### 安全推理

| Workflow | 级别 | 独立思维结果 |
|---|---:|---|
| `review-security-practices` | A | 追踪真实安全数据流，验证问题可达性并给出证据化加固优先级。 |
| `threat-model-system` | A | 映射资产、信任边界、攻击目标、攻击路径、控制、负责人和残余风险。 |

### 设计推理

| Workflow | 级别 | 独立思维结果 |
|---|---:|---|
| `design-frontend` | A | 把用户目标和证据转成有意图的层级、状态、响应式和审美方向，并防止参考漂移。 |
| `design-motion` | A | 只为反馈、连续性、状态或层级使用动效，并推理时序、中断、降级和性能。 |
| `design-visual-theme` | A | 把产品与品牌意图转成语义化颜色、字体、间距和组件规则。 |

## 本轮删除测试

- `execute-plan`：淘汰。执行已有计划属于常驻核心的基本执行循环，独立 skill 会重复加载范围控制、逐步验证和偏差处理。
- `orchestrate-agent-work`：淘汰。是否可委派、并发上限和隔离规则由宿主能力与当前系统指令决定，不应固化成跨宿主全局 skill。
- `formulate-scientific-hypotheses`：并入 `research-primary-sources` 的条件 reference；保留竞争假设、可证伪预测和分析计划机制。
- `evaluate-scientific-evidence`：并入同一条件 reference；保留研究设计、测量、偏差、统计推断和结论边界机制。

被淘汰名称不再进入 runtime catalog、语义路由或本机同步集合；历史与来源仍由 Git 提交保留。

## 已移出 canonical runtime

本轮移出 18 个 owner：办公文件操作、PostgreSQL、CLI、MCP、截图、Git worktree/冲突、Jupyter、浏览器测试、视频制作，以及 skill 创建/发现、仓库准备、分支收尾和安全 ownership 工具流程。它们的历史实现仍可从 Git 历史恢复，但不再占用模型的 runtime catalog。

没有简单丢弃其中可迁移的原则：验证渲染或消费结果、保留权威状态、先对账再完成、保护不变量和安全恢复路径，已经进入常驻核心或现有 workflow。命令、格式、SDK 和产品细节则由 Agent 在任务时从当前环境和一手文档获取。

## 后续保留标准

新来源可以无限增长，但 canonical 只接受两种结果：

1. 经 held-out 或重复证据证明能跨场景提升行为的思维核心机制；
2. 有独立认知结果、无法由核心或现有 owner 简洁覆盖的按需 workflow。

删除产品、工具、文件格式和领域名后若没有可复用决策规则，就不进入 canonical。没有匹配 workflow 是合法结果。
