# 我在一个display Process UNIT里看到axi bus上有armmusid[7:0]/armmusecsid这样的信号，但是没有ssid的信号，但是寄存器配置里有s1sid/s2sid的设置，且内部有TBU模块，有DTI接口和smmu通讯

对，这个信息一补充出来，**架构就完全不一样了**。你这个 Display Processing Unit 里面的 TBU 很可能不是单纯“把 AXI transaction 原样送到外部 SMMU”的 requester，而是一个**本地集成的 TBU（Translation Buffer Unit）**，通过 DTI 和外部 SMMU 的 TCU 通信。

而你看到的：

* AXI 上有 `ARMMUSID[7:0]`
* AXI 上有 `ARMMUSECSID`
* **没有** `ARMMUSSID`
* 寄存器却有 `S1SID` / `S2SID`
* 内部有 TBU
* TBU 有 DTI interface 连接 SMMU

这其实非常有代表性。

## 先说结论

这里很可能存在**两套不同层次的 SID**，不要把 AXI 上的 `ARMMUSID` 和寄存器里的 `S1SID/S2SID` 简单当成同一个东西。

大致可以理解成：

```text
                     Display Processing Unit
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  Layer processing                                          │
│       │                                                    │
│       │ AXI transaction                                    │
│       │ ARMMUSID / ARMMUSECSID                             │
│       ▼                                                    │
│      TBU                                                   │
│       │                                                    │
│       │ DTI                                                │
│       │                                                     │
└───────┼────────────────────────────────────────────────────┘
        │
        ▼
       SMMU
       TCU
```

而 `S1SID/S2SID` 更可能是**TBU 用来指定 S1/S2 translation context 的配置参数**。

---

# 1. 首先纠正一个容易产生的误解

前面我们讨论 SMMU 时说：

```text
SID → STE → Stage 2
          ↓
         CD
          ↑
        SSID
```

这是从**标准 SMMU transaction identity**角度看的。

但是现在你的 DPU 自己内部已经有一个：

> **TBU**

那么 transaction 在进入 SMMU TCU 之前，已经经过了一个**TBU translation front-end**。

这时候：

```text
DPU AXI
   ↓
 TBU
   ↓ DTI
SMMU TCU
```

和：

```text
DPU AXI
   ↓
SMMU
```

是完全不同的集成方式。

---

# 2. DTI 是这里最关键的线索

Arm 的 MMU-600 文档明确说：

> DTI interface manages communication between the TBUs and the TCU.

并且：

> The TCU includes a slave DTI interface and each TBU includes a master DTI interface. ([Arm开发者][1])

所以你的结构：

```text
DPU
 └── TBU
      │
      │ DTI
      ▼
     SMMU TCU
```

是一个标准的 **distributed SMMU architecture**。

也就是说：

**TBU 在 DPU 本地，真正的 translation control / page table walk / configuration 等功能在 SMMU TCU。**

可以粗略理解为：

```text
                 SMMU
        ┌─────────────────────┐
        │                     │
        │        TCU          │
        │                     │
        │  translation       │
        │  control / walk    │
        │                     │
        └─────────▲───────────┘
                  │
                  │ DTI
                  │
        ┌─────────┴───────────┐
        │        TBU          │
        │                     │
DPU AXI ──► translation cache │
        │                     │
        └─────────────────────┘
```

TBU 本身主要负责 translation cache / lookup 等，miss 时通过 DTI 向 TCU 请求 translation。

---

# 3. 那为什么 AXI 上还有 `ARMMUSID`？

这恰恰是关键。

AXI5 本身定义了这些 MMU-related signals：

```text
ARMMUSECSID
ARMMUSID
ARMMUSSIDV
ARMMUSSID
ARMMUATST
ARMMUFLOW
ARMMUVALID
```

其中：

* `ARMMUSID` = StreamID
* `ARMMUSECSID` = Secure Stream Identifier
* `ARMMUSSID` = SubstreamID

而且 **SubstreamID 是可选的**。AXI specification 明确规定，如果 `SSID_WIDTH = 0`，那么 `AxMMUSSID` 和 `AxMMUSSIDV` 就不存在。([Arm文档服务][2])

所以：

```text
ARMMUSID[7:0]
ARMMUSECSID
```

存在，而：

```text
ARMMUSSID
ARMMUSSIDV
```

不存在，

完全符合 AXI 协议。

这说明：

> **你的 DPU AXI interface 本身没有使用 AXI transaction-level SubstreamID。**

这一点很重要。

---

# 4. 那 `S1SID` / `S2SID` 是什么？

这里我认为应该把它们和 **AXI `ARMMUSID`** 分开看。

你看到：

```text
S1SID
S2SID
```

很可能表示：

```text
Stage 1 StreamID
Stage 2 StreamID
```

也就是说，它们不是：

```text
SSID
```

而是：

```text
SID associated with Stage 1
SID associated with Stage 2
```

这在**内部已经集成 TBU 的 IP**里非常合理。

---

# 5. 为什么一个 TBU 会需要 S1SID 和 S2SID？

考虑一个典型的两阶段 translation：

```text
VA
 ↓
Stage 1
 ↓
IPA
 ↓
Stage 2
 ↓
PA
```

Stage 1 和 Stage 2 实际上属于两个不同的 translation context。

例如：

```text
Stage 1:
    Process / application address space

Stage 2:
    VM / guest address space
```

因此 DPU 内部的 TBU 需要知道：

```text
Stage 1 translation context
Stage 2 translation context
```

而这些 context 的标识可能分别通过：

```text
S1SID
S2SID
```

来指定。

于是你可能看到：

```text
DPU register

S1SID = 0x12
S2SID = 0x35
```

内部：

```text
                TBU
                 │
        ┌────────┴────────┐
        │                 │
     S1SID              S2SID
        │                 │
        ▼                 ▼
    Stage 1 context    Stage 2 context
```

---

# 6. 这里特别容易产生一个误解

千万不要看到：

```text
S1SID
S2SID
```

就认为：

```text
S1SID = SubstreamID
S2SID = SubstreamID
```

**不是这么理解的。**

`SID` 和 `SSID` 是两个不同概念。

标准 AXI 定义的是：

```text
SID
SSID
```

而你 IP 的 register：

```text
S1SID
S2SID
```

从命名上更像：

```text
Stage-1 SID
Stage-2 SID
```

也就是**两个 translation stage 对应的 Stream Identifier**。

---

# 7. 为什么不需要 AXI SSID？

这其实很好解释。

你的 DPU 可能根本没有：

```text
multiple application address spaces
```

也就是说，它不需要：

```text
SID = 0x20
SSID = 0
SID = 0x20
SSID = 1
SID = 0x20
SSID = 2
```

这种机制。

而是：

```text
DPU
 │
 └── 固定的 translation context
```

所以它只需要：

```text
AXI:
    ARMMUSID
    ARMMUSECSID
```

而不需要：

```text
ARMMUSSID
ARMMUSSIDV
```

这并不矛盾。

---

# 8. 那 `S1SID/S2SID` 和 AXI `ARMMUSID` 之间到底是什么关系？

这里我建议你暂时不要直接假定：

```text
ARMMUSID = S1SID
```

或者：

```text
ARMMUSID = S2SID
```

因为**这取决于这个 DPU 的 TBU 集成方式**。

有几种可能。

---

## 情况 A：AXI SID 是 requester identity，S1/S2 SID 是内部 translation identity

可能是：

```text
                 DPU
                  │
       AXI SID = 0x20
                  │
                  ▼
                 TBU
             ┌────┴────┐
             │         │
          S1SID      S2SID
             │         │
             ▼         ▼
          Stage 1    Stage 2
```

这里：

```text
ARMMUSID
```

描述的是：

> **这个 AXI transaction 是谁发出来的。**

而：

```text
S1SID/S2SID
```

描述的是：

> **TBU 做两级 translation 时使用什么 SID/context。**

这种情况下三者完全可以不同。

---

# 9. 情况 B：S1SID/S2SID 是由同一个 transaction identity 派生出来的

也可能：

```text
ARMMUSID
    │
    ▼
   TBU
    │
    ├── S1SID
    │
    └── S2SID
```

例如：

```text
S1SID = ARMMUSID
S2SID = some configured SID
```

具体怎么映射，需要看这个 TBU 的寄存器定义。

---

# 10. 情况 C：DPU 自己就是一个 SMMU translation requester

这时候可能更像：

```text
              DPU
               │
          AXI transaction
               │
          ARMMUSID
               │
               ▼
              TBU
               │
               │ DTI
               ▼
              TCU
```

TBU 将 transaction 的 translation request 通过 DTI 发给 TCU。

此时 DTI transaction 里面会有 translation identity/context 信息。

**注意：DTI 不是简单地把 AXI 的 `ARMMUSID` 几根线直接“接到”SMMU。**

它是另一套接口协议。

MMU-600 的 TBU 和 TCU 正是通过 DTI 进行通信。([Arm开发者][1])

---

# 11. 所以你现在这个 DPU 的数据流，很可能是这样

我认为你现在应该先建立这个模型：

```text
                         Display Processing Unit
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│   Layer processing                                            │
│        │                                                      │
│        │ AXI transaction                                     │
│        │                                                      │
│        │ ARMMUSID[7:0]                                       │
│        │ ARMMUSECSID                                         │
│        ▼                                                      │
│      ┌─────────┐                                              │
│      │   TBU   │                                              │
│      │         │                                              │
│      │ TLB     │                                              │
│      │ lookup  │                                              │
│      └────┬────┘                                              │
│           │                                                   │
│           │ DTI                                               │
└───────────┼───────────────────────────────────────────────────┘
            │
            ▼
      ┌─────────────┐
      │ SMMU TCU    │
      │             │
      │ translation │
      │ table walk  │
      └─────────────┘
```

而寄存器：

```text
S1SID
S2SID
```

属于：

```text
                TBU configuration
                       │
              ┌────────┴────────┐
              │                 │
            S1SID             S2SID
              │                 │
              ▼                 ▼
          Stage 1            Stage 2
         translation         translation
```

---

# 12. 这和你之前问的“Stage-1 / Stage-2 SID 怎么送给 SMMU”正好联系起来

现在可以回答得更准确：

**不一定是通过 AXI 上的两个 SID signal 送给 SMMU。**

如果 DPU 内置 TBU，那么很可能是：

```text
AXI side
   │
   │ ARMMUSID
   ▼
 TBU
   │
   │ DTI transaction
   │
   │ carries the translation context information
   ▼
SMMU TCU
```

而 `S1SID/S2SID` 是 TBU 内部配置，用于建立：

```text
Stage 1 translation identity
Stage 2 translation identity
```

所以：

> **AXI `ARMMUSID` 是 AXI transaction-level StreamID；`S1SID/S2SID` 则很可能是这个 DPU 内置 TBU 对两级 translation 所使用的 SID/context 配置。二者属于不同层次。**

---

# 13. 还有一个非常重要的线索：你的 AXI 是“translated”还是“untranslated”？

这个一定要确认。

AXI 的 `AxMMUSID` 这些信号属于 **untranslated transaction signaling**。AXI 规范里明确把 `AxMMUSID` 定义为：

> Stream Identifier for untranslated transactions. ([studylib.net][3])

同时还有：

```text
AxMMUVALID
```

用于说明 transaction 的地址是否需要 MMU translation。([Arm文档服务][2])

所以你应该在这个 DPU 的 AXI interface 附近找一下有没有：

```text
ARMMUVALID
AWMMUVALID
ARMMUATST
AWMMUATST
ARMMUFLOW
AWMMUFLOW
```

如果有，特别值得看它们怎么连接。

---

## 14. 我建议你下一步重点查这几个东西

你现在手头这个 IP，**最有价值的不是继续猜 `S1SID/S2SID`，而是把 TBU 的 register description 和 DTI interface 找出来。**

尤其找：

```text
S1SID
S2SID
```

对应 register 的完整 description，看它有没有类似：

* Stage 1 StreamID
* Stage 2 StreamID
* StreamID used for translation
* SID used for TBU
* SID used for SMMU
* security context
* translation context

然后再找 TBU 的 DTI interface signal。

如果你能把 **这个 DPU 的 `S1SID/S2SID` 寄存器说明，以及 TBU/DTI 那一页**贴出来，我可以直接帮你把这几个 ID 的关系画成：

```text
DPU AXI
  │
  │ ARMMUSID / ARMMUSECSID
  ▼
 TBU
  │
  ├── S1SID ───────► SMMU Stage-1 context
  │
  └── S2SID ───────► SMMU Stage-2 context
  │
  │ DTI
  ▼
SMMU TCU
```

并且可以进一步判断 **`ARMMUSID` 到底是 S1SID、S2SID，还是与两者都不同**。这一点仅凭目前的信息还不能百分之百确定。

另外，标准 AXI 确实支持 `ARMMUSSID/ARMMUSSIDV`，但它们是**可选信号**；你这个 DPU 没有它们并不意味着 TBU 没有“substream/context”能力。([Arm文档服务][2])

[1]: https://developer.arm.com/documentation/100310/0202/Functional-description/Interfaces/TCU-interfaces?lang=en&utm_source=chatgpt.com "Arm CoreLink MMU-600 System Memory Management Unit Technical Reference Manual r2p2"
[2]: https://documentation-service.arm.com/static/63ff0ebd56ea36189d4e7ee7?token=&utm_source=chatgpt.com "AMBA® AXI Protocol"
[3]: https://studylib.net/doc/27771202/ihi0022k-amba-axi-protocol-spec?utm_source=chatgpt.com "AMBA AXI Protocol Specification - ARM IHI 0022 Issue K"

# 具体翻译一个request address，是历经stage-1、stage-2才翻译为物理地址？还是说并不是一定非要历经stage-1到stage-2？

不是一定要经历 **Stage-1 → Stage-2**。在 SMMU 里，**Stage-1 和 Stage-2 是可以独立启用/旁路的**。所以一个 request address 最终如何变成 PA，取决于当前这个 Stream 对应的 STE/CD 配置。

可以把它理解成下面几种情况。

### 1. Stage-1 + Stage-2 都开启

这是最完整的两阶段翻译：

```text
Request Address
     │
     │ Stage-1
     ▼
    IPA
     │
     │ Stage-2
     ▼
     PA
```

例如：

```text
VA = 0x4000
   │
   │ Stage-1
   ▼
IPA = 0x84000
   │
   │ Stage-2
   ▼
PA = 0x184000
```

这里：

* Request address 是 **VA（Virtual Address）**
* Stage-1：VA → IPA
* Stage-2：IPA → PA

这是虚拟化场景最典型的情况。

---

### 2. 只开启 Stage-1

```text
Request Address
     │
     │ Stage-1
     ▼
     PA
```

这时候 Stage-1 的输出地址虽然从概念上仍然是 **Intermediate Physical Address**，但因为没有 Stage-2，所以它直接作为最终的物理地址使用。

可以简单理解为：

```text
VA ──Stage-1──> IPA (= final PA)
```

例如：

```text
VA 0x4000
    │
    ▼
IPA 0x84000
    │
    └── 没有 Stage-2
            ↓
        最终 PA = 0x84000
```

所以对于实际系统来说，可以把它理解成 **VA → PA**。

---

### 3. 只开启 Stage-2

这种情况也完全可以存在：

```text
Request Address
     │
     │ Stage-2
     ▼
     PA
```

此时 request address 本身不是 VA，而是 **IPA**。

也就是：

```text
IPA ──Stage-2──> PA
```

这在虚拟机/虚拟化相关场景非常重要。

例如：

```text
Guest OS
   │
   │ guest physical address
   ▼
IPA
   │
   │ SMMU Stage-2
   ▼
PA
```

这里没有 Stage-1。

---

### 4. Stage-1 和 Stage-2 都关闭

那就是 bypass：

```text
Request Address
       │
       │ bypass
       ▼
      PA
```

也就是：

```text
Input address = Output address
```

当然，这里的 address 从系统语义上应该是一个已经可以直接用于物理内存访问的地址。

---

## 所以可以总结成这张表

| Stage-1 | Stage-2 | Request address | 地址转换          |
| ------- | ------- | --------------- | ------------- |
| Enable  | Enable  | VA              | VA → IPA → PA |
| Enable  | Disable | VA              | VA → PA       |
| Disable | Enable  | IPA             | IPA → PA      |
| Disable | Disable | PA              | Bypass        |

最关键的是：

> **Stage-1 和 Stage-2 不是一个不可拆分的“流水线”。它们是两个独立的 translation stage，可以分别启用或 bypass。**

---

## 这也能解释你前面看到的 S1SID / S2SID

现在回头看你那个 Display Processing Unit 的：

```text
S1SID
S2SID
```

就很好理解了。

它很可能允许这个 TBU/translation request 分别确定：

```text
              Request Address
                    │
                    ▼
               ┌─────────┐
               │ Stage 1 │ ← S1SID / S1 context
               └────┬────┘
                    │
                   IPA
                    │
               ┌────▼────┐
               │ Stage 2 │ ← S2SID / S2 context
               └────┬────┘
                    │
                    ▼
                   PA
```

但实际配置可能是：

```text
S1 only:
    VA → PA

S2 only:
    IPA → PA

S1 + S2:
    VA → IPA → PA

None:
    bypass
```

---

### 还有一个特别重要的细节

**不要把“Stage-1 输出一定叫 IPA”和“最终物理地址一定必须经过 Stage-2”混为一谈。**

更准确地说：

```text
Stage-1 的输出地址类型：IPA
Stage-2 的输出地址类型：PA
```

如果 Stage-2 没启用，那么 **Stage-1 的输出 IPA 就直接作为最终访问地址使用**。

同理，如果 Stage-1 没启用，SMMU 可以直接把 request address 当作 IPA，送入 Stage-2：

```text
Request Address (= IPA)
          │
          ▼
       Stage-2
          │
          ▼
         PA
```

这也是为什么在看 TBU RTL 时，最好不要简单地把输入地址命名成 `VA`。**TBU 的 request address 到底是 VA 还是 IPA，要结合当前 STE 的 translation configuration 判断。**

如果你愿意继续往你这个 **Display Processing Unit + TBU + DTI + SMMU** 的实际架构深入，那么下一步最值得搞清楚的是：**TBU 到底怎么知道一个 request 要做 S1、S2 还是 S1+S2？是由 `S1SID/S2SID` 配置决定，还是由 DTI request 中携带的 translation attributes 决定。** 这个和你现在看到的寄存器设计会直接对应起来。


