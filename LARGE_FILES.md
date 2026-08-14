# LARGE_FILES.md — 大文件清单

仓库 `.git` 从约 48MB 瘦身至约 18MB（2026-08-14 用 `git filter-repo` 重写历史，两个大 PDF 已从全部历史中清除）。

## 已从历史中清除（本次重写）

| 文件 | 大小 | 说明 |
|---|---|---|
| `0_大佬的刷题指南.pdf` | 27 MB | 从全部历史清除（含提交 `7cf5320` 引入的 blob） |
| `2025-autumn/5.4-training-framework/5.4 训练框架.pdf`（原 `2025秋/5.4 训练框架/5.4 训练框架.pdf`） | 9.9 MB | 从全部历史清除；本地工作树仍保留该文件，已被 `.gitignore`（`*.pdf`）忽略，不再入库 |

> 注意：历史重写后**所有提交哈希均已变更**，旧克隆需重新拉取；远程已 force push 覆盖。

## 仍在仓库中的大文件（> 500KB）

| 文件 | 大小 |
|---|---|
| `2024-spring-intern-algorithms/Microsoft-intern/test.ipynb` | 2.5 MB |
| `2024-spring-intern-algorithms/Microsoft-intern/correlation_heatmap.png` | 1.9 MB |
| `2025-spring-intern-review/transformer-basics/grpo-from-scratch/image/rl-grpo-ppo-critic-actor/1740660712222.png` | 1.5 MB |
| `2025-autumn/5.4-training-framework/images/image-5.png` | 849 KB |
| `tmp6278.png` | 813 KB |
| `2025-autumn/5.4-training-framework/images/image-38.png` | 798 KB |
| `2025-autumn/5.4-training-framework/images/image-24.png` | 585 KB |

## 未来避免

- `.gitignore` 已包含 `*.pdf` / `*.gif`（只对未跟踪文件生效；已跟踪文件需显式 `git rm --cached`）。
- 超过 1MB 的图片建议压缩后入库，或使用 Git LFS。
- 备份：重写前的完整历史保存在本机 `/tmp/AF-backup`（如需恢复原始历史）。
