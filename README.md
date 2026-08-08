<p align="center">
  <img src="assets/y-line-walkthrough.gif" width="720" alt="夜行人字纪 · 建成场景动态漫游">
</p>

<h1 align="center">人字纪 · The Y-Line</h1>

<p align="center"><b>百年京张 AI 创新带城市设计开源征集 · 正式参赛方案</b><br>
An AI-generated urban design submission for Beijing's Centennial Jing-Zhang AI Innovation Belt open call<br><br>
<a href="https://heyuxuan0209.github.io/y-line/">🚶 在线漫游 Live Demo</a> ·
<a href="https://github.com/open-city-ai/haidian/pull/280">📦 正式提交 PR #280</a> ·
<a href="#-关注我--follow-me">🔗 关注我 Follow me</a></p>

---

## 中文

### 这是什么

2026 年 8 月，北京海淀把 **43.6 km² 的真实城市设计**（京张铁路遗址公园沿线）开放给全球 AI Agent 投稿——全球首次。这个仓库是我和 Claude Code 共同完成的正式参赛方案 **「人字纪 · The Y-Line」** 的公开展示：概念原型、动态漫游、设计图与全部生成脚本。

正式方案包（9 层 GeoJSON + 复算指标 + 1.6 万字报告 + 三大证据矩阵 + A3/A0 图纸，自检四关全部 PASS）在官方仓库：**[open-city-ai/haidian PR #280](https://github.com/open-city-ai/haidian/pull/280)**。

### 一个"人"字的三重回答

1909 年，詹天佑在青龙桥画下"人"字形铁路——中国自主创新的第一笔。而"人"字分叉与 **git branch 是同一个图形**：铁路人看见人字轨与枕木，开发者看见一次 branch 与三个 commit。

- **器 · 中华文化 × 现代科技** — 600 年前永乐大钟铸 23 万字铭文，100 年前人字轨刻进关沟，今天代码接续"造物记名"的文明传统
- **道 · 大国风范** — 世界在争论 AI 把人带向哪里，这条带用命名作答：智能爆发的纪元仍以"人"为名。*The Y stands for Human.*
- **世 · 世界融合** — 一撇一捺互相支撑；北京为全球开发者留一面永久刻名的墙

### 方案核心

| 模块 | 内容 |
|---|---|
| 空间结构 | **一轨两撇三芯**：遗址公园主脊 × 中关村/小月河双翼 × 众智园/原点社区/大钟寺三芯 |
| 纪年体系 | **Y-Era 人字纪元**：Y0 = 1909，2026 = Y117，全线双纪年 |
| 运营系统 | **city-as-repo**：城市 issue → 全球 PR → 人类评审 → 每年 9 月 **Merge Day·鸣钟合并** |
| 治理品牌 | **青龙桥对话**：在铁轨分叉的地方，讨论 AI 的分叉走向何方 |
| 五大朝圣地标 | 人字碑·全球贡献者荣誉墙 / 青龙桥对话馆 / Fork Plaza / Commit 纪念带 / 源点广场 0km |

### 仓库导览

```
index.html                 夜行人字纪 · 可交互滚动漫游（Pages 主页，零依赖单文件）
prototypes/concepts.html   三个概念方向的可点对比原型（A 人字形 / B 源线 / C 开源城市）
prototypes/yline-fusion.html  A+C 融合版概念 mock
assets/figures/            五张正式方案图（纸感 × 信号红工程图纸体系）
tools/                     全部生成脚本：几何+指标 / 五图 / A3·A0 图纸 / 录屏
```

### 怎么做出来的

从读题到提交 PR 全程由 Claude Code（Fable 5）驱动：读取官方结构化任务书 → 拓扑安全的用地剖分（25 单元无缝无叠）→ EPSG:4548 指标复算 → 报告与证据矩阵 → matplotlib 出图出纸 → 官方四道自检 PASS → GitHub PR。人类只做了三次决策：选概念方向、定融合策略、按下提交键。

---

## English

### What is this

In August 2026, Beijing's Haidian district opened a **real 43.6 km² urban design brief** (along the centennial Jing-Zhang railway heritage park) to AI agents worldwide — a world first. This repo showcases **"The Y-Line (人字纪)"**, my formal submission co-created with Claude Code: concept prototypes, an animated walkthrough, design figures, and every generation script.

The formal package (9 GeoJSON layers, recomputed metrics, a full Chinese design report, three evidence matrices, A3/A0 drawings — all four official self-checks PASS) lives at **[open-city-ai/haidian PR #280](https://github.com/open-city-ai/haidian/pull/280)**.

### The idea, in one breath

In 1909, engineer Zhan Tianyou drew the famous **Y-shaped switchback** — the first railway designed by Chinese engineers. That same Y is exactly a **git branch**. From one shared glyph, the plan derives everything: a naming system (*The Y stands for Human*), a calendar (**Y-Era**, Y0 = 1909), a spatial structure (one heritage-park spine, two wings, three cores), and a permanent operating system for the city (**city-as-repo**: open issues → global PRs → human review → an annual **Merge Day**, opened by the toll of the 600-year-old Great Bell, when new contributors' names are carved into the Y-Monument wall).

### Highlights

- **Scroll walkthrough** ([live demo](https://heyuxuan0209.github.io/y-line/)): walk the 9.7 km belt at night, six built scenes, your position tracked on the real plan boundary
- **Honest data**: provisional boundaries clearly labeled; unknown statutory controls declared `unknown` instead of fabricated
- **Fully reproducible**: `tools/` regenerates geometry, metrics, figures and drawings from scratch

---

## 🔗 关注我 · Follow me

边做 AI 产品边把一手经验和思考公开分享，欢迎关注、来聊。<br>
I build AI products in public and share the notes here — come say hi:

<table>
  <tr>
    <td align="center"><b>小红书 · Xiaohongshu</b></td>
    <td align="center"><b>公众号 · WeChat</b></td>
    <td align="center"><b>视频号 · Channels</b></td>
    <td align="center"><b>抖音 · Douyin</b></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/qr-xiaohongshu.jpg" width="200" alt="小红书 杰西卡"></td>
    <td align="center"><img src="assets/qr-wechat.jpg" width="200" alt="公众号 杰西卡聊AI"></td>
    <td align="center"><img src="assets/qr-shipinhao.jpg" width="200" alt="视频号 杰西卡"></td>
    <td align="center"><img src="assets/qr-douyin.jpg" width="200" alt="抖音 杰西卡"></td>
  </tr>
</table>

## License & 二开须知 · Contributing

MIT — 见 [LICENSE](LICENSE)。方案内容本身遵循征集的开放共创规则（全部为概念建议，不构成官方结论）。欢迎 **Star / Fork / Issue**，二开或转载时请**注明出处并 @ 我**（公众号 / 小红书「**杰西卡聊AI**」）🙏。

MIT licensed — see [LICENSE](LICENSE). The design content follows the open call's co-creation rules (all conceptual suggestions, no official conclusions). **Star / Fork / Issues welcome** — if you remix or repost, please **credit and @ me** (Jessica · 杰西卡聊AI) 🙏.
