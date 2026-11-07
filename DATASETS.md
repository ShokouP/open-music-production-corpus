# 数据集发布清单（DATASETS）

## Releases

| Release | 内容 | 大小 |
|---|---|---|
| **corpus-v0.8**（最新） | 71,844 docs / 121.6M 字符 / ~32.52M tokens（train 70,443 / val 1,401） | 见下方 |
| corpus-v0.7 | 71,627 docs / 120.7M 字符 / ~32.08M tokens | 见 v0.7 Release |

## v0.8 附件

- `corpus_train.jsonl.gz` / `corpus_val.jsonl.gz`：结构化语料
- `cpt_train_text.jsonl.gz` / `cpt_val_text.jsonl.gz`：CPT 训练格式
- `manifest.json.gz`：计数、sha256、逐源统计
- `stats.md.gz`：分布统计
- `ATTRIBUTIONS.md.gz`：逐源署名
- `licenses.tar.gz`：逐源许可原文
- `MERGE-REPORT.md.gz` / `ZHWIKI-REPORT.md.gz`：构建报告

## 下载

```bash
gh release download corpus-v0.8 -R ShokouP/open-music-production-corpus -D data
cd data && for f in *.gz; do gunzip -k "$f"; done
```

## 校验

```bash
sha256sum *.gz   # 与 Release 说明中的 checksum 对照
```

## 商用白名单子集

完整语料含 CC BY-SA 内容；商用训练建议：
1. 使用 `data-permissive`（仅 CC0/PD/MIT/ISC/BSD/Apache，约 9.5M tokens）；
2. 或在完整语料上过滤 `license_class == permissive` 的记录。

## lite 版（仓库内）

`cpt/data/` 提供 ~3M tokens 的 lite 语料（`corpus_{train,val}.jsonl` + manifest + stats），用于快速浏览和冒烟测试。
