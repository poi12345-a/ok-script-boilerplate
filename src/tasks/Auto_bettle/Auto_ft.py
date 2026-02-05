
import unittest
from src.config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.Auto_bettle.TimeTask import MyOneTimeTask

class TestMyTriggerTask(TaskTestCase):
    task_class = MyOneTimeTask
    config = config

    def test_01_ocr_battle_list(self):
        """测试场景：主界面点击‘战斗列表’"""
        self.set_image('assets/images/main.png')
        target = self.task.find_text_one()
        self.assertIsNotNone(target, "未能识别到‘战斗列表’")

    def test_02_ocr_filter_icon(self):
        """测试场景：战斗列表页识别‘筛选’图标"""
        self.set_image('assets/images/0.png')
        target = self.task.find_ocr_one()
        self.assertIsNotNone(target, "未能识别到筛选图标特征")

    def test_03_ocr_confirm_btn(self):
        """测试场景：筛选菜单点击‘确定’"""
        self.set_image('assets/fzhj/Confirm.png')
        target = self.task.find_text_tow()
        self.assertIsNotNone(target, "未能识别到‘确定’按钮")

    def test_04_ocr_physical(self):
        """测试场景：体力提取逻辑"""
        self.set_image('assets/fzhj/Physical_strength4.png')
        val = self.task.find_ocr_four()
        self.assertIsInstance(val, int, "体力应解析为整数")
        self.log_info(f"体力数值测试结果: {val}")

    def test_05_ocr_skip_turn(self):
        """测试场景：战斗中‘跳过回合’"""
        self.set_image('assets/fzhj/Skip_Turn.png')
        target = self.task.ocr(match="跳过回合")
        self.assertIsNotNone(target, "未能识别到‘跳过回合’")

    def test_06_ocr_victory(self):
        """测试场景：战斗结算‘战斗胜利’"""
        self.set_image('assets/fzhj/Battle_Victory.png')
        target = self.task.ocr(match="战斗胜利")
        self.assertIsNotNone(target, "未能识别到‘战斗胜利’")

    def test_07_ocr_stop_auto_menu(self):
        """测试场景：战斗列表'等待页面跳转'"""
        self.set_image('assets/fzhj/stop_suto2.png')
        target_icon = self.task.ocr(match="菜单")
        self.assertIsNotNone(target_icon, "未能识别到菜单特征图标")

    def test_077_ocr_stop_auto_menu(self):
        """测试场景：战斗中'停止自动挂机'"""
        self.set_image('assets/fzhj/stop_suto.png')
        stop_text = self.task.ocr(match="停止挂机")
        self.assertIsNotNone(stop_text, "未能识别到‘停止挂机’文本")

    def test_08_ocr_friend_request(self):
        self.set_image('assets/fzhj/Friend_Request.png')
        target = self.task.ocr(match="好友申请")
        self.assertIsNotNone(target, "未能识别到‘好友申请’")

    def test_09_ocr_friend_request_esc(self):
        self.set_image('assets/fzhj/Friend_Request_esc.png')
        target = self.task.ocr(match="取消")
        self.assertIsNotNone(target, "未能识别到‘取消’")

    def test_10_ocr_app_sp(self):
        """测试：识别主界面体力‘+’号"""
        self.set_image('assets/fzhj/Add_Physical_strength.png')
        target = self.task.find_one("Add_Physical_strength")
        self.assertIsNotNone(target, "未能识别到‘添加体力’")

    def test_11_ocr_10sp(self):
        """测试：识别10点精力瓶"""
        self.set_image('assets/fzhj/10sp.png')
        target = self.task.ocr(match="使用")
        self.assertIsNotNone(target, "未能识别到‘使用体力’")

    def test_12_ocr_1sp(self):
        """测试：识别1点精力瓶"""
        self.set_image('assets/fzhj/1sp.png')
        target = self.task.ocr(match="使用")
        self.assertIsNotNone(target, "未能识别到‘使用体力’")

    def test_13_ocr_sp_add(self):
        """测试：识别数量调整的‘+’号"""
        self.set_image('assets/images/15.png')
        target = self.task.find_one("sp_add")
        self.assertIsNotNone(target, "未能识别到‘添加体力’")

    def test_14_ocr_sp_use(self):
        """测试：识别‘使用’按钮"""
        self.set_image('assets/fzhj/use_sp_confirm.png')
        target = self.task.ocr(match="使用")
        self.assertIsNotNone(target, "未能识别到‘使用’")

    def test_15_ocr_sp_use_confirm(self):
        """测试：识别‘关闭’按钮"""
        self.set_image('assets/fzhj/use_spesc_confirm.png')
        target = self.task.ocr(match="关闭")
        self.assertIsNotNone(target, "未能识别到‘关闭’")

    def test_16_ocr_gb(self):
        """测试：识别‘点击空白区域关闭’"""
        self.set_image('assets/fzhj/guanbi.png')
        target = self.task.ocr(match="点击空白区域关闭")
        self.assertIsNotNone(target, "未能识别到‘点击空白区域关闭’")

    def test_17_ocr_back(self):
        """测试：识别‘返回’按钮"""
        self.set_image('assets/fzhj/back.png')
        target = self.task.find_one("back")
        self.assertIsNotNone(target, "未能识别到‘返回’")


if __name__ == '__main__':
    unittest.main()
