# 3,250 万 tokens 免费开源！音乐制作 & 音频工程语料库 v0.8

> 做音乐 AI 的人都在找的「能直接训练、许可还干净」的中文+英文音乐领域语料——这次一口气放出来。

**32,520,758 tokens · 71,844 篇文档 · 19 个来源 · 逐源许可审计 · 纯 CPU 可复现 · 开箱即训（CPT / SFT）**

## 一句话介绍

这是一个**开放、逐源许可审计、可复现构建**的音乐制作 / 音频工程文本语料库：
混音、母带、EQ、压缩、混响、声学、乐理、DAW 工程格式、音频编程文档、中文维基音乐条目，全部整理成可直接喂给 Qwen/Llama 的训练格式。

- ✅ **免费开源**：代码 Apache-2.0 + 语料 CC BY-SA 4.0 / 公版 / MIT / ISC
- ✅ **许可干净**：19 个来源逐一声明，附 11 份开放文档的原始许可文本（`licenses.tar.gz`）
- ✅ **可商用路径**：另附 permissive 子集（CC0/PD/MIT/ISC，约 950 万 tokens），不用 SA 也能训
- ✅ **中文补齐**：中文维基全量 dump 扫描 + 清洗，中文 token 约占 12%
- ✅ **可复现**：`fetch → curate → build → merge → check` 全脚本，纯 Python/CPU，无 GPU 依赖
- ✅ **开箱可训**：`cpt_train_text.jsonl` 只有 `{"text": ...}`，直接接 HF Trainer

## 数据规模

| 指标 | 值 |
|---|---|
| 文档数 | **71,844**（train 70,443 / val 1,401） |
| 字符数 | **121,595,600** |
| 估算 tokens | **32,520,758** |
| 语言 | 英文 69,984 / 中文 1,459 / 中英混合 401 |
| 许可分类 | share-alike 65,861（CC BY-SA）/ permissive 5,983（CC0/PD/MIT/ISC） |
| 去重 | 移除 64,950 条重复；无重复、无同源跨集（group-aware split） |

## 里面有什么

- **Stack Exchange 官方转储**：sound / music / avp 三站全量问答（混音/母带/录音/EQ/压缩/乐理）
- **Project Gutenberg 公版书**：乐理/声学/乐器/歌唱类（精选 2,683 篇）
- **中文维基百科**：全量 dump 扫 160 万页，清洗后 1,459 篇音乐/音频条目
- **arXiv 摘要**：混音/源分离/响度/空间音频/效果器等方向
- **11 个开放文档仓库**：sfz、librosa、mido、pretty-midi、pyloudnorm、sounddevice、audioflux、pyroomacoustics、clap、windows-midi、Sonic Pi 教程（固定 commit + 许可证据）
- **DAWproject 规范**（MIT）与自建参数语义手册（CC0）

## 下载与校验

```bash
gh release download corpus-v0.8 -R ShokouP/open-music-production-corpus -D data
cd data && for f in *.gz; do gunzip -k "$f"; done
```

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

## 怎么用

**CPT（继续预训练）**
```python
from datasets import load_dataset
ds = load_dataset("json", data_files="cpt_train_text.jsonl", split="train")
# 接 Qwen/Llama Trainer，seq 1024–2048，domain:general replay ≈ 1:0.1–0.3
```

**SFT / 评测**：结构化的 `corpus_train.jsonl` 保留 `source/license/url/text_sha256/group_key`，方便按来源/许可采样与切分。

**商用**：用 permissive 子集，或在完整语料上过滤 `license_class == permissive`。

## 许可

- 代码：Apache-2.0；自建手册：CC0
- 语料：整体按 **CC BY-SA 4.0** 分发（Stack Exchange / Wikipedia / Sonic Pi 教程），另有公版与 MIT/ISC 部分
- 逐源署名与要求见 `ATTRIBUTIONS.md` / `licenses.tar.gz`
- 受版权内容（REAPER/FL Studio 手册）**不在**语料中

## 谁在用

本语料是 **DAWcoder** 预览版（音乐制作参数模型）的 CPT 语料；与具体模型解耦，任何音乐/音频方向 LLM 都能直接用。

## 已知限制（不吹牛）

- 中文 ~12%，以音乐领域文本为主，现代 DAW 操作细节不足（手册有版权）
- 中文维基已全量扫完（160 万页），继续扩中文需要教科书/授权教材
- 不含真实工程参数与音频（这是另一类数据）
- wikitext 清洗为启发式，少量残缺句；问答体建议与教材类 1:1 混用
