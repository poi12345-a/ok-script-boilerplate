from ok import TriggerTask


class MyTriggerTask(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "野怪挂机"
        self.description = ("走到特定位置挂机"
                            "\n启动没反应按F9")

    def run(self):
        # 1. 精准锁定左下角底部（避开上方的聊天框干扰）
        # x:0 -> 0.2 (只看左边五分之一)
        # y:0.9 -> 1.0 (只看最底部十分之一)

        # 检查“惑星之间”
        target_a = self.ocr(x=0, y=0.93, to_x=0.2, to_y=1.0, match="惑星之间")
        if target_a:
            self.log_info(f"精准捕获【惑星之间】: {target_a[0].x}, {target_a[0].y}")
            self.click(target_a)
            self.sleep(1.5)  # 给界面跳转留点缓冲
            return True

            # 2. 检查“世界”
        # 同样缩小范围，世界频道的消息一般在 y=0.8
        target_b = self.ocr(x=0, y=0.93, to_x=0.2, to_y=1.0, match="世界")
        if target_b:
            self.log_info(f"精准捕获【世界】: {target_b[0].x-0.3}, {target_b[0].y}")
            self.click(target_b)
            self.sleep(1.5)
            return True

        # 3. 适当降低频率，防止 OCR 占用过高
        self.sleep(0.5)





