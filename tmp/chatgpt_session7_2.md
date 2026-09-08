下面整理成一个适合长期保存和后续继续补充的 Markdown 笔记结构。内容按 **Display Controller AFBC Decoder 设计视角** 组织，而不是简单复述对话。

你可以保存为：

```text
AFBC_Decoder_Design_Notes.md
```

---

```markdown
# AFBC Decoder Design Notes

## 1. Overview

AFBC (Arm Frame Buffer Compression) is a lossless image compression format designed by Arm for reducing memory bandwidth and storage requirements in GPU and Display systems.

In a Display Controller, the AFBC Decoder is responsible for:

- Reading AFBC Header information
- Locating compressed Body data
- Decoding compressed superblocks
- Reconstructing original pixel data
- Feeding the pixel pipeline

An AFBC buffer consists of:

```

+----------------+
| Header Buffer  |
+----------------+
| Body Buffer    |
+----------------+

```

The decoder needs both:

- Buffer-level metadata
- Per-superblock header information

to correctly reconstruct pixels.

---

# 2. AFBC Buffer Organization

## 2.1 Superblock

AFBC divides an image into fixed-size superblocks.

Common block sizes:

| Block Type | Size |
|---|---|
| Standard Block | 16x16 pixels |
| Wide Block | 32x8 pixels |

Each superblock contains:

```

+-------------+
| Header      |
+-------------+
| Body        |
+-------------+

```

Header describes how the corresponding Body should be decoded.

---

# 3. AFBC Metadata Hierarchy

AFBC information can be divided into two levels.

## 3.1 Buffer-level Metadata

These describe the whole framebuffer.

Examples:

- Pixel format
- AFBC enable
- Wide Block enable
- Split Block enable
- Tiled Header enable
- Sparse layout enable
- YTR enable


These are usually provided by:

- DRM modifier
- Buffer descriptor
- Display Controller registers


Example:

```

AFBC Buffer Descriptor

```
Pixel Format = ARGB2101010
Wide Block   = Enable
Split        = Enable
Sparse       = Enable
```

```

---

## 3.2 Superblock-level Metadata

Stored in AFBC Header.

Examples:

- Compression mode
- Solid color indication
- YTR information
- Split information
- Body related information

Header describes:

```

How to decode this specific superblock

```

---

# 4. AFBC Pixel Format (FourCC)

FourCC describes the uncompressed pixel format.

Examples:

| FourCC | Format |
|-|-|
| AR24 | ARGB8888 |
| XR24 | XRGB8888 |
| AR30 | ARGB2101010 |
| BR30 | ABGR2101010 |


Example:

## AR30

```

31                         0

A       R        G        B
2bit   10bit    10bit   10bit

```

Total:

```

2 + 10 + 10 + 10 = 32 bits

```

"30" means RGB precision:

```

10 + 10 + 10 = 30 bits

```

not total pixel width.

---

# 5. AFBC Layout Types

AFBC uses multiple independent layout concepts.

Do not confuse:

| Concept | Meaning |
|-|-|
| Buffer Layout | Body memory organization |
| Header Layout | Header memory organization |
| Block Layout | Superblock geometry |


---

# 6. Buffer Layout

## 6.1 Free Layout

Body locations are freely allocated.

Header provides Body location information.

Flow:

```

Header

|
| Body Offset

v

Body

```

Address calculation:

```

BodyAddr = Header.BodyOffset

```


---

## 6.2 Sparse Layout

Sparse layout uses deterministic Body addressing.

Body address can be calculated:

```

BodyAddr =
BodyBase +
Superblock_Index * Stride

```

Therefore:

Header does not need to provide a variable Body offset.

However:

**Header is still required.**

Reason:

Header contains per-superblock decoding information:

- compression mode
- solid color
- encoding status
- etc.


Important:

Sparse does NOT mean:

```

No Header

```

It means:

```

Header is no longer required for Body address lookup

```

---

## 6.3 Stripe Layout

Stripe layout is another Body organization method.

It groups Body data into stripes.

Support depends on AFBC version and hardware implementation.

---

# 7. Header Layout

## 7.1 Linear Header

Header entries are stored sequentially.

Example:

```

H00 H01 H02 H03
H10 H11 H12 H13
H20 H21 H22 H23

```

Address:

```

addr =
base +
(superblock_index * header_size)

```

---

## 7.2 Tiled Header

Header entries are stored in tiles.

Example:

```

+---------+---------+
| Tile0   | Tile1   |
| 8x8 SB  | 8x8 SB |
+---------+---------+
| Tile2   | Tile3   |
+---------+---------+

```

Purpose:

- Improve cache locality
- Improve DDR burst efficiency
- Reduce header fetch overhead


Decoder needs to know:

```

Tiled Header Enable

```

before accessing Header.

Because Header address calculation changes.

---

# 8. Wide Block Layout

Wide Block changes superblock geometry.

Example:

Standard:

```

16 x 16

################
################
################
################
...

```

Wide:

```

32 x 8

################################
################################
...

```

Both contain:

```

256 pixels

```

Difference:

- X/Y distribution
- Address calculation
- Compression behavior


Register example:

```

AFBC_WIDE_BLOCK_ENABLE

```

Meaning:

```

Use Wide Superblock format

```

---

# 9. Split Block

Split Block divides compressed Body into partitions.

Example RGBA:

Without split:

```

Body

RGBARGBARGBARGBA

```

With split:

```

Body

+------------+
| RGB data   |
+------------+

+------------+
| Alpha data |
+------------+

```

Benefits:

- Better compression efficiency
- Better alpha handling
- Potential bandwidth reduction


Decoder needs:

```

Split Enable

```

because Body interpretation changes.

---

# 10. AFBC Decoder Required Configuration

Typical Display Controller registers:

```

AFBC_CTRL

```
Enable
```

AFBC_FORMAT

```
Pixel Format
```

AFBC_LAYOUT

```
Sparse
Tiled Header
Wide Block
Split
```

AFBC_BASE

```
Header Address
Body Address
```

```

---

# 11. Why Layout Cannot Be Stored in Header

A common question:

"Why doesn't Header contain Sparse/Free information?"

Because decoder must know the layout before reading Header.

Example:

To read Header:

```

Header Address =
?

```

But Header address depends on:

- Linear Header
- Tiled Header


Similarly:

Body address depends on:

- Free
- Sparse


Therefore:

Layout must come from external metadata:

```

Buffer Descriptor
|
v
AFBC Decoder Configuration
|
v
Read Header
|
v
Decode Body

```

---

# 12. Display Controller AFBC Decode Flow

```

```
            Buffer Metadata
                  |
                  v
          AFBC Configuration
                  |
                  |
    +-------------+-------------+
    |                           |
    v                           v
```

Header Address Generator     Body Address Generator

```
    |                           |
    v                           v

  Header                  Compressed Body

    |
    |
    v
```

Superblock Decode Engine

```
    |
    v
```

Original Pixel Data

```
    |
    v
```

Display Pipeline

```

---

# 13. Design Questions Checklist

When implementing or reviewing an AFBC Decoder:

## Pixel format

- Which FourCC formats are supported?
- RGB/YUV?
- Bit depth?


## Header

- Linear or tiled header?
- Header size?
- Address calculation?


## Body

- Free?
- Sparse?
- Stripe?


## Block

- 16x16?
- Wide Block?


## Compression features

- Split?
- YTR?
- Solid Color?


## Software interface

Where does metadata come from?

- DRM modifier?
- Register?
- Descriptor?


---

# Summary

AFBC decoding requires three independent types of information:

```

1. Pixel Format

   AR30 / XR24 / NV12

2. Header Layout

   Linear / Tiled Header

3. Body Layout

   Free / Sparse / Stripe

4. Block Geometry

   16x16 / Wide Block

```

The decoder cannot discover these from Header alone.

They must be configured before decoding starts.
```

---

这个版本偏 **IP 设计 / Display Controller RTL 评审笔记** 风格，后续如果继续研究 AFBC，建议继续往里面补：

1. **AFBC Header bit field（如果拿到 Arm NDA spec）**
2. **Header/Body address generator RTL architecture**
3. **AXI read pattern（Header fetch + Body burst）**
4. **AFBC error handling（ECC、CRC、invalid header）**
5. **与 Mali GPU AFBC encoder 的对应关系**

这样会逐渐变成一份完整的 AFBC Decoder Design Spec。
