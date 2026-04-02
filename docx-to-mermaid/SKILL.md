---
name: docx-to-mermaid
description: "Convert PRD .docx files to AI-friendly Markdown with Mermaid diagrams. Use this skill when the user wants to convert a .docx PRD document to markdown, when they mention docx-to-mermaid, or as Step 0 of the openspec workflow before /opsx:explore or /opsx:propose. Triggers on: 'convert docx', 'docx to md', 'docx to mermaid', 'convert PRD', '转换 PRD', '转换 docx'."
---

# Docx-to-Mermaid Converter

Convert raw PRD `.docx` files into AI-friendly Markdown + Mermaid diagrams for use in the openspec workflow.

## When to use

- **Step 0** of the openspec new-feature workflow (before `/opsx:explore`)
- Anytime the user has a `.docx` PRD that needs to become a readable `.md`

## Input

The user provides one or more `.docx` file paths. If they also specify a service name, use it for the output path. Otherwise infer from the file location or ask.

**Output convention**: `docs/<srv>/prd/<name>.md` with images in `docs/<srv>/prd/images/<name>/`

## Workflow

### 1. Extract text and images

Run the bundled extraction script (pure Python, no dependencies beyond stdlib):

```bash
python <skill-dir>/scripts/extract_docx.py "<docx_path>" "<image_output_dir>"
```

This prints paragraphs to stdout with `[IMAGE:<filename>]` markers where images appear in the document. Images are saved to `<image_output_dir>/`.

### 2. View every extracted image

**This step is critical.** Read each image file using the Read tool to visually inspect it. Classify each image:

| Type | Action |
|------|--------|
| **Flowchart / state diagram / sequence diagram** | Convert to mermaid, keep image link below |
| **Mind map / tree structure** | Convert to mermaid graph, keep image link below |
| **UI mockup / wireframe / screenshot** | Keep as image link only (not suitable for mermaid) |
| **Table / spreadsheet screenshot** | Convert to markdown table, keep image link below |
| **Decorative / logo** | Skip or keep as image link if referenced |

### 3. Rename images

Rename extracted images from generic names (`image1.png`) to semantic names that describe their content:

| Original | Renamed |
|----------|---------|
| `image1.png` | `version_history.png` |
| `image2.jpeg` | `flow_avatar_equip.jpeg` |
| `image3.jpeg` | `ui_main_mockup.jpeg` |

Use prefixes: `flow_` for flowcharts, `ui_` for mockups, `state_` for state diagrams, `seq_` for sequences, `map_` for mind maps, `table_` for table screenshots.

### 4. Write the markdown

Structure the markdown following these rules:

**Frontmatter**: Include title as H1, status line (`> 状态：已评审 | 版本：V1.0`), and change log table if present in docx.

**Diagram conversion pattern**: For each diagram image, place the mermaid block first, then the original image link below it:

```markdown
#### 4.7 头像佩戴流程图

\`\`\`mermaid
flowchart TD
    A([开始]) --> B[步骤一]
    B --> C{判断}
    C -- 是 --> D[结果A]
    C -- 否 --> E[结果B]
    D --> F([结束])
\`\`\`

![头像佩戴流程图](images/个人信息装扮/flow_avatar_equip.jpeg)
```

**UI mockup pattern**: Just the image link with a descriptive alt text:

```markdown
![头像交互界面](images/个人信息装扮/ui_avatar_mockups.jpeg)
```

**Image paths**: Use relative paths from the markdown file location: `images/<name>/<image_file>`

**Content fidelity rules**:
- Preserve ALL content from the docx — do not summarize or omit sections
- Preserve the original heading hierarchy and numbering
- Convert bullet points and numbered lists to markdown lists
- Convert tables to markdown tables
- Mark deprecated/abandoned content with `> 此方案已废弃` blockquotes rather than deleting it
- Preserve Chinese text as-is

### 5. Clean up

- Remove any previously extracted segmented images (`*_seg_*.jpeg`) if they exist from prior conversions
- Verify all image links in the markdown point to existing files

## Mermaid Conversion Tips

**Flowcharts**: Use `flowchart TD` for top-down flows. Use `([text])` for start/end nodes, `[text]` for process, `{text}` for decisions, `["text"]` for quoted text with special chars.

**State diagrams**: Use `stateDiagram-v2`. Map Chinese state names with underscores: `已解锁_未佩戴`.

**Mind maps / tree structures**: Use `graph LR` or `graph TD`. Keep node text concise.

**Escape special characters**: Wrap node text in quotes if it contains parentheses, brackets, or other mermaid-special characters.

## Example

Input: `docs/lobby/prd/个人信息装扮.docx`

Output:
- `docs/lobby/prd/个人信息装扮.md` — Full markdown with mermaid diagrams
- `docs/lobby/prd/images/个人信息装扮/` — Contains:
  - `version_history.png` — Change log table
  - `flow_avatar_equip.jpeg` — Avatar equip flowchart (→ mermaid + image)
  - `ui_avatar_mockups.jpeg` — UI wireframes (→ image only)
  - `flow_title_equip.jpeg` — Title equip flowchart (→ mermaid + image)
  - `ui_title_mockups.jpeg` — Title UI wireframes (→ image only)
