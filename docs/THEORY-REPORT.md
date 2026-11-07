# 古典乐理 / 管弦配器语料采集报告（v0.9 新增）

## 新增来源

| 源 | 许可 | 文档 | 估算 tokens | 内容 |
|---|---|---|---|---|
| gutenberg-theory | 公版（Project Gutenberg） | 624 | ~1.83M | 乐理/和声/对位/配器/指挥/总谱阅读类公版书（按 3k–12k 字符分块） |
| wikisource-grove | 公版（Wikisource） | 255 | ~0.44M | 《A Dictionary of Music and Musicians》（Grove 1900）中的配器、乐器法、和声、对位、指挥、总谱等条目 |
| open-music-theory | CC BY-SA 4.0 | 106 | ~0.13M | Open Music Theory 教材章节（和声、曲式、配器基础） |

合计 **+2.4M tokens**，合并后语料 **72,828 docs / 131.17M 字符 / 34.91M tokens**。

## 采集方式

- `cpt/fetch_theory.py`
  - Wikisource Grove：枚举 `A Dictionary of Music and Musicians/` 全部 4,000 条目，按理论/乐器/配器关键词筛选 203 条，用 `action=parse` 渲染（解决条目正文是 transclusion 的问题）；
  - Open Music Theory：抓取 `contents.html` 章节链接后逐章清洗 HTML；
  - Gutenberg：按 Subjects 严格筛选（music theory / harmony / counterpoint / orchestration / instrumentation / score reading / conducting 等），排除小说/诗歌/歌剧脚本。
- `cpt/theory_to_corpus.py`：长书分块、去重、按 `group_key=<source>:<title>` 分组切分。

## 质量与限制

- 公版书多为 19 世纪–20 世纪初教材（如配器法、和声学），术语与现代 DAW 有代差，但对**古典乐理/管弦配器**是高质量系统材料；
- Grove 词典条目经过 HTML 清洗，仍可能有目录/边栏残留；
- Open Music Theory 章节数量有限（站点结构简单）；
- 未纳入 Internet Archive 扫描本（版权状态不明确），也未纳入受版权保护的现代配器教材。
