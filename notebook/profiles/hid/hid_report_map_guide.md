# HID Report Map 实战指南

**Report Map (报表描述符)** 是 HID 设备的灵魂。它是一串二进制数据，告诉主机：“我是什么设备，我的数据长什么样，每个比特代表什么意思”。

如果 Report Map 写错了，无论你的固件代码写得多完美，电脑都无法正确响应按键。

> **参考来源**: *USB HID Usage Tables* & *HOGP Specification*

---

## 1. 描述符基本语法 (Item Encoding)

HID 描述符不是简单的键值对，而是一种流式编码语言。每个条目（Item）由 **前缀（Prefix）** 和 **数据（Data）** 组成。

### 1.1 前缀结构解析 (Short Item Format)
前缀字节（1 Byte）决定了该 Item 的类型和随后的数据长度。

`Prefix = (Tag << 4) | (Type << 2) | Size`

*   **Tag (4 bit)**: 功能标识 (如 Usage Page, Report Count)。
*   **Type (2 bit)**: 作用域类型。
    *   `0 (Main)`: 定义条目 (Input, Output, Collection)。
    *   `1 (Global)`: 全局参数 (Usage Page, Report Size)，**状态保留**直到被覆盖。
    *   `2 (Local)`: 局部参数 (Usage)，**仅对下一个 Main Item 有效**，之后立即清除。
*   **Size (2 bit)**: 后续数据长度。
    *   `0`: 0 Bytes
    *   `1`: 1 Byte
    *   `2`: 2 Bytes
    *   `3`: 4 Bytes (注意：是 4 字节，不是 3 字节)

**示例解析**:
*   **`0x05`** (`0000 01 01`) -> Tag: Usage Page, Type: Global, Size: 1 Byte.
*   **`0x19`** (`0001 10 01`) -> Tag: Usage Min, Type: Local,  Size: 1 Byte.
*   **`0x26`** (`0010 01 10`) -> Tag: Logical Max, Type: Global, Size: 2 Bytes.

### 1.2 常用 Item 速查表

| Item Name | Prefix Hex | Data Bytes | Type (Scope) | 含义与行业惯例 |
| :--- | :--- | :--- | :--- | :--- |
| **Usage Page** | `0x05` / `0x06` | 1 / 2 | **Global** | 命名空间 (如 0x01=Generic Desktop, 0x0C=Consumer)。设置后一直有效。 |
| **Usage** | `0x09` | 1 | **Local** | 具体功能 (如 Keyboard, Mouse)。**用完即焚**。 |
| **Usage Min/Max**| `0x19`/`0x29` | 1 | **Local** | 批量定义 Usage，常用于数组或 Bitmap。 |
| **Logical Min/Max**| `0x15`/`0x25`| 1 / 2 | **Global** | 数据的逻辑值范围 (如 -127 ~ 127)。**注意符号位**。 |
| **Report Size** | `0x75` | 1 | **Global** | **位宽**。每个数据字段占用的 bit 数 (如 1 bit, 8 bits)。 |
| **Report Count** | `0x95` | 1 | **Global** | **数量**。重复多少个 Report Size 的字段。 |
| **Unit** | `0x65` | 1 | **Global** | 物理单位 (如 厘米, 秒)。通常用于数字化仪或传感器。 |
| **Collection** | `0xA1` | 1 | **Main** | 开启一个分组 (Application, Physical)。 |
| **End Collection**| `0xC0` | 0 | **Main** | 关闭当前分组。 |
| **Input** | `0x81` | 1 | **Main** | 定义输入数据 (Dev->Host)。参数掩码决定属性 (Const/Var/Abs)。 |
| **Output** | `0x91` | 1 | **Main** | 定义输出数据 (Host->Dev, 如 LED)。 |
| **Feature** | `0xB1` | 1 | **Main** | 双向特征数据，通常用于配置。 |

---

## 2. 进阶核心概念 (Industry Insights)

在阅读或编写描述符时，新手常在以下几点“踩坑”：

### 2.1 全局 vs 局部 (Global vs Local)
*   **Global (如 Usage Page, Report Size)**: 像编程语言中的“全局变量”。一旦设置，它会一直生效，直到遇到新的 Global Item 修改它。
    *   *Bug 示例*: 在 Mouse Collection 里设置了 `Usage Page (Button)`，退出 Collection 后没有改回 `Usage Page (Generic Desktop)`，导致后续定义的键盘按键变成了“按钮”。
*   **Local (如 Usage, Usage Min)**: 像“函数参数”。它们会被下一个 `Input/Output/Feature` item **消费掉**。消费后，Local 状态清空。

### 2.2 字节对齐 (Byte Alignment)
虽然 HID 允许任意 bit 长度的数据，但在 Windows/Android 等主流系统上，**整个 Report 的总长度最好是 8 bits (1 byte) 的整数倍**。
*   *Best Practice*: 如果有效数据只有 3 bit，请务必使用 `Const` (Padding) 填充剩余的 5 bit。

### 2.3 逻辑范围与符号 (Logical Min/Max & Signedness)
*   HID 解析器根据 Logical Min/Max 判断数据是有符号还是无符号。
*   如果 Min < 0 (补码表示)，则数据被视为有符号整数。
*   *Trap*: `Logical Min (0x80), Logical Max (0x7F)` 在 8-bit 下表示 -128 到 127。但如果写成 `0x00, 0xFF`，则是 0 到 255。

---

## 3. 标准键盘 Report Map (8 字节)

这是最兼容、最常见的键盘描述符。对应的数据包长度固定为 **8 字节**。

### 3.1 描述符代码解析

```c
const uint8_t keyboard_report_map[] = {
    0x05, 0x01,        // Usage Page (Generic Desktop Ctrls)
    0x09, 0x06,        // Usage (Keyboard)
    0xA1, 0x01,        // Collection (Application)
    
    // --- Byte 0: Modifiers (Ctrl, Shift, Alt, GUI) ---
    0x05, 0x07,        //   Usage Page (Keyboard/Keypad)
    0x19, 0xE0,        //   Usage Minimum (0xE0 = Left Control)
    0x29, 0xE7,        //   Usage Maximum (0xE7 = Right GUI)
    0x15, 0x00,        //   Logical Minimum (0)
    0x25, 0x01,        //   Logical Maximum (1)
    0x75, 0x01,        //   Report Size (1) -> 1 bit
    0x95, 0x08,        //   Report Count (8) -> 8 bits
    0x81, 0x02,        //   Input (Data, Var, Abs) -> 变量，每一位独立

    // --- Byte 1: Reserved (保留字节) ---
    0x95, 0x01,        //   Report Count (1)
    0x75, 0x08,        //   Report Size (8) -> 8 bits
    0x81, 0x03,        //   Input (Const, Var, Abs) -> 常量，通常填 0

    // --- Byte 2-7: Key Arrays (普通按键) ---
    0x95, 0x06,        //   Report Count (6) -> 6 个按键槽
    0x75, 0x08,        //   Report Size (8) -> 每个槽 8 bits
    0x15, 0x00,        //   Logical Minimum (0)
    0x25, 0x65,        //   Logical Maximum (101)
    0x05, 0x07,        //   Usage Page (Key Codes)
    0x19, 0x00,        //   Usage Minimum (0)
    0x29, 0x65,        //   Usage Maximum (101)
    0x81, 0x00,        //   Input (Data, Array, Abs) -> 数组模式！

    // --- Output Report (LEDs) ---
    0x95, 0x05,        //   Report Count (5) -> Num, Caps, Scroll, Compose, Kana
    0x75, 0x01,        //   Report Size (1)
    0x05, 0x08,        //   Usage Page (LEDs)
    0x19, 0x01,        //   Usage Min (Num Lock)
    0x29, 0x05,        //   Usage Max (Kana)
    0x91, 0x02,        //   Output (Data, Var, Abs) -> 主机发给设备
    
    0x95, 0x01,        //   Report Count (1)
    0x75, 0x03,        //   Report Size (3) -> Padding to byte boundary
    0x91, 0x03,        //   Output (Const)

    0xC0               // End Collection
};
```

### 3.2 数据包结构 (Payload)

| Byte | 内容 | 说明 |
| :--- | :--- | :--- |
| 0 | **Modifiers** | Bit 0: L-Ctrl, Bit 1: L-Shift ... Bit 7: R-GUI |
| 1 | **Reserved** | 总是 `0x00` (OEM 也可以用来传私有数据，但不推荐) |
| 2 | **Key 1** | 第一个按下的键的 Usage ID (如 `0x04` = 'A') |
| 3 | **Key 2** | 第二个按下的键 |
| ... | ... | ... |
| 7 | **Key 6** | 第六个按下的键 |

> **限制**: 这种模式最多只能同时报告 6 个普通按键。如果你按了 7 个，设备通常会发送 `0x01` (Error Roll Over)。

---

## 4. 全键无冲 (NKRO) 与 Bitmap

要实现 104 键全无冲，不能使用 `Array` 模式，必须使用 `Variable` (Bitmap) 模式。

**原理**: 发送一个 13 字节（104 bit）的包，每一位对应一个键。如果 'A' 键按下，则第 4 位置 1。

```c
// NKRO 描述符片段
0x05, 0x07,    // Usage Page (Keyboard)
0x19, 0x00,    // Usage Min (0)
0x29, 0x7F,    // Usage Max (127) -> 覆盖 128 个键
0x15, 0x00,    // Logical Min (0)
0x25, 0x01,    // Logical Max (1) -> 0 或 1
0x75, 0x01,    // Report Size (1)
0x95, 0x80,    // Report Count (128) -> 16 字节
0x81, 0x02,    // Input (Data, Variable, Abs)
```

---

## 5. 多媒体键 (Consumer Page)

音量加减、播放暂停不属于 Keyboard Page (0x07)，而是 **Consumer Page (0x0C)**。通常使用 **Report ID** 将其与普通键盘数据区分开。

**示例**:
*   Report ID 1: 普通键盘数据 (8 Bytes)。
*   Report ID 2: 多媒体数据 (2 Bytes)。

**多媒体描述符片段**:
```c
0x05, 0x0C,        // Usage Page (Consumer)
0x09, 0x01,        // Usage (Consumer Control)
0xA1, 0x01,        // Collection (Application)
0x85, 0x02,        //   Report ID (2)
0x19, 0x00,        //   Usage Min
0x2A, 0x3C, 0x02,  //   Usage Max (0x023C = AC Format)
0x15, 0x00,        //   Logical Min (0)
0x26, 0x3C, 0x02,  //   Logical Max (0x023C)
0x95, 0x01,        //   Report Count (1)
0x75, 0x10,        //   Report Size (16) -> 16 bit Usage ID
0x81, 0x00,        //   Input (Data, Array, Abs)
0xC0               // End Collection
```

**数据包示例 (音量+)**:
`02 E9 00`
*   `02`: Report ID
*   `E9 00`: Usage ID `0x00E9` (Volume Increment)
