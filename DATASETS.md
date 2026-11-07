# 数据集发布清单（DATASETS）

## Releases

| Release | 内容 | 日期 |
|---|---|---|
| **corpus-v0.9（最新）** | 72,828 docs / 131.2M 字符 / **~34,914,423 tokens**；新增古典乐理/管弦配器 2.4M tokens | 2026-11-07 |
| corpus-v0.8 | 71,844 docs / ~32.52M tokens | 2026-11-07 |

下载最新版：

```bash
gh release download corpus-v0.9 -R ShokouP/open-music-production-corpus -D data
cd data && for f in *.gz; do gunzip -k "$f"; done
```

## v0.9 附件与校验和

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

## 文件用途

- `corpus_*.jsonl`：结构化语料（逐条 `source/license/url/text_sha256/group_key`）
- `cpt_*_text.jsonl`：CPT 训练格式（仅 `{"text": ...}`），直接接 HF Trainer / LLaMA-Factory
- `manifest.json`：计数、sha256、逐源统计（含 license/tier）
- `stats.md`：分布统计
- `ATTRIBUTIONS.md`：逐源署名与许可要求
- `licenses.tar.gz`：逐源许可原文（14 份）
- `MERGE-REPORT.md` / `ZHWIKI-REPORT.md` / `THEORY-REPORT.md`：合并、中文、古典乐理构建报告

## 版本历史

- v0.9：新增 gutenberg-theory（624 docs / ~1.83M tokens）、wikisource-grove（255 / ~0.44M）、open-music-theory（106 / ~0.13M）
- v0.8：全量中文维基 dump 扫描（1,459 docs）+ 19 源合并，32.52M tokens
- v0.7：中文维基首批清洗语料，32.08M tokens

## 商用白名单子集

完整语料含 CC BY-SA 内容；商用训练建议用 `license == permissive`（CC0/PD/MIT/ISC，约 680 万 tokens）过滤。

## lite 版（仓库内）

`cpt/data/` 提供 ~3M tokens 的 lite 语料（`corpus_{train,val}.jsonl` + manifest + stats）。
