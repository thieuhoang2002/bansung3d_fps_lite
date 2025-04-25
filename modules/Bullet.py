from ursina import *


class Bullet(Entity):
    '''
    Tạo và quản lý đạn: Khi người chơi bắn (bằng súng AK47 hoặc súng ngắn), một đối tượng Bullet được tạo với hình dạng quả cầu (model='sphere') và màu vàng (color.yellow), có kích thước scale=6.
    '''

    def __init__(self, position, direction, listObjectIgnore: list, getPlayerClass, ignorePosition, listClientCallBack: list):
        super().__init__(
            model='sphere',
            texture='white_cube',
            color=color.yellow,
            scale=6,  # kích thước đạn
            position=position,
            collider='sphere'
        )
        self.ignorePosition = ignorePosition
        self.time_start = time.time()
        self.alive = True
        self.getPlayerClass = getPlayerClass
        self.listClientCallBack = listClientCallBack
        self.listObjectIgnore = listObjectIgnore
        self.direction = direction
        self.trail = Entity(parent=self, model='sphere',
                            color=color.red, scale=0.3)  # Thêm một trail
        self.gun_sound = Audio(
            'asset/static/sound_effect/shotgun-firing-4-6746.mp3', loop=False, autoplay=False)

    def update(self):
        if time.time() - self.time_start >= 5:
            self.alive = False
        if not self.alive:
            self.deleteBullet()
            return
        if self.alive:
            self.move_bullet()

    def move_bullet(self):

        if self.y_getter() > 2000 or self.z_getter() > 2000 or self.x_getter() > 2000:
            self.deleteBullet()
            return
        self.position += self.direction * 120  # tốc độ đạn
        self.rotation_y += 5
        self.animate_trail()
        hit_info = self.intersects(ignore=self.listObjectIgnore)
        if hit_info.hit and not isinstance(hit_info.entity, self.getPlayerClass()) and hit_info.entity.position != self.ignorePosition:
            print('ban da ban trung muc tieu co vi tri la:',
                  hit_info.entity.position)
            self.listClientCallBack[0]()
            self.listClientCallBack[2](hit_info.entity.position)  # bị bắn
            self.alive = False

    def animate_trail(self):
        self.trail.position = self.position
        self.trail.scale_y *= 0.9

    def shoot(self):
        self.gun_sound.play()
        self.move_bullet()

    def deleteBullet(self):
        self.trail.enable = False
        destroy(self.trail)
        destroy(self)
