spyglass 的verilog lint检查的选项lint_rtl/lint_turbo_rtl/lint_functional_rtl有什么区别


这三个 Goal 都属于 SpyGlass 的 RTL Lint，但它们的分析深度、依赖信息以及检查内容是不一样的。一般可以理解为：

| Goal                    | 分析重点                   | 是否需要SGDC/SDC | 分析深度 | 运行时间 |
| ----------------------- | ---------------------- | ------------ | ---- | ---- |
| **lint_rtl**            | 基本RTL静态检查              | 不需要          | ★    | 最快   |
| **lint_turbo_rtl**      | RTL + Design Context检查 | 通常需要         | ★★   | 中等   |
| **lint_functional_rtl** | 功能级静态分析（结合Formal）      | 不一定，但有约束效果更好 | ★★★  | 最慢   |

下面分别介绍。

---

## 1. lint_rtl —— 最基础的RTL Lint

这是大家每天都会跑的Goal。

它主要检查：

* Verilog/SystemVerilog语法
* Coding Style
* STARC规范
* OpenMORE规范
* 综合相关问题
* 位宽不匹配
* latch推断
* combinational loop
* 未连接端口
* 多驱动
* 未使用变量
* case语句完整性
* reset写法
* always块问题

例如：

```verilog
always @(*) begin
    if (en)
        out = a;
    // else忘了
end
```

直接报：

```
InferLatch
```

例如

```verilog
wire [3:0] a;
wire [7:0] b;

assign b = a;
```

会报

```
Width mismatch
```

这些都是纯RTL静态分析，不需要任何约束。([博客园][1])

---

# 2. lint_turbo_rtl —— 增加了Design Context

很多人第一次用都会奇怪：

> 为什么 lint_rtl 能跑，而 lint_turbo_rtl Fatal？

原因就是：

Turbo Lint希望知道设计真正的运行环境。

因此通常需要：

* SGDC
* Clock定义
* Reset定义
* Black box信息
* Design hierarchy

否则很多Rule无法分析。

例如：

```
create_clock
```

```
set_case_analysis
```

```
define_reset
```

等等。

它比lint_rtl多出来很多和设计环境有关的检查，例如：

* Clock使用是否合法
* Reset传播
* Clock gating
* Constant propagation
* 不可达逻辑
* 约束一致性
* false path导致的问题
* 时钟相关Lint

所以很多公司的流程都是：

```
lint_rtl
        ↓
所有Error清零
        ↓
加入SGDC
        ↓
lint_turbo_rtl
```

如果没有SGDC，经常直接报Fatal。([博客园][1])

---

# 3. lint_functional_rtl —— Functional Lint

这是SpyGlass近几年最重要的新能力。

很多人误以为：

> Functional Lint = 更多Rule

其实不是。

它最大的区别是：

**引入了Formal Analysis（VC Formal技术）**。

传统Lint只能看代码。

例如：

```verilog
if (sel)
    a = b;
else
    a = c;
```

Lint只能检查：

* 写法是否合法
* 有没有Latch

但是不知道：

```
sel是不是永远为0？
```

Functional Lint则会进行状态空间分析。

例如：

```
sel 永远不会等于1
```

那么：

```
if(sel)
```

整个分支就是

```
Dead Code
```

传统Lint完全发现不了。

Synopsys官方把这种称为：

> Beyond Traditional Lint（超越传统Lint）([Synopsys][2])

---

## Functional Lint能发现什么

官方重点强调包括：

### Dead Code

例如

```verilog
if (1'b0)
    ...
```

或者

```verilog
parameter MODE=0;

generate
if(MODE)
    ...
endgenerate
```

不可达代码。

---

### FSM问题

例如：

```
FSM Live Lock
```

状态机进入某状态后永远出不来。

例如：

```
S0
 ↓
S1
 ↑
 └──
```

永远循环。

传统Lint几乎检测不到。

---

### Width问题

例如

```verilog
wire [3:0] a;
wire [7:0] b;

assign a = b + c;
```

普通Lint只能看到：

```
宽度不同
```

Functional Lint会进一步分析：

到底有没有真正发生overflow。

---

### Array越界

例如

```verilog
reg [7:0] mem[15:0];

assign x = mem[index];
```

如果：

```
index可能达到31
```

Functional Lint会报告：

```
Out of Bound
```

---

### Constant propagation

例如：

```
parameter ENABLE = 0;
```

那么整个设计：

```
if(ENABLE)
```

都是Dead Logic。

---

### X传播

例如：

某些分支可能导致X传播。

---

### Arithmetic分析

例如：

```
Signed/Unsigned
```

这种Rule很多就是：

```
Av_width_...
```

```
Arith_...
```

很多人在lint_functional_rtl第一次都会看到这些Rule。([Synopsys][2])

---

# 为什么叫 Functional Lint？

因为它已经不是简单的

```
Code Style Check
```

而是在做：

```
静态功能验证
```

不用Testbench

不用Simulation

不用Assertion

直接利用Formal Engine分析RTL可达状态。

Synopsys官方资料也明确指出：

> Functional Lint integrates formal technology with traditional lint to detect deeper RTL issues (如 DeadCode、FSM LiveLock、Width Mismatch、Out-of-Bounds 等)，并降低误报。([Synopsys][2])

---

# 实际项目中建议的使用顺序

一般大公司的RTL Signoff流程都是：

```
RTL完成
    │
    ▼
lint_rtl
    │
    ├── 修所有Error
    │
    ▼
lint_turbo_rtl
    │
    ├── 加SGDC
    ├── 修Clock/Reset相关问题
    │
    ▼
lint_functional_rtl
    │
    ├── 修Dead Code
    ├── 修Width问题
    ├── 修FSM问题
    │
    ▼
CDC
    ▼
RDC
    ▼
综合
```

对于日常开发，`lint_rtl` 足够快，适合作为每次提交前的检查；在模块准备交付或做 RTL signoff 时，再运行 `lint_turbo_rtl` 和 `lint_functional_rtl`，能够发现更多与设计环境和潜在功能缺陷相关的问题。

[1]: https://www.cnblogs.com/sasasatori/p/18401030?utm_source=chatgpt.com "数字asic流程实验（EX2）Spyglss Lint - sasasatori - 博客园"
[2]: https://www.synopsys.com/blogs/chip-design/linting-techniques-automotive-aerospace-chip-design.html?utm_source=chatgpt.com "Linting for Automotive & Aerospace Chip Design | Linting Part 2 | Synopsys Blog"
