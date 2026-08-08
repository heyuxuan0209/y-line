#!/usr/bin/env python3
"""Generate A3 booklet and A0 boards for the Y-Line package."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

plt.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

SUB = Path("/Users/heyuxuan/opencity-haidian/haidian/submissions/heyuxuan0209/y-line")
FIG = SUB / "assets/figures"
PAPER, INK, RED, GREY = "#F5F1E8", "#211D18", "#C8402A", "#8a8175"

A3 = (16.54, 11.69)
A0 = (46.81, 33.11)

FIGS = {n: mpimg.imread(FIG / f"{n}.png") for n in [
    "site-overview", "land-use-structure", "key-areas", "mobility-bluegreen",
    "metrics-evidence"]}

DISCLAIMER = ("本方案为面向全球智能体的开源征集成果，全部内容为开放共创建议（概念建议/参考方案），不替代正式规划，"
              "不构成政府审定结论；边界为 provisional 粗略替代范围，不代表官方红线。")


def page(pdf, size):
    fig = plt.figure(figsize=size, dpi=100)
    fig.patch.set_facecolor(PAPER)
    return fig


def header(fig, title, subtitle, page_no, total):
    fig.text(0.04, 0.955, title, fontsize=22, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.915, subtitle, fontsize=11, color="#5c5346", va="top")
    fig.text(0.96, 0.955, "人字纪 · THE Y-LINE", fontsize=11, color=RED, ha="right",
             va="top", fontweight="bold")
    fig.text(0.96, 0.930, "百年京张AI创新带城市设计开源征集 · heyuxuan0209", fontsize=8.5,
             color=GREY, ha="right", va="top")
    fig.text(0.96, 0.03, f"{page_no} / {total}", fontsize=9, color=GREY, ha="right")
    fig.text(0.04, 0.03, DISCLAIMER, fontsize=7.5, color="#8a8175")
    fig.lines.append(plt.Line2D([0.04, 0.96], [0.905, 0.905], transform=fig.transFigure,
                                color=INK, lw=1.2))


def img_panel(fig, img, rect):
    ax = fig.add_axes(rect)
    ax.imshow(img)
    ax.axis("off")


def logo(fig, x, y, s, dark=False):
    """Draw the Y-Line logo centered at figure fraction (x, y), height s."""
    col = PAPER if dark else INK
    ax = fig.add_axes([x - s / 2, y - s / 2, s, s])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    kw = dict(color=col, lw=4, solid_capstyle="round")
    ax.plot([50, 50], [5, 48], **kw)
    ax.plot([50, 24], [48, 88], **kw)
    ax.plot([50, 76], [48, 88], **kw)
    for yy in (14, 26, 38):
        ax.plot([44, 56], [yy, yy], color=col, lw=1.6, alpha=.65)
    ax.plot(50, 48, "o", ms=11, color=RED)
    ax.plot(24, 88, "o", ms=7, color="#3E6B4F")
    ax.plot(76, 88, "o", ms=7, color="#3E6B4F")
    ax.plot(50, 5, "o", ms=7, color=col)


def text_col(fig, x, y, pairs, hsize=13, bsize=9.5, gap=0.052, width_hint=None):
    for head, body in pairs:
        fig.text(x, y, head, fontsize=hsize, fontweight="bold", color=RED, va="top")
        fig.text(x, y - 0.024, body, fontsize=bsize, color=INK, va="top",
                 linespacing=1.65)
        yy_lines = body.count("\n") + 1
        y -= gap + 0.017 * yy_lines


# ================================================================ A3 booklet
with PdfPages(SUB / "drawings/a3-booklet.pdf") as pdf:
    total = 8
    # p1 cover
    fig = page(pdf, A3)
    fig.patch.set_facecolor(INK)
    logo(fig, 0.5, 0.60, 0.34, dark=True)
    fig.text(0.5, 0.40, "人字纪 · 京张AI创新带", fontsize=40, fontweight="bold",
             color=PAPER, ha="center")
    fig.text(0.5, 0.345, "The Y-Line — An Open-Source City Belt", fontsize=16,
             color="#b8b0a2", ha="center", style="italic")
    fig.text(0.5, 0.27, "百年京张AI创新带城市设计开源征集 · 正式方案 A3 文册",
             fontsize=12, color="#b8b0a2", ha="center")
    fig.text(0.5, 0.225, "1909 年，詹天佑画下“人”字——这座城市的 initial commit；"
             "智能爆发的新纪元，仍以“人”为名。", fontsize=11, color=PAPER, ha="center")
    fig.text(0.5, 0.13, "提交人：heyuxuan0209 × Claude Code（Fable 5）    "
             "The Y stands for Human.", fontsize=10, color="#b8b0a2", ha="center")
    fig.text(0.5, 0.06, DISCLAIMER, fontsize=8, color="#8a8175", ha="center")
    pdf.savefig(fig, facecolor=INK)
    plt.close(fig)

    # p2 concept
    fig = page(pdf, A3)
    header(fig, "总体概念 · 器 × 道 × 世", "一个“人”字的三重回答（agent.1 / agent.5）", 2, total)
    logo(fig, 0.16, 0.62, 0.30)
    text_col(fig, 0.33, 0.85, [
        ("器 · 中华文化 × 现代科技",
         "600 年前，永乐大钟铸下 23 万字铭文；100 年前，詹天佑用人字轨让火车翻过关沟；\n"
         "今天，代码接续这个传统。人字轨与 git branch 是同一个图形——\n"
         "自主创新的工程图腾，横跨百年而同构。"),
        ("道 · 大国风范",
         "世界正在争论 AI 会把人带向哪里，这条带用命名作答：\n"
         "智能爆发的纪元，仍以“人”为名。The Y stands for Human——\n"
         "承载“AI 治理全球话语权”的空间宣言，年度“青龙桥对话”全球AI治理论坛落位于此。"),
        ("世 · 世界融合",
         "“人”字一撇一捺互相支撑——中国与世界、人类与 AI、政府与开发者互为撇捺。\n"
         "北京为全球开发者留出一面永久刻名的墙：人字碑·全球贡献者荣誉墙，\n"
         "每年 Merge Day 沿轨生长一段。"),
        ("历 · 人字纪元 Y-Era",
         "以 1909 为 Y0，2026 即 Y117；全线里程碑、碑刻与活动采用公元 × Y 历双纪年，\n"
         "北京北站与众智园成为纪元的南北端点。"),
    ], gap=0.075)
    pdf.savefig(fig, facecolor=PAPER)
    plt.close(fig)

    # p3-6 figure pages
    for i, (name, title, sub) in enumerate([
        ("site-overview", "总体结构 · 一轨两撇三芯", "总体设计范围空间结构（概念建议）"),
        ("land-use-structure", "用地布局 · 拓扑完整分区", "25 个用地单元无缝无叠 · EPSG:4548 复算"),
        ("key-areas", "三芯详细设计索引", "众智园 · 原点社区 · 大钟寺（方向性详细设计）"),
        ("mobility-bluegreen", "交通慢行 × 蓝绿公共空间", "南北贯通 · 东西缝合 · 站城一体（概念线位）"),
    ], start=3):
        fig = page(pdf, A3)
        header(fig, title, sub, i, total)
        img = FIGS[name]
        h, w = img.shape[0], img.shape[1]
        avail_w, avail_h = 0.90, 0.80
        fig_ar = (A3[0] * avail_w) / (A3[1] * avail_h)
        img_ar = w / h
        if img_ar > fig_ar:
            rw, rh = avail_w, avail_w * (A3[0] / A3[1]) / img_ar
        else:
            rh, rw = avail_h, avail_h * img_ar / (A3[0] / A3[1])
        img_panel(fig, img, [0.5 - rw / 2, 0.47 - rh / 2, rw, rh])
        pdf.savefig(fig, facecolor=PAPER)
        plt.close(fig)

    # p7 scenarios & operations
    fig = page(pdf, A3)
    header(fig, "AI 场景 × 长期运营", "12 张场景卡（含 3 个测试验证）· city-as-repo 年度周期（agent.3 / agent.6）", 7, total)
    text_col(fig, 0.04, 0.85, [
        ("场景卡（12 张）",
         "①代码朗读亭 ②AI导览员·人字纪线 ③无障碍出行伴随 ④校园—园区实习桥 ⑤智能原生店铺\n"
         "⑥AI+医疗预诊导流 ⑦AI+教育开放课堂 ⑧城市issue广场屏 ⑨Merge Day直播场 ⑩端侧算力便民柜\n"
         "测试验证：⑪低速接驳测试环（围栏+人工接管） ⑫具身机器人街区测试（远程监护）\n"
         "⑫b 城市级导览压力测试（灰度+熔断）。全部场景：最小数据采集、保留人工复核，\n"
         "测试场景不表述为已批准运营。"),
        ("用户画像（6 类）",
         "全栈研发者 / 高校师生创业者 / AI原生企业经营者 / 国际访问学者与开发者 /\n"
         "沿线居民 / 城市访客与公众——画像校准各芯功能配比与场景清单。"),
        ("city-as-repo 年度周期",
         "Q4–Q1 发布城市命题（Open Issues）→ Q1–Q2 全球提案（Global PRs）→\n"
         "Q3 专业+社区双评审（人类最终判断）→ 9月 Merge Day·鸣钟合并：\n"
         "大钟寺鸣钟开幕 · 入选公布 · 碑刻揭幕 · 深化开工 · 全球直播。"),
        ("贡献者机制",
         "Contributor（被 merge）→ Maintainer（参与深化）→ Core（年度评审团）；\n"
         "荣誉资产空间化：人字碑荣誉墙 · Commit 纪念带 · 数字荣誉档案。"),
    ], gap=0.072)
    pdf.savefig(fig, facecolor=PAPER)
    plt.close(fig)

    # p8 metrics evidence
    fig = page(pdf, A3)
    header(fig, "核心指标复算与证据链", "所有指标由 GeoJSON 在 EPSG:4548 下复算 · JSON 为权威数据", 8, total)
    img = FIGS["metrics-evidence"]
    h, w = img.shape[0], img.shape[1]
    rh = 0.80
    rw = rh * (w / h) / (A3[0] / A3[1])
    img_panel(fig, img, [0.5 - rw / 2, 0.47 - rh / 2, rw, rh])
    pdf.savefig(fig, facecolor=PAPER)
    plt.close(fig)
print("A3 booklet done")

# ================================================================ A0 boards
with PdfPages(SUB / "drawings/a0-boards.pdf") as pdf:
    # board 1: concept + structure
    fig = page(pdf, A0)
    header(fig, "人字纪 · 京张AI创新带  The Y-Line — 展板一 · 概念与空间结构",
           "百年京张AI创新带城市设计开源征集 · 正式方案（开放共创建议）", 1, 2)
    logo(fig, 0.085, 0.76, 0.13)
    fig.text(0.16, 0.845, "新纪元，以人为名", fontsize=30, fontweight="bold", color=INK,
             va="top")
    fig.text(0.16, 0.800, "1909 年詹天佑画下“人”字——这座城市的 initial commit；\n"
             "智能爆发的纪元，仍以“人”为名。一撇中国，一捺世界，互相支撑。",
             fontsize=13, color="#5c5346", va="top", linespacing=1.7)
    for j, (head, body) in enumerate([
            ("器", "人字轨 = git branch\n百年工程图腾与代码同构"),
            ("道", "The Y stands for Human\nAI 治理话语权的空间宣言"),
            ("世", "一撇一捺互相支撑\n为全球开发者留一面刻名墙"),
            ("历", "Y-Era 纪年 Y0=1909\n公元×Y 历双纪年体系")]):
        x = 0.16 + j * 0.115
        fig.text(x, 0.715, head, fontsize=22, fontweight="bold", color=RED, va="top")
        fig.text(x + 0.018, 0.712, body, fontsize=10, color=INK, va="top",
                 linespacing=1.6)
    img = FIGS["site-overview"]
    h, w = img.shape[0], img.shape[1]
    rh = 0.56
    rw = rh * (w / h) / (A0[0] / A0[1])
    img_panel(fig, img, [0.045, 0.075, rw, rh])
    img = FIGS["key-areas"]
    h2, w2 = img.shape[0], img.shape[1]
    rw2 = 0.44
    rh2 = rw2 * (h2 / w2) * (A0[0] / A0[1])
    img_panel(fig, FIGS["key-areas"], [0.52, 0.30, rw2, rh2])
    text_col(fig, 0.52, 0.255, [
        ("五大 AI 朝圣地标",
         "① 人字碑·全球贡献者荣誉墙（每年 Merge Day 沿轨生长）  ② 青龙桥对话馆（全球AI治理年度论坛）\n"
         "③ 分叉广场 Fork Plaza（技术树广场·下一次分叉属于你）  ④ Commit 纪念带·开源成果展示廊\n"
         "⑤ 源点广场·0km 标（中国自主创新 0 公里·双刻度盘）"),
        ("文化叙事 · 造物记名",
         "600 年前永乐大钟铸 23 万字铭文 → 100 年前人字轨刻进关沟 → 今天贡献者的名字刻进人字碑。\n"
         "文化导览线：源点广场→人字纪展示馆→对话分馆→Commit纪念带→Fork Plaza→人字碑。"),
    ], hsize=15, bsize=11, gap=0.09)
    pdf.savefig(fig, facecolor=PAPER)
    plt.close(fig)

    # board 2: systems + metrics + operation
    fig = page(pdf, A0)
    header(fig, "人字纪 · 京张AI创新带  The Y-Line — 展板二 · 系统 · 指标 · 运营",
           "用地 / 交通蓝绿 / 指标证据链 / city-as-repo 运营体系", 2, 2)
    for img_name, rect in [
            ("land-use-structure", [0.045, 0.30, 0.27, 0.55]),
            ("mobility-bluegreen", [0.345, 0.30, 0.27, 0.55]),
            ("metrics-evidence", [0.645, 0.30, 0.27, 0.55])]:
        img = FIGS[img_name]
        h, w = img.shape[0], img.shape[1]
        rw = rect[2]
        rh = rw * (h / w) * (A0[0] / A0[1])
        if rh > 0.56:
            rh = 0.56
            rw = rh * (w / h) / (A0[0] / A0[1])
        img_panel(fig, img, [rect[0] + (rect[2] - rw) / 2, 0.86 - rh, rw, rh])
    text_col(fig, 0.045, 0.255, [
        ("拓扑完整用地剖分",
         "25 个用地单元无缝无叠覆盖总体设计范围；绿地率 16.7%，公共空间率 3.1%（EPSG:4548 复算）；\n"
         "科研两端强、职住内嵌、消费在钟、文化锚南端、留白可进化。"),
        ("三芯先行 · 三期实施",
         "近期三芯先行 4.31 km²（与 9 月征集落地节奏衔接）→ 中期走廊缝合 5.25 km² → 远期门户织补 1.86 km²。"),
    ], hsize=15, bsize=11, gap=0.085)
    text_col(fig, 0.52, 0.255, [
        ("city-as-repo 城市操作系统",
         "Open Issues（城市命题公开）→ Global PRs（全球智能体与团队提案）→ Review（人类最终判断）→\n"
         "Merge Day·鸣钟合并（每年 9 月·大钟寺鸣钟·碑刻揭幕·深化开工·全球直播）。"),
        ("诚实的数据边界",
         "法定容积率 / 高度管控 / 道路红线 / 现状建筑底数均为 unknown——不虚构、不伪装，\n"
         "官方数据公布后整包按既定脚本链路重算。组织方数据缺口不影响内容评分。"),
    ], hsize=15, bsize=11, gap=0.085)
    pdf.savefig(fig, facecolor=PAPER)
    plt.close(fig)
print("A0 boards done")
