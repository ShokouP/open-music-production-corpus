# 3,490 万 tokens 音乐制作 & 音频工程语料 v0.9 — 新增古典乐理 / 管弦配器 240 万 tokens

> 这次把「古典乐理 + 管弦配器」补进来了：Grove 音乐词典、公版配器/和声教材、Open Music Theory 教材章节。
> 语料从 3,252 万 tokens 涨到 **3,491 万 tokens**，全部开源、逐源许可审计、纯 CPU 可复现。

**34,914,423 tokens · 72,828 篇文档 · 22 个来源 · 开箱即训（CPT / SFT）**

## 本版新增（v0.9 vs v0.8）

| 新增来源 | 许可 | 文档 | 估算 tokens | 内容 |
|---|---|---|---|---|
| gutenberg-theory | 公版 | 624 | ~1.83M | 乐理/和声/对位/配器/指挥/总谱阅读类公版书 |
| wikisource-grove | 公版 | 255 | ~0.44M | Grove《A Dictionary of Music and Musicians》配器/乐器法/和声/对位条目 |
| open-music-theory | CC BY-SA 4.0 | 106 | ~0.13M | Open Music Theory 教材章节（和声/曲式/配器基础） |

合计 **+2.4M tokens**，合并后去重 64,951 条，无同源跨集。

## 全量规模

| 指标 | 值 |
|---|---|
| 文档数 | **72,828**（train 71,422 / val 1,406） |
| 字符数 | **131,171,491** |
| 估算 tokens | **34,914,423** |
| 语言 | 英文 70,968 / 中文 1,459 / 中英混合 401 |
| 许可 | share-alike 65,967 / permissive 6,861（CC0/PD/MIT/ISC） |

## 下载与校验

```bash
gh release download corpus-v0.9 -R ShokouP/open-music-production-corpus -D data
cd data && for f in *.gz; do gunzip -k "$f"; done
```

| 文件 | 大小 | sha256 |
|---|---|---|
| corpus_train.jsonl.gz | 61.1 MB | `8f85a68335f7b9e7e34d91e38237a5000b90996e64361307420e0a9cb2f17639` |
| corpus_val.jsonl.gz | 1.1 MB | `f54f44b1da5219982cb1534cd6f910cc4f476b0b2d64df234db26abc87b73efa` |
| cpt_train_text.jsonl.gz | 53.8 MB | `1f43ee6970c662973209e2197e12b68937ae1980862879abd68d2093f5310730` |
| cpt_val_text.jsonl.gz | 0.9 MB | `e51ba887270a2d1b57bfd781aa65f43d74ef09c373ed644fd493c44537288271` |
| manifest.json.gz | 1.6 KB | `e1d182d8b6b6bbd3633f0740c790d538180a359d3cc6849e13a1ae0a517d9197` |
| stats.md.gz | 1.1 KB | `1d7485aa3a1c6b28a045d86211c61cb9586392c7ab473c11b4843f8d8f90d114` |
| ATTRIBUTIONS.md.gz | 1.8 KB | `bc5e65ebf656acca2355237a6de3a6108d1cef449615da547a27a67f2de54388` |
| MERGE-REPORT.md.gz | 1.3 KB | `ba584c7d7eaa6e376f7954ba75651bcdcaf17d937d9e32b59425d6b48f945a62` |
| ZHWIKI-REPORT.md.gz | 2.0 KB | `516e469f55d7e33a7b44f5672088d0f969686749f0ab8c61f462cfdad2d73e1a` |
| THEORY-REPORT.md.gz | 1.2 KB | `11aaced3b67dbafe797613090541a7e08085541e45a6d7053be37f39fc65d3cc` |
| licenses.tar.gz | 5.8 KB | `e5143cbe590071fcb9ad593adc1afb6036c0116a9d08f97de27a13d5861f3393` |

## 用法

- **CPT**：`cpt_train_text.jsonl`（仅 `{"text": ...}`）直接接 HF Trainer；domain:general replay ≈ 1:0.1–0.3
- **SFT/评测**：结构化 `corpus_*.jsonl` 保留 `source/license/url/text_sha256/group_key`
- **商用**：permissive 子集（约 680 万 tokens，CC0/PD/MIT/ISC），或按 `license` 过滤

## 许可

代码 Apache-2.0；语料整体 CC BY-SA 4.0 + 公版 + MIT/ISC/CC0；逐源署名与许可原文见 `ATTRIBUTIONS.md` / `licenses.tar.gz`。

## 已知限制

- 公版教材多为 19 世纪–20 世纪初，术语与现代 DAW 有代差（但古典乐理/配器体系完整）
- 中文仍约 12%（1,459 docs），现代 DAW 操作细节不足
- 不含真实工程参数与音频数据
- wikitext/HTML 清洗为启发式，少量残缺句
