# BlueGemini Bluetooth Protocol Stack Knowledge Base

> **Auto-Generated Index**
> *Last Updated: 2026-01-31 19:24:14*

Based on `Bluetooth Core Specification v6.2` and `HOGP v1.1`.
This knowledge base is governed by the Gemini Agent and utilizes the `pdf` skill for accurate specification extraction.

---

## 📚 Knowledge Index

- **Profiles/** 
  - **Hid/** 
    - [嵌入式Hid设备开发——自底向上视角 V0](Knowledge_Base/profiles/hid/嵌入式HID设备开发——自底向上视角_v0.md)
    - [嵌入式 HID 设备开发——自底向上视角](Knowledge_Base/profiles/hid/嵌入式HID设备开发——自底向上视角_v1.md)
    - [嵌入式 HID 设备开发——自底向上视角 (v2)](Knowledge_Base/profiles/hid/嵌入式HID设备开发——自底向上视角_v2.md)
    - **00 Hgop/** 
      - [GAP 视角下的 HOGP：从配对到加密全景解析](Knowledge_Base/profiles/hid/00_HGOP/gap_role_in_hogp.md)
      - [从按键到RF PHY：HID Report 全栈数据流解构](Knowledge_Base/profiles/hid/00_HGOP/hid-report_2_RF_packet_flow.md)
      - [HID 认知体系构建：从协议定义到内核实现](Knowledge_Base/profiles/hid/00_HGOP/hid_cognitive_system.md)
      - [HOGP (HID over GATT Profile) 架构详解](Knowledge_Base/profiles/hid/00_HGOP/hogp_architecture.md)
      - [HOGP 初始化中的 ATT 报文交换详解](Knowledge_Base/profiles/hid/00_HGOP/hogp_att_packet_exchange_deep_dive.md)
      - [HOGP 设备完整初始化流程：从广播到可用](Knowledge_Base/profiles/hid/00_HGOP/hogp_device_initialization_flow.md)
      - [HOGP 初始化与配置：ATT 报文全解析](Knowledge_Base/profiles/hid/00_HGOP/hogp_initialization_packet_flow.md)
    - **02 Descriptors/** 
      - [HID Report Descriptor 实战指南](Knowledge_Base/profiles/hid/02_Descriptors/00_hid_report_desc_guide.md)
      - [标准键盘 HID Usage Map (Page 0x07)](Knowledge_Base/profiles/hid/02_Descriptors/01_standard_keyboard_usage_map.md)
      - [进阶 HID 多媒体与系统键开发指南](Knowledge_Base/profiles/hid/02_Descriptors/02_Consumer_and_SC_AC_keys.md)
    - **03 App Notes/** 
      - [Hid Kb Long Pressed情景分析](Knowledge_Base/profiles/hid/03_App_notes/hid-kb-long_pressed情景分析.md)
      - [HID 多媒体键实现指南](Knowledge_Base/profiles/hid/03_App_notes/multimedia_keys_implementation.md)
      - [机械键盘全键无冲 (NKRO) 实现指南](Knowledge_Base/profiles/hid/03_App_notes/nkro_implementation_guide.md)
    - **04 Kernel Os/** 
      - [Linux Kernel HID Subsystem: 补充阅读与实战指南](Knowledge_Base/profiles/hid/04_Kernel_OS/Addt-kernel-hid-wiki.md)
- **Vol1 Architecture/** 
  - [蓝牙传输架构层级 (Transport Architecture Hierarchy)](Knowledge_Base/vol1_architecture/transport_hierarchy.md)
- **Vol3 Host/** : *蓝牙主机（Host）协议栈位于 HCI 层之上，负责处理逻辑链路、安全、属性管理以及应用程序的通用访问。*
  - **Att/** 
    - [Attribute Protocol (ATT) 深度解析](Knowledge_Base/vol3_host/att/att_pdu_formats.md)
  - **Gap/** 
    - [GAP Advertising Data Format (广播数据格式)](Knowledge_Base/vol3_host/gap/gap_advertising_data.md)
    - [GAP Modes & Procedures (模式与过程)](Knowledge_Base/vol3_host/gap/gap_modes_procedures.md)
  - **Gatt/** 
    - [GATT Caching & Robustness (缓存与健壮性)](Knowledge_Base/vol3_host/gatt/caching_robustness.md)
    - [GATT 交互操作 (GATT Procedures)](Knowledge_Base/vol3_host/gatt/gatt_attribuite-IO交互.md)
    - [GATT 核心概念与角色 (GATT Overview & Roles)](Knowledge_Base/vol3_host/gatt/gatt_overview.md)
    - [GATT Service Discovery (服务发现子过程)](Knowledge_Base/vol3_host/gatt/service_discovery.md)
  - **L2Cap/** 
    - [L2CAP 核心机制 (General Operation & Channels)](Knowledge_Base/vol3_host/l2cap/l2cap_general_operation.md)
    - [L2CAP 数据包格式 (Packet Formats)](Knowledge_Base/vol3_host/l2cap/l2cap_packet_formats.md)
  - **Smp/** 
    - [SMP Key Distribution (密钥分发与管理)](Knowledge_Base/vol3_host/smp/smp_keys_distribution.md)
    - [SMP Pairing Process (配对与安全连接流程)](Knowledge_Base/vol3_host/smp/smp_pairing_process.md)
- **Vol4 Hci/** 
  - [HCI Initialization & Command Flow (初始化与核心流程)](Knowledge_Base/vol4_hci/hci_initialization_flow.md)
  - [HCI Packet Structures (HCI 包结构详解)](Knowledge_Base/vol4_hci/hci_packet_structures.md)
  - **Hci Raw/** 
    - [HCI Command: Read Local Version](Knowledge_Base/vol4_hci/hci_raw/hci_cmd_read_ver_raw.md)
    - [HCI Command: Reset](Knowledge_Base/vol4_hci/hci_raw/hci_cmd_reset_raw.md)
    - [HCI Command: LE Set Adv Params](Knowledge_Base/vol4_hci/hci_raw/hci_cmd_set_adv_param_raw.md)
    - [HCI Packet Formats (Command, Event, ACL)](Knowledge_Base/vol4_hci/hci_raw/hci_packet_formats_raw.md)
- **Vol6 Controller/** 
  - [BLE 空口包格式 (Air Interface Packets)](Knowledge_Base/vol6_controller/air_interface_packets.md)
  - [BLE 连接建立流程 (Connection Establishment Flow)](Knowledge_Base/vol6_controller/connection_establishment.md)
  - [Isochronous Channels & ISOAL (等时通道详解)](Knowledge_Base/vol6_controller/isochronous_channels.md)
  - [BLE Link Layer 状态机 (Link Layer State Machine)](Knowledge_Base/vol6_controller/link_layer_states.md)
  - [MSC Raw Text Extraction](Knowledge_Base/vol6_controller/msc_raw_text.md)
  - **Iso Raw/** 
    - [ISOAL Features (Framed vs Unframed PDU)](Knowledge_Base/vol6_controller/iso_raw/isoal_features_raw.md)
    - [ISOAL Timing (Time Stamp & Offset)](Knowledge_Base/vol6_controller/iso_raw/isoal_timing_raw.md)
---

## 🚀 自动化工作流 (Automation Workflow)

本项目集成了自动化运维脚本，建议通过 `do.bat` 进行所有日常操作：

- **`do.bat`**: 核心自动化入口。依次运行 README 索引更新、JSON 索引生成，并引导完成 Git 提交流程。
  - 用法：`do -m "commit message"` (自动更新并提交)
  - 用法：`do --check` (仅更新并预览索引，不提交)

## 🛠️ 运维工具库 (Operational Tools)

这些脚本位于 `.gemini/scripts/`，用于维持知识库的结构化与准确性：

- **索引治理**:
  - `generate_root_index.py`: (本脚本) 自动扫描 `Knowledge_Base` 并重建根目录 `README.md` 导航树。
  - `generate_kb_index.py`: 为 Agent 生成结构化的 `index.json`，提升机器检索效率。
- **PDF 提取**: `optimized_split_pdf.py`, `extract_gatt.py`, `extract_hid_core.py` 等。
- **质量校验**: `validate_kb_pdfs.py` (检查 PDF 完整性), `recover_kb.py` (知识库恢复)。

---

## 📜 License & Copyright

Copyright (c) 2026 **yceachan** (<yceachan@foxmail.com>)

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
