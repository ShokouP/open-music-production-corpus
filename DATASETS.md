# 数据集发布清单（DATASETS）

## Releases

| Release | 内容 | 日期 |
|---|---|---|
| **corpus-v1.0（最新）** | 73,586 docs / 140.0M 字符 / **~37,127,816 tokens**；新增 theory-deep 和声/对位/乐器法/总谱分析教材 ~4.04M tokens | 2026-11-07 |
| corpus-v0.9 | 72,828 docs / ~34.91M tokens（古典乐理/配器首批） | 2026-11-07 |
| corpus-v0.8 | 71,844 docs / ~32.52M tokens | 2026-11-07 |

下载最新版：

```bash
gh release download corpus-v1.0 -R ShokouP/open-music-production-corpus -D data
cd data && for f in *.gz; do gunzip -k "$f"; done
```

## v1.0 附件与校验和

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

## 文件用途

- `corpus_*.jsonl`：结构化语料（逐条 `source/license/url/text_sha256/group_key`）
- `cpt_*_text.jsonl`：CPT 训练格式（仅 `{"text": ...}`），直接接 HF Trainer / LLaMA-Factory
- `manifest.json`：计数、sha256、逐源统计（含 license/tier）
- `stats.md`：分布统计
- `ATTRIBUTIONS.md`：逐源署名与许可要求
- `licenses.tar.gz`：逐源许可原文（16 份）
- `MERGE-REPORT.md` / `ZHWIKI-REPORT.md` / `THEORY-REPORT.md`：合并、中文、古典理论构建报告

## 版本历史

- **v1.0**：新增 theory-deep（和声/对位/乐器法/配器/总谱分析，1,382 docs / ~4.04M tokens），23 源，37.13M tokens
- v0.9：新增 Grove 词典 + Gutenberg 理论书 + Open Music Theory（~2.4M tokens）
- v0.8：全量中文维基 dump（1,459 docs）+ 19 源合并，32.52M tokens

## 商用白名单子集

完整语料含 CC BY-SA 内容；商用训练建议用 `license == permissive`（CC0/PD/MIT/ISC，约 760 万 tokens）过滤。

## lite 版（仓库内）

`cpt/data/` 提供 ~3M tokens 的 lite 语料（`corpus_{train,val}.jsonl` + manifest + stats）。
