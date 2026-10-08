# Architecture Governance

[English](README.md) · [한국어](README.ko.md) · **简体中文** · [日本語](README.ja.md)

**在修改代码时，始终遵循项目既有的架构。**

Architecture Governance 是一款 Claude Code 插件，将软件变更的规划、实现、审查和验证整合到一个 Skill 中。它帮助 AI 代理确定某项行为由谁负责、变更应该落在哪个位置，以及在宣布工作完成之前需要哪些验证依据。

它不会向项目强加新的架构。设计上的最终依据始终是目标项目自身的规范文档、契约和测试。

## 为什么需要它？

代码即使能够编译、通过部分测试，也可能违背系统设计。例如：引入第二个事实来源、绕过公开契约、自行规定错误处理策略，或者将某条命令执行成功误认为正确性的证明。

Architecture Governance 将这些问题纳入开发流程：

- **找到责任归属：** 在引入新抽象之前，先确认已有的职责及其契约。
- **理解行为语义：** 根据需要检查状态、身份标识、执行顺序、故障、恢复和依赖边界。
- **按风险规划：** 简单修改保持轻量；涉及公开契约或全系统规则的变更则严格审查。
- **检验实际变更：** 不只检查正常流程，还要审查实际 Git diff 和失败路径。
- **明确验证依据：** 区分已经定义、已经实现、实际执行过以及真正得到验证的内容。

## 安装

在 Claude Code 中执行：

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

安装后，请启动新的 Claude Code 会话。

## 快速开始

向 Skill 描述要完成的任务：

```text
/architecture-governance:architecture-governance plan 设计保存失败后的安全恢复流程
```

如果要按照既有架构实现变更：

```text
/architecture-governance:architecture-governance implement 修复编辑器重新配置后的过期响应处理
```

如果要审查现有设计或代码变更：

```text
/architecture-governance:architecture-governance audit 检查架构文档及实现中的违规之处
/architecture-governance:architecture-governance review 审查当前的 Git diff
```

对于相关任务，Claude 也可能自动选择此 Skill。需要指定工作流程时，可以显式调用。

## 工作流程

| 模式 | 功能 |
| --- | --- |
| `plan` | 确定职责归属、契约、备选方案、影响范围和验证计划。 |
| `implement` | 先分析既有职责，再实施变更、审查 diff 并运行相关检查。 |
| `audit` | 查找架构违规，包括规范设计文档自身的矛盾。 |
| `review` | 将计划中的变更或实际改动与架构要求进行比较。 |
| `verify` | 执行适用的检查，并说明验证依据及尚未覆盖的部分。 |
| `project` | 基于既有权威数据源，辅助生成项目状态和待办工作的派生视图。 |
| `adopt` | 协助将工作流程接入现有仓库及其验证机制。 |

所有模式都属于**同一个 Skill**。如果没有指定模式，默认使用 `plan`；但当任务意图明确指向其他流程时，会选择相应模式。

## 不提供哪些保证？

Architecture Governance 用于指导 AI 代理的工程工作，不能替代项目自身的架构检查器、测试套件、安全强制机制或 CI。Skill 不保证在每次变更时都会被调用，仅靠文本审查也无法证明所有语义不变量都得到满足。

同样，找到测试文件或记录一条成功执行的命令，并不等于证明其完整契约正确。尚未检查或无法得出结论的部分必须明确保留，不能直接标记为完成。

需要强制执行的规则，应交由**目标项目自身的 CI 和检查机制**保证。

## 文档

- [可选工具与高级用法（英文）](docs/TOOLS.md)
- [工程原则（英文）](doctrine/ENGINEERING_CONSTITUTION.md)
- [贡献与开发指南（英文）](CONTRIBUTING.md)

## 许可证

[Apache-2.0](LICENSE)
