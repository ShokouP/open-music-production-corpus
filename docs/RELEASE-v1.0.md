# 3,710 万 tokens 音乐制作 & 音频工程语料 v1.0 — 新增和声/对位/乐器法/总谱分析 460 万 tokens

> 做音乐 AI 最缺的不是"音乐知识"，而是**系统性的和声学、对位法、乐器法与总谱分析**。
> v1.0 一次补了 65 本公版教材（和声学、对位法、配器法、音乐分析），语料涨到 **3,713 万 tokens**。

[![GitHub stars](https://img.shields.io/github/stars/ShokouP/open-music-production-corpus?style=social)](https://github.com/ShokouP/open-music-production-corpus)

**37,127,816 tokens · 73,586 篇文档 · 23 个来源 · 逐源许可审计 · 纯 CPU 可复现 · 开箱即训（CPT / SFT）**

如果这个语料库对你有用，欢迎给仓库点个 Star，让更多做音乐 AI 的人找到它。

## 本版新增（v1.0 vs v0.9）：theory-deep 深度理论来源

| 新增 | 许可 | 文档 | 估算 tokens | 内容 |
|---|---|---|---|---|
| **theory-deep** | 公版 | **1,382** | **~4.04M** | 和声学、对位法、乐器法、配器法、总谱分析/音乐分析教材（Gutenberg 书籍 + Internet Archive 公版扫描本） |

代表书目：Prout《Harmony》《Instrumentation》《The Orchestra》、Ouseley《A Treatise on Harmony》、Cherubini《A Treatise on Counterpoint and Fugue》、Kitson《The Art of Counterpoint》、Berlioz《A Treatise upon Modern Instrumentation and Orchestration》、Widor《Technique de l'orchestre moderne》、Gevaert《Traité général d'instrumentation》、Coerne《Evolution of Modern Orchestration》、Goetschius 系列等。

## 全量规模

| 指标 | 值 |
|---|---|
| 文档数 | **73,586**（train 72,080 / val 1,506） |
| 字符数 | **140,026,215** |
| 估算 tokens | **37,127,816** |
| 语言 | 英文 71,726 / 中文 1,459 / 中英混合 401 |
| 许可 | share-alike 65,967 / permissive 7,619（CC0/PD/MIT/ISC） |
| 去重 | 移除 64,951 条；无重复、无同源跨集 |

## 下载与校验

```bash
gh release download corpus-v1.0 -R ShokouP/open-music-production-corpus -D data
cd data && for f in *.gz; do gunzip -k "$f"; done
```

| 文件 | 大小 | sha256 |
|---|---|---|
| corpus_train.jsonl.gz | 63.9 MB | `770a9e01bc194a942fefb1a18270d84b36fe79a3267ad3b441cbdbb1c8a0a062` |
| corpus_val.jsonl.gz | 1.6 MB | `4b415fbe90ea5fdc62ca449406b927329aff20902727c82a0353dbd951ca4407` |
| cpt_train_text.jsonl.gz | 56.5 MB | `8c17402dabe14927b782cbe5124c24908f6a8e06514ced075904870948d77ef9` |
| cpt_val_text.jsonl.gz | 1.4 MB | `83529f2bceceb9fbb55b9d1904e24195428b818e9e1491aef9904a5dd1362d9f` |
| manifest.json.gz | 1.6 KB | `dad80a8c8da9e4f9660c30d13226010cff7044119d78bcd2d088dc330e9f7b2e` |
| stats.md.gz | 1.1 KB | `38eb64d831542ad527f3086924da3cf846c96bf959e3c60d59bf316534d7ad59` |
| ATTRIBUTIONS.md.gz | 1.8 KB | `2e81543898f6b705ab5590884453807f1b5ab58d641a86a7e927f0aeb7c34153` |
| MERGE-REPORT.md.gz | 1.3 KB | `1f97f40e74d9de43afdaf7250cf4f22aa90f2bf78b70144df83ecc1c9caf649c` |
| ZHWIKI-REPORT.md.gz | 2.0 KB | `d957e6333fca3d77511de46332832a86aaf49e867cef8c7a4fe19f76d16e5744` |
| THEORY-REPORT.md.gz | 1.2 KB | `a22046f2af613bdd2ec22b5e89c316e5765b083c40b870ab935d6894e8a7c917` |
| licenses.tar.gz | 6.1 KB | `d031c017f9a48cb49098badf20155350a50f5536ae1f74f191ea9ce333bdbfae` |

## 里面有什么（23 源）

- **theory-deep**：和声学 / 对位法 / 乐器法 / 配器法 / 总谱分析公版教材（本版新增，~4.04M tokens）
- **wikisource-grove**：Grove 音乐词典配器/乐器法/和声/对位条目
- **open-music-theory**：Open Music Theory 教材章节
- **Stack Exchange**（sound/music/avp 官方转储）：混音/母带/录音/EQ/压缩/乐理问答
- **Gutenberg 音乐公版书**、**中文维基百科**（1,459 篇音乐/音频条目）、**arXiv 摘要**
- **11 个开放文档仓库**（sfz/librosa/mido/pretty-midi/pyloudnorm/sounddevice/audioflux/pyroomacoustics/clap/windows-midi/Sonic Pi）
- **DAWproject 规范**（MIT）+ 自建参数语义手册（CC0）

## 用法

- **CPT**：`cpt_train_text.jsonl`（仅 `{"text": ...}`）直接接 HF Trainer；domain:general replay ≈ 1:0.1–0.3
- **SFT / 评测**：结构化 `corpus_*.jsonl` 保留 `source/license/url/text_sha256/group_key`
- **商用**：permissive 子集（约 760 万 tokens，CC0/PD/MIT/ISC），或按 `license` 过滤

## 许可

代码 Apache-2.0；语料整体 CC BY-SA 4.0 + 公版 + MIT/ISC/CC0；逐源署名与许可原文见 `ATTRIBUTIONS.md` / `licenses.tar.gz`。

## 已知限制

- 公版理论教材多为 19 世纪–20 世纪初，体系完整但术语与现代 DAW 有代差；
- Internet Archive OCR 有少量识别噪声；
- 中文仍约 12%，和声/配器中文教材缺（需授权教材）；
- 不含真实工程参数与音频数据（工程数据另发布）。
