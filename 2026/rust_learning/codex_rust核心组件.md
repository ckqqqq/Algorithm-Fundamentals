# Codex (codex-rs) Rust 核心组件地图

> 基于 `/Users/qiker/Desktop/work/code/deepseek/codex/codex-rs` 实际代码整理
> workspace 共 **95 个 crate**，`core` 单 crate 含 **170+ 源文件**（模块 + 同名 `*_tests.rs` 测试）

---

## 1. Workspace 四层结构

| 层 | crates | 职责 |
|---|---|---|
| 前端层 | `cli`, `tui`, `exec`, `app-server`, `app-server-daemon` | 用户交互界面（TUI 用 ratatui） |
| 协议层 | `protocol`, `app-server-protocol`, `exec-server-protocol` | Submission/Event 双向消息定义，全系统的词汇表 |
| 核心层 | `core`（codex-core） | agent loop、会话、上下文、工具编排 |
| 能力层 | 其余 80+ 小 crate | 被 core 依赖的可插拔能力（见下） |

核心设计原则：**core 只编排不实现，能力全部下沉到独立 crate，编译期强制边界。**

---

## 2. 能力层关键 crate（core 的依赖）

### 沙箱与安全
- `sandboxing` —— 沙箱抽象层（trait 契约）
- `linux-sandbox` / `bwrap` —— Linux namespace/seccomp、bubblewrap 实现
- `windows-sandbox-rs` —— Windows 沙箱
- `process-hardening` —— 进程加固
- `execpolicy` —— 命令策略引擎（允许/拒绝/询问）
- `shell-escalation` —— 提权执行
- `network-proxy` —— 网络访问控制

### 工具与文件
- `tools` —— 工具注册与分发
- `apply-patch` —— patch DSL 编辑文件（不用全量 write）
- `file-system`, `file-search`, `file-watcher` —— 文件操作/搜索/监听
- `shell-command` —— shell 执行
- `git-utils` —— git 集成

### MCP 生态
- `rmcp-client`（依赖官方 `rmcp` SDK）—— MCP 客户端
- `mcp-server`, `codex-mcp` —— 对外暴露 MCP 服务
- `plugin`, `core-plugins`, `skills`, `core-skills` —— 插件与技能系统

### 会话与持久化
- `rollout` / `rollout-trace` —— 轨迹 append-only 落盘（回放/训练数据之源）
- `thread-store`, `state`, `message-history` —— 会话状态存储
- `agent-graph-store` —— 多代理关系图

### 模型接入
- `model-provider`, `model-provider-info`, `models-manager` —— 提供商抽象
- `codex-api`, `codex-client`, `backend-client` —— API 客户端
- `responses-api-proxy` —— Responses API 代理
- `ollama`, `lmstudio` —— 本地模型后端

### 基础设施
- `config`, `features` —— 配置与 feature flag
- `otel`, `analytics`, `feedback` —— 可观测性
- `login`, `keyring-store`, `secrets` —— 认证与密钥
- `hooks` —— 钩子系统
- `http-client`, `async-utils`, `terminal-detection` —— 通用设施

---

## 3. core 内部模块地图（按职责分组）

路径均为 `codex-rs/core/src/`。

### 3.1 会话与主循环（主干）
- `lib.rs` —— crate 入口，公共 API 导出
- `codex_thread.rs` —— 单个会话线程：agent loop 本体
- `thread_manager.rs` —— 多会话管理
- `spawn.rs` —— 会话/子代理创建
- `codex_delegate.rs` —— 子代理委派
- `agent_communication.rs` —— 代理间通信

### 3.2 模型客户端
- `client.rs` / `client_common.rs` —— Responses API 调用，SSE 流式
- `responses_retry.rs` / `responses_metadata.rs` —— 重试与元数据
- `stream_events_utils.rs` —— 流事件解析
- `event_mapping.rs` —— API 事件 → 内部 Event 映射

### 3.3 上下文与压缩
- `compact.rs` —— 本地压缩主逻辑
- `compact_remote.rs` / `compact_remote_v2*.rs` —— 远程压缩
- `compact_token_budget.rs` —— token 预算
- `compact_model_fallback.rs` —— 压缩失败降级
- `agents_md.rs` / `agents_md_manager.rs` —— AGENTS.md 项目指令注入
- `session_prefix.rs` —— 会话前缀（KV cache 相关纪律所在）
- `prompts/`（独立 crate）—— 提示词模板

### 3.4 工具执行与安全
- `exec.rs` / `exec_env.rs` —— 命令执行
- `exec_policy.rs` —— 策略判定（命令白名单/审批）
- `safety.rs` —— 安全检查
- `shell.rs` / `shell_snapshot.rs` —— shell 环境
- `user_shell_command.rs` —— 用户主动命令
- `command_canonicalization.rs` —— 命令归一化（策略匹配前置）
- `apply_patch.rs` —— patch 应用
- `function_tool.rs` —— 函数工具桥接
- `web_search.rs` —— 网络搜索工具
- `sandbox_tags.rs`, `windows_sandbox*.rs` —— 沙箱标记与 Windows 侧

### 3.5 MCP
- `mcp.rs` —— MCP 连接管理
- `mcp_tool_call.rs` / `mcp_tool_exposure.rs` —— 工具调用与暴露
- `mcp_skill_dependencies.rs` —— 技能依赖

### 3.6 记忆与轨迹
- `rollout.rs` / `rollout_budget.rs` —— 轨迹落盘与预算
- `thread_rollout_truncation.rs` —— 轨迹截断
- `message-history`（crate）—— 历史消息
- `turn_diff_tracker.rs` —— 每轮 git diff 追踪（证据链）

### 3.7 可观测与其他
- `otel_init.rs`, `turn_timing.rs`, `turn_metadata.rs` —— 遥测与计时
- `memory_usage.rs` —— 内存监控
- `realtime_conversation.rs` / `realtime_context.rs` —— 实时语音会话
- `elicitation.rs` —— 向用户追问澄清
- `hook_runtime.rs` —— 钩子执行
- `image_preparation.rs` —— 多模态输入
- `environment_selection.rs`, `network_policy_decision.rs` —— 环境/网络决策

---

## 4. 蒸馏：自研 harness 的 8 个核心组件对照

| 核心组件 | codex 对应 | 职责一句话 |
|---|---|---|
| Protocol | `protocol` crate | Submission/Event/ToolCall 类型，只放类型 |
| TrajectoryStore | `rollout.rs` + `thread_rollout_truncation.rs` | append-only 轨迹落盘，可回放 |
| ModelClient | `client.rs` + `stream_events_utils.rs` | SSE 流式调用，trait 抽象可 mock |
| Sandbox | `sandboxing` + `linux-sandbox` + `exec.rs` | 命令执行的安全边界 |
| ContextManager | `compact*.rs` + `session_prefix.rs` + `agents_md.rs` | 组装/预算/压缩，强制前缀稳定 |
| ToolRuntime | `tools` + `mcp.rs` + `function_tool.rs` | 工具注册、schema、分发、取消 |
| PolicyEngine | `exec_policy.rs` + `safety.rs` + `command_canonicalization.rs` | 允许/拒绝/询问的横切决策 |
| Runtime | `codex_thread.rs` + `thread_manager.rs` + `spawn.rs` | 事件循环编排，越薄越好 |

---

## 5. 推荐阅读顺序

1. **`protocol/src/`** —— Submission/Event 两个枚举，全系统词汇表（回报最快）
2. **主干**：`core/src/lib.rs` → `codex_thread.rs` → `client.rs`（一个请求走完全程）
3. **一条命令的旅程**：`exec_policy.rs` → `safety.rs` → `sandboxing/` → `linux-sandbox/`
4. **记忆**：`rollout.rs` → `compact.rs` → `thread_rollout_truncation.rs`
5. **扩散**：`mcp.rs`、`apply-patch/`、`tui/`（按兴趣）

技巧：每个模块配 `*_tests.rs`，**先读测试再看实现**；外围 crate（login/ollama/utils-*）知道存在即可，不必通读。
