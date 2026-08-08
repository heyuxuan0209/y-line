#!/usr/bin/env python3
"""Generate Y-Line design geometry + metrics for submissions/heyuxuan0209/y-line.

Design concept: 人字纪 · The Y-Line — 一轨两撇三芯.
All geometry is derived from the provisional site boundary (PROV-SITE-001) by
topology-safe partitioning: every land-use cell is site ∩ box(band, strip),
so coverage is exact and overlaps are impossible by construction.
"""
from __future__ import annotations

import json
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import box, shape, mapping, LineString, MultiPolygon, Polygon
from shapely.ops import transform as shp_transform, unary_union

REPO = Path("/Users/heyuxuan/opencity-haidian/haidian")
SUB = REPO / "submissions/heyuxuan0209/y-line"
GEOM = SUB / "geometry"

T4548 = Transformer.from_crs("EPSG:4326", "EPSG:4548", always_xy=True)


def proj(geom):
    return shp_transform(T4548.transform, geom)


def area4548(geom) -> float:
    return float(proj(geom).area)


def rbox(lon0, lat0, lon1, lat1):
    return box(lon0, lat0, lon1, lat1)


def bbox_m(center_lon, center_lat, w_m, h_m):
    """Axis-aligned box of w×h meters centered at lon/lat."""
    dlat = h_m / 111000.0 / 2
    dlon = w_m / 85200.0 / 2  # cos(40°)·111.3km ≈ 85.2 km/deg
    return box(center_lon - dlon, center_lat - dlat, center_lon + dlon, center_lat + dlat)


# ---------------------------------------------------------------- site + keys
site_fc = json.loads((GEOM / "site_boundary.geojson").read_text())
SITE = shape(site_fc["features"][0]["geometry"])

# Strips (lon) and bands (lat) — cover the whole site extent with shared cuts.
LON_MIN, LON_MAX = 116.30, 116.37
SPINE_W, SPINE_E = 116.3460, 116.3485
BANDS = {  # south → north
    "G": (39.939, 39.944),
    "F": (39.944, 39.94984),
    "E": (39.94984, 39.958),
    "D": (39.958, 39.9835),
    "C": (39.9835, 39.9935),
    "B": (39.9935, 40.0075),
    "A": (40.0075, 40.0265),
}
W, S, E = (LON_MIN, SPINE_W), (SPINE_W, SPINE_E), (SPINE_E, LON_MAX)

# cell spec: id, band, strip(lon pair), optional lat sub-range, code, name, phase
CELLS = [
    ("LU-G-W", "G", W, None, "05",   "北站门户商务区（源点门户）", 3),
    ("LU-G-S", "G", S, None, "1403", "源点广场（公园南端锚点）", 3),
    ("LU-G-E", "G", E, None, "0803", "京张文化展示带·南锚", 3),
    ("LU-F-W", "F", W, None, "05",   "大钟寺智能原生消费区", 1),
    ("LU-F-S", "F", S, None, "1401", "京张遗址公园·大钟寺段", 1),
    ("LU-F-E", "F", E, None, "0802", "AI原生企业总部区", 1),
    ("LU-E-W", "E", W, None, "0701", "织补居住区（西）", 3),
    ("LU-E-S", "E", S, None, "1401", "京张遗址公园·过渡段", 3),
    ("LU-E-E", "E", E, None, "05",   "商务服务织补区", 3),
    ("LU-D-W", "D", W, None, "0804", "高校开放创新区（北航—北邮走廊）", 2),
    ("LU-D-S", "D", S, None, "1401", "京张遗址公园·高校段", 2),
    ("LU-D-ES", "D", E, (39.958, 39.9705), "0702", "社区服务与配套区", 2),
    ("LU-D-EN", "D", E, (39.9705, 39.9835), "0701", "职住平衡住区（北）", 2),
    ("LU-C-W", "C", W, None, "0802", "原点社区成果转化区", 1),
    ("LU-C-S1", "C", S, (39.9835, 39.9875), "1401", "京张遗址公园·原点南段", 1),
    ("LU-C-SP", "C", S, (39.9875, 39.9895), "1403", "分叉广场 Fork Plaza", 1),
    ("LU-C-S2", "C", S, (39.9895, 39.9935), "1401", "京张遗址公园·原点北段", 1),
    ("LU-C-E", "C", E, None, "05",   "五道口创新消费区", 1),
    ("LU-B-W", "B", W, None, "0804", "科教走廊校区开放区", 2),
    ("LU-B-S", "B", S, None, "1401", "京张遗址公园·科教段", 2),
    ("LU-B-E", "B", E, None, "0802", "校地联合研发区", 2),
    ("LU-A-W", "A", W, None, "0802", "众智园全栈自主创新区", 1),
    ("LU-A-S", "A", S, None, "1401", "清河绿谷·公园北延段", 1),
    ("LU-A-ES", "A", E, (40.0075, 40.017), "16", "战略留白·可进化用地", 1),
    ("LU-A-EN", "A", E, (40.017, 40.0265), "0701", "国际人才社区", 1),
]

CODE_LABEL = {
    "05": "商业服务业用地", "0701": "城镇住宅用地", "0702": "城镇社区服务设施用地",
    "0802": "科研用地", "0803": "文化用地", "0804": "教育用地",
    "1401": "公园绿地", "1403": "广场用地", "16": "留白用地",
}

BASE_PROPS = dict(source_type="agent_generated_design", confidence="medium",
                  geometry_role="design_proposal")


def feature(fid, layer, geom, extra=None, declared=True):
    props = {"id": fid, "layer": layer, **BASE_PROPS}
    if extra:
        props.update(extra)
    if declared and geom.geom_type in ("Polygon", "MultiPolygon"):
        props["area_sqm_declared"] = round(area4548(geom), 3)
    return {"type": "Feature", "id": fid, "properties": props,
            "geometry": json.loads(json.dumps(mapping(geom)))}


def write_fc(name, feats, fc_name):
    fc = {"type": "FeatureCollection", "name": fc_name, "features": feats}
    (GEOM / name).write_text(json.dumps(fc, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    print(f"wrote {name}: {len(feats)} features")


# ---------------------------------------------------------------- land use
cells = {}
lu_feats = []
for fid, band, strip, sub, code, name, phase in CELLS:
    lat0, lat1 = sub if sub else BANDS[band]
    cell = SITE.intersection(rbox(strip[0], lat0, strip[1], lat1))
    if cell.is_empty or area4548(cell) < 50:
        raise SystemExit(f"empty cell {fid}")
    cells[fid] = cell
    lu_feats.append(feature(fid, "LAND_USE", cell, {
        "land_use_code": code, "land_use_label_zh": CODE_LABEL[code],
        "name_zh": name, "phase": phase,
        "note_zh": "基于 provisional 总体设计范围的概念性用地布局建议，不构成法定用地边界或控规结论。",
    }))
# sanity: coverage + overlap
union = unary_union(list(cells.values()))
gap = area4548(SITE.difference(union))
assert gap < 500, f"coverage gap {gap}"
write_fc("land_use.geojson", lu_feats, "y-line land use partition")

# ---------------------------------------------------------------- green space
GREEN_CELLS = [c for c in cells if any(
    x[0] == c and x[4] in ("1401",) for x in CELLS)]
green_feats = []
for i, cid in enumerate(GREEN_CELLS, 1):
    name = next(x[5] for x in CELLS if x[0] == cid)
    green_feats.append(feature(f"GREEN-{i:03d}", "GREEN_SPACE", cells[cid], {
        "land_use_code": "1401", "name_zh": name,
        "note_zh": "遗址公园活力带主脊绿地，概念建议。"}))
write_fc("green_space.geojson", green_feats, "y-line green spine")

# ---------------------------------------------------------------- public space
PUBS = [
    ("PUB-001", "源点广场（1909 起点纪念广场）", cells["LU-G-S"]),
    ("PUB-002", "分叉广场 Fork Plaza（技术树广场）", cells["LU-C-SP"]),
    ("PUB-003", "人字碑纪念广场·全球贡献者荣誉墙", rbox(116.3465, 40.009, 116.348, 40.0105)),
    ("PUB-004", "鸣钟广场（Merge Day 主会场）", rbox(116.3445, 39.9445, 116.346, 39.9455)),
    ("PUB-005", "五道口站前广场", rbox(116.3495, 39.9905, 116.351, 39.9918)),
    ("PUB-006", "大钟寺站四象限连通空间", MultiPolygon([
        rbox(116.3486, 39.9469, 116.3494, 39.9474),
        rbox(116.3496, 39.9469, 116.3504, 39.9474),
        rbox(116.3486, 39.9461, 116.3494, 39.9466),
        rbox(116.3496, 39.9461, 116.3504, 39.9466)])),
    ("PUB-007", "开源成果展示廊（Commit 纪念带·高校段）", rbox(116.3479, 39.962, 116.3487, 39.9695)),
    ("PUB-008", "智能体贡献荣誉步廊（人字碑北延）", rbox(116.3462, 40.018, 116.347, 40.0255)),
]
pub_feats = []
for fid, name, geom in PUBS:
    geom = geom.intersection(SITE)
    assert not geom.is_empty, fid
    pub_feats.append(feature(fid, "PUBLIC_SPACE", geom, {
        "name_zh": name,
        "note_zh": "AI 公共空间/朝圣地标概念建议，位置为示意，需专业团队深化。"}))
write_fc("public_space.geojson", pub_feats, "y-line public spaces and landmarks")

# ---------------------------------------------------------------- buildings
BLDG = [
    # id suffix, cell, lon, lat, w, h, type, floors, name
    ("A1", "LU-A-W", 116.3435, 40.0095, 60, 40, "lab", 10, "全栈自主创新实验室一号楼"),
    ("A2", "LU-A-W", 116.3435, 40.0125, 60, 40, "lab", 10, "全栈自主创新实验室二号楼"),
    ("A3", "LU-A-W", 116.3435, 40.0155, 60, 40, "lab", 10, "全栈自主创新实验室三号楼"),
    ("A4", "LU-A-W", 116.3435, 40.0185, 60, 40, "lab", 10, "全栈自主创新实验室四号楼"),
    ("A5", "LU-A-W", 116.3450, 40.0105, 50, 50, "incubator", 20, "众智加速塔"),
    ("A6", "LU-A-W", 116.3450, 40.0145, 60, 40, "office", 12, "标准与安全治理中心"),
    ("A7", "LU-A-W", 116.3435, 40.0215, 80, 50, "ai_r_and_d", 6, "算力与数据要素枢纽"),
    ("A8", "LU-A-W", 116.3450, 40.0185, 60, 45, "mixed_use", 8, "国际创新交往中心"),
    ("A9", "LU-A-EN", 116.3510, 40.0180, 55, 35, "talent_apartment", 16, "国际人才公寓一期"),
    ("A10", "LU-A-EN", 116.3510, 40.0205, 55, 35, "talent_apartment", 16, "国际人才公寓二期"),
    ("A11", "LU-A-EN", 116.3510, 40.0230, 55, 35, "talent_apartment", 16, "国际人才公寓三期"),
    ("B1", "LU-B-W", 116.3437, 39.9970, 70, 45, "education", 8, "校地共创教学创新楼（西）"),
    ("B2", "LU-B-W", 116.3437, 40.0020, 70, 45, "education", 8, "校地共创教学创新楼（东）"),
    ("B3", "LU-B-E", 116.3505, 39.9970, 70, 45, "ai_r_and_d", 10, "校地联合研发楼一号"),
    ("B4", "LU-B-E", 116.3505, 40.0030, 70, 45, "ai_r_and_d", 10, "校地联合研发楼二号"),
    ("C1", "LU-C-W", 116.3420, 39.9855, 65, 45, "incubator", 10, "原点孵化器一号"),
    ("C2", "LU-C-W", 116.3440, 39.9855, 65, 45, "incubator", 10, "原点孵化器二号"),
    ("C3", "LU-C-W", 116.3420, 39.9915, 65, 45, "lab", 12, "成果转化实验楼一号"),
    ("C4", "LU-C-W", 116.3440, 39.9915, 65, 45, "lab", 12, "成果转化实验楼二号"),
    ("C5", "LU-C-E", 116.3505, 39.9855, 90, 60, "retail", 8, "五道口智能生活综合体"),
    ("C6", "LU-C-E", 116.3525, 39.9890, 70, 50, "mixed_use", 6, "开源社区中心"),
    ("D1", "LU-D-W", 116.3425, 39.9660, 70, 45, "education", 8, "开放实验共享楼（南）"),
    ("D2", "LU-D-W", 116.3425, 39.9760, 70, 45, "education", 8, "开放实验共享楼（北）"),
    ("D3", "LU-D-EN", 116.3510, 39.9730, 60, 40, "residential", 12, "有机更新住区示范一期"),
    ("D4", "LU-D-EN", 116.3510, 39.9780, 60, 40, "residential", 12, "有机更新住区示范二期"),
    ("D5", "LU-D-ES", 116.3510, 39.9625, 70, 45, "community_service", 4, "社区综合服务中心"),
    ("E1", "LU-E-W", 116.3435, 39.9520, 55, 35, "residential", 14, "织补住宅一号"),
    ("E2", "LU-E-W", 116.3435, 39.9550, 55, 35, "residential", 14, "织补住宅二号"),
    ("E3", "LU-E-E", 116.3510, 39.9535, 65, 45, "office", 12, "商务织补楼"),
    ("F1", "LU-F-W", 116.3435, 39.9455, 80, 55, "retail", 6, "智能原生消费旗舰空间"),
    ("F2", "LU-F-W", 116.3452, 39.9475, 50, 50, "office", 24, "大钟寺国际交往塔"),
    ("F3", "LU-F-W", 116.3435, 39.9480, 60, 45, "office", 12, "数据要素与数字资产服务中心"),
    ("F4", "LU-F-E", 116.3520, 39.9448, 70, 45, "ai_r_and_d", 12, "AI原生企业总部一号"),
    ("F5", "LU-F-E", 116.3520, 39.9468, 70, 45, "ai_r_and_d", 12, "AI原生企业总部二号"),
    ("F6", "LU-F-E", 116.3520, 39.9488, 70, 45, "ai_r_and_d", 12, "AI原生企业总部三号"),
    ("G1", "LU-G-W", 116.3435, 39.9405, 70, 50, "office", 15, "北站门户商务楼（南）"),
    ("G2", "LU-G-W", 116.3435, 39.9425, 70, 50, "office", 15, "北站门户商务楼（北）"),
    ("G3", "LU-G-E", 116.3510, 39.9415, 90, 55, "cultural", 4, "人字纪展示馆"),
    ("G4", "LU-G-E", 116.3525, 39.9425, 60, 40, "cultural", 5, "青龙桥对话·城区分馆"),
]
bldg_feats = []
total_floor = 0.0
for sfx, cell_id, lon, lat, w, h, btype, floors, name in BLDG:
    geom = bbox_m(lon, lat, w, h)
    if not cells[cell_id].contains(geom):
        raise SystemExit(f"building {sfx} not inside {cell_id}")
    a = area4548(geom)
    total_floor += a * floors
    bldg_feats.append(feature(f"BLDG-{sfx}", "BUILDING_FOOTPRINT", geom, {
        "name_zh": name, "building_type": btype, "floors_proposed": floors,
        "note_zh": "更新示范项目建筑基底概念建议；现状建筑底数缺失，不构成拆改留或工程结论。",
    }))
write_fc("buildings.geojson", bldg_feats, "y-line catalytic projects")

# ---------------------------------------------------------------- roads
ROADS = [
    ("ROAD-001", "secondary", "西线创新大街（南北次干路）",
     [(116.3445, 39.9400), (116.3445, 40.0255)]),
    ("ROAD-002", "secondary", "东线学院创新街（南北次干路）",
     [(116.3495, 39.9400), (116.3495, 40.0255)]),
    ("ROAD-003", "greenway", "京张遗址公园绿道（主脊）",
     [(116.34725, 39.9395), (116.34725, 40.0260)]),
    ("ROAD-004", "branch", "大钟寺东西连通支路",
     [(116.3425, 39.9470), (116.3525, 39.9470)]),
    ("ROAD-005", "branch", "过渡段东西支路",
     [(116.3425, 39.9540), (116.3525, 39.9540)]),
    ("ROAD-006", "branch", "高校走廊东西支路（南）",
     [(116.3425, 39.9705), (116.3525, 39.9705)]),
    ("ROAD-007", "branch", "原点社区东西支路",
     [(116.3425, 39.9885), (116.3525, 39.9885)]),
    ("ROAD-008", "branch", "科教走廊东西支路",
     [(116.3430, 39.9990), (116.3525, 39.9990)]),
    ("ROAD-009", "branch", "众智园东西支路（南）",
     [(116.3435, 40.0120), (116.3525, 40.0120)]),
    ("ROAD-010", "branch", "众智园东西支路（北）",
     [(116.3437, 40.0210), (116.3520, 40.0210)]),
    ("ROAD-011", "transit_connection", "五道口站接驳通道",
     [(116.3485, 39.9925), (116.3520, 39.9925)]),
    ("ROAD-012", "transit_connection", "大钟寺站接驳通道",
     [(116.3480, 39.9468), (116.3535, 39.9468)]),
    ("ROAD-013", "cycleway", "原点社区骑行环",
     [(116.3435, 39.9840), (116.3520, 39.9840), (116.3520, 39.9930),
      (116.3435, 39.9930), (116.3435, 39.9840)]),
    ("ROAD-014", "pedestrian", "上跨北五环步道（缝合示意）",
     [(116.3470, 40.0240), (116.3470, 40.0263)]),
    ("ROAD-015", "pedestrian", "南端门户步道（西直门外大街衔接示意）",
     [(116.3470, 39.9392), (116.3470, 39.9420)]),
]
road_feats = []
road_len = 0.0
for fid, cls, name, pts in ROADS:
    geom = LineString(pts)
    road_len += float(proj(geom).length)
    road_feats.append(feature(fid, "ROAD_CENTERLINE", geom, {
        "road_class": cls, "name_zh": name,
        "note_zh": "道路组织概念建议，不代表道路红线或工程线形。"}, declared=False))
write_fc("roads.geojson", road_feats, "y-line mobility network")

# ---------------------------------------------------------------- phasing
PHASES = [
    ("PHASE-001", 1, "近期（三芯先行）", ["A", "C", "F"],
     "众智园、原点社区、大钟寺三个分叉芯与公园主脊同步启动。"),
    ("PHASE-002", 2, "中期（走廊缝合）", ["B", "D"],
     "科教走廊与高校段缝合，东西连通、开源展示廊贯通。"),
    ("PHASE-003", 3, "远期（门户与织补）", ["E", "G"],
     "南端源点门户与过渡段织补，完成一轨两撇三芯整体。"),
]
phase_feats = []
phase_areas = {}
for fid, no, name, bands, note in PHASES:
    geom = unary_union([SITE.intersection(
        rbox(LON_MIN, BANDS[b][0], LON_MAX, BANDS[b][1])) for b in bands])
    phase_areas[no] = area4548(geom)
    phase_feats.append(feature(fid, "PHASE", geom, {
        "phase": no, "name_zh": name, "note_zh": note + "分期为概念建议。"}))
write_fc("phasing.geojson", phase_feats, "y-line three phases")

# ---------------------------------------------------------------- constraints
CONS = [
    ("CONS-001", "EXISTING_RAIL", "京张旧线走廊示意（遗址公园主脊线索）",
     LineString([(116.34725, 39.9392), (116.34725, 40.0263)]),
     "依据公开叙述的京张铁路遗址公园走向绘制的示意线，非官方线位。"),
    ("CONS-002", "EXISTING_WATER", "清河方向蓝绿联系示意（北端）",
     LineString([(116.3430, 40.0258), (116.3550, 40.0258)]),
     "示意北端与清河蓝绿空间的联系方向，非水系蓝线。"),
    ("CONS-003", "EXISTING_WATER", "小月河方向蓝绿联系示意（东翼）",
     LineString([(116.3548, 39.9660), (116.3548, 39.9990)]),
     "示意东翼与小月河场景赋能翼的联系方向，非水系蓝线。"),
]
cons_feats = []
for fid, layer, name, geom, note in CONS:
    cons_feats.append(feature(fid, layer, geom, {
        "name_zh": name, "note_zh": note,
        "source_type": "agent_inferred_from_public_data",
        "confidence": "low", "geometry_role": "existing_condition"}, declared=False))
write_fc("constraints.geojson", cons_feats, "y-line existing-condition hints")

# ---------------------------------------------------------------- metrics
site_area = area4548(SITE)
green_union = unary_union([shape(f["geometry"]) for f in green_feats])
green_area = area4548(green_union)
pub_union = unary_union([shape(f["geometry"]) for f in pub_feats])
pub_area = area4548(pub_union)
bldg_union = unary_union([shape(f["geometry"]) for f in bldg_feats])
bldg_area = area4548(bldg_union)

lu_by_group = {}
GROUPS = {"05": "commercial", "0701": "residential", "0702": "residential",
          "0802": "research", "0803": "culture", "0804": "education",
          "1401": "green_open", "1403": "green_open", "16": "reserved_white"}
for x in CELLS:
    lu_by_group.setdefault(GROUPS[x[4]], 0.0)
    lu_by_group[GROUPS[x[4]]] += area4548(cells[x[0]])

key_fc = json.loads((GEOM / "key_areas.geojson").read_text())
key_total = sum(area4548(shape(f["geometry"])) for f in key_fc["features"])

PROV_NOTE = "基于 provisional 总体设计范围复算，官方边界公布后需重算。"
DESIGN_NOTE = "设计方案值（概念建议），非法定控规指标。"


def m_known(value, unit, files, formula, conf="medium", assumptions=None):
    return {"status": "known", "value": round(value, 6 if unit == "ratio" else 3),
            "unit": unit, "source_files": files, "formula": formula,
            "confidence": conf, "assumptions": assumptions or []}


def m_unknown(unit, reason, files=None, formula=""):
    return {"status": "unknown", "value": None, "unit": unit,
            "source_files": files or [], "formula": formula,
            "confidence": "unknown", "assumptions": [], "reason": reason,
            "required_for_formal_submission": True}


SB = ["geometry/site_boundary.geojson"]
metrics = {
    "site_area_sqm": m_known(site_area, "sqm", SB, "polygon_area(site_boundary)@EPSG:4548",
                             "medium", [PROV_NOTE]),
    "green_space_area_sqm": m_known(green_area, "sqm",
                                    ["geometry/green_space.geojson"],
                                    "union_area(green_space)@EPSG:4548", "medium",
                                    [PROV_NOTE, DESIGN_NOTE]),
    "green_ratio": m_known(green_area / site_area, "ratio",
                           ["geometry/green_space.geojson"] + SB,
                           "green_space_area_sqm / site_area_sqm", "medium",
                           [PROV_NOTE, DESIGN_NOTE]),
    "public_space_area_sqm": m_known(pub_area, "sqm",
                                     ["geometry/public_space.geojson"],
                                     "union_area(public_space)@EPSG:4548", "medium",
                                     [PROV_NOTE, DESIGN_NOTE]),
    "public_space_ratio": m_known(pub_area / site_area, "ratio",
                                  ["geometry/public_space.geojson"] + SB,
                                  "public_space_area_sqm / site_area_sqm", "medium",
                                  [PROV_NOTE, DESIGN_NOTE]),
    "building_footprint_area_sqm": m_known(bldg_area, "sqm",
                                           ["geometry/buildings.geojson"],
                                           "union_area(building_footprints)@EPSG:4548",
                                           "medium",
                                           ["建筑图层仅表达更新示范项目，非全域建筑底数。"]),
    "catalyst_total_floor_area_sqm": m_known(total_floor, "sqm",
                                             ["geometry/buildings.geojson"],
                                             "sum(footprint_area × floors_proposed)",
                                             "low",
                                             ["层数为方案假设值 A-DEMO-FLOORS-001。", DESIGN_NOTE]),
    "catalyst_far_index": m_known(total_floor / bldg_area, "index",
                                  ["geometry/buildings.geojson"],
                                  "catalyst_total_floor_area_sqm / building_footprint_area_sqm",
                                  "low", ["示范项目平均容积（毛）指数，非法定FAR。"]),
    "road_centerline_length_m": m_known(road_len, "m",
                                        ["geometry/roads.geojson"],
                                        "sum(length(road_centerlines))@EPSG:4548",
                                        "medium", [DESIGN_NOTE]),
    "key_area_count": m_known(3, "count", ["geometry/key_areas.geojson"],
                              "count(key_areas)", "high"),
    "key_area_total_sqm": m_known(key_total, "sqm", ["geometry/key_areas.geojson"],
                                  "sum(polygon_area(key_areas))@EPSG:4548", "medium",
                                  ["重点区 polygon 为 provisional，面积仅供参考。"]),
    "phase1_area_sqm": m_known(phase_areas[1], "sqm", ["geometry/phasing.geojson"],
                               "polygon_area(PHASE-001)@EPSG:4548", "medium",
                               [PROV_NOTE, DESIGN_NOTE]),
    "phase2_area_sqm": m_known(phase_areas[2], "sqm", ["geometry/phasing.geojson"],
                               "polygon_area(PHASE-002)@EPSG:4548", "medium",
                               [PROV_NOTE, DESIGN_NOTE]),
    "phase3_area_sqm": m_known(phase_areas[3], "sqm", ["geometry/phasing.geojson"],
                               "polygon_area(PHASE-003)@EPSG:4548", "medium",
                               [PROV_NOTE, DESIGN_NOTE]),
    "landuse_research_area_sqm": m_known(lu_by_group["research"], "sqm",
                                         ["geometry/land_use.geojson"],
                                         "sum(area(land_use where code in 0802))@EPSG:4548",
                                         "medium", [DESIGN_NOTE]),
    "landuse_residential_area_sqm": m_known(lu_by_group["residential"], "sqm",
                                            ["geometry/land_use.geojson"],
                                            "sum(area(land_use where code in 0701,0702))@EPSG:4548",
                                            "medium", [DESIGN_NOTE]),
    "landuse_commercial_area_sqm": m_known(lu_by_group["commercial"], "sqm",
                                           ["geometry/land_use.geojson"],
                                           "sum(area(land_use where code=05))@EPSG:4548",
                                           "medium", [DESIGN_NOTE]),
    "landuse_education_area_sqm": m_known(lu_by_group["education"], "sqm",
                                          ["geometry/land_use.geojson"],
                                          "sum(area(land_use where code=0804))@EPSG:4548",
                                          "medium", [DESIGN_NOTE]),
    "landuse_culture_area_sqm": m_known(lu_by_group["culture"], "sqm",
                                        ["geometry/land_use.geojson"],
                                        "sum(area(land_use where code=0803))@EPSG:4548",
                                        "medium", [DESIGN_NOTE]),
    "landuse_green_open_area_sqm": m_known(lu_by_group["green_open"], "sqm",
                                           ["geometry/land_use.geojson"],
                                           "sum(area(land_use where code in 1401,1403))@EPSG:4548",
                                           "medium", [DESIGN_NOTE]),
    "landuse_reserved_white_area_sqm": m_known(lu_by_group["reserved_white"], "sqm",
                                               ["geometry/land_use.geojson"],
                                               "sum(area(land_use where code=16))@EPSG:4548",
                                               "medium", [DESIGN_NOTE]),
    "ai_scenario_card_count": m_known(12, "count", ["proposal.md"],
                                      "count(scenario cards in proposal)", "high"),
    "ai_test_validation_scenario_count": m_known(3, "count", ["proposal.md"],
                                                 "count(test/validation scenario cards)",
                                                 "high"),
    "persona_type_count": m_known(6, "count", ["proposal.md"],
                                  "count(user personas in proposal)", "high"),
    "ai_landmark_count": m_known(5, "count",
                                 ["proposal.md", "geometry/public_space.geojson"],
                                 "count(AI pilgrimage landmarks)", "high"),
    "ecosystem_case_count": m_known(6, "count", ["proposal.md"],
                                    "count(global AI ecosystem case studies)", "high"),
    "floor_area_ratio": m_unknown("ratio",
                                  "法定容积率控制指标缺失（控规条件未公开），不得虚构。",
                                  SB, "official_far(pending)"),
    "building_height_control_m": m_unknown("m",
                                           "官方高度管控缺失（含航空/景观/文保限高），不得虚构。"),
    "road_area_sqm": m_unknown("sqm", "道路红线数据缺失，道路用地面积无法复算。"),
}
out = {"schema_version": "0.1.0", "units": {"length": "m", "area": "sqm"},
       "metrics": metrics}
(SUB / "metrics.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                                  encoding="utf-8")
print(f"metrics: site={site_area:,.0f} green={green_area/site_area:.3f} "
      f"pub={pub_area/site_area:.4f} bldg={bldg_area:,.0f} floor={total_floor:,.0f} "
      f"roads={road_len/1000:.1f}km")
