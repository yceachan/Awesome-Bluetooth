# 蓝牙协议栈知识库项目 (Bluetooth Protocol Stack Knowledge Base)

**项目代号**: BlueGemini
**核心真理来源**: `Bluetooth Core Specification v6.2` (PDF)
**目标用户**: 蓝牙固件工程师、协议栈开发者、应用开发人员。
**输出语言**: **中文 (Chinese)** (保留英文专业术语)。

---

## 1. 项目架构 (Project Architecture)

本项目将庞大的 PDF 规范解构为三个层级：

1.  **源数据层 (`Docs/<spec>/chunk`)**: 
    *   基于 Vol/Part 结构切分后的 PDF 原文。
    *   *Agent 须知*: 严禁全量读取原始大文件。读取时必须通过索引找到对应的 `source.pdf`。
2.  **知识层 (`Knowledge_Base/`)**: 
    *   经过治理、提炼、结构化的 Markdown 笔记。
    *   包含 Mermaid 图表、核心概念解析、协议交互流程。
    *   `index.json` : py脚本维护的知识库索引
3.  **工具层 (`.gemini/scripts/`)**: 
    *   用于自动化处理 PDF、提取文本、验证数据的 Python 脚本库。

---

## 2. 工具库清单 (Toolbox & Scripts)

新会话开始时，优先使用如下先前治理过程中固化的可用脚本，path： `.gemini/scripts/`。

e.g.:包括不限于如下script：

| 脚本名 | 功能描述 | 典型用法 |
| :--- | :--- | :--- |
| **`optimized_split_pdf.py`** | **PDF 切分器**。基于 XML 索引将 Core Spec 大文件切分为 Part 级小文件。 | `python .gemini/scripts/optimized_split_pdf.py` |
| **`validate_kb_pdfs.py`** | **完整性校验**。检查切分后的 PDF 是否损坏，必要时自动清理。 | `python .gemini/scripts/validate_kb_pdfs.py` |
| **`extract_gatt.py`** | **GATT 提取器**。从 Vol 3 Part G 提取 GATT 角色、层级和流程。 | 模板脚本，可复制修改用于其他章节提取。 |
| **`extract_l2cap.py`** | **L2CAP 提取器**。提取 Vol 3 Part A 的通道和包结构。 | 同上。 |
| **`extract_msc.py`** | **MSC 提取器**。提取 Vol 6 Part D 的时序图文本描述。 | 用于辅助绘制 Mermaid 时序图。 |
| **`extract_le_controller.py`** | **Controller 提取器**。提取 LL 状态机和空口包格式。 | - |
| **`extract_transport_arch.py`** | **架构提取器**。提取 Vol 1 的传输层级架构。 | - |

> **开发提示**: 当你需要从新的章节提取内容时，请参考 `extract_gatt.py` 作为模板，修改页码范围 (Range) 和输出路径即可。

---

## 3. 知识治理进度 (Progress Snapshot)

*最后更新: 2026-01-23*

### ✅ 已完成 (Done)
> [!tip]
>
> check the index json [index.json](Knowledge_Base/index.json)

### ⏳ 待办 (To-Do)

> [!tip]
>
> **Maintenance**: 随着 Spec 更新由AGENT持续维护。

*   **SMP Deep Dive**: Legacy vs LE Secure Connections, Pairing Phases 1-3, Key Distribution details.
*   **More Profiles**: 扩展至 HRP (Heart Rate), FTMS (Fitness Machine) 等。
*   **Advanced Controller**: Channel Sounding (v6.0) 深度实战。

---

## 4. 标准作业程序 (SOP)

在新会话中治理新章节时，请遵循以下步骤：

（以bt-core文档为案例演示，其他大文档as so）

0. (开发者任务，do once)：
    - 使用`.gemini/script/threaded_split_pdf.py`的脚本范式，chunk大文档。

1. **定位资源**:

   *   查阅`Docs/Bt-core/Bluetooth_Core_v6.2_Index.md` 或读取 `Docs/Bt-core/chunk/` 目录结构，找到目标 Part 的 `source.pdf` 路径。
   *   读取该 Part 目录下的 `README.md`，获取精确的**内部页码 (Internal Page Numbers)** 索引。

2. **提取内容**:

   - 充分利用 pdf skill

   *   **不要**试图一次性读取整个 PDF。
   *   复制并修改 `.gemini/scripts/extract_template.py` (或参考现有的 `extract_gatt.py`)。
   *   设置准确的 `Page Range`。
   *   运行脚本将原始文本提取到 `Knowledge_Base/xxx/xxx_raw.md` 或直接生成目标文件。

3. **知识重构**:
   *   读取提取的原始文本。
   *   使用 Markdown 重写，要求：
       *   **结构清晰**: 使用 H1/H2/H3 标题。
       *   **中文输出**: 翻译并解释核心概念，但保留英文术语 (如 "Advertising Interval")。
       *   **图表化**: 遇到流程、状态机、层级结构，必须使用 **Mermaid Skill** 绘制。
       *   **Mermaid自检** : 根据mermiad skill 的prompt ，检查验证语法错误，保证输出graph能正常渲染。
       *   **表格化**: 遇到参数列表、PDU 结构，使用 Markdown 表格。

4. **文件归档**:
   *   将治理好的文件保存在 `Knowledge_Base/` 下对应的分类目录中。

5. 文档规范：


   - **Mermaid** 
     
     - **whenever** naming a node ,especially with chars like `/ \ () （）`,and chinese,using`""`to include the whole node name.
       - e.g. `GpioLib["GPIO库"] -- register --> Sysfs["/sys/class/gpio"]`
     - **SequenceDiagram**:
       - Always include `autonumber` to clearly mark the execution sequence.
       - When using `rect rgb(...)` blocks, the background color must maintain **High Brightness** (each RGB component > 200) to ensure high contrast and readability for black text on light backgrounds.

   - 中文知识输出：
     - 最终结论和文档输出必须使用中文，同时保留专业英文术语
     - 高价值的知识输出始终应固化在文件系统而非上下文缓存，当开发者未明确指示路径，Agent应智能判断一个适合的路径，并提出写入建议。
     
   - Reference:

     - always respective source of truth , if Agent refer then ,mark it  below the 1st H1 Title :

       - not only web wiki , **but also local code、note、docs。**
       
       - ```md
         # H1 Title
         
         > [!note]
         > **Ref:** [wiki](url)
         
         text...
         ```
