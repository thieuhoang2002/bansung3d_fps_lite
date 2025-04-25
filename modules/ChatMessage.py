from ursina import *


class ChatMessage:
    inputText = None
    messages = []
    y_mess = 0.2
    username = ''
    prevLenMessages = 0

    def __init__(self, username='player'):
        self.inputText = InputField(
            scale=(1.24, 0.08, 1), position=(0, -1, 0), character_limit=20)
        self.username = username
        self.textPanel = Entity(
            model='quad', parent=camera.ui, color=color.rgba(0, 0, 0, 0.6))
        self.textPanel.position = Vec3(-0.69, -0.04, 0)
        self.textPanel.scale = Vec3(0.460001, 0.53, 1)

    def addNewMessage(self, contentMessage, usermes):
        mesItem = Text(parent=camera.ui, position=(-0.869999, self.y_mess, 0))
        mesItem.text = f'<blue>{usermes}: <white>{contentMessage}'
        self.messages.append(mesItem)
        self.y_mess -= .04
        self.y_mess = round(self.y_mess, 2)

        self.inputText.text = ''

    def scrollcustom(self):
        if len(self.messages) > 10 and len(self.messages) != self.prevLenMessages:
            '''
            Trong Ursina, mọi thứ trong giao diện (camera.ui) hiển thị trong phạm vi cụ thể:
                Trục X: từ khoảng -0.75 → 0.75
                Trục Y: từ khoảng -0.5 → 0.5 (tuỳ theo camera và scale UI)
            '''
            self.messages[-11].y = 1  # ẩn đi, ném dòng tin nhắn sớm nhất ra khỏi khung hình chính luôn
            for message in self.messages:
                message.y += .04
            self.y_mess = -.2
            self.prevLenMessages = len(self.messages)
