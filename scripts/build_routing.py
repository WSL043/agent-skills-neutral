from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def R(
    kind: str,
    choose: str,
    avoid: str,
    triggers: list[str],
    negative: list[str] | None = None,
    maturity: str = "stable",
    explicit_only: bool = False,
) -> dict[str, object]:
    return {
        "kind": kind,
        "maturity": maturity,
        "choose_when": choose,
        "avoid_when": avoid,
        "triggers": triggers,
        "negative_triggers": negative or [],
        "explicit_only": explicit_only,
    }


CATEGORY_SUMMARIES = {
    "agent-skill-ecosystem": "Create, discover, compare, and maintain Agent Skills.",
    "agent-tooling": "Build protocols and tools that expose capabilities to agents.",
    "architecture-codebase": "Design code boundaries and domain models before large structural change.",
    "artifacts-documents": "Read, create, edit, and visually verify office and document formats.",
    "developer-tooling": "Operate developer workflows, repositories, notebooks, screenshots, and scaffolding.",
    "implementation-quality": "Implement, diagnose, review, and verify software behavior.",
    "mobile-desktop-development": "Build explicitly requested Android, Flutter, iOS, React Native, or WinUI applications.",
    "planning-orchestration": "Plan, execute, delegate, and finish bounded engineering work.",
    "requirements-design": "Clarify decisions or prototype a specific uncertainty.",
    "research-communication": "Research authoritative sources and coauthor decision-ready documents.",
    "security": "Threat-model, review, and map ownership of security-sensitive systems.",
    "visual-design-motion": "Design visual systems, interfaces, motion, art, and shaders.",
    "web-backend-development": "Build explicitly requested ASP.NET Core or end-to-end full-stack applications.",
    "web-ui-testing": "Exercise and diagnose web applications in a real browser.",
}


ROUTING = {
    "create-agent-skill": R(
        "meta",
        "The task is to create, consolidate, test, or revise an Agent Skill or SKILL.md.",
        "Do not use merely to find or install an existing skill.",
        ["create agent skill", "write skill.md", "skill authoring", "skill creator", "创建技能", "创建 agent skill", "编写技能", "整合技能", "修改 skill"],
        ["find skill", "install skill", "查找技能", "安装技能"],
    ),
    "discover-agent-skills": R(
        "meta",
        "The task is to find, compare, audit, or install an existing Agent Skill.",
        "Do not use when the requested outcome is authoring a new skill.",
        ["find skill", "discover skill", "install skill", "skill registry", "skills catalog", "查找技能", "查找可安装技能", "发现技能", "安装技能", "技能清单"],
        ["write skill.md", "create agent skill", "编写技能", "创建技能"],
    ),
    "build-mcp-server": R(
        "domain",
        "The user explicitly needs an MCP server, MCP tools/resources, or an API exposed through MCP.",
        "Do not use for an ordinary API or CLI that is not consumed through MCP.",
        ["mcp server", "model context protocol", "mcp tool", "mcp resource", "构建 mcp", "mcp 服务", "mcp 工具"],
        ["rest api only", "普通 api"],
    ),
    "design-codebase": R(
        "domain",
        "The task concerns module boundaries, dependency direction, modularization, or architecture migration.",
        "Do not use for a small localized implementation with no structural decision.",
        ["codebase architecture", "module boundary", "modularize", "dependency direction", "architecture proposal", "代码库架构", "模块边界", "架构重构", "模块化"],
    ),
    "model-domain": R(
        "domain",
        "Business concepts, invariants, state transitions, or bounded contexts need explicit modeling.",
        "Do not use for directory organization without domain-rule ambiguity.",
        ["domain model", "bounded context", "ubiquitous language", "business invariant", "state transition", "领域模型", "限界上下文", "统一语言", "业务不变量"],
    ),
    "work-with-docx": R(
        "domain",
        "A DOCX, DOTX, Microsoft Word document, tracked change, or Word template is a primary input or output.",
        "Do not use for PDF-only, plain Markdown, or general prose with no Word deliverable.",
        [".docx", ".dotx", "docx", "docx document", "word document", "microsoft word", "tracked changes", "word template", "word 文档", "docx 文档", "修订模式"],
        ["pdf only", "纯 markdown"],
    ),
    "work-with-pdf": R(
        "domain",
        "A PDF must be read, created, filled, edited, merged, split, OCRed, or visually checked.",
        "Do not use when PDF is only an incidental citation link.",
        [".pdf", "pdf form", "merge pdf", "split pdf", "ocr pdf", "create pdf", "pdf 表单", "合并 pdf", "拆分 pdf", "生成 pdf", "读取 pdf"],
    ),
    "work-with-pptx": R(
        "domain",
        "PowerPoint slides, PPTX/POTX files, slide templates, or rendered deck QA are primary.",
        "Do not use for a static poster or prose outline with no slide deliverable.",
        [".pptx", ".potx", "powerpoint", "slide deck", "presentation template", "rendered slides", "幻灯片", "演示文稿", "ppt 模板", "制作 ppt", "编辑 ppt"],
        ["static poster", "静态海报"],
    ),
    "work-with-xlsx": R(
        "domain",
        "An Excel/XLSX/XLSM workbook, spreadsheet formulas, pivots, or CSV-to-workbook deliverable is primary.",
        "Do not use for a small Markdown table or database query with no spreadsheet artifact.",
        [".xlsx", ".xlsm", "excel workbook", "spreadsheet", "pivot table", "excel formula", "excel 表格", "电子表格", "工作簿", "数据透视表"],
        ["markdown table", "数据库查询"],
    ),
    "build-cli": R(
        "domain",
        "The task explicitly creates or substantially changes a command-line interface.",
        "Do not use for a one-off shell command or internal function with no CLI surface.",
        ["build cli", "command line interface", "subcommand", "exit code", "cli tool", "命令行工具", "设计 cli", "子命令"],
        ["one-off command", "单条命令"],
    ),
    "capture-screen": R(
        "support",
        "The user explicitly needs a screenshot, window capture, pixel evidence, or coordinate-preserving image.",
        "Do not select merely because another visual skill will eventually render an artifact.",
        ["take screenshot", "capture screen", "window capture", "screen region", "pixel coordinates", "截图", "截屏", "窗口截图", "屏幕区域"],
    ),
    "configure-pre-commit": R(
        "domain",
        "The repository explicitly needs pre-commit hooks or commit-time lint/format checks.",
        "Do not use for ordinary CI configuration or a one-time formatter run.",
        ["pre-commit", "commit hook", "git hook", "commit-time lint", "提交前检查", "提交钩子", "precommit"],
        ["ci only", "只跑一次格式化"],
        maturity="conditional",
    ),
    "migrate-test-fixtures": R(
        "domain",
        "The explicit task is a repeatable migration of test fixtures, fixture formats, or fixture factories.",
        "Do not use for ordinary test edits or application data migration.",
        ["migrate test fixtures", "fixture conversion", "fixture format migration", "迁移测试夹具", "转换 fixture", "测试数据夹具迁移"],
        ["database migration", "普通测试修改", "数据库迁移"],
        maturity="experimental",
    ),
    "resolve-merge-conflicts": R(
        "domain",
        "Git reports merge/rebase conflicts or the user explicitly asks to integrate conflicting histories.",
        "Do not use for ordinary code review or non-conflicting branch updates.",
        ["merge conflict", "rebase conflict", "unmerged paths", "conflict markers", "解决冲突", "合并冲突", "变基冲突"],
    ),
    "scaffold-exercises": R(
        "domain",
        "The explicit deliverable is a coding exercise, workshop, kata, starter repo, hints, and reference solution.",
        "Do not use for ordinary project scaffolding or production features.",
        ["coding exercise", "workshop exercise", "code kata", "starter exercise", "training task", "编程练习", "课程练习", "代码 kata", "教学脚手架"],
        ["production scaffold", "生产项目脚手架"],
        maturity="conditional",
    ),
    "use-git-worktrees": R(
        "domain",
        "The task explicitly needs an isolated Git checkout, concurrent branches, or a worktree lifecycle.",
        "Do not use for normal branch switching in one checkout.",
        ["git worktree", "isolated checkout", "parallel branch checkout", "创建 worktree", "隔离工作树", "并行分支"],
    ),
    "work-with-jupyter-notebook": R(
        "domain",
        "A .ipynb notebook, clean-kernel execution, notebook tutorial, or notebook repair is primary.",
        "Do not use for a normal Python module or script with no notebook artifact.",
        [".ipynb", "jupyter notebook", "clean kernel", "notebook cells", "jupyter 笔记本", "运行 notebook", "笔记本单元格"],
        ["python script only", "普通 python 脚本"],
    ),
    "develop-with-tdd": R(
        "workflow",
        "The user requests TDD, test-first implementation, or a behavior change suited to a red-green-refactor cycle.",
        "Do not force it onto exploratory spikes or changes that cannot be meaningfully tested first.",
        ["tdd", "test driven", "test-first", "red green refactor", "测试驱动", "先写测试", "红绿重构"],
        ["throwaway spike", "一次性探索"],
    ),
    "diagnose-software": R(
        "workflow",
        "A bug, flaky behavior, regression, failure, or unexplained runtime symptom needs root-cause diagnosis.",
        "Do not use when the cause is already proven and the task is only implementation.",
        ["debug", "diagnose", "root cause", "flaky", "regression", "intermittent failure", "排查问题", "诊断 bug", "根因", "偶发失败", "为什么失败"],
        ["known fix only", "原因已确定"],
    ),
    "review-code": R(
        "workflow",
        "The user requests review of a diff, patch, branch, or implementation quality and requirement fit.",
        "Use the security review skill instead when the primary question is vulnerability or hardening analysis.",
        ["code review", "review diff", "review patch", "pull request review", "self review", "代码评审", "审查 diff", "审查补丁", "评审代码"],
        ["security review", "vulnerability review", "安全审查", "漏洞审查"],
    ),
    "verify-completion": R(
        "support",
        "The task asks to prove completion, validate a claimed result, or perform final evidence checks.",
        "Do not make it the primary domain skill when a concrete artifact or runtime skill matches better.",
        ["verify completion", "prove it works", "final validation", "completion evidence", "确认完成", "验证是否成功", "最终验证", "完成证据"],
    ),
    "build-android-app": R(
        "domain",
        "The task explicitly targets native Android, Kotlin, Jetpack Compose, Gradle Android modules, or Android platform APIs.",
        "Do not use for Flutter, React Native, or generic mobile design.",
        ["android app", "android compose", "kotlin android", "jetpack compose", "android gradle", "安卓应用", "安卓原生", "compose 页面"],
        ["flutter", "react native", "ios"],
        maturity="conditional",
    ),
    "build-flutter-app": R(
        "domain",
        "The task explicitly uses Flutter, Dart, Flutter widgets, or Flutter multi-platform targets.",
        "Do not use for native Android/iOS or React Native.",
        ["flutter app", "dart app", "flutter widget", "flutter 应用", "dart 项目", "flutter 页面"],
        ["jetpack compose", "swiftui", "react native"],
        maturity="conditional",
    ),
    "build-ios-app": R(
        "domain",
        "The task explicitly targets iOS, Swift, SwiftUI, UIKit, Xcode, or Apple mobile platform APIs.",
        "Do not use for Flutter, React Native, or generic mobile design.",
        ["ios app", "swiftui", "uikit", "xcode project", "swift app", "ios 应用", "苹果原生应用"],
        ["flutter", "react native", "android"],
        maturity="conditional",
    ),
    "build-react-native-app": R(
        "domain",
        "The task explicitly uses React Native and needs Android/iOS shared mobile implementation.",
        "Do not use for React web, native Swift/Kotlin, or Flutter.",
        ["react native", "react-native", "rn mobile app", "react native 应用", "rn 应用"],
        ["react web", "flutter", "swiftui", "jetpack compose"],
        maturity="conditional",
    ),
    "build-winui-app": R(
        "domain",
        "The task explicitly targets WinUI, Windows App SDK, XAML desktop UI, or packaged Windows applications.",
        "Do not use for generic .NET backend or cross-platform desktop UI.",
        ["winui", "windows app sdk", "xaml desktop", "msix", "winui 应用", "windows 桌面应用"],
        ["asp.net", "wpf only", "maui"],
        maturity="conditional",
    ),
    "execute-plan": R(
        "workflow",
        "An approved implementation plan already exists and the user asks to carry it out.",
        "Do not use when the plan still needs to be written or key decisions remain unresolved.",
        ["execute the plan", "implement existing plan", "follow this plan", "按计划执行", "按现有计划执行", "执行现有计划", "照这个计划实现"],
        ["write a plan", "create implementation plan", "制定计划", "写实现计划"],
    ),
    "finish-development-branch": R(
        "workflow",
        "Implementation is complete and the branch must be verified, prepared for review/merge, handed off, or cleaned up.",
        "Do not use in the middle of active implementation.",
        ["finish branch", "prepare for merge", "ready for review", "finalize development branch", "完成开发分支", "准备合并", "提交前收尾"],
        ["start implementation", "开始实现"],
    ),
    "orchestrate-agent-work": R(
        "workflow",
        "The runtime supports delegation and the task contains independent bounded subtasks or explicit multi-agent work.",
        "Do not use for a single blocking task or overlapping writes without isolation.",
        ["multiple agents", "parallel agents", "delegate tasks", "subagent", "多 agent", "并行代理", "委派任务", "子代理"],
    ),
    "plan-implementation": R(
        "workflow",
        "The user asks for a concrete implementation plan, migration plan, or file-by-file engineering plan.",
        "Do not use when an approved plan already exists and should be executed.",
        ["implementation plan", "migration plan", "plan the changes", "file-by-file plan", "实现计划", "迁移计划", "制定开发计划", "拆解实现步骤"],
        ["execute the plan", "按计划执行", "已有计划直接实现"],
    ),
    "clarify-requirements": R(
        "workflow",
        "Requirements are materially ambiguous, conflicting, high-impact, or the user explicitly asks for requirement clarification.",
        "Do not trigger merely because any task could benefit from more detail; inspect available context first.",
        ["clarify requirements", "requirements ambiguous", "acceptance criteria", "challenge this proposal", "澄清需求", "需求不清", "验收标准", "拷问方案"],
    ),
    "prototype-solution": R(
        "workflow",
        "A prototype, spike, proof of concept, or experiment is needed to answer one named uncertainty.",
        "Do not use when the user expects production-ready implementation without a learning goal.",
        ["prototype", "proof of concept", "poc", "technical spike", "clickable prototype", "原型", "概念验证", "技术预研", "做个 poc"],
        ["production ready", "生产级完整实现"],
    ),
    "coauthor-documents": R(
        "workflow",
        "The task is collaborative long-form writing, outlining, or revising a proposal, design doc, memo, report, or policy.",
        "Use a file-format skill as primary when manipulating DOCX/PDF/PPTX is the dominant task.",
        ["coauthor document", "write proposal", "design document", "draft memo", "long-form report", "共同写文档", "撰写提案", "设计文档", "起草备忘录"],
        [".docx", ".pdf", ".pptx", "编辑 word 格式"],
    ),
    "research-primary-sources": R(
        "workflow",
        "The answer requires current authoritative primary sources, precise citations, or fact/inference separation.",
        "Do not use for purely local code inspection with no external or documentary research need.",
        ["primary sources", "official documentation", "research with citations", "verify sources", "authoritative source", "查官方资料", "一手资料", "带引用研究", "核实来源"],
    ),
    "map-security-ownership": R(
        "domain",
        "The task asks who owns security-sensitive code, bus factor, stewardship, or CODEOWNERS gaps.",
        "Do not use for general contributor statistics or ordinary code review.",
        ["security ownership", "security bus factor", "codeowners gap", "sensitive code owners", "安全归属", "安全代码负责人", "关键代码所有权"],
    ),
    "review-security-practices": R(
        "domain",
        "The primary task is secure-coding review, vulnerability analysis, or framework-specific hardening.",
        "Do not use for a general quality review with no security focus.",
        ["security review", "secure coding", "vulnerability review", "security hardening", "安全审查", "安全代码审查", "漏洞检查", "安全加固", "安全最佳实践"],
        ["general code review", "普通代码评审"],
        explicit_only=True,
    ),
    "threat-model-system": R(
        "domain",
        "The task explicitly needs assets, trust boundaries, attacker goals, abuse cases, attack paths, or a threat model.",
        "Do not use for a narrow code finding that is already known.",
        ["threat model", "trust boundary", "attack path", "abuse case", "attacker goal", "威胁建模", "信任边界", "攻击路径", "滥用场景"],
    ),
    "create-visual-art": R(
        "domain",
        "The primary deliverable is an original static poster, cover, artwork, or print composition.",
        "Do not use for application UI, charts, slide decks, or image editing requiring a dedicated generation tool.",
        ["visual artwork", "poster design", "book cover", "static art", "print composition", "视觉艺术", "海报设计", "封面设计", "静态作品"],
        ["app ui", "dashboard", "slide deck", "图片编辑", "应用界面", "演示文稿"],
        maturity="conditional",
    ),
    "design-frontend": R(
        "domain",
        "The task is interface hierarchy, responsive layout, component design, UI polish, or implementation-aware frontend design.",
        "Do not use for a static poster, presentation, or backend-only task.",
        ["frontend design", "ui design", "responsive interface", "design component", "polish ui", "前端设计", "界面设计", "响应式页面", "组件设计", "优化 ui"],
        ["static poster", "backend only", "静态海报", "纯后端"],
    ),
    "design-motion": R(
        "domain",
        "The task explicitly concerns UI animation, transition timing, easing, motion audit, or reduced-motion behavior.",
        "Do not use for video editing or animation unrelated to interface behavior.",
        ["ui animation", "motion design", "transition timing", "easing", "animation audit", "界面动画", "动效设计", "过渡动画", "缓动", "动效审计"],
        ["video editing", "视频剪辑"],
    ),
    "design-visual-theme": R(
        "domain",
        "The task needs reusable color, typography, spacing, style tokens, or a visual theme across artifacts.",
        "Do not use when only one isolated color value or font choice is requested.",
        ["visual theme", "design tokens", "color typography system", "theme system", "视觉主题", "设计 token", "配色字体", "主题系统", "设计规范"],
    ),
    "develop-shaders": R(
        "domain",
        "The task explicitly involves GLSL, HLSL, WGSL, GPU materials, post-processing, or real-time shader performance.",
        "Do not use for ordinary CSS effects or offline image editing.",
        ["glsl", "hlsl", "wgsl", "shader", "gpu material", "post-processing", "着色器", "实时渲染", "gpu 材质", "后处理"],
        ["css gradient", "图片编辑"],
        maturity="conditional",
    ),
    "build-aspnet-core": R(
        "domain",
        "The task explicitly targets ASP.NET Core, .NET web APIs, middleware, or server-rendered .NET web applications.",
        "Do not use for generic full-stack work or non-.NET backends.",
        ["asp.net core", "aspnet core", ".net web api", "asp.net middleware", "asp.net 应用", ".net 后端"],
        ["node backend", "python backend", "非 .net"],
        maturity="conditional",
    ),
    "build-fullstack-app": R(
        "domain",
        "The user explicitly needs one end-to-end feature crossing frontend, backend, data, and authentication boundaries.",
        "Do not use for frontend-only, backend-only, or architecture-only work.",
        ["full-stack app", "fullstack app", "end-to-end web feature", "frontend and backend", "全栈应用", "前后端一起实现", "端到端 web 功能"],
        ["frontend only", "backend only", "纯前端", "纯后端"],
        maturity="conditional",
    ),
    "test-web-app": R(
        "domain",
        "A real browser must exercise a web flow, inspect console/network state, or perform UI/runtime verification.",
        "Do not use for screenshot-only capture or non-web application testing.",
        ["test web app", "browser test", "playwright", "ui flow test", "browser automation", "测试网页", "浏览器测试", "自动化页面", "验证 web 流程"],
        ["screenshot only", "native mobile app", "只截图", "原生移动应用"],
    ),
}


IMPLEMENTATION = {
    "create-agent-skill": "Standard frontmatter, concise trigger description, progressive disclosure, with-skill/baseline evaluation, and structural validation.",
    "discover-agent-skills": "Manifest-first discovery followed by full-body, dependency, trust, overlap, and license inspection before recommendation.",
    "build-mcp-server": "Model operations as narrow MCP tools/resources with schemas, transport-independent domain logic, structured errors, and client tests.",
    "design-codebase": "Map dependencies and change pressure, compare structural options, then stage an incremental migration with rollback points.",
    "model-domain": "Build a glossary, entities/values, invariants, events, state transitions, ownership, and bounded contexts from real scenarios.",
    "work-with-docx": "Route between high-level DOCX libraries and surgical OOXML editing, then reopen and render for layout verification.",
    "work-with-pdf": "Route structural extraction/editing, forms, OCR, generation, merge/split, and rendered page QA through one entry.",
    "work-with-pptx": "Use editable generation for new decks, OOXML/package editing for high-fidelity templates, and rendered slide QA.",
    "work-with-xlsx": "Use dataframe/workbook libraries normally and package-level XML edits when macros, pivots, or unsupported features must survive.",
    "build-cli": "Separate parsing, domain logic, I/O, and presentation; define configuration precedence, stdout/stderr, JSON output, and exit-code tests.",
    "capture-screen": "Capture the smallest screen/window region with known scale and coordinates, then inspect privacy, clipping, and dimensions.",
    "configure-pre-commit": "Reuse pinned repository-native fast checks with file filters; keep slow or networked checks in pre-push/CI.",
    "migrate-test-fixtures": "Inventory fixture consumers and build a deterministic dry-run converter, then compare scenario semantics before removing the source format.",
    "resolve-merge-conflicts": "Inspect base/ours/theirs and relevant commits, integrate both intents, regenerate derived files, and test both change sets.",
    "scaffold-exercises": "Define learning objectives, starter state, tests, hints, and a separate reference solution verified from a clean environment.",
    "use-git-worktrees": "Create an explicit isolated path and branch, verify baseline state, and clean up only after reachability is confirmed.",
    "work-with-jupyter-notebook": "Organize a reproducible narrative, move reusable logic to modules, restart the kernel, and execute all cells in order.",
    "develop-with-tdd": "Run a strict red-green-refactor cycle around observable behavior, with characterization tests for legacy code.",
    "diagnose-software": "Reproduce and minimize, instrument the first divergence, test one falsifiable hypothesis, fix the root cause, and add regression evidence.",
    "review-code": "Review requirement fit and implementation quality separately, validate reachable findings, and support self/request/receive review modes.",
    "verify-completion": "Map each claim to a fresh authoritative check, verify side effects and final state, and narrow claims when checks are blocked.",
    "build-android-app": "Guide a Kotlin/Compose vertical slice with lifecycle, permissions, accessibility, unit/UI tests, and emulator/device checks.",
    "build-flutter-app": "Guide a Flutter vertical slice with explicit state, adaptive UI, target adapters, widget tests, and release builds per target.",
    "build-ios-app": "Guide a SwiftUI/UIKit slice with state ownership, concurrency/cancellation, accessibility, tests, and simulator/archive checks.",
    "build-react-native-app": "Guide shared React Native behavior with small native adapters, performance controls, tests, and fresh Android/iOS builds.",
    "build-winui-app": "Guide WinUI/XAML state, packaging mode, DPI/theme/accessibility, tests, and runtime verification on Windows.",
    "execute-plan": "Validate plan assumptions, execute dependency-ordered batches, run step evidence, and stop when a new decision changes scope.",
    "finish-development-branch": "Inspect the branch/diff, run final checks, choose merge/PR/handoff safely, and preserve reachability before cleanup.",
    "orchestrate-agent-work": "Keep the blocker local, delegate disjoint side tasks with explicit outputs, then integrate and run cross-task checks.",
    "plan-implementation": "Inspect the repository and produce dependency-ordered file/symbol steps with tests, migration, rollback, and acceptance evidence.",
    "clarify-requirements": "Separate facts, assumptions, constraints, and open decisions; ask only high-information questions and produce testable acceptance criteria.",
    "prototype-solution": "Time-box the smallest visual or executable artifact that can accept/reject one explicit uncertainty.",
    "coauthor-documents": "Agree audience and outline first, draft claims with evidence section by section, then run a fresh-reader pass.",
    "research-primary-sources": "Discover broadly, read authoritative primary sources, track versions and contradictions, and cite each material claim.",
    "map-security-ownership": "Combine sensitive-path mapping, ownership files, history, review activity, recency, and concentration metrics.",
    "review-security-practices": "Trace real security data flows, compare current official guidance, validate reachable findings, and prioritize hardening with verification.",
    "threat-model-system": "Map assets, flows, trust boundaries, attacker goals, attack paths, controls, owners, and residual risk.",
    "create-visual-art": "Define concept and visual system, build a low-fidelity composition, render at target dimensions, and verify print/screen constraints.",
    "design-frontend": "Set visual direction and tokens, design critical and failure states, implement responsive components, and review accessibility and polish.",
    "design-motion": "Name motion purpose and exact timing/easing/interruption behavior, prototype in context, and test reduced motion and performance.",
    "design-visual-theme": "Create semantic color/type/spacing tokens, test representative content, and apply them through shared styles.",
    "develop-shaders": "Build a minimal test shader, visualize intermediate spaces/ranges, handle numerical edges, capture references, and profile GPU cost.",
    "build-aspnet-core": "Guide an ASP.NET Core vertical slice with contracts, DI lifetimes, cancellation, auth, problem responses, tests, and production-like startup.",
    "build-fullstack-app": "Guide one thin end-to-end slice across UI, server contract, data, auth, browser tests, and production build behavior.",
    "test-web-app": "Control server readiness and browser lifecycle, use semantic selectors, collect assertions/console/network/screenshots, and rerun fresh.",
}


RISK_NOTES = {
    "configure-pre-commit": "Low incremental value for experienced agents; keep only for explicit repository hook work.",
    "migrate-test-fixtures": "Weakest retained item: upstream inspiration was ShoeHorn-specific; this generic rewrite is an experimental checklist, not a bundled converter.",
    "scaffold-exercises": "Niche educational workflow with no bundled starter templates; explicit training tasks only.",
    "create-visual-art": "No rendering engine is bundled and it overlaps image-generation tools; use as art-direction workflow only.",
    "develop-shaders": "Broad and hardware/runtime-sensitive; requires an existing renderer and profiling tools.",
    "build-android-app": "Broad platform guide with no project template or pinned SDK; project conventions and current docs remain authoritative.",
    "build-flutter-app": "Broad platform guide with no project template or pinned SDK; explicit Flutter tasks only.",
    "build-ios-app": "Broad platform guide with no project template or pinned SDK; requires Apple tooling and project context.",
    "build-react-native-app": "Broad platform guide; React Native version and native architecture materially affect implementation.",
    "build-winui-app": "Broad platform guide; Windows SDK, packaging, and deployment model must be inspected live.",
    "build-aspnet-core": "Broad framework guide; target .NET version and repository conventions must be inspected live.",
    "build-fullstack-app": "High overlap with frontend/backend/testing skills; route only for explicit end-to-end full-stack work.",
}


PROFILES = {
    "default": [
        "clarify-requirements",
        "plan-implementation",
        "execute-plan",
        "diagnose-software",
        "review-code",
        "verify-completion",
    ],
    "software-engineering": [
        "clarify-requirements",
        "plan-implementation",
        "execute-plan",
        "develop-with-tdd",
        "diagnose-software",
        "review-code",
        "verify-completion",
        "resolve-merge-conflicts",
        "use-git-worktrees",
        "finish-development-branch",
        "orchestrate-agent-work",
        "build-cli",
        "test-web-app",
    ],
    "documents": ["work-with-docx", "work-with-pdf", "work-with-pptx", "work-with-xlsx", "coauthor-documents"],
    "security": ["threat-model-system", "review-security-practices", "map-security-ownership"],
    "design": ["design-frontend", "design-motion", "design-visual-theme", "create-visual-art", "develop-shaders"],
    "application-platforms": [
        "build-android-app",
        "build-flutter-app",
        "build-ios-app",
        "build-react-native-app",
        "build-winui-app",
        "build-aspnet-core",
        "build-fullstack-app",
    ],
}


catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
catalog_by_name = {item["name"]: item for item in catalog["skills"]}
if set(catalog_by_name) != set(ROUTING) or set(catalog_by_name) != set(IMPLEMENTATION):
    raise SystemExit("Routing and implementation maps must cover every catalog skill exactly once")

routes_dir = ROOT / "routes"
profiles_dir = ROOT / "profiles"
routes_dir.mkdir(exist_ok=True)
profiles_dir.mkdir(exist_ok=True)

categories = []
for category in sorted(CATEGORY_SUMMARIES):
    entries = []
    for name in sorted(item["name"] for item in catalog["skills"] if item["category"] == category):
        item = catalog_by_name[name]
        route = dict(ROUTING[name])
        route.update({"name": name, "level": item["reference_level"], "path": item["path"] + "/SKILL.md"})
        entries.append(route)
    route_path = routes_dir / f"{category}.json"
    route_path.write_text(
        json.dumps(
            {"schema_version": 1, "category": category, "summary": CATEGORY_SUMMARIES[category], "skills": entries},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    categories.append(
        {
            "name": category,
            "summary": CATEGORY_SUMMARIES[category],
            "route_file": f"routes/{category}.json",
            "skill_count": len(entries),
        }
    )

for profile, names in PROFILES.items():
    (profiles_dir / f"{profile}.txt").write_text("\n".join(f"skills/{name}" for name in names) + "\n", encoding="utf-8")

index = {
    "schema_version": 1,
    "library": "agent-skills-neutral",
    "preferred_router": "python scripts/select_skills.py <task> --json",
    "manual_protocol": [
        "Choose one category from this index.",
        "Read only that category's route_file.",
        "Load the best matching SKILL.md completely.",
        "Add at most one support skill unless the task explicitly spans multiple phases.",
    ],
    "default_profile": "profiles/default.txt",
    "profiles": {name: f"profiles/{name}.txt" for name in PROFILES},
    "categories": categories,
}
(ROOT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

review = [
    "# Skill Implementation and Retention Review",
    "",
    "All 45 entries are original vendor-neutral syntheses. No provider-only, deprecated, placeholder, or organization-specific skill remains active.",
    "",
    "## Conditional items",
    "",
    "Twelve B-level skills remain for reference but are excluded from the default profile. Seven are broad platform guides and five are niche or tool-light workflows. `migrate-test-fixtures` is explicitly experimental and is the weakest retained item.",
    "",
    "| Level | Skill | Concrete implementation | Risk or limitation | Routing decision |",
    "|---|---|---|---|---|",
]
for item in sorted(catalog["skills"], key=lambda value: (value["reference_level"], value["category"], value["name"])):
    name = item["name"]
    route = ROUTING[name]
    risk = RISK_NOTES.get(name, "No material design defect found; still requires task-local tools and verification.")
    decision = (
        "Explicit trigger only; never in default profile."
        if item["reference_level"] == "B"
        else "Stable but exact-trigger-only to prevent false-positive security routing."
        if route["explicit_only"]
        else "Default core profile."
        if name in PROFILES["default"]
        else "Stable on-demand route."
    )
    if route["maturity"] == "experimental":
        decision = "Experimental and exact-trigger-only; remove if it proves unused."
    review.append(f"| {item['reference_level']} | `{name}` | {IMPLEMENTATION[name]} | {risk} | {decision} |")

(ROOT / "docs" / "SKILL_REVIEW.md").write_text("\n".join(review) + "\n", encoding="utf-8")

print(
    f"generated index=1 routes={len(categories)} routed_skills={len(ROUTING)} "
    f"profiles={len(PROFILES)} review_rows={len(IMPLEMENTATION)}"
)
