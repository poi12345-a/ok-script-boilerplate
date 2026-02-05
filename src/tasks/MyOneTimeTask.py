
from qfluentwidgets import FluentIcon

from src.tasks.MyBaseTask import MyBaseTask


class MyOneTimeTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "点击触发运行任务"
        self.description = "用户点击时调用run方法"
        self.icon = FluentIcon.SYNC
        # self.default_config.update({
        #     '下拉菜单选项': "第一",
        #     '是否选项默认支持': False,
        #     'int选项': 1,
        #     '文字框选项': "默认文字",
        #     '长文字框选项': "默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字",
        #     'list选项': ['第一', '第二', '第3'],
        # })
        # self.config_type["下拉菜单选项"] = {'type': "drop_down",
        #                               'options': ['第一', '第二', '第3']}

    def run(self):
        # 1. 在调整后的坐标系（549*945）内进行 OCR 识别
        self.log_info("执行点击测试")
        self.do_run()

    def find_some_text_one(self):
        target = self.ocr(x=0, y=0.8, to_x=0.3, to_y=1.0, match="惑星之间")


        if target:
            # 2. 直接传入整个对象，框架会自动处理中心点点击和前台穿透逻辑
            print(self.click(target))

            self.log_info(f"成功识别并点击目标: {target[0].name}")
        else:
            self.log_error("未能在当前区域找到‘惑星之间’，请检查窗口是否完全可见")
        return target


    def do_run(self):
        self.find_some_text_one()




