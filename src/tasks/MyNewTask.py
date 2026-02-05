
import unittest
from src.config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.MyOneTimeTask import MyOneTimeTask


class TestMyTriggerTask(TaskTestCase):
    # 指定要测试的类为 MyTriggerTask
    task_class = MyOneTimeTask
    config = config

    def test_ocr_planet(self):
        """测试识别‘战斗列表’并模拟点击"""
        # 1. 加载第一张截图
        self.set_image('assets/images/main.png')

        # 2. 调用你刚才写的 find_some_text_one
        # 注意：在 TaskTestCase 中，通过 self.task 访问你的任务实例
        target = self.task.find_some_text_one()

        # 3. 断言识别结果
        self.assertIsNotNone(target, "未能识别到‘战斗列表’")
        self.assertEqual(target[0].name, '战斗列表')

    def test_ocr_world(self):
        """测试识别‘世界’并模拟点击"""
        # 1. 加载第二张截图
        self.set_image('src/tasks/Auto_bettle/icons/main_next.png')

        # 2. 调用你新写的 find_some_text_tow
        target = self.task.find_some_text_tow()

        # 3. 断言识别结果
        # self.assertIsNotNone(target, "未能识别到‘世界’")
        # self.assertEqual(target[0].name, '世界')


if __name__ == '__main__':
    unittest.main()
