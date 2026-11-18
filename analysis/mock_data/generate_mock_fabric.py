"""섬유 메커니즘 기반 모의 직물 데이터 생성기 (설명·파이프라인 시험용)

사슬: 소재(섬유) → 실 → 직물 구조(제직·편직·부직) → 물성 19항목(X) → 전기 특성 Y(마찰전기)
- 구조 계산: Peirce(1937) 직물 기하, 커버 팩터, Munden(1959) 편직 상수, 부직포 고형률
- 물성: 굽힘 ∝ E·섬도, 압축은 van Wyk 계열(공극이 클수록 압축 일 큼), 마찰은 Howell형 F = a·N^n
- Y: 접촉-분리형 TENG 이론(Niu 2013) Voc = σ·x/ε0, Q = σ·S, 평균 전류 = 2·Q·f
      σ_eff = σ0 · (대전 서열 차) · (실접촉 비율) · (습도 계수)
모든 계수는 문헌의 '방향'과 대표값을 따른 가정이며, 실측 원단으로 보정해야 한다.
이 데이터로 얻은 관계는 넣은 가정을 되찾는 것일 뿐 연구 결과가 아니다.

사용: python3 generate_mock_fabric.py [n_per_cell] [seed] [out_dir]
"""
import json, math, os, sys
import numpy as np
import pandas as pd

VERSION = "1.0 (2026-11-18)"

# ---------------- 0. 소재(섬유) 대표값 ----------------
# rho 밀도 g/cm3, regain 표준 수분율 %, E 섬유 탄성률 GPa, tribo 대전 서열 상대 점수(+ 양전하 경향),
# resil 압축 회복 경향(0~1), mu0 기준 마찰계수, kth 상대 열 전달(냉온감) 계수, dfib 섬유 지름 μm
MATERIALS = {
    "cotton":    dict(ko="면",          rho=1.52, regain=8.5,  E=8.0,  tribo=+0.20, resil=0.45, mu0=0.30, kth=1.00, dfib=15),
    "polyester": dict(ko="폴리에스터",  rho=1.38, regain=0.4,  E=10.0, tribo=-0.50, resil=0.65, mu0=0.25, kth=0.80, dfib=13),
    "nylon":     dict(ko="나일론",      rho=1.14, regain=4.5,  E=3.0,  tribo=+0.80, resil=0.80, mu0=0.28, kth=0.85, dfib=14),
    "wool":      dict(ko="울",          rho=1.31, regain=16.0, E=3.0,  tribo=+0.50, resil=0.85, mu0=0.35, kth=0.75, dfib=20),
    "pp":        dict(ko="폴리프로필렌", rho=0.91, regain=0.05, E=4.0,  tribo=-0.80, resil=0.75, mu0=0.22, kth=0.70, dfib=18),
}
COUNTER = dict(name="PTFE 필름", tribo=-1.00)   # 상대 전극 물질(측정 프로토콜에서 고정)

# ---------------- 0. 구조(제작 방법) ----------------
# float 뜬 길이(교차 사이 실 수), surf 실-실 접촉 표면 계수, Kmin/Kmax 경·위 커버 팩터 합 범위(SI), jam 한계
STRUCTURES = {
    "plain":    dict(ko="평직",           kind="woven",    float=1, surf=1.00, Kmin=20, Kmax=28, jam=32, interl=1.0),
    "twill22":  dict(ko="능직 2/2",       kind="woven",    float=2, surf=1.25, Kmin=22, Kmax=32, jam=36, interl=0.5),
    "hopsack22":dict(ko="호프색 2/2",     kind="woven",    float=2, surf=1.30, Kmin=22, Kmax=32, jam=36, interl=0.5),
    "jersey":   dict(ko="싱글 저지(편직)", kind="knit",     float=1, surf=1.15),
    "needle":   dict(ko="니들펀치 부직포", kind="nonwoven", float=0, surf=0.90),
}

PROTOCOL = dict(gap_mm=1.0, area_cm2=25.0, freq_hz=2.0, pressure_kpa=5.0, rh_mean=65.0, rh_sd=2.0, repeats=3)
EPS0 = 8.854e-12
SIGMA0_UC = 0.55      # 규모 계수 μC/m² — 실측 첫 원단들로 보정
SRA_OPT = 45.0        # 실접촉에 가장 유리한 거칠기 μm (역U자 꼭짓점, 가정 — 실측으로 보정)

ITEMS = ["W", "SFC_F", "SFC_B", "SRA_F", "SRA_B", "SRW_F", "SRW_B", "BAR_F", "BAR_B",
         "BW_FL", "BW_FC", "BW_BL", "BW_BC", "CW_F", "CW_B", "CRR_F", "CRR_B", "Qmax_F", "Qmax_B"]


def yarn_diameter_mm(tex, rho, packing=0.6):
    """실 지름: 단면적 = 선밀도 / (섬유 밀도 × 충전율). tex = g/km"""
    area_cm2 = tex * 1e-5 / (rho * packing)
    return math.sqrt(4 * area_cm2 / math.pi) * 10.0


def structure(d):
    """설계 인자 d → 구조량(지름, 밀도, 두께, 평량, 충전율 등). 잡음 없음."""
    m, s = MATERIALS[d["material"]], STRUCTURES[d["structure"]]
    out = {}
    if s["kind"] == "woven":
        tex = d["tex"]; dy = yarn_diameter_mm(tex, m["rho"])
        Kt = d["cover"]                       # 경+위 커버 팩터 합 (SI: 올/cm × √tex / 10)
        K1 = Kt * d["warp_share"]; K2 = Kt - K1
        epc = K1 * 10 / math.sqrt(tex); ppc = K2 * 10 / math.sqrt(tex)
        p1, p2 = 10.0 / epc, 10.0 / ppc       # 실 간격 mm
        # Peirce 기하 근사: 굴곡률 ∝ (지름/간격)^2 × 교차 비율
        c1 = 0.9 * s["interl"] * (dy / p2) ** 2; c2 = 0.9 * s["interl"] * (dy / p1) ** 2
        gsm = (epc * tex * (1 + c1) + ppc * tex * (1 + c2)) / 10.0
        t = 2 * dy * (1.0 + 0.12 * (s["float"] - 1))
        srw = p1 * s["float"]                 # 표면 요철 주기 ≈ 실 간격 × 뜬 길이
        sra_base = dy * 1000 * 0.18 * (1 + 0.6 * (s["float"] - 1)) * (1 - 0.35 * min(Kt / s["jam"], 1))
        dens_L, dens_C = epc, ppc
        out.update(epc=epc, ppc=ppc, crimp_warp=c1, crimp_weft=c2, cover=Kt, jam_ratio=Kt / s["jam"])
    elif s["kind"] == "knit":
        tex = d["tex"]; dy = yarn_diameter_mm(tex, m["rho"])
        l_mm = math.sqrt(tex) / d["tf"]       # 조임 계수 TF = √tex / 루프 길이(mm)
        Kc, Kw = d["kc"], d["kw"]             # Munden 상수 (건조 이완 상태 대표값)
        cpc, wpc = Kc / (l_mm / 10), Kw / (l_mm / 10)
        S = cpc * wpc
        gsm = S * (l_mm / 10) * tex / 10.0
        t = 2.2 * dy
        srw = 10.0 / wpc
        sra_base = dy * 1000 * 0.22
        dens_L, dens_C = wpc, cpc
        out.update(loop_mm=l_mm, cpc=cpc, wpc=wpc, tf=d["tf"])
    else:  # 부직포
        tex = None; dy = m["dfib"] / 1000.0
        gsm = d["gsm"]; sol = d["solidity"]
        t = gsm / (m["rho"] * sol * 1000.0)
        srw = 0.8 + 3 * (1 - sol)              # 무작위 섬유망: 짧고 넓게 퍼진 요철
        sra_base = 6 + 60 * (1 - sol) * (m["dfib"] / 15)
        dens_L, dens_C = 1.3, 1.0              # MD/CD 섬유 배향 비
        out.update(solidity=sol)
    phi = gsm / (t * m["rho"] * 1000.0)        # 직물 충전율(섬유가 차지하는 부피 비)
    out.update(kind=s["kind"], yarn_d_mm=dy, gsm=gsm, thick_mm=t, phi=phi, srw_base=srw,
               sra_base=sra_base, dens_L=dens_L, dens_C=dens_C)
    return out


def properties(d, st):
    """구조 → 물성 19항목 (원단 간 변동 잡음 없음, '참값')."""
    m, s = MATERIALS[d["material"]], STRUCTURES[d["structure"]]
    k = st["kind"]
    # 앞·뒤 차이: 능직·호프색은 앞면에 뜬 실이 많음, 편직 뒷면(퍼얼)은 더 거칠다
    fb_sra = {"woven": (1.0 + 0.15 * (s["float"] - 1), 1.0 - 0.10 * (s["float"] - 1)), "knit": (0.85, 1.30), "nonwoven": (1.0, 1.10)}[k]
    sra_f, sra_b = st["sra_base"] * fb_sra[0], st["sra_base"] * fb_sra[1]
    srw_f = st["srw_base"]; srw_b = st["srw_base"] * (1.15 if k == "knit" else 1.0)
    # 마찰: Howell형 F = a·N^n → 측정 하중에서의 μ. 거칠기가 클수록 맞물림이 커진다(로그 효과)
    mu = lambda sra: m["mu0"] * (1 + 0.25 * math.log(max(sra, 1) / 20.0))
    # 굽힘: 실 굽힘 강성 ∝ E × (섬유 단면 관성 합 ∝ tex × 섬유 지름²) × 폭당 실 수, 교차가 적을수록 유연
    if k == "nonwoven":
        b0 = m["E"] * (m["dfib"] / 15) ** 2 * st["gsm"] / 100 * (0.6 + 2.0 * st["solidity"])
    else:
        b0 = m["E"] * d["tex"] / 20 * (m["dfib"] / 15) ** 2 * (1.0 if k == "woven" else 0.45)
    if k == "woven":
        bL = b0 * st["dens_L"] / 25 * (1.0 if s["float"] == 1 else 0.80)
        bC = b0 * st["dens_C"] / 25 * (1.0 if s["float"] == 1 else 0.80)
    elif k == "knit":
        bL, bC = b0 * 1.5 * st["dens_L"] / 12, b0 * st["dens_C"] / 15
    else:
        bL, bC = b0 * st["dens_L"], b0 * st["dens_C"]
    bar = (bL + bC) / 2
    # 압축: van Wyk 계열 — 공극(1-φ)이 크고 섬유가 유연할수록 압축 일이 크다
    cw = 0.9 * st["thick_mm"] * (1 - st["phi"]) ** 2 * (10 / (m["E"] + 2)) ** 0.3
    crr = 100 * (0.25 + 0.55 * m["resil"]) * {"woven": 0.95, "knit": 1.05, "nonwoven": 0.85}[k]
    # 접촉 냉온감 Qmax: 충전율·열 전달 클수록, 거칠수록(접촉 면적 작음) 작다
    q = lambda sra: 0.18 * m["kth"] * math.sqrt(st["phi"]) * (1 - 0.25 * math.log(max(sra, 1) / 10) / math.log(10)) * (1 + 0.02 * m["regain"])
    v = dict(W=st["gsm"], SFC_F=mu(sra_f), SFC_B=mu(sra_b), SRA_F=sra_f, SRA_B=sra_b, SRW_F=srw_f, SRW_B=srw_b,
             BAR_F=bar, BAR_B=bar * (1.08 if k == "knit" else 1.0),
             BW_FL=bL * 0.9, BW_FC=bC * 0.9, BW_BL=bL * 0.9 * (1.05 if k == "knit" else 1.0), BW_BC=bC * 0.9,
             CW_F=cw, CW_B=cw * (1.05 if k == "knit" else 1.0), CRR_F=crr, CRR_B=crr * (0.97 if k == "knit" else 1.0),
             Qmax_F=q(sra_f), Qmax_B=q(sra_b))
    return v


def electrical(d, st, v, rh):
    """물성·구조 → 마찰전기 특성 Y (접촉-분리형, 상대 전극 PTFE). 잡음 없음."""
    m, s = MATERIALS[d["material"]], STRUCTURES[d["structure"]]
    P = PROTOCOL
    dtribo = m["tribo"] - COUNTER["tribo"]                       # 대전 서열 차이
    sra = (v["SRA_F"])
    g_rough = math.exp(-(math.log(sra / SRA_OPT)) ** 2 / (2 * 0.8 ** 2))   # 역U자: 적당한 요철이 실접촉에 유리
    pstar = 6.0 / (1 + 4 * v["CW_F"])                            # 압축이 쉬울수록 낮은 압력에서 포화
    contact = s["surf"] * g_rough * (1 - math.exp(-P["pressure_kpa"] / pstar))
    beta = 0.25 * (1 + m["regain"] / 10)                          # 흡습성 섬유일수록 습도에 민감
    hum = max(0.05, 1 - beta * (rh - 40) / 100)
    sigma_uc = SIGMA0_UC * dtribo * contact * hum                 # μC/m²
    sigma = sigma_uc * 1e-6
    voc = sigma * (P["gap_mm"] / 1000) / EPS0                     # V
    q_nc = sigma * (P["area_cm2"] * 1e-4) * 1e9                   # nC
    i_avg_na = 2 * q_nc * P["freq_hz"]                            # nA (반주기마다 Q가 한 번 이동)
    return dict(sigma_uCm2=sigma_uc, Voc_V=voc, Qsc_nC=q_nc, Iavg_nA=i_avg_na, contact_index=contact, hum_factor=hum)


def sample_designs(n_per_cell, rng):
    """소재 × 구조 칸마다 라틴 하이퍼큐브로 연속 인자를 뽑는다."""
    def lhs(n, k):
        u = (np.argsort(rng.random((k, n)), axis=1).T + rng.random((n, k))) / n
        return u
    rows = []
    for mat in MATERIALS:
        for stc, s in STRUCTURES.items():
            U = lhs(n_per_cell, 4)
            for u in U:
                d = dict(material=mat, structure=stc)
                if s["kind"] == "woven":
                    d.update(tex=10 + 40 * u[0], cover=s["Kmin"] + (s["Kmax"] - s["Kmin"]) * u[1], warp_share=0.45 + 0.15 * u[2])
                elif s["kind"] == "knit":
                    d.update(tex=10 + 30 * u[0], tf=1.2 + 0.5 * u[1], kc=4.8 + 0.6 * u[2], kw=3.8 + 0.5 * u[3])
                else:
                    d.update(gsm=40 + 160 * u[0], solidity=0.06 + 0.14 * u[1])
                rows.append(d)
    return rows


def feasible(d, st):
    s = STRUCTURES[d["structure"]]
    if st["kind"] == "woven":
        return st["jam_ratio"] <= 0.98
    if st["kind"] == "knit":
        return 1.15 <= st["tf"] <= 1.75
    return 0.03 <= st["phi"] <= 0.30


def generate(n_per_cell=20, seed=20261118):
    rng = np.random.default_rng(seed)
    P = PROTOCOL
    rows = []
    for i, d in enumerate(sample_designs(n_per_cell, rng)):
        st = structure(d)
        if not feasible(d, st):
            continue
        v_true = properties(d, st)
        # (1) 원단 간 변동: 식이 다 설명하지 못하는 몫 (CV 6%)
        v_fab = {k: x * math.exp(rng.normal(0, 0.06)) for k, x in v_true.items()}
        # (2) 측정 반복 오차: 물성 CV 4%, 반복 3회 평균
        v_meas = {k: float(np.mean([x * math.exp(rng.normal(0, 0.04)) for _ in range(P["repeats"])])) for k, x in v_fab.items()}
        rh = float(rng.normal(P["rh_mean"], P["rh_sd"]))
        y_true = electrical(d, st, v_fab, rh)
        # 전기 특성 측정은 더 흔들린다: 반복 CV 12%
        reps = [y_true["Voc_V"] * math.exp(rng.normal(0, 0.12)) for _ in range(P["repeats"])]
        k = y_true["Voc_V"] and np.mean(reps) / y_true["Voc_V"]
        row = dict(fabric_id=f"M{i+1:04d}", material=d["material"], material_ko=MATERIALS[d["material"]]["ko"],
                   structure=d["structure"], structure_ko=STRUCTURES[d["structure"]]["ko"], kind=st["kind"],
                   tex=d.get("tex"), cover=d.get("cover"), warp_share=d.get("warp_share"), tf=d.get("tf"),
                   gsm_design=d.get("gsm"), solidity=d.get("solidity"),
                   yarn_d_mm=st["yarn_d_mm"], thick_mm=st["thick_mm"], phi=st["phi"],
                   epc=st.get("epc"), ppc=st.get("ppc"), cpc=st.get("cpc"), wpc=st.get("wpc"), loop_mm=st.get("loop_mm"),
                   rh=rh)
        row.update({k2: v_meas[k2] for k2 in ITEMS})
        row.update(Voc_V=float(np.mean(reps)), Voc_cv=float(np.std(reps, ddof=1) / np.mean(reps)),
                   Qsc_nC=y_true["Qsc_nC"] * k, Iavg_nA=y_true["Iavg_nA"] * k, sigma_uCm2=y_true["sigma_uCm2"] * k,
                   contact_index=y_true["contact_index"], hum_factor=y_true["hum_factor"], is_mock=True)
        rows.append(row)
    return pd.DataFrame(rows)


def dictionary():
    return dict(version=VERSION, materials=MATERIALS, structures=STRUCTURES, counter=COUNTER, protocol=PROTOCOL,
                sigma0_uCm2=SIGMA0_UC, sra_opt_um=SRA_OPT, items=ITEMS,
                note="모든 계수는 문헌 방향을 따른 가정값. 실측으로 보정 전에는 결과 해석 금지. is_mock=True 열로 실측과 구분.")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261118
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.dirname(os.path.abspath(__file__))
    df = generate(n, seed)
    df.to_csv(os.path.join(out, "mock_fabric_data.csv"), index=False, encoding="utf-8-sig", float_format="%.5g")
    json.dump(dictionary(), open(os.path.join(out, "mock_fabric_dictionary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(df)} rows · seed {seed} · {VERSION}")
