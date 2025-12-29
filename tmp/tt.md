下面给你一个**工程视角、但不踩厂商 NDA 细节**的说明，讲清 **TZMP v1 vs v2** 在**架构理念、能力边界、典型使用方式**上的区别。
（TZMP = **TrustZone Media Protection**，主要用于 DRM / Secure Video Path）

> 先说结论一句话版：
> **TZMP v1 是“把媒体保护搬进 TrustZone 的早期方案”，
> TZMP v2 是“把媒体保护做成可扩展、可并行、可现代 DRM 适配的体系”。**

---

## 一、整体定位差异（最重要）

| 维度    | TZMP v1      | TZMP v2               |
| ----- | ------------ | --------------------- |
| 时代背景  | 早期智能电视 / 机顶盒 | 现代 Android / 高分辨率 DRM |
| 设计目标  | “能跑起来的安全播放”  | “可扩展、高性能、DRM 友好”      |
| 架构成熟度 | 偏定制 / 偏封闭    | 模块化 / 标准化             |
| 当前主流  | ❌ 基本淘汰       | ✅ 主流                  |

---

## 二、架构层面的核心区别

### 1️⃣ TZMP v1：**单体式、强绑定**

**特点：**

* Secure World 中：

  * 解密
  * 解码控制
  * 显示控制
    **高度耦合**
* Normal World 参与度低
* 典型是 **“secure everything”**

📌 工程感受：

* 改动困难
* 很多逻辑写死在 secure side
* 不利于多 DRM / 多 codec 扩展

---

### 2️⃣ TZMP v2：**分层式、可扩展**

**核心变化：**

* 引入清晰的 **Trusted Layer / Secure Services 分层**
* Secure World：

  * 只保留**必须安全的部分**
* Normal World：

  * 负责 pipeline orchestration
* 明确区分：

  * control plane（安全）
  * data plane（高性能）

📌 工程感受：

* 更像“安全加速器”
* Secure World 不再成为性能瓶颈

---

## 三、Protected Mode / Secure Pipeline 的变化

### TZMP v1

* Protected mode：

  * 粗粒度
  * 通常是“整个 decoder + display 都 secure”
* Secure buffer 管理简单但死板

### TZMP v2

* Protected mode：

  * **细粒度**
  * 可只保护关键阶段
* 支持：

  * secure/non-secure buffer 混合
  * zero-copy secure path
* 更容易对接：

  * modern GPU
  * multi-plane display

---

## 四、对 DRM 的支持差异（非常关键）

| DRM 能力           | TZMP v1 | TZMP v2  |
| ---------------- | ------- | -------- |
| 多 DRM 并存         | 困难      | ✅ 设计目标之一 |
| Widevine L1      | 勉强 / 定制 | ✅ 原生友好   |
| PlayReady SL3000 | 有限制     | ✅        |
| 动态 session       | ❌       | ✅        |
| Key rotation     | 有限      | ✅        |

👉 **TZMP v2 是为现代 DRM 明确设计的**

---

## 五、性能与可扩展性

### TZMP v1 的问题

* Secure World 参与太多
* SMC / context switch 频繁
* 高分辨率（4K/8K）压力大

### TZMP v2 的改进

* Secure World **最小化参与**
* 支持：

  * 并行 session
  * 多 stream
* 更适合：

  * 4K / HDR / HEVC / AV1

---

## 六、工程/软件栈视角对比

### TZMP v1

```
App
 ↓
Normal World Media
 ↓
Secure World (monolithic TZMP)
 ↓
Decoder / Display
```

### TZMP v2

```
App
 ↓
Normal World Media Pipeline
 ↓         ↘
Secure Control   Secure Data Path
(Trusted Layer)  (Protected Mode)
```

---

## 七、为什么 v2 几乎全面取代 v1？

一句话总结原因：

> **v1 把“安全”当作目的，
> v2 把“安全”当作能力。**

现实驱动因素：

* Android TV / AOSP 演进
* DRM 复杂度提升
* 分辨率 & 帧率上升
* SoC 多核、多媒体并行

---

## 八、你可以在文档中这样写（工程级表述）

> TZMP v1 provides a monolithic TrustZone-based media protection solution with limited scalability.
> TZMP v2 introduces a layered and modular architecture, enabling fine-grained protected modes, improved DRM support, and better performance for modern high-resolution media pipelines.

---

## 九、一个非常重要的现实提醒（工程经验）

⚠️ **TZMP v1 / v2 的“具体实现细节”高度依赖 SoC vendor**

不同厂商可能：

* 名字相同
* 行为不同
* 文档描述不完全一致

👉 但**上面这些“理念级差异”是跨厂商成立的**。

---

如果你愿意，下一步我可以帮你：

* 对照 **Android Widevine L1 pipeline** 解释 TZMP v2
* 或画一份 **v1 vs v2 的 media pipeline 对比图（文字版）**
* 或帮你写一段 **design spec / review 用的官方口吻说明**

你这个问题已经是**平台架构级别**了，不是入门问题。



那是否Protected display也是在Rich execution environment中工作？
============================================================


简短回答先给你结论，然后再展开说明，方便你直接放进文档或和同事对齐理解。

---

## 结论（直接回答你的问题）

**是的，Protected display 仍然是在 Rich Execution Environment（REE）中参与工作的，
但它并不是“完全由 REE 信任或控制”的。**

更准确地说：

> **Protected display 的控制路径跨越 REE 与 TEE，
> REE 负责功能驱动，TEE 负责安全授权，硬件负责强制执行。**

---

## 为什么不能简单地说“它在 TEE 中工作”？

### 1️⃣ Display 硬件本身不“属于”某个 execution environment

* Display processor 是 **SoC 硬件**
* 它既不是 REE 的软件，也不是 TEE 的软件
* 它通过：

  * **REE 驱动**进行功能配置
  * **TEE / TrustZone**进行安全授权与访问控制

---

## Protected Display 的实际工作模式（工程视角）

### 🔹 运行环境分工

| 组件                  | 所在环境 | 作用                |
| ------------------- | ---- | ----------------- |
| Display driver      | REE  | 配置显示管线            |
| Media framework     | REE  | 管理图层 / 场景         |
| Secure monitor / TA | TEE  | 授权 protected mode |
| Display hardware    | 硬件   | 强制执行保护            |

---

### 🔹 Protected display 的关键点

* REE：

  * 发起 protected display 请求
  * 负责正常的显示控制逻辑
* TEE：

  * 验证请求是否合法
  * 控制是否允许进入 **protected display mode**
* 硬件：

  * 阻断非安全访问
  * 保护 secure buffer
  * 强制 secure display path

👉 **没有 TEE 授权，REE 无法真正启用 protected display**

---

## 和 Trusted Layer 的对比（你前面问过的）

| 特性          | Trusted Layer     | Protected Display |
| ----------- | ----------------- | ----------------- |
| 是否在 REE 中配置 | 是                 | 是                 |
| 是否需要 TEE 授权 | 是                 | 是                 |
| 主要保护对象      | UI 图层数据           | 媒体内容路径            |
| 安全强制点       | Display processor | 全媒体显示路径           |
| 是否独立        | 是                 | 是                 |

---

## 一句话工程化总结（推荐用在文档）

> Protected display is configured by software in the Rich Execution Environment, but its activation and enforcement are authorized by the Trusted Execution Environment and implemented by hardware.

或者更短一点：

> Protected display operates under REE control with TEE authorization and hardware enforcement.

---

## 常见误解澄清（很重要）

❌ **Protected display 在 TEE 中运行**
✅ **Protected display 由 REE 驱动配置，但不被 REE 信任**

❌ **REE 能完全控制 protected display**
✅ **TEE 决定 REE 是否有权限**

---

## 如果你要一句“规范级”的表述

> Although protected display is managed by software in the rich execution environment, it relies on TrustZone and the trusted execution environment to authorize and enforce secure display operation.

---

如果你愿意，我可以下一步帮你：

* 画一个 **REE / TEE / Display HW 的交互时序说明**
* 或把 **Trusted layer + Protected display + TZMPv2** 合并成一个统一安全显示架构说明
