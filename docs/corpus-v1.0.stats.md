# 合并语料统计

- 语料版本：`open-music-corpus-v1.0`
- 输入：theory-corpus-v1.0, zhwiki-corpus-v3, data-expanded, data-curated, data-permissive
- 文档数：**73,586**（train 72,080 / val 1,506）
- 字符数：**140,026,215**；估算 tokens：**37,127,816**
- 语言分布：中文 1459 / 英文 71726 / 中英混合 401
- 许可分类：{'share-alike': 65967, 'permissive': 7619}
- 去重：移除重复 64,951 条（按 text_sha256）
- 长度分位：p50 939 / p90 3,555 / p99 11,997

| 源 | 文档 | 字符 | 估算 tokens | 许可 |
|---|---:|---:|---:|---|
| arxiv-audio | 1169 | 1,405,757 | 351,004 | CC0-1.0 |
| audioflux-docs | 186 | 244,774 | 61,162 | MIT |
| clap-docs | 1 | 8,588 | 2,147 | MIT |
| dawcoder-ir-handbook | 617 | 862,365 | 237,322 | CC0-1.0 |
| dawproject-spec | 2 | 59,924 | 14,981 | MIT |
| gutenberg-music | 2682 | 32,024,093 | 8,005,047 | Public-Domain |
| librosa-docs | 295 | 563,246 | 140,693 | ISC |
| mido-docs | 16 | 8,679 | 2,164 | MIT |
| open-music-theory | 106 | 520,939 | 130,245 | CC-BY-SA-4.0 |
| pretty-midi-docs | 37 | 26,382 | 6,584 | MIT |
| pyloudnorm-docs | 7 | 8,647 | 2,159 | MIT |
| pyroomacoustics-docs | 243 | 254,210 | 63,460 | MIT |
| sfz-format-docs | 222 | 435,977 | 108,913 | CC0-1.0 |
| sonic-pi-tutorial | 90 | 341,376 | 90,429 | CC-BY-SA-4.0 |
| sounddevice-docs | 5 | 13,466 | 3,365 | MIT |
| stackexchange-avp | 12645 | 14,089,846 | 3,517,761 | CC-BY-SA-4.0 |
| stackexchange-music | 30821 | 41,185,035 | 10,284,739 | CC-BY-SA-4.0 |
| stackexchange-sound | 20762 | 20,206,646 | 5,043,929 | CC-BY-SA-4.0 |
| theory-deep | 1382 | 16,180,748 | 4,044,673 | Public-Domain |
| wikisource-grove | 255 | 1,740,926 | 435,139 | Public-Domain |
| windows-midi-docs | 500 | 2,070,491 | 517,444 | MIT |
| zh-wikipedia-audio | 32 | 101,989 | 47,727 | CC-BY-SA-4.0 |
| zh-wikipedia-dump | 1511 | 7,672,111 | 4,016,729 | CC-BY-SA-4.0 |

> tokens 为字符估算（CJK/1.6 + 其他/4），训练前请用 Qwen 分词器实测。
