"""
测试皮带长度计算，对比目标值 1370.25
"""
import sys
sys.path.insert(0, '/workspace/backend')

from app.services.gear_base import GearBaseService

# 前端默认测试数据
pulleys = [
    {'code': 'FAN', 'name': 'FAN', 'type': 'groove', 'x': 0,    'y': 0,     'groove_dia': 194, 'flat_dia': None},
    {'code': 'ALT', 'name': 'ALT', 'type': 'groove', 'x': 250,  'y': -80,    'groove_dia': 75,  'flat_dia': None},
    {'code': 'AC',  'name': 'AC',  'type': 'groove', 'x': 268,  'y': 132.5,  'groove_dia': 110, 'flat_dia': None},
    {'code': 'TEN', 'name': 'TEN', 'type': 'flat',   'x': 171.42,'y': 17.35,  'groove_dia': None,'flat_dia': 70},
]

# 测试不同 belt/lining 组合
configs = [
    ('belt=1.5, lining=0.99 (前端默认)', 1.5, 0.99),
    ('belt=1.2, lining=1.0  (代码默认)', 1.2, 1.0),
    ('belt=4.4, lining=1.0  (旧默认)',   4.4, 1.0),
    ('belt=1.5, lining=0.8  (4.6=2*(1.5+0.8))', 1.5, 0.8),
]

target = 1370.25
print(f'目标值: {target}')
print('='*80)

for desc, bt, lt in configs:
    svc = GearBaseService(belt_thickness=bt, lining_thickness=lt)
    res = svc.calc_belt_length(pulleys)
    diff = res['belt_length'] - target
    print(f'\n[{desc}]')
    print(f'  belt_length = {res["belt_length"]}  (差 {diff:+.4f})')
    print(f'  total_straight = {res["total_straight"]}, total_arc = {res["total_arc"]}')
    print('  详细数据:')
    for d in res['details']:
        print(f'    {d["code"]:5s} type={d["type"]:6s} K={d["pitch_diameter"]:.4f} '
              f'C={d["center_dist"]:.4f} E={d["upper_tangent_angle"]:.4f} '
              f'G={d["lower_tangent_angle"]:.4f} I={d["cumulative_angle"]:.4f} '
              f'S={d["wrap_angle"]:.4f} Q={d["tangent_length"]:.4f} arc={d["arc_length"]:.4f}')
