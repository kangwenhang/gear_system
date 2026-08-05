"""
反向求解：找让 belt_length = 1370.25 的 TEN 的 K 值
"""
import sys
sys.path.insert(0, '/workspace/backend')

from app.services.gear_base import GearBaseService

pulleys = [
    {'code': 'FAN', 'name': 'FAN', 'type': 'groove', 'x': 0,    'y': 0,     'groove_dia': 194, 'flat_dia': None},
    {'code': 'ALT', 'name': 'ALT', 'type': 'groove', 'x': 250,  'y': -80,    'groove_dia': 75,  'flat_dia': None},
    {'code': 'AC',  'name': 'AC',  'type': 'groove', 'x': 268,  'y': 132.5,  'groove_dia': 110, 'flat_dia': None},
    {'code': 'TEN', 'name': 'TEN', 'type': 'flat',   'x': 171.42,'y': 17.35,  'groove_dia': None,'flat_dia': 70},
]

target = 1370.25
svc = GearBaseService(belt_thickness=1.5, lining_thickness=0.99)

# 重写 calc_pitch_diameter 用静态 K 表，方便扫描
orig = svc.calc_pitch_diameter
def make_k_override(k_ten):
    def f(p):
        if p.get('code') == 'TEN':
            return k_ten
        return orig(p)
    return f

# 二分搜索 K_TEN
lo, hi = 60.0, 90.0
for _ in range(60):
    mid = (lo + hi) / 2
    svc.calc_pitch_diameter = make_k_override(mid)
    L = svc.calc_belt_length_raw(pulleys)
    if L < target:
        lo = mid
    else:
        hi = mid

k_target = (lo + hi) / 2
print(f'目标 belt_length = {target}')
print(f'所需 TEN K = {k_target:.4f}')
print(f'  = 70 + {k_target - 70:.4f}')

# 测试几个候选公式
print('\n候选 K 公式（flat, dia=70）:')
candidates = [
    ('旧: 70 + 4.6', 70 + 4.6),
    ('新: 70 + 2*(1.5+0.99) + 4.6', 70 + 2*(1.5+0.99) + 4.6),
    ('70 + 2*(1.2+1.0) + 4.6 (Excel 参数)', 70 + 2*(1.2+1.0) + 4.6),
    ('70 + 2*(1.5+0.99) (无4.6)', 70 + 2*(1.5+0.99)),
    ('70 + 2*1.5 + 0.99 (混合)', 70 + 2*1.5 + 0.99),
    ('70 + 2*0.99 + 4.6 (只lining+4.6)', 70 + 2*0.99 + 4.6),
    ('70 + 2*1.5 + 4.6 (只belt+4.6)', 70 + 2*1.5 + 4.6),
    ('70 + 2.4 + 0.83', 70 + 2.4 + 0.83),
]
for desc, k in candidates:
    svc.calc_pitch_diameter = make_k_override(k)
    L = svc.calc_belt_length_raw(pulleys)
    print(f'  K={k:.4f}  →  L={L:.4f}  (差 {L-target:+.4f})  [{desc}]')

svc.calc_pitch_diameter = orig
