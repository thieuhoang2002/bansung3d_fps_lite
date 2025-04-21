from ursina import *
from modules.Character import Character
from modules.CustomHealthbar import CustomHealthBar


class OtherPlayer(Entity):
    def __init__(self, id, position):
        super().__init__(parent=scene)  # Đảm bảo nó nằm trong scene
        self.pos = position
        self.id = id

        # Nhân vật
        self.character = Character(position)
        self.character.stand_entity.visible = True

        # Thanh máu
        self.healthbar = CustomHealthBar(3, (0, 1, 0))

        # Collider & Model Copy
        self.collider = 'box'
        self.model_copy = Entity(
            model='cube', scale=(15, 120, 15), position=position,
            collider='box', parent=self
        )
        self.model_copy.visible = False

    def setPos(self, position):
        self.character.stand_entity.position = position
        self.character.running_entity.position = position
        self.model_copy.position = position
        self.pos = position

    def setRot(self, rotation):
        self.character.stand_entity.rotation = rotation
        self.character.running_entity.rotation = rotation
        self.model_copy.rotation = rotation

    def logout(self):
        self.character.log_out()
        destroy(self.model_copy)
        destroy(self)  # Hủy OtherPlayer khỏi scene

    def running(self):
        self.character.running_entity.visible = True
        self.character.stand_entity.visible = False

    def stand(self):
        self.character.stand_entity.visible = True
        self.character.running_entity.visible = False

    def update_health(self, new_hp):
        self.healthbar.value = new_hp
        self.healthbar.text = f"HP: {new_hp}"  # Cập nhật hiển thị trên UI
