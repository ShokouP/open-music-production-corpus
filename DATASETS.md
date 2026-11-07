# 数据集发布清单（DATASETS）

## Releases

| Release | 内容 | 日期 |
|---|---|---|
| **corpus-v0.8（最新）** | 71,844 docs / 121.6M 字符 / **~32,520,758 tokens**（train 70,443 / val 1,401） | 2026-11-07 |
| corpus-v0.7（旧，已合并进 v0.8） | 71,627 docs / 120.7M 字符 / ~32.08M tokens | 2026-11-07 |

下载：

```bash
gh release download corpus-v0.8 -R ShokouP/open-music-production-corpus -D data
cd data && for f in *.gz; do gunzip -k "$f"; done
```

## v0.8 附件与校验和

| 文件 | 大小 | sha256 |
|---|---|---|
| corpus_train.jsonl.gz | 57.5 MB | `132f1d2b0107b37fe6be09b9f090dac7bce6beed8cca35a5c32f94f5183c4767` |
| corpus_val.jsonl.gz | 1.1 MB | `9bfd85703e586a68922532ccf8d4ee37a69064705a43325fc2dfbcdf05c3b7ee` |
| cpt_train_text.jsonl.gz | 50.3 MB | `4cd656020068fee5f39e32cf8a1bfc29ae04c917307ae95faecb749731bcf09e` |
| cpt_val_text.jsonl.gz | 0.9 MB | `0860860555ee8c1b44bcd192180bf56e88fcdeb3529156e42b09e13ecf9db4da` |
| manifest.json.gz | 1.5 KB | `e0979baada96ed45f7ef08261ba9c1e037c6f378b7839f032faf11c5f3b2debf` |
| stats.md.gz | 1.1 KB | `27263425eaeddaed45d757c6c6ba0e82c4ce43b81550a07d04dc803ae82c7f5f` |
| ATTRIBUTIONS.md.gz | 1.8 KB | `b971203f3801064663868de7a0b09f423482c0f95f8ac69ba73c6d9767cfd1cc` |
| MERGE-REPORT.md.gz | 1.2 KB | `08031990740ad3377af7676b1bc6f0a64c36fc7b93af3853a70dfb618abb342c` |
| ZHWIKI-REPORT.md.gz | 2.0 KB | `1c7c61676380701d4506b8a58603d8101c889b8b029e03aa6828f67be3f1f350` |
| licenses.tar.gz | 5.3 KB | `9929a755ad5d6bb133f7a6484f13e929affb5cb8de92543aa93b3951b7aef521` |

## 文件用途

- `corpus_*.jsonl`：结构化语料（逐条 `source/license/url/text_sha256/group_key`），适合按来源/许可采样
- `cpt_*_text.jsonl`：CPT 训练格式（仅 `{"text": ...}`），直接接 HF Trainer / LLaMA-Factory
- `manifest.json`：计数、sha256、逐源统计（含 license/tier）
- `stats.md`：分布统计
- `ATTRIBUTIONS.md`：逐源署名与许可要求
- `licenses.tar.gz`：11 个开放文档仓库的原始许可文本
- `MERGE-REPORT.md` / `ZHWIKI-REPORT.md`：合并与中文构建报告

## 商用白名单子集

完整语料含 CC BY-SA 内容；商用训练建议：
1. 使用 permissive 子集（仅 CC0/PD/MIT/ISC/BSD/Apache，约 9.5M tokens，可用 `license_class == permissive` 从结构化语料过滤）；
2. 或在完整语料上按 `license` 字段过滤。

## lite 版（仓库内）

`cpt/data/` 提供 ~3M tokens 的 lite 语料（`corpus_{train,val}.jsonl` + manifest + stats），用于快速浏览和冒烟测试。
