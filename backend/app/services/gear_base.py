"""
几何计算服务 - 基于Excel Geometry Sheet公式

皮带长度 = Σ(切线段长度) + Σ(包角弧长)
         = Σ(C_i × cos(E_i)) + Σ(S_i × K_i × π / 360)
"""

import math
from typing import List, Dict, Optional


class GearBaseService:
    """几何计算服务"""

    def __init__(self, belt_thickness: float = 4.4, lining_thickness: float = 1.0):
        self.belt_thickness = belt_thickness      # Input!H21 带厚
        self.lining_thickness = lining_thickness  # Input!H22 衬厚

    def calc_pitch_diameter(self, pulley: Dict) -> float:
        """
        计算节圆直径 K
        - 槽轮(Grooved): K = Input!G (groove_dia)
        - 平轮(Flat): K = G + 2×(带厚 + 衬厚) = flat_dia + 2×(belt_thickness + lining_thickness)
        """
        p_type = pulley.get('type', 'groove')
        if p_type == 'flat':
            flat_dia = float(pulley.get('flat_dia') or 0)
            return flat_dia + 2 * (self.belt_thickness + self.lining_thickness)
        else:
            return float(pulley.get('groove_dia') or 0)

    def calc_center_distance(self, curr: Dict, next_p: Dict) -> float:
        """计算两带轮中心距 C = sqrt((x2-x1)² + (y2-y1)²)"""
        dx = float(next_p.get('x') or 0) - float(curr.get('x') or 0)
        dy = float(next_p.get('y') or 0) - float(curr.get('y') or 0)
        return math.sqrt(dx * dx + dy * dy)

    def calc_upper_tangent_angle(self, curr: Dict, next_p: Dict,
                                  k_curr: float, k_next: float,
                                  center_dist: float) -> float:
        """
        计算上切点角 E（小角，用 ASIN）

        同类型（Grooved-Grooved）:
          E = DEGREES(ASIN((K_curr - K_next) / (2×C)))
        同类型（Flat-Flat）:
          E = -DEGREES(ASIN((K_curr - K_next) / (2×C)))
        不同类型（Grooved-Flat）:
          E = DEGREES(ASIN((K_curr + K_next) / (2×C)))
        不同类型（Flat-Grooved）:
          E = -DEGREES(ASIN((K_curr + K_next) / (2×C)))
        """
        if center_dist == 0:
            return 0

        curr_type = curr.get('type', 'groove')
        next_type = next_p.get('type', 'groove')
        is_curr_groove = curr_type == 'groove'
        is_next_groove = next_type == 'groove'

        if is_curr_groove == is_next_groove:
            # 同类型
            ratio = (k_curr - k_next) / (2 * center_dist)
            ratio = max(-1, min(1, ratio))
            angle = math.degrees(math.asin(ratio))
            if not is_curr_groove:
                # Flat-Flat: 取反
                angle = -angle
        else:
            # 不同类型
            ratio = (k_curr + k_next) / (2 * center_dist)
            ratio = max(-1, min(1, ratio))
            angle = math.degrees(math.asin(ratio))
            if not is_curr_groove:
                # Flat-Grooved: 取反
                angle = -angle

        return angle

    def calc_lower_tangent_angle(self, curr: Dict, next_p: Dict,
                                  center_dist: float) -> float:
        """
        计算下切点角 G（大角，用 ACOS）

        G = DEGREES(ACOS((x_next - x_curr) / C))
        若 y_next < y_curr: G = 360 - G
        """
        if center_dist == 0:
            return 0

        dx = float(next_p.get('x') or 0) - float(curr.get('x') or 0)
        dy = float(next_p.get('y') or 0) - float(curr.get('y') or 0)

        ratio = dx / center_dist
        ratio = max(-1, min(1, ratio))
        g = math.degrees(math.acos(ratio))

        # Excel公式: IF(y_next > y_curr, G, 360-G)
        if dy < 0:
            g = 360 - g

        return g

    def calc_cumulative_angle(self, g: float, e: float) -> float:
        """
        计算累计切点角 I = G + E
        若 I < 0: I = I + 360
        """
        i = g + e
        if i < 0:
            i += 360
        return i

    def calc_wrap_angle(self, i_curr: float, i_next: float,
                         pulley_type: str) -> float:
        """
        计算包角 S

        槽轮(Grooved):
          diff = I_next - I_curr
          S = diff + 360 if diff < 0 else diff

        平轮(Flat):
          diff = I_next - I_curr
          if diff < 0:
            if |diff| > 360: S = |diff| - 360
            else: S = 360 - (diff + 360)
          else:
            S = 360 - diff
        """
        diff = i_next - i_curr
        two_pi_deg = 360.0

        if pulley_type == 'groove':
            if diff < 0:
                return diff + two_pi_deg
            return diff
        else:
            # Flat
            if diff < 0:
                if abs(diff) > 360:
                    return abs(diff) - two_pi_deg
                else:
                    return two_pi_deg - (diff + two_pi_deg)
            else:
                return two_pi_deg - diff

    def calc_belt_length(self, pulleys: List[Dict]) -> Dict:
        """
        计算皮带总长

        皮带总长 = Σ(切线段长度Q) + Σ(包角弧长)
                 = Σ(C_i × cos(E_i)) + Σ(S_i × K_i × π / 360)

        参数:
            pulleys: 带轮列表，每个带轮包含:
                - code: 带轮编号
                - x, y: 中心坐标
                - type: 'groove' 或 'flat'
                - groove_dia: 槽轮节圆直径
                - flat_dia: 平轮节径

        返回:
            {
                'belt_length': 皮带总长,
                'details': 每个带轮的详细计算数据,
                'segments': 每段皮带的直线段长度,
                'arcs': 每个带轮的弧长
            }
        """
        # 过滤有效带轮
        lst = [p for p in pulleys if p.get('code') and p.get('x') is not None and p.get('y') is not None]
        n = len(lst)
        if n < 2:
            return {'belt_length': 0, 'details': [], 'segments': [], 'arcs': []}

        # 1. 计算节圆直径 K
        k_values = []
        for p in lst:
            k = self.calc_pitch_diameter(p)
            k_values.append(k)

        # 2. 计算切点距离 C、上切点角 E、下切点角 G、累计切点角 I
        c_values = []  # 中心距
        e_values = []  # 上切点角
        g_values = []  # 下切点角
        i_values = []  # 累计切点角

        for idx in range(n):
            curr = lst[idx]
            # 下一带轮（最后一个回第一个）
            next_idx = (idx + 1) % n
            next_p = lst[next_idx]

            # 中心距
            c = self.calc_center_distance(curr, next_p)
            c_values.append(c)

            # 上切点角
            e = self.calc_upper_tangent_angle(
                curr, next_p, k_values[idx], k_values[next_idx], c
            )
            e_values.append(e)

            # 下切点角
            g = self.calc_lower_tangent_angle(curr, next_p, c)
            g_values.append(g)

            # 累计切点角
            i_val = self.calc_cumulative_angle(g, e)
            i_values.append(i_val)

        # 3. 计算包角 S
        # Excel公式: S[i] = I[i] - I[prev]（当前累计角 - 前一带轮累计角）
        s_values = []
        for idx in range(n):
            curr = lst[idx]
            prev_idx = (idx - 1 + n) % n
            s = self.calc_wrap_angle(
                i_values[prev_idx], i_values[idx], curr.get('type', 'groove')
            )
            s_values.append(s)

        # 4. 计算切线段长度 Q = C × cos(E)
        q_values = []
        for idx in range(n):
            q = c_values[idx] * math.cos(math.radians(e_values[idx]))
            q_values.append(q)

        # 5. 计算弧长 arc = S × K × π / 360
        arc_values = []
        for idx in range(n):
            arc = s_values[idx] * k_values[idx] * math.pi / 360
            arc_values.append(arc)

        # 6. 皮带总长
        total_straight = sum(q_values)
        total_arc = sum(arc_values)
        belt_length = total_straight + total_arc

        # 构建详细结果
        details = []
        for idx in range(n):
            curr = lst[idx]
            next_idx = (idx + 1) % n
            next_p = lst[next_idx]
            details.append({
                'code': curr.get('code'),
                'type': curr.get('type'),
                'x': float(curr.get('x') or 0),
                'y': float(curr.get('y') or 0),
                'pitch_diameter': round(k_values[idx], 4),
                'center_dist': round(c_values[idx], 4),
                'upper_tangent_angle': round(e_values[idx], 4),
                'lower_tangent_angle': round(g_values[idx], 4),
                'cumulative_angle': round(i_values[idx], 4),
                'wrap_angle': round(s_values[idx], 4),
                'tangent_length': round(q_values[idx], 4),
                'arc_length': round(arc_values[idx], 4),
                'next_code': next_p.get('code'),
            })

        return {
            'belt_length': round(belt_length, 4),
            'total_straight': round(total_straight, 4),
            'total_arc': round(total_arc, 4),
            'details': details,
        }
