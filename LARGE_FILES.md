# LARGE_FILES.md — 大文件清单

仓库 `.git` 约 48MB，克隆缓慢的主要原因是历史中的大文件。本文件记录现状与建议。

## 已从工作树删除（仍在 git 历史中）

| 文件 | 大小 | 说明 |
|---|---|---|
| `0_大佬的刷题指南.pdf` | 27 MB | 曾于提交 `7cf5320` 入库；已从工作树删除并随本次整理提交删除。**blob 仍在历史中**，.git 不会因此变小 |

## 仍在仓库中的大文件（> 500KB）

| 文件 | 大小 |
|---|---|
| `2025-autumn/5.4-training-framework/5.4 训练框架.pdf` | 9.9 MB |
| `2024-spring-intern-algorithms/Microsoft-intern/test.ipynb` | 2.5 MB |
| `2024-spring-intern-algorithms/Microsoft-intern/correlation_heatmap.png` | 1.9 MB |
| `2025-spring-intern-review/transformer-basics/grpo-from-scratch/image/rl-grpo-ppo-critic-actor/1740660712222.png` | 1.5 MB |
| `2025-autumn/5.4-training-framework/images/image-5.png` | 849 KB |
| `tmp6278.png` | 813 KB |
| `2025-autumn/5.4-training-framework/images/image-38.png` | 798 KB |
| `2025-autumn/5.4-training-framework/images/image-24.png` | 585 KB |

## 为什么克隆慢

- 历史中累计包含 27MB + 9.9MB 两个 PDF，加上各版本 ipynb，pack 体积约 47.7MB。
- 每次全新克隆都要下载全部历史，因此首次 clone 很慢。

## 建议

1. **保持现状**：如果接受克隆慢，什么都不用做。
2. **大文件移出仓库**：把两个 PDF 放到网盘/本地，从工作树删除（如 0_大佬的刷题指南.pdf 已做）。
3. **彻底瘦身（可选，谨慎）**：用 `git filter-repo` 从历史中清除大 blob 后 force push。这会改写全部提交哈希，**需要其他协作者重新克隆**，并重新授权推送：

   ```sh
   # 仅当明确要彻底瘦身时执行
   git filter-repo --path "0_大佬的刷题指南.pdf" --path "5.4 训练框架.pdf" --invert-paths
   git remote add origin git@github.com:ckqqqq/Algorithm-Fundamentals.git
   git push --force origin main
   ```

4. **未来避免**：.gitignore 已包含 `.*pdf`（注意：该规则只对未跟踪文件生效；已跟踪文件需显式 `git rm --cached`）。超过 1MB 的图片建议压缩后入库，或使用 Git LFS。
