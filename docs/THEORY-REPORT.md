# 古典乐理 / 管弦配器语料报告（v0.9 → v1.0）

## 新增来源（v1.0：theory-deep）

| 源 | 许可 | 文档 | 估算 tokens | 内容 |
|---|---|---|---|---|
| theory-deep | 公版 | **1,382** | **~4.04M** | 和声学、对位法、乐器法、配器法、总谱分析/音乐分析教材（Gutenberg 书籍 + Internet Archive 公版扫描本，OCR 清洗后按 3k–12k 字符分块） |
| wikisource-grove | 公版 | 255 | ~0.44M | Grove《A Dictionary of Music and Musicians》配器/乐器法/和声/对位条目 |
| open-music-theory | CC BY-SA 4.0 | 106 | ~0.13M | Open Music Theory 教材章节 |

合计 **~4.61M tokens**（v0.9 为 ~2.4M），合并后语料 **73,586 docs / 140.03M 字符 / 37.13M tokens**。

## 采集方式

- `cpt/fetch_theory_deep.py`
  - Project Gutenberg：按 Subjects/Title 匹配 harmony / counterpoint / fugue / instrumentation / orchestration / score reading / musical analysis / appreciation 等主题，排除小说/诗歌/剧本；
  - Internet Archive：多组 advancedsearch 查询（和声、对位、乐器法、配器、总谱分析），逐本检查 `possible-copyright-status == NOT_IN_COPYRIGHT`（或显式公有领域许可）后下载 `_djvu.txt`，做 OCR 清洗（去页眉页脚/页码/form feed）。
- `cpt/clean_theory_deep.py`：标题/正文相关性过滤（去 gospel/小说/传记等噪声）、同书去重、≤10k 字符丢弃。
- `cpt/theory_to_corpus.py`：分块、文本去重、按 `group_key=<source>:<title>` 分组切分。

## 代表书目（示例）

- 和声学：Prout *Harmony: Its Theory and Practice*、Ouseley *A Treatise on Harmony*、Day *A Treatise on Harmony*、Clarke、Pole、C. P. E. Bach 相关论述、Goetschius 系列；
- 对位法：Cherubini *A Treatise on Counterpoint and Fugue*、Ouseley、Kitson *The Art of Counterpoint*、Bernu、Hamer *A Course of Counterpoint*；
- 乐器法/配器：Prout *Instrumentation*、*The Orchestra*、Berlioz *A Treatise upon Modern Instrumentation and Orchestration*、Widor *Technique de l'orchestre moderne*、Gevaert *Traité général d'instrumentation*、Coerne *Evolution of Modern Orchestration*、Kling 配器法、Strauss 相关；
- 总谱分析/音乐分析：Prout *Musical Form*、score reading 类、musical analysis 类。

## 质量与限制

- 公版书多为 19 世纪–20 世纪初教材，体系完整（和声学/对位学/配器法正是那个时代的成熟学科），但与现代 DAW 术语有代差；
- IA OCR 仍有少量识别噪声（如旧式谱例字符），已做基本清洗；
- 未纳入 1929 年后的现代教材（版权原因）；
- 中文和声/配器教材仍缺（后续需授权中文教材）。
