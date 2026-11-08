# Open Music Production & Audio Engineering Corpus (OMPAC)

[![GitHub stars](https://img.shields.io/github/stars/ShokouP/open-music-production-corpus?style=social)](https://github.com/ShokouP/open-music-production-corpus)
[![Data v1.0](https://img.shields.io/badge/data-v1.0%20%C2%B7%2037.1M%20tokens-blue)](https://github.com/ShokouP/open-music-production-corpus/releases/tag/corpus-v1.0)
[![License](https://img.shields.io/badge/license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)

> 如果这个语料库对你有用，欢迎点个 Star，让更多做音乐 AI 的人找到它。

一个**开放、逐源许可审计、可复现构建**的音乐制作 / 音频工程文本语料库，面向小模型继续预训练（CPT）、指令微调与评测。

- 当前版本：**v1.0** — 73,586 docs / 140,026,215 字符 / **~37,127,816 tokens**
- 语言：英文 70,968 docs / 中文 1,459 docs / 中英混合 401 docs（中文 token ≈12%）
- 源：23 个（Stack Exchange 官方转储、theory-deep 和声/对位/乐器法/总谱分析公版教材、Grove 音乐词典、Open Music Theory、Project Gutenberg 音乐公版书、中文维基百科、arXiv 摘要、11 个开放文档仓库、DAWproject 规范、自建参数语义手册）
- 许可：CC BY-SA 4.0 为主 + 公版 + MIT/ISC/CC0；**逐源署名与许可证据**在 `cpt/licenses/` 与 `docs/ATTRIBUTIONS.md`
- 构建：纯 Python/CPU，全流程脚本在 `cpt/`，可从公开源复现

> 这是**第一次系统整理并单独发布**的语料库。它同时是 DAWcoder 预览版模型的训练语料，但与具体模型解耦：任何音乐/音频方向的 LLM 训练、评测、研究都可以直接使用。

## 生态（相关项目）

| 项目 | 内容 |
|---|---|
| **open-music-production-corpus**（本仓库） | 3,713 万 tokens 文本 CPT 语料（23 源，含和声/对位/乐器法/总谱分析） |
| [open-music-engineering-data](https://github.com/ShokouP/open-music-engineering-data) | 10,208 鼓 Pattern / 30,336 结构边界 / DAWproject 规范 / 参数样本 |
| [daw-mcp-server](https://github.com/ShokouP/daw-mcp-server) | 11 个 MCP tools：DAW 自动化、渲染、WAV 指标、闭环验证（REAPER/FL/DAWproject） |

## 数据下载

完整语料通过 GitHub Release 发布（仓库内仅保留 lite 版，避免超过 Git 限制）：

**Release：** https://github.com/ShokouP/open-music-production-corpus/releases

```bash
gh release download corpus-v1.0 -R ShokouP/open-music-production-corpus -D data
cd data && for f in *.gz; do gunzip -k "$f"; done
```

| 文件 | 用途 |
|---|---|
| `corpus_train.jsonl` / `corpus_val.jsonl` | 结构化语料（逐条 source/license/url/text_sha256/group_key） |
| `cpt_train_text.jsonl` / `cpt_val_text.jsonl` | CPT 训练格式（仅 `{"text": ...}`，可直接喂 HF Trainer） |
| `manifest.json` / `stats.md` / `ATTRIBUTIONS.md` | 统计、sha256、逐源署名 |
| `licenses.tar.gz` | 逐源原始许可文本（证据） |
| `MERGE-REPORT.md` / `ZHWIKI-REPORT.md` / `THEORY-REPORT.md` | 合并、中文、古典理论语料构建报告 |

仓库内 `cpt/data/` 还有一份 **lite 语料**（~3M tokens），可直接浏览与冒烟测试。

## 构成（v1.0）

| 源 | 许可 | 内容 |
|---|---|---|
| stackexchange-sound / music / avp | CC BY-SA 4.0 | 混音/母带/录音/EQ/压缩/乐理问答（官方数据转储） |
| gutenberg-music | 公版 | 乐理/声学/乐器/歌唱类公版书（精选） |
| **theory-deep** | 公版 | **和声学/对位法/乐器法/配器法/总谱分析教材（1,382 docs，含 Prout、Ouseley、Cherubini、Kitson、Berlioz、Widor、Gevaert、Coerne、Goetschius 等）** |
| **wikisource-grove** | 公版 | **Grove《A Dictionary of Music and Musicians》配器/乐器法/和声/对位条目（255 docs）** |
| **open-music-theory** | CC BY-SA 4.0 | **Open Music Theory 教材章节（106 docs）** |
| zh-wikipedia-dump | CC BY-SA 4.0 | 中文维基音乐/音频条目（1,459 docs，含乐理/乐器/录音/音频技术） |
| zh-wikipedia-audio | CC BY-SA 4.0 | 中文维基音频术语条目 |
| arxiv-audio | CC0（元数据） | 混音/分离/响度/空间音频等论文摘要 |
| 开放文档 ×11 | MIT / ISC / CC0 | sfz / librosa / mido / pretty-midi / pyloudnorm / sounddevice / audioflux / pyroomacoustics / clap / windows-midi / sonic-pi 教程 |
| dawproject-spec | MIT | DAWproject 开放工程格式规范 |
| dawcoder-ir-handbook | CC0 | 自建：参数语义与任务示例手册 |

## 许可与使用边界

- **公开/研究/非商用与 SA 兼容场景**：直接使用完整语料（按 CC BY-SA 4.0 分发，保留署名）。
- **商用训练**：使用 permissive 子集（仅 CC0 / Public-Domain / MIT / ISC / BSD / Apache，约 760 万 tokens），或在完整语料上按 `license_class=permissive` 过滤。
- 受版权内容（REAPER/FL Studio 手册等）**不在**本语料中。
- 逐源许可原文：`cpt/licenses/`；每篇语料保留 `source`/`license`/`url` 字段与 `ATTRIBUTIONS.md` 署名。

## 复现构建

```bash
pip install -r cpt/requirements.txt

# 1) Stack Exchange 官方转储（sound/music/avp）
python cpt/fetch_se_dumps.py --site all

# 2) 公版书 / arXiv / DAWproject / 中文维基条目
python cpt/fetch.py --source gutenberg-music
python cpt/fetch.py --source arxiv-audio
python cpt/fetch.py --source dawproject-spec
python cpt/fetch.py --source zh-wikipedia-audio

# 3) 中文维基 dump（约 3.45GB；下载后解析 + 清洗）
python cpt/fetch_zhwiki_dump.py --max-pages 1600000 --max-chars 60000000
python cpt/clean_zhwiki_raw.py
python cpt/zhwiki_to_corpus.py

# 4) 开放文档（11 个仓库，固定 commit）
python cpt/collect_open_docs.py --source all

# 5) 清洗 / 合并 / 校验
python cpt/curate.py
python cpt/merge_corpora.py --inputs <zhwiki-corpus> cpt/data-expanded cpt/data-curated cpt/data-permissive --out <out>
python cpt/check.py --data <out>
python cpt/make_cpt_text.py <out>
```

各脚本顶部的 docstring 有详细说明；`docs/MERGE-REPORT-v0.8.md` 记录合并细节与去重统计。

## 已知限制

- 中文 token 占比约 12%，以音乐领域文本为主，现代 DAW 操作细节不足（手册受版权限制）；
- 中文维基全量 dump 已扫完（160 万页），相关条目已基本取尽，继续扩中文需要其他来源（教科书/授权教材）；
- 语料为通用音乐领域文本，不含真实工程参数/音频数据（那是另一类数据）；
- wikitext 清洗为启发式，仍可能有少量残缺句；
- Stack Exchange 为问答体，建议与教材/文档类按 1:1 配比使用。

## 许可

- 代码（`cpt/*.py`）：Apache-2.0（见 `LICENSE`）
- 自建语料/手册：CC0-1.0
- 第三方语料：按来源许可（CC BY-SA 4.0 / 公版 / MIT / ISC），整体按 CC BY-SA 4.0 分发
- 引用：如果使用本语料，请引用本仓库与 `docs/ATTRIBUTIONS.md` 中的逐源出处。

## DAWcoder 模型

基于本语料训练的音乐制作参数模型（4B，Qwen3.5-4B 基座，GGUF Q4_K_M）：
- Hugging Face：https://huggingface.co/Shokou1/dawcoder
- GitHub：https://github.com/ShokouP/dawcoder
