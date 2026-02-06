import re
import time
from qfluentwidgets import FluentIcon
from src.tasks.MyBaseTask import MyBaseTask


class MyOneTimeTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "自动岛主黑叔叔"
        self.description = "设置好要打的副本和队伍"
        self.icon = FluentIcon.SYNC

    def run(self):
        self.log_info("脚本启动")
        # self.do_run()
        self.operate(lambda :self.do_run())

    # --- 原子识别与点击 ---
    def find_text_one(self):
        """点击战斗列表"""
        target = self.ocr(match="战斗列表")
        if target:
            self.click(target[0])
            return True
        return False

    def find_ocr_one(self):
        """点击筛选图标 - 确保点开为止"""
        img_filter = self.find_one("Filter")
        if img_filter:
            self.click(img_filter)
            # 等待菜单弹出来
            self.sleep(1)
            # 如果 OCR 到了“确定”，说明菜单真的开了
            if self.ocr(match="确定"):
                return True

        return False

    def find_text_tow(self):
        """点击确定"""
        target = self.ocr(match="确定")
        if target:
            self.click(target[0])
            return True

        return False

    def find_orc_three(self):
        """点击仅显示筛选 - 内部安全点击"""
        target = self.find_one("next_filter")
        if target:
            self.click(target)
            return True
        return False

    def find_ocr_four(self):
        """体力提取"""
        targets = self.ocr(x=0.78, y=0.01, to_x=0.92, to_y=0.05)
        if targets:
            match = re.search(r'(\d+)', targets[0].name)
            if match:
                return int(match.group(1))
        return None

    def recover_energy(self):
        """
        补充体力的逻辑：
        流程：点击加号 -> 选择体力瓶 -> 连点+号 -> 确认使用 -> 关闭弹窗 -> 返回
        """
        self.log_info("检测到体力不足，开始执行补充逻辑...")

        # 1. 点击主界面的体力“+”号
        add_btn = self.find_one("Add_Physical_strength")
        if add_btn:
            self.click(add_btn)
            self.sleep(1)

        # 2. 检测并选择体力瓶 (优先找10sp，找不到找1sp)
        sp_bottle = self.ocr(match="使用")  # 对应 test_11 和 test_12
        if sp_bottle:
            self.click(sp_bottle)
            self.sleep(0.5)

        # 3. 连点 4 次 “+” 号增加使用数量
        for i in range(6):
            self.click(439, 520)
            self.sleep(0.3)
        # 4. 点击“使用”弹出调整数量界面
        use_btn = self.ocr(match="使用")  # 对应 test_14
        if use_btn:
            self.click(use_btn[0])
            self.sleep(1)
        # 6. 处理可能的“关闭”或“空白区域关闭”弹窗
        for _ in range(2):  # 尝试关闭两次，应对多层弹窗
            self.next_frame()
            close_btn = self.ocr(match="关闭") or self.ocr(match="点击空白区域关闭")
            if close_btn:
                self.click(close_btn[0])
                self.sleep(0.8)

        # 7. 最后点击“返回”回到主界面
        back_btn = self.find_one("back")  # 对应 test_17
        if back_btn:
            self.click(back_btn)
            self.log_info("补充体力完成，返回主界面")
            self.sleep(1)

    def handle_energy_logic(self):
        """体力判断核心逻辑"""
        energy = self.find_ocr_four()

        if energy is None:
            return True

        if energy >= 3:
            self.log_info(f"当前体力充足: {energy}")
            return True
        else:
            self.log_info(f"体力不足({energy})，触发补充...")
            self.recover_energy()
            # 补充体力后重新检测体力
            return self.find_ocr_four() >= 3

    # --- 核心驱动流程 ---
    def do_run(self):
        self.operate(lambda: self.find_text_one())
        self.sleep(1)
        self.operate(lambda: self.find_ocr_one())
        self.sleep(1)
        self.operate(lambda: self.find_text_tow())
        self.sleep(1)
        self.operate(lambda: self.find_orc_three())
        self.sleep(1)
        # 阶段 4: 进入战斗主循环
        self.log_info("阶段 4: 进入战斗监控")
        while True:
            if self.next_frame() is None: continue
            self.find_ocr_eight()  # 执行原有的体力检测+战斗逻辑
            self.sleep(1)

    def find_ocr_eight(self):
        # 体力检测逻辑
        self.operate(lambda: self.handle_energy_logic())
        self.sleep(1)
        # 1. 尝试开启
        targets_auto = self.find_one("Auto")
        if targets_auto:
            self.click(targets_auto)

            # --- 状态锁：强制锁死，不进场绝对不往下走 ---
            self.log_info("状态锁：等待进场图标 ...")
            while True:
                if self.next_frame() is None: continue
                # 只有看到进场后的特征才 break
                if self.ocr(match="菜单"):
                    break
                self.sleep(0.5)

            # --- 进场后才执行的操作 ---
            self.log_info("已确认进场，处理后续逻辑")
            stop_btn = self.ocr(match="停止挂机")
            if stop_btn:
                self.click(stop_btn[0])
        else:
            # 如果在列表页根本没看到 Auto 按钮，直接退出，不要进监控
            self.log_info("当前不在战斗准备界面，拒绝进入监控循环")
            return

        # 4. 进入纯粹的战斗监控大循环
        self.monitor_battle()
        self.sleep(3)
        self.find_orc_ten()

    def monitor_battle(self):
        """专门负责战斗中的 OCR 监控，避免在外面乱认"""
        self.log_info("开始战斗监控：自动处理跳过回合")
        while True:
            if self.next_frame() is None: continue

            # 检查跳过回合
            skip = self.ocr(match="跳过回合")
            if skip:
                self.click(skip[0])
                self.sleep(1)

            # 这里可以加入“战斗结束”的判断来 break 掉这个大循环
            # 例如：if self.ocr(match="结算"): break

            self.sleep(0.5)

            # 检查胜利
            victory = self.ocr(match="战斗胜利")
            if victory:
                self.log_info("检测到战斗胜利")
                for _ in range(3):
                    self.click(victory[0])
                    self.sleep(0.5)
                break

            self.sleep(0.5)

        # D. 结算确认
        confirm = self.find_one("victory_confirm")
        if confirm:
            for _ in range(3):
                self.click(confirm)
                self.sleep(0.5)
            self.sleep(2)

    def find_orc_ten(self):
        frd_ocr = self.ocr(match="好友申请")
        frd_esc_ocr = self.ocr(match="取消")
        if frd_ocr and frd_esc_ocr:
            self.log_info("关闭好友请求")
            self.click(frd_esc_ocr[0])
