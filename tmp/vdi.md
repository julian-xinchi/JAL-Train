# 公司里经常说的”VDI物理服务器“中的VDI是什么

这里的 **VDI** 一般是 **Virtual Desktop Infrastructure**，中文通常叫：

> **虚拟桌面基础设施**

所以公司里说的 **“VDI 物理服务器”**，通常不是说“物理服务器本身就是 VDI”，而是：

> **用物理服务器作为底层基础设施，运行很多虚拟桌面（Virtual Desktop）。**

### 举个你工作环境里比较典型的例子

可能是：

```text
                    公司 VDI 系统
                         │
              ┌──────────┴──────────┐
              │                     │
          VDI Server 1          VDI Server 2
          物理服务器              物理服务器
              │                     │
       ┌──────┼──────┐       ┌──────┼──────┐
       │      │      │       │      │      │
      VM1    VM2    VM3     VM4    VM5    VM6
       │      │      │       │      │      │
      Linux  Linux  Linux   Linux  Linux  Linux
```

你坐在自己的 PC 前，通过：

```text
PC
 ↓
VDI Client
 ↓
网络
 ↓
你的 Virtual Desktop
```

使用远程 Linux/Windows 桌面。

---

### 为什么会说“VDI物理服务器”？

因为在公司 IT 语境中，经常把服务器分成：

* **物理服务器（Physical Server）**
* **虚拟机（VM）**
* **VDI 服务器**

而“VDI 物理服务器”通常是指：

> **承载 VDI 虚拟机的那台真实物理机器。**

例如你之前使用的：

```bash
bsub -q qname -Is gvim netlist.v
```

如果公司的开发环境是 VDI，那么可能存在这样的层次：

```text
你的电脑
   ↓
VDI Desktop
   ↓
VDI Host / Physical Server
   ↓
你的 Linux VM
   ↓
LSF
   ↓
compute node
```

这里要特别区分：

**VDI Server ≠ LSF Compute Server。**

VDI 主要解决的是**“给你一个远程桌面/工作环境”**；LSF 主要解决的是**“把计算任务调度到计算节点”**。

所以你可能登录的是 VDI 上的 Linux 桌面，然后：

```bash
bsub ...
```

把 VCS、Verdi、gvim 等任务提交到另外的 compute server。

---

### VDI 最核心的概念

可以简单记成：

> **VDI = 把“你的电脑桌面”虚拟化并放到服务器上。**

因此你看到的：

> “VDI物理服务器”

更准确地理解为：

> **运行 VDI 虚拟桌面环境的底层物理服务器（VDI host）。**

另外，VDI 有时也会被泛称为“虚拟桌面环境”，但严格来说 **VDI 是 Virtual Desktop Infrastructure**，不是 Virtual Desktop 本身。
