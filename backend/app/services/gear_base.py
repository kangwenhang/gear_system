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

    def calc_belt_length_raw(self, pulleys: List[Dict]) -> float:
        """计算皮带总长（原始浮点值），供求解器使用"""
        lst = [p for p in pulleys if p.get('code') and p.get('x') is not None and p.get('y') is not None]
        n = len(lst)
        if n < 2:
            return 0.0
        k_values = [self.calc_pitch_diameter(p) for p in lst]
        c_values, e_values, g_values, i_values = [], [], [], []
        for idx in range(n):
            curr = lst[idx]
            next_p = lst[(idx + 1) % n]
            c = self.calc_center_distance(curr, next_p)
            c_values.append(c)
            e_values.append(self.calc_upper_tangent_angle(
                curr, next_p, k_values[idx], k_values[(idx + 1) % n], c))
            g_values.append(self.calc_lower_tangent_angle(curr, next_p, c))
            i_values.append(self.calc_cumulative_angle(g_values[idx], e_values[idx]))
        s_values = []
        for idx in range(n):
            prev_idx = (idx - 1 + n) % n
            s_values.append(self.calc_wrap_angle(
                i_values[prev_idx], i_values[idx], lst[idx].get('type', 'groove')))
        q_values = [c_values[idx] * math.cos(math.radians(e_values[idx])) for idx in range(n)]
        arc_values = [s_values[idx] * k_values[idx] * math.pi / 360 for idx in range(n)]
        return sum(q_values) + sum(arc_values)

    @staticmethod
    def _normalize_angle(deg: float) -> float:
        """角度归一化到 0~360°"""
        return deg % 360.0

    def calc_tensioner_position(self, pulleys: List[Dict], target_length: float,
                                 tensioner_code: str, pivot_x: float,
                                 pivot_y: float) -> Dict:
        """
        沿张紧轮臂弧（以枢轴为圆心）搜索使皮带长度等于目标长度的张紧轮XY坐标。
        使用牛顿法+步长阻尼沿枢轴圆弧搜索角度。
        返回张紧轮XY、臂角度(0-360°)、达成长度等。
        """
        tensioner_idx = None
        for i, p in enumerate(pulleys):
            if p.get('code') == tensioner_code:
                tensioner_idx = i
                break
        if tensioner_idx is None:
            return {'error': f'未找到张紧轮: {tensioner_code}'}

        curr_x = float(pulleys[tensioner_idx].get('x') or 0)
        curr_y = float(pulleys[tensioner_idx].get('y') or 0)
        arm_length = math.sqrt((curr_x - pivot_x) ** 2 + (curr_y - pivot_y) ** 2)
        if arm_length < 1e-6:
            return {'error': '臂长为零，无法搜索'}

        curr_angle = math.degrees(math.atan2(curr_y - pivot_y, curr_x - pivot_x))
        current_belt = self.calc_belt_length_raw(pulleys)

        if abs(current_belt - target_length) < 0.001:
            return {
                'tensioner_x': round(curr_x, 4),
                'tensioner_y': round(curr_y, 4),
                'tensioner_angle': round(self._normalize_angle(curr_angle), 4),
                'achieved_length': round(current_belt, 4),
                'arm_length': round(arm_length, 4),
                'iterations': 0,
                'converged': True
            }

        def belt_at_angle(angle_deg: float) -> float:
            rad = math.radians(angle_deg)
            pulleys[tensioner_idx]['x'] = pivot_x + arm_length * math.cos(rad)
            pulleys[tensioner_idx]['y'] = pivot_y + arm_length * math.sin(rad)
            return self.calc_belt_length_raw(pulleys)

        angle = curr_angle
        best_angle = curr_angle
        best_error = abs(current_belt - target_length)
        converged = False
        max_iterations = 200
        h = 0.05
        iteration = 0

        for iteration in range(1, max_iterations + 1):
            belt = belt_at_angle(angle)
            error = belt - target_length
            if abs(error) < 0.001:
                converged = True
                break
            if abs(error) < best_error:
                best_error = abs(error)
                best_angle = angle
            belt_plus = belt_at_angle(angle + h)
            dL_dangle = (belt_plus - belt) / h
            if abs(dL_dangle) < 1e-12:
                break
            step = -error / dL_dangle
            max_step = 10.0
            if abs(step) > max_step:
                step = max_step if step > 0 else -max_step
            angle += step
            if abs(angle - curr_angle) > 60:
                angle = curr_angle + (60 if angle > curr_angle else -60)

        if not converged:
            angle = best_angle

        final_belt = belt_at_angle(angle)
        final_x = pulleys[tensioner_idx]['x']
        final_y = pulleys[tensioner_idx]['y']

        return {
            'tensioner_x': round(final_x, 4),
            'tensioner_y': round(final_y, 4),
            'tensioner_angle': round(self._normalize_angle(angle), 4),
            'achieved_length': round(final_belt, 4),
            'arm_length': round(arm_length, 4),
            'iterations': iteration,
            'converged': converged or best_error < 0.05
        }

    def calc_free_position(self, pulleys: List[Dict], tensioner_code: str,
                            pivot_x: float, pivot_y: float,
                            nominal_angle: float, rotation: str) -> Dict:
        """
        计算张紧器自由位置的皮带长度和张紧轮XY坐标。

        张紧器从自由位置旋转名义扭转角(nominal_angle)到达工作位置。
        旋转方向决定角度变化方向：
          - cw（顺时针，屏幕坐标系角度增加）：工作角 = 自由角 + nominal_angle
            → 自由角 = 工作角 - nominal_angle
          - ccw（逆时针，屏幕坐标系角度减少）：工作角 = 自由角 - nominal_angle
            → 自由角 = 工作角 + nominal_angle

        返回自由位置的张紧轮XY、自由角度(0-360°)、皮带长度、工作角度、臂长。
        """
        import copy
        pulleys_copy = copy.deepcopy(pulleys)

        tensioner_idx = None
        for i, p in enumerate(pulleys_copy):
            if p.get('code') == tensioner_code:
                tensioner_idx = i
                break
        if tensioner_idx is None:
            return {'error': f'未找到张紧轮: {tensioner_code}'}

        curr_x = float(pulleys_copy[tensioner_idx].get('x') or 0)
        curr_y = float(pulleys_copy[tensioner_idx].get('y') or 0)
        arm_length = math.sqrt((curr_x - pivot_x) ** 2 + (curr_y - pivot_y) ** 2)
        if arm_length < 1e-6:
            return {'error': '臂长为零'}

        # 工作角度（0-360°）
        work_angle = self._normalize_angle(
            math.degrees(math.atan2(curr_y - pivot_y, curr_x - pivot_x)))

        # 自由角度
        if rotation == 'cw':
            free_angle = work_angle - nominal_angle
        else:  # ccw
            free_angle = work_angle + nominal_angle
        free_angle = self._normalize_angle(free_angle)

        # 自由位置的张紧轮XY
        free_rad = math.radians(free_angle)
        free_x = pivot_x + arm_length * math.cos(free_rad)
        free_y = pivot_y + arm_length * math.sin(free_rad)

        # 用自由位置的张紧轮替换工作位置，计算皮带长度
        pulleys_copy[tensioner_idx]['x'] = free_x
        pulleys_copy[tensioner_idx]['y'] = free_y
        free_belt_length = self.calc_belt_length_raw(pulleys_copy)

        return {
            'free_tensioner_x': round(free_x, 4),
            'free_tensioner_y': round(free_y, 4),
            'free_angle': round(free_angle, 4),
            'free_belt_length': round(free_belt_length, 4),
            'work_angle': round(work_angle, 4),
            'arm_length': round(arm_length, 4),
            'nominal_angle': round(nominal_angle, 4),
            'rotation': rotation
        }

    def calc_install_position(self, pulleys: List[Dict], tensioner_code: str,
                               pivot_x: float, pivot_y: float,
                               stroke: float, rotation: str,
                               long_belt_length: float) -> Dict:
        """
        计算张紧器安装位置的皮带长度和张紧轮XY坐标。

        安装位置与自由位置在相反方向：
          - 自由位置：远离工作方向（皮带路径变长，张紧器被皮带拉回工作位置）
          - 安装位置：朝工作方向继续旋转（皮带路径变短，皮带松弛可套上）

          即安装方向 = 工作方向（与自由方向相反）：
            cw（工作方向=角度增加）：install_angle = work_angle + stroke
            ccw（工作方向=角度减少）：install_angle = work_angle - stroke

        安装困难判断：
          安装位置路径长度 > 长皮带长度 → 最长皮带也比路径短，套不上 → 困难
          安装位置路径长度 <= 长皮带长度 → 皮带比路径长，松弛可套上 → 正常

        返回安装位置的张紧轮XY、安装角度(0-360°)、安装皮带长度、
        工作角度、臂长、是否安装困难、困难提示信息。
        """
        import copy
        pulleys_copy = copy.deepcopy(pulleys)

        tensioner_idx = None
        for i, p in enumerate(pulleys_copy):
            if p.get('code') == tensioner_code:
                tensioner_idx = i
                break
        if tensioner_idx is None:
            return {'error': f'未找到张紧轮: {tensioner_code}'}

        curr_x = float(pulleys_copy[tensioner_idx].get('x') or 0)
        curr_y = float(pulleys_copy[tensioner_idx].get('y') or 0)
        arm_length = math.sqrt((curr_x - pivot_x) ** 2 + (curr_y - pivot_y) ** 2)
        if arm_length < 1e-6:
            return {'error': '臂长为零'}

        # 工作角度（0-360°）
        work_angle = self._normalize_angle(
            math.degrees(math.atan2(curr_y - pivot_y, curr_x - pivot_x)))

        # 安装角度（与自由方向相反，即工作方向继续旋转 stroke 度）
        if rotation == 'cw':
            install_angle = work_angle + stroke
        else:  # ccw
            install_angle = work_angle - stroke
        install_angle = self._normalize_angle(install_angle)

        # 安装位置的张紧轮XY
        install_rad = math.radians(install_angle)
        install_x = pivot_x + arm_length * math.cos(install_rad)
        install_y = pivot_y + arm_length * math.sin(install_rad)

        # 用安装位置的张紧轮替换工作位置，计算皮带路径长度
        pulleys_copy[tensioner_idx]['x'] = install_x
        pulleys_copy[tensioner_idx]['y'] = install_y
        install_belt_length = self.calc_belt_length_raw(pulleys_copy)

        # 工作位置皮带长度（原数据）
        work_belt_length = self.calc_belt_length_raw(
            [{**p, 'x': float(p.get('x') or 0), 'y': float(p.get('y') or 0)} for p in pulleys]
        )

        # 安装困难判断：安装位置路径 > 长皮带长度 → 困难
        difficult = False
        messages = []
        if long_belt_length is not None and install_belt_length > long_belt_length:
            difficult = True
            gap = install_belt_length - long_belt_length
            messages.append(
                f'安装困难：安装位置路径长度({install_belt_length:.2f}mm) '
                f'大于长皮带长度({long_belt_length:.2f}mm)，'
                f'差值 {gap:.2f}mm，最长皮带也无法套上。'
                f'建议：增大张紧器总行程、调整枢轴位置或缩短皮带路径。'
            )

        # 行程利用情况：达到长皮带长度所需旋转角度
        required_rotation = None
        if install_belt_length != work_belt_length and stroke != 0:
            # 安装方向每旋转1度，路径变化量
            delta_per_deg = (install_belt_length - work_belt_length) / stroke
            if abs(delta_per_deg) > 1e-9:
                # 要让路径 = long_belt_length，需要变化 (long - work)
                required_rotation = (long_belt_length - work_belt_length) / delta_per_deg
                if required_rotation < 0:
                    required_rotation = 0
                if required_rotation > stroke and not difficult:
                    difficult = True
                    messages.append(
                        f'行程不足：达到长皮带长度需旋转 {required_rotation:.2f}°，'
                        f'超过总行程 {stroke}°，差值 {required_rotation - stroke:.2f}°。'
                    )

        if not difficult:
            slack = long_belt_length - install_belt_length if long_belt_length is not None else 0
            messages.append(
                f'安装正常：安装位置路径长度({install_belt_length:.2f}mm) '
                f'小于长皮带长度({long_belt_length:.2f}mm)，'
                f'皮带松弛量 {slack:.2f}mm，可正常安装。'
            )

        return {
            'install_tensioner_x': round(install_x, 4),
            'install_tensioner_y': round(install_y, 4),
            'install_angle': round(install_angle, 4),
            'install_belt_length': round(install_belt_length, 4),
            'work_angle': round(work_angle, 4),
            'work_belt_length': round(work_belt_length, 4),
            'long_belt_length': round(long_belt_length, 4) if long_belt_length is not None else None,
            'arm_length': round(arm_length, 4),
            'stroke': round(stroke, 4),
            'rotation': rotation,
            'required_rotation': round(required_rotation, 4) if required_rotation is not None else None,
            'difficult': difficult,
            'messages': messages
        }
