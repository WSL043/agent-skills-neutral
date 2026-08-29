from __future__ import annotations

import json
from collections import Counter
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
    "change-evolution": "Reason about observable system change, staged migration, recoverability, and operational feedback.",
    "design-reasoning": "Turn product intent and evidence into deliberate interface, motion, and visual-system decisions.",
    "implementation-reasoning": "Implement, simplify, optimize, diagnose, review, and verify software behavior.",
    "learning-evaluation": "Evaluate agent behavior and evidence-gated improvements without confusing activity with capability lift.",
    "planning-coordination": "Plan and transfer bounded work while preserving decisions and evidence.",
    "problem-framing": "Clarify consequential uncertainty or prototype the smallest discriminating experiment.",
    "research-communication": "Research primary evidence, appraise scientific claims when needed, and structure decision-ready writing.",
    "security-reasoning": "Reason about threats, reachable vulnerabilities, controls, owners, and residual risk.",
    "system-design": "Design code boundaries, domain models, and public contracts before structural change.",
}


ROUTING = {
    "evaluate-agent": R(
        "workflow",
        "The task evaluates an agent, skill, workflow, or tool-using system with explicit tasks, graders, traces, or failure analysis.",
        "Do not use for ordinary product or model evaluation without an agent or workflow behavior contract.",
        ["evaluate agent", "agent evaluation", "evaluate skill", "skill evaluation", "agent evaluation loop", "benchmark agent", "compare two versions of this agent", "task success and tool use", "agent baseline and candidate eval", "compare agent prompts", "compare agent variants", "评估 agent", "评估技能", "智能体评估", "评测 agent", "评测技能"],
        ["model weights", "普通模型评估", "create agent skill", "create a new agent skill", "install agent skill", "install an agent skill", "find agent skill", "find an agent skill", "创建技能", "创建新的 agent skill", "安装技能", "查找技能"],
    ),
    "design-codebase": R(
        "workflow",
        "The task concerns module boundaries, dependency direction, modularization, or architecture migration.",
        "Do not use for a small localized implementation with no structural decision.",
        ["codebase architecture", "module boundary", "modularize", "dependency direction", "architecture proposal", "代码库架构", "模块边界", "架构重构", "模块化"],
    ),
    "model-domain": R(
        "workflow",
        "Business concepts, invariants, state transitions, or bounded contexts need explicit modeling.",
        "Do not use for directory organization without domain-rule ambiguity.",
        ["domain model", "bounded context", "ubiquitous language", "business invariant", "state transition", "领域模型", "限界上下文", "统一语言", "业务不变量"],
    ),
    "review-api-design": R(
        "workflow",
        "An API contract, OpenAPI description, public interface, versioning policy, or compatibility promise needs design review before or alongside implementation.",
        "Do not use for debugging one handler, reviewing an ordinary code diff, or merely documenting an already-fixed private function.",
        ["api design review", "review api contract", "openapi review", "public api interface", "api compatibility", "api versioning", "审查 api 设计", "评审 api 契约", "openapi 评审", "接口兼容性"],
        ["debug api handler", "review code diff", "ordinary code diff", "private helper", "调试接口实现", "普通代码评审"],
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
    "optimize-performance": R(
        "workflow",
        "The task explicitly optimizes measured software performance or addresses a latency, throughput, resource, or performance regression with a remeasurement loop.",
        "Do not use for an unexplained failure whose primary need is root-cause diagnosis, or for a generic code cleanup with no performance signal.",
        ["optimize performance", "performance optimization", "performance regression", "latency regression", "throughput regression", "slow query optimization", "slow endpoint", "measured bottleneck", "profile slow endpoint", "make this faster", "make this endpoint faster", "speed up", "reduce latency", "improve throughput", "测量后再优化", "性能优化", "性能回归", "延迟回归", "吞吐量优化", "提升性能", "加速"],
        [],
    ),
    "simplify-code": R(
        "workflow",
        "The task reduces incidental code complexity, duplication, nesting, or confusing structure while preserving the existing behavior contract.",
        "Do not use for a performance optimization, a public contract redesign, or a broad architecture migration without a simplification goal.",
        ["simplify code", "code simplification", "simplify implementation", "simplify this function", "reduce code complexity", "remove duplication", "简化代码", "简化实现", "减少代码复杂度", "减少重复", "降低复杂度"],
        ["performance optimization", "性能优化", "architecture migration", "架构迁移"],
        "stable",
        True,
    ),
    "review-code": R(
        "workflow",
        "The user requests review of a diff, patch, branch, or implementation quality and requirement fit.",
        "Use the security review skill instead when the primary question is vulnerability or hardening analysis.",
        ["code review", "review diff", "review patch", "pull request review", "self review", "代码评审", "审查 diff", "审查补丁", "评审代码"],
        ["security review", "vulnerability review", "安全审查", "漏洞审查"],
    ),
    "verify-completion": R(
        "workflow",
        "The task asks to prove completion, validate a claimed result, or perform final evidence checks.",
        "Do not use when no completion claim exists and the task still needs its primary work.",
        ["verify completion", "prove it works", "final validation", "completion evidence", "确认完成", "验证是否成功", "最终验证", "完成证据"],
    ),
    "handoff-task-context": R(
        "workflow",
        "The user explicitly asks to save, transfer, resume, or reconstruct bounded task context for another agent or later session.",
        "Do not use for a conversational status summary, generic JSON export, commit message, or automatic context compaction.",
        ["create handoff", "task handoff", "save task context", "resume from handoff", "continue in another agent", "交接任务", "保存任务上下文", "恢复任务交接", "给下个 agent"],
        ["status summary", "export json", "commit message", "自动压缩上下文", "总结当前状态"],
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
        "Do not use when the task is only file-format conversion or mechanical layout editing with no writing decision.",
        ["coauthor document", "write proposal", "design document", "draft memo", "long-form report", "共同写文档", "撰写提案", "设计文档", "起草备忘录"],
        [".docx", ".pdf", ".pptx", "docx", "pdf", "pptx", "编辑 word 格式"],
    ),
    "research-primary-sources": R(
        "workflow",
        "The task requires synthesizing authoritative primary sources, resolving material versioned claims, producing traceable citations, forming scientific hypotheses, or appraising what a study supports.",
        "Do not use for purely local inspection or a single replaceable tool-option lookup that current documentation can answer directly.",
        ["primary sources", "official documentation", "research with citations", "verify sources", "authoritative source", "latest papers", "research latest papers", "scientific hypothesis", "rival hypotheses", "study validity", "critique paper methods", "scientific evidence", "observational study", "causal claim evidence", "查官方资料", "一手资料", "带引用研究", "核实来源", "查最新论文", "科学假设", "研究设计有效性", "科学证据评估", "评估这篇论文"],
    ),
    "review-security-practices": R(
        "workflow",
        "The primary task is secure-coding review, vulnerability analysis, or framework-specific hardening.",
        "Do not use for a general quality review with no security focus.",
        ["security review", "secure coding", "vulnerability review", "security hardening", "安全审查", "安全代码审查", "漏洞检查", "安全加固", "安全最佳实践"],
        ["general code review", "普通代码评审"],
        explicit_only=True,
    ),
    "threat-model-system": R(
        "workflow",
        "The task explicitly needs assets, trust boundaries, attacker goals, abuse cases, attack paths, or a threat model.",
        "Do not use for a narrow code finding that is already known.",
        ["threat model", "trust boundary", "attack path", "abuse case", "attacker goal", "威胁建模", "信任边界", "攻击路径", "滥用场景"],
    ),
    "design-frontend": R(
        "workflow",
        "The task is interface hierarchy, responsive layout, component design, UI aesthetic judgment, anti-generic visual critique, redesign, polish, or implementation of a visual reference as frontend code.",
        "Do not use for a static poster, presentation, or backend-only task.",
        ["frontend design", "ui design", "ui aesthetics", "aesthetic review", "design taste", "generic ai design", "ai-looking ui", "anti-generic ui", "responsive interface", "design component", "polish ui", "redesign landing page", "image to code", "screenshot to code", "implement this mockup", "前端设计", "界面设计", "界面审美", "前端审美", "设计品味", "ui ai味", "界面ai味", "去ai味", "响应式页面", "组件设计", "优化 ui", "重新设计页面", "截图转前端", "按设计稿实现"],
        ["static poster", "backend only", "静态海报", "纯后端"],
    ),
    "design-motion": R(
        "workflow",
        "The task explicitly concerns UI animation, transition timing, easing, motion audit, or reduced-motion behavior.",
        "Do not use for video editing or animation unrelated to interface behavior.",
        ["ui animation", "motion design", "transition timing", "easing", "animation audit", "界面动画", "动效设计", "过渡动画", "缓动", "动效审计"],
        ["video editing", "视频剪辑"],
    ),
    "design-visual-theme": R(
        "workflow",
        "The task needs reusable color, typography, spacing, style tokens, a brand kit, or a coherent visual system across artifacts.",
        "Do not use when only one isolated color value or font choice is requested.",
        ["visual theme", "design tokens", "color typography system", "theme system", "brand kit", "brand system", "视觉主题", "设计 token", "配色字体", "主题系统", "设计规范", "品牌套件", "品牌视觉系统"],
    ),
    "instrument-observability": R(
        "workflow",
        "A system needs structured logs, metrics, traces, correlation, SLO signals, or production telemetry that answers operational questions.",
        "Do not use as the primary workflow for diagnosing one current bug or adding a temporary print statement.",
        ["observability", "structured logs", "metrics and traces", "correlation id", "distributed tracing", "production telemetry", "slo instrumentation", "可观测性", "结构化日志", "指标和链路", "关联 id", "生产遥测"],
        ["debug current bug", "temporary print", "一次性打印", "排查当前故障"],
    ),
    "migrate-system-safely": R(
        "workflow",
        "A live schema, API, dependency, data representation, or behavior must migrate through compatibility, backfill, cutover, and cleanup stages.",
        "Do not use for resolving Git conflicts, moving one local file, or changing isolated test fixtures with no live consumers.",
        ["safe migration", "expand contract", "database backfill", "dual write", "compatibility migration", "deprecation plan", "cutover plan", "安全迁移", "扩展收缩迁移", "数据回填", "双写", "兼容迁移", "弃用计划", "切换方案"],
        ["git conflict", "move one file", "test fixtures only", "解决 git 冲突", "移动文件"],
    ),
}


IMPLEMENTATION = {
    "evaluate-agent": "Define the claim and graders before running like-for-like baseline/candidate tasks, persist traces, and analyze failures without hiding uncertainty.",
    "design-codebase": "Map dependencies and change pressure, compare structural options, then stage an incremental migration with rollback points.",
    "model-domain": "Build a glossary, entities/values, invariants, events, state transitions, ownership, and bounded contexts from real scenarios.",
    "develop-with-tdd": "Run a strict red-green-refactor cycle around observable behavior, with characterization tests for legacy code.",
    "diagnose-software": "Reproduce and minimize, instrument the first divergence, and test one falsifiable hypothesis; fix and add regression evidence only when changes are authorized.",
    "optimize-performance": "Measure a comparable baseline, isolate the bottleneck, make one targeted change, remeasure correctness and impact, and install a durable guard.",
    "simplify-code": "Define the observable contract, simplify only proven incidental complexity, and verify behavior with focused and broader checks.",
    "review-code": "Review requirement fit and implementation quality separately, validate reachable findings, and support self/request/receive review modes.",
    "verify-completion": "Map each claim to a fresh authoritative check, verify side effects and final state, and narrow claims when checks are blocked.",
    "handoff-task-context": "Capture objective, verified current state, evidence, decisions, frontier, blockers, next actions, and bounded file references; reconcile every claim when resuming.",
    "plan-implementation": "Inspect the repository and produce dependency-ordered tracer slices with file/symbol steps, dependency edges, migration, rollback, and acceptance evidence.",
    "clarify-requirements": "Separate facts, assumptions, constraints, and open decisions; ask only high-information questions and produce testable acceptance criteria.",
    "prototype-solution": "Time-box the smallest visual or executable artifact that can accept/reject one explicit uncertainty.",
    "coauthor-documents": "Agree audience and outline first, draft claims with evidence section by section, then run a fresh-reader pass.",
    "research-primary-sources": "Discover broadly, read authoritative primary sources, track versions and contradictions, cite each material claim, and load the scientific-evidence mode only for hypothesis or study-appraisal tasks.",
    "review-security-practices": "Trace real security data flows, compare current official guidance, validate reachable findings, and prioritize hardening with verification.",
    "threat-model-system": "Map assets, flows, trust boundaries, attacker goals, attack paths, controls, owners, and residual risk.",
    "review-api-design": "Inventory consumers and compatibility promises, review resources/operations/schemas/errors/evolution, then report evidence, impact, recommendation, and severity.",
    "design-frontend": "Infer or confirm a brief, establish one coherent design system, implement hierarchy and complete states responsively, and audit accessibility, performance, and reference drift.",
    "design-motion": "Use motion only for feedback, continuity, state, or hierarchy; specify timing/easing/interruption, then test reduced motion and performance.",
    "design-visual-theme": "Translate product and brand intent into semantic color/type/spacing tokens, test representative content, and apply them through shared styles.",
    "instrument-observability": "Start from operational questions, add bounded-cardinality logs/metrics/traces and correlation, then verify emitted signals, redaction, dashboards, and actionable alerts.",
    "migrate-system-safely": "Inventory consumers and source of truth, run expand/backfill/switch/contract stages with reconciliation and rollback, and remove compatibility only after measured zero use.",
}


RISK_NOTES = {
    "diagnose-software": "Intermittent failures may require probabilistic or repeated evidence rather than deterministic reproduction.",
    "evaluate-agent": "Intentional treatment-variable differences must be separated from uncontrolled confounds.",
    "handoff-task-context": "A handoff is a claim, not authority; resume mode must reconcile it with live repository and runtime state.",
    "review-api-design": "API conventions are contextual and can change; repository contracts and current primary standards override generic preferences.",
    "instrument-observability": "Useful only with the real telemetry backend and representative traffic; avoid secrets and unbounded labels.",
    "migrate-system-safely": "Cleanup requires measured consumer and runtime evidence, not elapsed time or a successful deploy alone.",
    "research-primary-sources": "Scientific appraisal frameworks are design- and domain-specific; reporting completeness, statistical significance, and evidence hierarchy are not standalone validity scores.",
}




catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
catalog_by_name = {item["name"]: item for item in catalog["skills"]}
if set(catalog_by_name) != set(ROUTING) or set(catalog_by_name) != set(IMPLEMENTATION):
    raise SystemExit("Routing and implementation maps must cover every catalog skill exactly once")

routes_dir = ROOT / "routes"
routes_dir.mkdir(exist_ok=True)

expected_route_files = {f"{category}.json" for category in CATEGORY_SUMMARIES}
for old_path in routes_dir.glob("*.json"):
    if old_path.name not in expected_route_files:
        old_path.unlink()

profiles_dir = ROOT / "profiles"
if profiles_dir.exists():
    for old_path in profiles_dir.iterdir():
        if not old_path.is_file():
            raise SystemExit(f"Unexpected non-file in retired profiles directory: {old_path}")
        old_path.unlink()
    profiles_dir.rmdir()

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

index = {
    "schema_version": 1,
    "library": "agent-skills-neutral",
    "routing_authority": "model-native-semantic",
    "thinking_core": {
        "source": "runtime/AGENTS.md",
        "serving": "AGENTS.md",
        "loading": "always-on",
    },
    "runtime_catalog": "runtime-catalog.json",
    "advisory_router": "python scripts/select_skills.py <task> --json",
    "manual_protocol": [
        "Keep runtime/AGENTS.md active as the default thinking core for every task.",
        "Use host-discovered workflow metadata or runtime-catalog.json for model-native semantic selection.",
        "Choose by the current cognitive outcome and workflow description, not keyword, domain, file-format, product, or tool overlap.",
        "Load only the selected SKILL.md body and its task-relevant resources.",
        "Use category route files only as hierarchical navigation or diagnostic metadata.",
        "Use select_skills.py only as advisory fallback/regression evidence.",
        "No workflow is a valid result when the thinking core is sufficient or the need is only replaceable tool knowledge.",
    ],
    "categories": categories,
}
(ROOT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

runtime_catalog = {
    "schema_version": 1,
    "library": "agent-skills-neutral",
    "routing_authority": "model-native-semantic",
    "skills": [
        {
            "name": item["name"],
            "description": item["description"],
            "location": f"{item['path']}/SKILL.md",
        }
        for item in sorted(catalog["skills"], key=lambda value: value["name"])
    ],
}
(ROOT / "runtime-catalog.json").write_text(
    json.dumps(runtime_catalog, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

level_counts = Counter(item["reference_level"] for item in catalog["skills"])
catalog_lines = [
    "# Agent Skills Catalog",
    "",
    f"{len(catalog['skills'])} canonical skills across {len(categories)} categories. "
    + "Levels: "
    + ", ".join(f"{level}={level_counts[level]}" for level in ("S", "A") if level_counts[level])
    + ".",
    "",
    "| Level | Category | Skill | Description |",
    "|---|---|---|---|",
]
for item in sorted(catalog["skills"], key=lambda value: (value["category"], value["reference_level"], value["name"])):
    catalog_lines.append(
        f"| {item['reference_level']} | {item['category']} | "
        f"[`{item['name']}`]({item['path']}/SKILL.md) | {item['description']} |"
    )
(ROOT / "CATALOG.md").write_text("\n".join(catalog_lines) + "\n", encoding="utf-8")

review = [
    "# Skill Implementation and Retention Review",
    "",
    f"All {len(catalog['skills'])} entries are vendor-neutral thinking workflows. No provider-only, tool-manual, file-format, domain-adapter, deprecated, placeholder, organization-specific, or B-level skill remains active.",
    "",
    "## Active skills",
    "",
    "The always-on thinking core is separate from this on-demand catalog. S marks high-transfer workflows and A marks scenario workflows; neither level is a persistent default profile.",
    "",
    "| Level | Skill | Concrete implementation | Risk or limitation | Routing decision |",
    "|---|---|---|---|---|",
]
for item in sorted(catalog["skills"], key=lambda value: (value["reference_level"], value["category"], value["name"])):
    name = item["name"]
    route = ROUTING[name]
    risk = RISK_NOTES.get(name, "No material design defect found; still requires task-local current evidence and verification.")
    decision = (
        "Stable but exact-trigger-only to prevent false-positive security routing."
        if route["explicit_only"] and name == "review-security-practices"
        else "Stable but exact-trigger-only to prevent false-positive routing."
        if route["explicit_only"]
        else "Stable on-demand thinking workflow."
    )
    review.append(f"| {item['reference_level']} | `{name}` | {IMPLEMENTATION[name]} | {risk} | {decision} |")

(ROOT / "docs" / "SKILL_REVIEW.md").write_text("\n".join(review) + "\n", encoding="utf-8")

print(
    f"generated index=1 routes={len(categories)} routed_skills={len(ROUTING)} "
    f"thinking_core=1 profiles=0 review_rows={len(IMPLEMENTATION)}"
)
