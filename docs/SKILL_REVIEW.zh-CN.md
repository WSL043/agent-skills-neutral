# 技能实现、去重与保留审查

当前活动库共 45 个通用 Agent Skill：S=9、A=36，分为 15 组。所有 B 级、厂商专属、组织流程绑定、占位或只提供宽泛建议的实现都已移出活动库。默认配置仍只有 6 个 S 级核心工作流；其余能力由中英双语正向/负向规则按需路由，一般只加载 1 个主技能和最多 1 个辅助技能。

## 完整活动清单

### Agent 技能生态

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `create-agent-skill` | S | 标准 frontmatter、精确触发描述、渐进披露、资源复用、有/无技能对照评测和结构校验。 | 按需 |
| `discover-agent-skills` | A | 先查清单，再完整审查正文、依赖、信任边界、重叠度和许可证，最后推荐最小集合。 | 按需 |
| `evaluate-agent` | A | 先定义 claim、任务集和 grader，再做同条件 baseline/candidate 运行，保存 trace 并分析失败和不确定性。 | 按需 |

### Agent 工具协议

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `build-mcp-server` | A | 把能力建模为窄粒度 MCP tools/resources，定义 schema、结构化错误、传输无关领域逻辑和客户端测试。 | 按需 |

### 架构、领域与 API

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `design-codebase` | A | 绘制依赖和变更压力，比较结构方案，再执行带回滚点的增量架构迁移。 | 按需 |
| `model-domain` | A | 从真实场景提炼术语、实体、值对象、不变量、事件、状态转换、所有权和限界上下文。 | 按需 |
| `review-api-design` | A | 盘点消费者与兼容承诺，审查资源、操作、schema、错误和演进策略；输出证据、影响、建议和严重级别。 | 明确 API 契约任务 |

### 文档与办公制品

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `work-with-docx` | A | 常规操作走 DOCX 库，高保真修改走 OOXML；重新打开并渲染验证版式。 | 按需 |
| `work-with-pdf` | A | 统一处理提取、编辑、表单、OCR、生成、拆分合并，并用页面渲染做视觉 QA。 | 按需 |
| `work-with-pptx` | A | 新建演示用可编辑生成，既有模板用 OOXML/包级修改，最后渲染每页检查。 | 按需 |
| `work-with-xlsx` | A | 常规处理用 dataframe/workbook 库；需保留宏、透视表等特性时使用包级 XML 修改。 | 按需 |

### 数据库与数据

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `work-with-postgresql` | A | 先确认运行时、schema、workload、权限和一致性，再基于 plan、锁、代表性数据和迁移证据做可回滚修改。 | PostgreSQL 任务 |

### 开发者工具

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `build-cli` | A | 分离参数解析、领域逻辑、I/O 和展示，并测试配置优先级、stdout/stderr、JSON 输出与退出码。 | 按需 |
| `capture-screen` | A | 只捕获必要区域，保留缩放与坐标，检查隐私、裁切和尺寸。 | 显式截图任务 |
| `resolve-merge-conflicts` | A | 同时检查 base/ours/theirs 与相关提交，整合双方意图，重建派生文件并测试两边改动。 | 显式冲突任务 |
| `use-git-worktrees` | A | 使用明确路径和分支创建隔离工作区，验证基线，只在提交可达性确认后清理。 | 显式 worktree 任务 |
| `work-with-jupyter-notebook` | A | 组织可复现叙事，把复用逻辑移到模块，重启内核后按顺序执行全部单元格。 | 按需 |
| `prepare-repository-for-agents` | A | 基于真实仓库约定、测试、CI、指令和缺口，只补充不重复的 Agent guidance，并运行结构和项目校验。 | 仓库 Agent-ready 任务 |

### 实现与质量

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `develop-with-tdd` | S | 围绕可观察行为执行 red-green-refactor；旧代码先补特征测试。 | 按需 |
| `diagnose-software` | S | 复现并缩小问题，定位第一次分歧，逐个检验可证伪假设，修根因并补回归证据。 | 默认 |
| `optimize-performance` | A | 用可比 baseline 定位 bottleneck，做 targeted change，重新测量 correctness 和收益，并留下 guard。 | 按需 |
| `simplify-code` | A | 明确可观察 contract，只简化已证明的 incidental complexity，并用聚焦和回归检查证明行为保持。 | 按需 |
| `review-code` | S | 分开审查需求符合度和实现质量，只报告可验证问题，并支持自审、请求审查和处理反馈。 | 默认 |
| `verify-completion` | S | 将每项声明映射到最新权威检查，同时验证副作用和最终状态；受阻时收窄结论。 | 默认 |

### 运行观测与系统演进

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `instrument-observability` | A | 从运营问题反推日志、指标和 trace；限制标签基数、关联请求、保护敏感数据，并验证真实发出的信号和告警。 | 明确可观测性任务 |
| `migrate-system-safely` | A | 盘点消费者和权威数据源，执行 expand/backfill/switch/contract，持续对账并保留回滚；只有实测零使用后才清理兼容层。 | 明确迁移任务 |

### 规划、交接与编排

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `execute-plan` | S | 验证计划假设，按依赖顺序执行可验证的 tracer slice；新决策改变范围时暂停并更新计划。 | 默认 |
| `finish-development-branch` | A | 检查分支和 diff，跑最终校验，安全选择合并、PR 或交接，并在清理前保证提交可达。 | 按需 |
| `handoff-task-context` | A | 保存目标、已验证现状、证据、决策、frontier、阻塞和下一步；恢复时逐项与实时仓库及运行状态对账。 | 明确保存/恢复交接 |
| `orchestrate-agent-work` | A | 绘制决策 frontier，主 Agent 保留阻塞路径，只委派隔离的 tracer slice，最后统一集成并做跨任务验证。 | 明确多 Agent 任务 |
| `plan-implementation` | S | 检查仓库后输出带依赖边的 tracer slice、文件/符号级步骤、测试、迁移、回滚和验收证据。 | 默认 |

### 需求与方案验证

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `clarify-requirements` | S | 分离事实、假设、约束和待决事项，只问高信息量问题并生成可测试验收条件。 | 默认 |
| `prototype-solution` | A | 对一个明确不确定性限时制作最小可视或可执行原型，用结果接受或否决方案。 | 按需 |

### 研究与沟通

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `coauthor-documents` | A | 先确定受众和大纲，再按章节用证据写作，最后做陌生读者检查。 | 按需 |
| `research-primary-sources` | A | 广泛发现、精读权威一手来源、记录版本和矛盾，并给每个重要结论就近引用。 | 按需 |
| `formulate-scientific-hypotheses` | A | 冻结 observation，区分 claim type，生成 rival explanations 和 discriminating predictions，并匹配测量与分析。 | 按需 |
| `evaluate-scientific-evidence` | A | 分离结果与解释，检查研究设计、测量、偏差、统计推断、稳健性与复现证据，再把每个主要结论限定到实际证据范围。 | 明确科研证据评估任务 |

### 安全

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `map-security-ownership` | A | 结合敏感路径、所有权文件、提交历史、审查活动、活跃度和集中度指标。 | 按需 |
| `review-security-practices` | A | 追踪真实安全数据流，对照当前官方指南，验证问题可达性并按验证成本排加固优先级。 | 显式安全意图 |
| `threat-model-system` | A | 映射资产、数据流、信任边界、攻击者目标、攻击路径、控制、负责人和残余风险。 | 按需 |

### 视觉、界面与动效

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `design-frontend` | A | 推断或确认 brief，建立单一设计系统，处理内容、资产、层级、完整状态、响应式、无障碍与性能；重设计时保持路由、IA、品牌和分析契约，并检查参考图漂移。 | UI、重设计、截图转代码 |
| `design-motion` | A | 动效必须服务反馈、连续性、状态或层级；明确时长、缓动、中断，测试减少动态效果和性能。 | 明确界面动效 |
| `design-visual-theme` | A | 将产品和品牌意图转成语义化颜色、字体、间距和组件 token，用代表性内容验证并通过共享样式应用。 | 主题、brand kit、token |

### 媒体制作

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `produce-programmatic-video` | A | 将源媒体和需求转成明确时间轴，只同步和重渲染受影响部分，分层完成字幕/音频/合成，并对最终成片执行 probe、关键帧和视听 QA。 | 明确视频合成/剪辑/渲染任务 |

### Web 运行时测试

| 技能 | 级别 | 具体实现 | 路由 |
|---|---:|---|---|
| `test-web-app` | S | 控制服务就绪和浏览器生命周期，使用语义选择器，收集断言、控制台、网络和截图后重新运行。 | 按需 |

## 本轮深度整合

- `Leonxlnx/taste-skill`：13 个技能、研究文档、脚本和插件清单均已阅读。保留 brief 推断、三个视觉轴、统一设计系统、内容与资产、布局节奏、完整状态、响应式/无障碍/性能、审计式重设计和图像参考防漂移；合并进 `design-frontend`、`design-motion`、`design-visual-theme`，没有复制 13 个重叠技能。
- `mattpocock/skills`：补齐 `ask-matt`、`implement`、`handoff`、`to-spec`、`to-tickets`、`triage`、`wayfinder` 的编排链路。把 phase transition、tracer slice、依赖边、decision frontier、expand-migrate-contract 和有界交接分别吸收进规划、执行、编排、迁移与交接技能。
- `psenger/ai-agent-skills`：新增 `handoff-task-context` 和 `review-api-design`。API 评审来源标记 CC-BY-4.0，并删除绝对化风格偏好，以仓库契约和当前一手规范为准。
- `addyosmani/agent-skills`：只保留现有库确实缺少的可观测性与系统迁移能力；上下文工程、增量开发、规格驱动等重叠内容并回现有核心工作流，不新增副本。
- `muratcankoylan/Agent-Skills-for-Context-Engineering`：只吸收文件化上下文、压缩保真和恢复对账原则；不保留运行时专属压缩、固定阈值和 KV-cache 假设。

## 已移除的 12 个旧实现

| 移除项 | 原因与替代 |
|---|---|
| `configure-pre-commit` | 过窄，且应遵循仓库既有 CI/钩子；通用检查由计划、执行和验证技能覆盖。 |
| `migrate-test-fixtures` | 原始实现绑定 ShoeHorn，通用化后仍只是弱检查清单；真正迁移使用 `migrate-system-safely`。 |
| `scaffold-exercises` | 小众且没有可复用模板或工具，未达到 A 级阈值。 |
| `create-visual-art` | 与专用图像生成/设计工具重叠，且自身不含渲染能力。 |
| `develop-shaders` | 依赖具体渲染器、GPU 和分析工具，宽泛清单无法提供稳定增量价值。 |
| `build-android-app` | 宽泛平台指南，无模板和固定 SDK；具体项目应路由到代码实现并读取当前官方文档。 |
| `build-flutter-app` | 同上，版本和目标平台差异太大。 |
| `build-ios-app` | 同上，且强依赖 Apple 工具链和项目状态。 |
| `build-react-native-app` | 同上，架构与版本差异会改变实现。 |
| `build-winui-app` | 同上，SDK、打包与部署模型必须实时检查。 |
| `build-aspnet-core` | 通用框架清单与现有工程流程高度重叠，目标 .NET 版本必须查当前项目和官方文档。 |
| `build-fullstack-app` | 与前端、架构、API、测试和执行技能重叠；薄垂直切片方法已并入规划和执行。 |

## 有意没有保留的新增实现

- Taste 的 v2 实验稿、固定框架/GSAP/Tailwind 规则、强制每节图片数量、强制暗色模式、任意字体/颜色/标点禁令、静态风格变体、Google Stitch 和没有证据支撑的“懒惰”百分比。
- Addy 的 source-driven/context/spec/incremental/shipping 等独立技能：方法有价值，但与现有研究、澄清、计划、执行、TDD、验证高度重复。
- psenger 的 `design-critique`、`arch-lens`：分别与需求澄清、代码库设计重叠，且后者绑定特定 subagent/tracker 工作流。
- Context Engineering 的独立压缩、退化与 latent briefing 技能：多数属于 Agent 运行时职责，固定阈值和 KV-cache 前提不具备跨客户端可移植性。

## 仍需遵守的限制

- `diagnose-software`：间歇性故障可能需要概率性或重复证据，而不是强求完全确定性的复现。
- `evaluate-agent`：必须区分主动改变的实验变量与未受控的混杂变量。
- `work-with-postgresql`：破坏性操作或权限变更需要明确授权；安全恢复有时应采用前向修复而非回滚。
- `create-agent-skill`：负向路由触发器属于硬排除，因此重要边界必须覆盖正负意图同时出现的回归场景。
- `handoff-task-context` 的内容只是待验证声明，恢复时必须检查实时文件、Git、测试和运行状态。
- `review-api-design` 不把 REST 风格偏好当成普遍真理；当前契约、消费者和官方标准优先。
- `instrument-observability` 必须接入真实遥测后端并用代表性流量验证，禁止秘密信息和无界标签。
- `migrate-system-safely` 的收缩清理必须有实际消费/运行数据，不能只凭部署成功或等待时间。
