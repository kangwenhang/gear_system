import math
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

router = APIRouter()


class PulleyItem(BaseModel):
    code: str
    name: str = ""
    type: str  # 'groove' or 'flat'
    x: Optional[float] = None
    y: Optional[float] = None
    groove_dia: Optional[float] = None
    flat_dia: Optional[float] = None
    centerHeightDiff: Optional[float] = 0  # S
    perpendicularity: Optional[float] = 0  # T
    tiltAngle: Optional[str] = ""  # 用户输入的倾斜方向


class ContactParamsRequest(BaseModel):
    pulleys: List[PulleyItem]
    pitch_to_effective: float = 0.99  # C4
    flat_to_pitch: float = 1.5  # C5


class AlignmentRequest(BaseModel):
    pulleys: List[PulleyItem]
    contact_params: Dict[str, Dict[str, float]]  # {code: {K, J, L, M, N, P, O, Q, U}}


def deg2rad(deg):
    return deg * math.pi / 180.0


# ========== Contact 参数计算 ==========

def calc_contact_params(pulleys, c4, c5):
    """计算 Contact 参数 K/J/L/M/N/P/O/Q/U"""
    lst = [p for p in pulleys if p.get('code') and p.get('x') is not None and p.get('y') is not None]
    n = len(lst)
    if n < 2:
        return {}

    K = [0] * n
    J = [0] * n
    L = [0] * n
    M = [0] * n
    N = [0] * n
    P = [0] * n
    O = [0] * n
    Q = [0] * n
    U = [0] * n

    # 第一遍: K, J, L
    for i in range(n):
        p = lst[i]
        is_groove = p['type'] == 'groove'
        K[i] = 1 if is_groove else -1
        J[i] = (float(p.get('groove_dia') or 0) + 0.99) if is_groove else float(p.get('flat_dia') or 0)
        L[i] = J[i] + 2 * (c4 if is_groove else c5)

    # 第二遍: M, N, P
    for i in range(n):
        curr = lst[i]
        next_idx = (i + 1) % n
        next_p = lst[next_idx]
        first = lst[0]

        if i == n - 1:
            target = first
            target_idx = 0
        else:
            target = next_p
            target_idx = next_idx

        dx = float(target.get('x') or 0) - float(curr.get('x') or 0)
        dy = float(target.get('y') or 0) - float(curr.get('y') or 0)
        M[i] = math.sqrt(dx * dx + dy * dy)

        half_diff = K[target_idx] * L[target_idx] / 2 - K[i] * L[i] / 2
        n_sq = M[i] * M[i] - half_diff * half_diff
        N[i] = math.sqrt(max(0, n_sq))

        # baseAngle
        if float(target.get('y') or 0) == float(curr.get('y') or 0) and float(target.get('x') or 0) != float(curr.get('x') or 0):
            base_angle = math.pi if float(target.get('x') or 0) < float(curr.get('x') or 0) else 0
        else:
            base_angle = math.acos(max(-1, min(1, dx / M[i]))) * (1 if dy >= 0 else -1)

        # signTerm
        kl = K[i] * K[target_idx]
        abs_half = abs(K[i] * L[i] / 2 - K[target_idx] * L[target_idx] / 2)
        ratio = max(-1, min(1, abs_half / M[i])) if M[i] > 0 else 0

        if kl > 0:
            if L[i] < L[target_idx]:
                acos_val = math.pi - math.acos(ratio)
            else:
                acos_val = math.acos(ratio)
        else:
            acos_val = math.acos(ratio)

        sign_term = K[i] * acos_val
        P[i] = (base_angle - sign_term) * 180 / math.pi

    # O
    O[0] = P[n - 1] + (0 if K[0] == K[n - 1] else 180)
    for i in range(1, n):
        O[i] = P[i - 1] + (0 if K[i] == K[i - 1] else 180)

    # Q
    for i in range(n):
        Q[i] = ((K[i] * (P[i] - O[i])) % 360 + 360) % 360

    # U
    for i in range(n):
        if K[i] == 1:
            U[i] = O[i] - 180 + Q[i] / 2
        else:
            U[i] = O[i] - Q[i] / 2 - 180

    result = {}
    for i in range(n):
        code = lst[i].get('code') or f'p{i}'
        result[code] = {
            'K': K[i], 'J': J[i], 'L': L[i], 'M': M[i],
            'N': N[i], 'P': P[i], 'O': O[i], 'Q': Q[i], 'U': U[i]
        }
    return result


# ========== 对齐度计算辅助函数 ==========

def get_u(pulley, contact_params):
    """获取U值：优先用户输入，否则用计算值"""
    cp = contact_params.get(pulley['code'])
    if not cp:
        return 0
    tilt = pulley.get('tiltAngle', '')
    if tilt != '' and tilt is not None:
        try:
            return float(tilt)
        except (ValueError, TypeError):
            pass
    return cp.get('U', 0)


def calc_v(pulley, contact_params):
    cp = contact_params.get(pulley['code'])
    if not cp:
        return 0
    T = float(pulley.get('perpendicularity') or 0)
    U = get_u(pulley, contact_params)
    P = cp['P']
    return T * (math.sin(deg2rad(P)) * math.sin(deg2rad(U)) + math.cos(deg2rad(P)) * math.cos(deg2rad(U)))


def calc_w(pulley, contact_params):
    cp = contact_params.get(pulley['code'])
    if not cp:
        return 0
    T = float(pulley.get('perpendicularity') or 0)
    U = get_u(pulley, contact_params)
    O = cp['O']
    return T * (math.sin(deg2rad(O)) * math.sin(deg2rad(U)) + math.cos(deg2rad(O)) * math.cos(deg2rad(U)))


def calc_x(pulley, contact_params):
    cp = contact_params.get(pulley['code'])
    if not cp:
        return 0
    T = float(pulley.get('perpendicularity') or 0)
    U = get_u(pulley, contact_params)
    P = cp['P']
    return T * (-math.cos(deg2rad(P)) * math.sin(deg2rad(U)) + math.sin(deg2rad(P)) * math.cos(deg2rad(U)))


def calc_y(pulley, contact_params):
    cp = contact_params.get(pulley['code'])
    if not cp:
        return 0
    T = float(pulley.get('perpendicularity') or 0)
    U = get_u(pulley, contact_params)
    O = cp['O']
    return T * (-math.cos(deg2rad(O)) * math.sin(deg2rad(U)) + math.sin(deg2rad(O)) * math.cos(deg2rad(U)))


def calc_twist_display(pulley, pulleys_list, contact_params):
    cp = contact_params.get(pulley['code'])
    if not cp:
        return None
    V_i = calc_v(pulley, contact_params)
    K_i = cp['K']
    idx = -1
    for i, item in enumerate(pulleys_list):
        if item['code'] == pulley['code']:
            idx = i
            break
    if idx == -1:
        return None
    next_idx = (idx + 1) % len(pulleys_list)
    next_pulley = pulleys_list[next_idx]
    cp_next = contact_params.get(next_pulley['code'])
    if not cp_next:
        return None
    W_next = calc_w(next_pulley, contact_params)
    K_next = cp_next['K']
    return V_i * K_i - W_next * K_next


def calc_flat_offset(flat_pulley, next_groove, contact_params):
    cp_flat = contact_params.get(flat_pulley['code'])
    cp_next = contact_params.get(next_groove['code'])
    if not cp_flat or not cp_next:
        return {'value': 0, 'debug': []}
    S_next = float(next_groove.get('centerHeightDiff') or 0)
    N_flat = cp_flat['N']
    X_flat = calc_x(flat_pulley, contact_params)
    X_flat_rad = X_flat * math.pi / 180
    L_flat = cp_flat['L']
    V_flat = calc_v(flat_pulley, contact_params)
    L_next = cp_next['L']
    W_next = calc_w(next_groove, contact_params)
    result = S_next + N_flat * math.sin(X_flat_rad) + L_flat / 2 * math.sin(deg2rad(V_flat)) - L_next / 2 * math.sin(deg2rad(W_next))
    return {
        'value': result,
        'debug': [
            {'name': 'S_next', 'value': S_next, 'desc': '下一个槽轮的中心高'},
            {'name': 'N_flat', 'value': N_flat, 'desc': '平轮的N值（跨段长）'},
            {'name': 'X_flat', 'value': X_flat, 'desc': '平轮的X值（Entry侧倾斜）'},
            {'name': 'X_flat_rad', 'value': X_flat_rad, 'desc': '平轮X_flat（弧度）'},
            {'name': 'L_flat', 'value': L_flat, 'desc': '平轮的L值'},
            {'name': 'V_flat', 'value': V_flat, 'desc': '平轮的V值（Entry侧Camber）'},
            {'name': 'L_next', 'value': L_next, 'desc': '下一个槽轮的L值'},
            {'name': 'W_next', 'value': W_next, 'desc': '下一个槽轮的W值（Exit侧Camber）'},
            {'name': 'N_flat*sin(X_flat)', 'value': N_flat * math.sin(X_flat_rad), 'desc': '平轮倾斜角偏移量'},
            {'name': 'L_flat/2*sin(V_flat)', 'value': L_flat / 2 * math.sin(deg2rad(V_flat)), 'desc': '平轮Entry侧偏移'},
            {'name': 'L_next/2*sin(W_next)', 'value': L_next / 2 * math.sin(deg2rad(W_next)), 'desc': '下一个槽轮Exit侧偏移'},
            {'name': 'AB(Offset)', 'value': result, 'desc': '平轮Offset = S_next + N_flat*sin(X_flat) + L_flat/2*sin(V_flat) - L_next/2*sin(W_next)'},
        ]
    }


def calc_alignment_pairs(pulleys_list, contact_params):
    """计算对齐度结果（带轮对）"""
    lst = pulleys_list
    if len(lst) < 2:
        return []

    groove_indices = []
    for i, p in enumerate(lst):
        if p['type'] == 'groove':
            groove_indices.append(i)
    if len(groove_indices) < 2:
        return []

    pairs = []
    for i in range(len(groove_indices)):
        curr_idx = groove_indices[i]
        next_idx = groove_indices[(i + 1) % len(groove_indices)]
        curr = lst[curr_idx]
        next_p = lst[next_idx]

        # 收集中间轮
        middle_pulleys = []
        j = (curr_idx + 1) % len(lst)
        while j != next_idx:
            middle_pulleys.append({'pulley': lst[j], 'index': j})
            j = (j + 1) % len(lst)

        cp_curr = contact_params.get(curr['code'])
        cp_next = contact_params.get(next_p['code'])
        if not cp_curr or not cp_next:
            continue

        if len(middle_pulleys) == 0:
            # 槽轮-槽轮
            S1 = float(curr.get('centerHeightDiff') or 0)
            S2 = float(next_p.get('centerHeightDiff') or 0)
            L1 = cp_curr['L']
            L2 = cp_next['L']
            V1 = calc_v(curr, contact_params)
            W2 = calc_w(next_p, contact_params)
            N = cp_curr['N']
            X = calc_x(curr, contact_params)
            K1 = cp_curr['K']
            K2 = cp_next['K']

            eff_y1 = S1 - L1 / 2 * math.sin(deg2rad(V1))
            eff_y2 = S2 - L2 / 2 * math.sin(deg2rad(W2))
            bea = math.atan((eff_y2 - eff_y1) / N) * 180 / math.pi - X if N > 0.001 else 0
            twist = K1 * V1 - K2 * W2

            debug = [
                {'name': 'S1', 'value': S1, 'desc': '当前槽轮中心高'},
                {'name': 'S2', 'value': S2, 'desc': '下一个槽轮中心高'},
                {'name': 'L1', 'value': L1, 'desc': '当前槽轮L值'},
                {'name': 'L2', 'value': L2, 'desc': '下一个槽轮L值'},
                {'name': 'V1', 'value': V1, 'desc': '当前槽轮V值（Entry侧Camber）'},
                {'name': 'W2', 'value': W2, 'desc': '下一个槽轮W值（Exit侧Camber）'},
                {'name': 'N', 'value': N, 'desc': '跨段长N'},
                {'name': 'X (curr槽轮倾斜角)', 'value': X, 'desc': '当前槽轮X列值（倾斜角）'},
                {'name': 'K1', 'value': K1, 'desc': '当前槽轮K值'},
                {'name': 'K2', 'value': K2, 'desc': '下一个槽轮K值'},
                {'name': 'effY1 = S1 - L1/2*sin(V1)', 'value': eff_y1, 'desc': '当前槽轮有效Y位置'},
                {'name': 'effY2 = S2 - L2/2*sin(W2)', 'value': eff_y2, 'desc': '下一个槽轮有效Y位置'},
                {'name': 'BEA = atan((effY2-effY1)/N)*180/PI - X', 'value': bea, 'desc': '切入角BEA'},
                {'name': 'Twist = K1*V1 - K2*W2', 'value': twist, 'desc': '扭转角Twist'},
            ]

            pairs.append({
                'type': 'groove-groove',
                'fromCode': curr.get('code') or '--',
                'toCode': next_p.get('code') or '--',
                'middleCode': None,
                'bea': bea,
                'twist': twist,
                'offset': None,
                'debug': debug
            })

        elif len(middle_pulleys) == 1 and middle_pulleys[0]['pulley']['type'] == 'flat':
            # 槽轮-平轮-槽轮
            mid = middle_pulleys[0]['pulley']
            cp_mid = contact_params.get(mid['code'])
            if not cp_mid:
                continue

            offset_result = calc_flat_offset(mid, next_p, contact_params)
            AB = offset_result['value']
            S1 = float(curr.get('centerHeightDiff') or 0)
            L1 = cp_curr['L']
            V1 = calc_v(curr, contact_params)
            L_mid = cp_mid['L']
            W_mid = calc_w(mid, contact_params)
            N = cp_curr['N']
            X = calc_x(curr, contact_params)
            K1 = cp_curr['K']
            K_mid = cp_mid['K']

            eff_y1 = S1 - L1 / 2 * math.sin(deg2rad(V1))
            eff_y2 = AB - L_mid / 2 * math.sin(deg2rad(W_mid))
            bea = math.atan((eff_y2 - eff_y1) / N) * 180 / math.pi - X if N > 0.001 else 0
            twist = K1 * V1 - K_mid * W_mid

            offset_debug = [{'name': 'Offset_' + d['name'], 'value': d['value'], 'desc': d['desc']} for d in offset_result['debug']]
            debug = [
                {'name': 'S1 (curr槽轮中心高)', 'value': S1, 'desc': '第一个槽轮（curr）的中心高'},
                {'name': 'L1 (curr槽轮L)', 'value': L1, 'desc': '第一个槽轮的L值'},
                {'name': 'V1 (curr槽轮V)', 'value': V1, 'desc': '第一个槽轮的V值（Entry侧Camber）'},
                {'name': 'L_mid (平轮L)', 'value': L_mid, 'desc': '中间平轮的L值'},
                {'name': 'W_mid (平轮W)', 'value': W_mid, 'desc': '中间平轮的W值（Exit侧Camber）'},
                {'name': 'N (curr槽轮N)', 'value': N, 'desc': '第一个槽轮的N值（跨段长）'},
                {'name': 'X (curr槽轮倾斜角)', 'value': X, 'desc': '第一个槽轮X列值（倾斜角）'},
                {'name': 'K1 (curr槽轮K)', 'value': K1, 'desc': '第一个槽轮的K值'},
                {'name': 'K_mid (平轮K)', 'value': K_mid, 'desc': '中间平轮的K值'},
            ] + offset_debug + [
                {'name': 'effY1 = S1 - L1/2*sin(V1)', 'value': eff_y1, 'desc': '第一个槽轮侧有效Y位置'},
                {'name': 'effY2 = AB - L_mid/2*sin(W_mid)', 'value': eff_y2, 'desc': '平轮侧有效Y位置'},
                {'name': 'effY2 - effY1', 'value': eff_y2 - eff_y1, 'desc': '有效Y差值'},
                {'name': 'BEA = atan((effY2-effY1)/N)*180/PI - X', 'value': bea, 'desc': '切入角BEA'},
                {'name': 'Twist = K1*V1 - K_mid*W_mid', 'value': twist, 'desc': '扭转角Twist'},
            ]

            pairs.append({
                'type': 'groove-flat-groove',
                'fromCode': curr.get('code') or '--',
                'toCode': next_p.get('code') or '--',
                'middleCode': mid.get('code') or '--',
                'bea': bea,
                'twist': twist,
                'offset': AB,
                'debug': debug
            })

    return pairs


# ========== API 路由 ==========

@router.post("/calc-contact-params")
def api_calc_contact_params(req: ContactParamsRequest):
    try:
        pulleys_data = [p.model_dump() for p in req.pulleys]
        result = calc_contact_params(pulleys_data, req.pitch_to_effective, req.flat_to_pitch)
        return {"success": True, "contact_params": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calc-alignment")
def api_calc_alignment(req: AlignmentRequest):
    try:
        pulleys_data = [p.model_dump() for p in req.pulleys]
        contact_params = {k: dict(v) for k, v in req.contact_params.items()}

        # 计算每个带轮的 V/W/X/Y/Twist
        per_pulley = []
        for p in pulleys_data:
            cp = contact_params.get(p['code'], {})
            tilt = p.get('tiltAngle', '')
            u_from_input = False
            if tilt != '' and tilt is not None:
                try:
                    float(tilt)
                    u_from_input = True
                except (ValueError, TypeError):
                    pass
            per_pulley.append({
                'code': p['code'],
                'type': p['type'],
                'S': float(p.get('centerHeightDiff') or 0),
                'T': float(p.get('perpendicularity') or 0),
                'U': get_u(p, contact_params),
                'UFromInput': u_from_input,
                'K': cp.get('K'),
                'J': cp.get('J'),
                'L': cp.get('L'),
                'M': cp.get('M'),
                'N': cp.get('N'),
                'P': cp.get('P'),
                'O': cp.get('O'),
                'Q': cp.get('Q'),
                'V': calc_v(p, contact_params),
                'W': calc_w(p, contact_params),
                'X': calc_x(p, contact_params),
                'Y': calc_y(p, contact_params),
                'twist': calc_twist_display(p, pulleys_data, contact_params),
            })

        # 计算带轮对
        pairs = calc_alignment_pairs(pulleys_data, contact_params)

        return {
            "success": True,
            "per_pulley": per_pulley,
            "pairs": pairs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
