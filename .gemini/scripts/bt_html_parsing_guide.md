# Bluetooth SIG HTML 文档解析规范

> [!note]
> **目标**: 固化蓝牙联盟 (Bluetooth SIG) 官方规范 HTML 版本的 DOM 结构特征，以便 Agent 能够高效、准确地提取和重构文档树。

通过对 `Basic Audio Profile` 和 `Common Audio Service` 等文档的分析，我们总结出以下层次结构和特征提取规则。

## 1. 标题与层级树 (Headings & TOC)

Bluetooth SIG 的 HTML 规范使用带有特定 `class` 的 `<h1...6>` 标签来标识章节标题。

### 1.1 章节标题提取特征
- **标签**: `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>`
- **Class**: 包含 `title`。
- **内部结构**:
  - `<span class="formal-number">`: 章节编号 (例如 `1.2.1`)。
  - `<span class="formal-title">`: 章节实际标题文本。
  
**示例 HTML**:
```html
<h3 class="title"><span class="formal-number">3.5</span><span class="formal-label-delimiter">.</span> <span class="formal-title">Unicast Server support requirements</span></h3>
```

**解析逻辑 (Python Regex / BeautifulSoup)**:
提取所有的 `<h[1-6]>` 且 `class="title"`。读取其子元素 `.formal-number` 和 `.formal-title`，即可重构出完整的文档大纲 (TOC)。

### 1.2 目录超链接提取
在文档开头的目录树中，对应的链接特征：
- **标签**: `<a>`
- **Class**: `topic-link`
- **内容**: `章节编号. 章节名称`

## 2. 表格数据 (Tables)

规范中包含大量的 Requirement 表格和数据结构表格。

### 2.1 表格提取特征
- **标签**: `<div class="table">` 包含 `<table>`，或者 `<div class="informaltable">`。
- **标题**: `<p class="title"><strong>Table X.Y: ...</strong></p>`。
- **表头**: `<thead>` 内部的 `<tr>` 和 `<th>`。
- **表体**: `<tbody>` 内部的 `<tr>` 和 `<td>`。

**解析策略**:
定位 `table` 标签，读取 `th` 提取列名，迭代 `tr` 提取每行数据。必要时转换为 Markdown 表格格式输出。

## 3. 内部链接与引用 (Cross-References)

规范内通常会交叉引用其他章节或外部文档。

### 3.1 交叉引用特征
- **标签**: `<a class="xref" href="...">`。
- **文本**: 通常是 "Section X.Y" 或 "Table Z"。

## 4. 段落与列表 (Paragraphs & Lists)

- **段落**: 普通 `<p>` 标签。
- **无序列表**: `<div class="itemizedlist"><ul class="itemizedlist"><li class="listitem"><p>...`。
- **要求/注意事项 (Notes)**: `<div class="note">` 包含 `<h3 class="title">Note</h3>`。

## 5. 通用解析脚本范式

针对此规范，推荐在 `.gemini/scripts/` 中维护 `parse_bt_html.py` 脚本：
1. **输入**: HTML 文件路径。
2. **模式**: 
   - `--toc`: 提取完整目录树。
   - `--section "X.Y"`: 提取特定章节的内容及表格。
   - `--tables`: 提取文档内所有表格并转换为 Markdown 格式。
3. **依赖**: `re` 或 `BeautifulSoup` (由于环境限制，当前推荐优先使用 `re` 正则提取，或确保环境中安装了 `beautifulsoup4`)。