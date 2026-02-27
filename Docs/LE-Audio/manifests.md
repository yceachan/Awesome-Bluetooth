### 🔗 官方下载通道

**官方规范库地址:** [Bluetooth Specifications](https://www.bluetooth.com/specifications/specs/) *(注：绝大多数文档可直接以 PDF 格式下载，部分可能需要注册免费的蓝牙官网账号)*

------

### 📚 LE Audio 核心规范清单

#### 1. 核心底座与编解码器 (Core & Codec)

这是 LE Audio 能运行的物理和算法基础。

- **Bluetooth Core Specification (v5.2 +)**：引入了 **LE Isochronous Channels (ISOC)** 等时通道，这是支撑低延迟音频传输的底层协议。
- **LC3 (Low Complexity Communication Codec)**：LE Audio 强制要求支持的全新高效音频编解码器规范。

#### 2. 基础音频架构 (Audio Architecture)

搭建 LE Audio 链路和拓扑结构的核心协议。

- **BAP (Basic Audio Profile)**：**最核心的文档！** 定义了单播（Unicast）和广播（Broadcast）音频的建立、控制和数据流管理。
- **CAP (Common Audio Profile)**：通用音频配置文件，规定了设备在执行音频启动、更新、停止等过程中的顶层状态机及组管理流。

#### 3. 媒体与通话场景 (Media & Telephony)

用于规范音乐播放、切歌、接打电话等具体使用场景。

- **TMAP (Telephony and Media Audio Profile)**：定义了设备如何处理电话接听和媒体音频的播放。
- **MCP (Media Control Profile)** & **MCS (Media Control Service)**：媒体控制（如播放、暂停、下一曲）。
- **CCP (Call Control Profile)** & **TBS (Telephone Bearer Service)**：通话控制（如接听、挂断、拒接）。

#### 4. 设备交互与控制 (Device Control & Coordination)

用于控制耳机音量、麦克风静音以及 TWS（真无线耳机）双耳的协同。

- **VCP (Volume Control Profile)** & **VCS (Volume Control Service)**：绝对音量控制。
- **MICP (Microphone Control Profile)** & **MICS (Microphone Control Service)**：麦克风静音与状态控制。
- **CSIP (Coordinated Set Identification Profile)** & **CSIS**：协调集识别。用于将左耳和右耳两个独立设备绑定为“一个整体（Set）”进行统一管理，这是开发 TWS 耳机必看的规范。

#### 5. 广播音频与助听 (Auracast™ & Hearing Aids)

- **PBA (Public Broadcast Profile)**：公共广播配置文件（与 Auracast 广播音频息息相关）。
- **BASS (Broadcast Audio Scan Service)**：广播音频扫描服务，用于辅助设备（如手机）帮另一个没有屏幕的设备（如耳机）搜索并加入广播流。
- **HAP (Hearing Access Profile)** & **HAS**：助听器接入规范，定义了如何将 LE Audio 技术用于助听设备。

## Fetched

> [!tip]
>
> this part should be maintained by Agent automatically

## PLAN
> [!tip]
>
> this part should be maintained by Agent automatically

建议阅读顺序是：**Core 5.2 (ISOC 章节)** ➡️ **LC3** ➡️ **BAP** ➡️ **CAP**。吃透 BAP 基本就掌握了 LE Audio 的骨架。