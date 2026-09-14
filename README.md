# Daily Briefing TrendRadar Publisher

这个公开仓库是日报助手的独立候选发现层。GitHub Actions 会定时拉取上游
[TrendRadar](https://github.com/sansan0/TrendRadar)，运行其 RSS 与热点聚合，
再把轻量候选 JSON 发布到 `trendradar-feed` 分支。

日报 Worker 配置：

```text
TRENDRADAR_FEED_URL=https://raw.githubusercontent.com/wang-studyhard/daily-briefing-trendradar/trendradar-feed/trendradar.json
```

这个 Feed 只提供候选，不直接写入日报数据库。日报 Worker 仍负责 URL 与标题去重、
正文补充、分类、拒绝和 D1 入库；Feed 过期、格式错误或抓取失败时保留上一版日报。

第一版工作流关闭 TrendRadar 的通知、AI 分析和 AI 翻译，不需要付费 API Key。上游
TrendRadar 的 GPL-3.0 代码只在独立 Actions 运行环境中执行，不复制进日报 Worker。

## 手动运行

在 GitHub Actions 中运行 `Publish TrendRadar candidate feed` 的 `workflow_dispatch`。
运行成功后，`trendradar-feed/trendradar.json` 即为日报 Worker 可读取的公开静态 Feed。

