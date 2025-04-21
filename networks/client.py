from ursinanetworking import *
from ursina import *
from modules.ChatMessage import ChatMessage
from modules.OtherPlayer import OtherPlayer
from modules.Player import Player
from data.RandomPosition import *

# Helper function to parse a string into a Vec3 object


def parse_vec3(vec_str):
    try:
        x, y, z = map(float, vec_str.strip("()").split(","))
        return Vec3(x, y, z)
    except Exception as e:
        print(f"Error parsing Vec3: {e}")
        return Vec3(0, 0, 0)


class MyClient:
    def __init__(self, username, ip, port, start_position):
        self.result = None
        self.ip = ip
        self.port = port
        # self.list_other_players:list[OtherPlayer] = []
        self.list_other_players = {}
        self.player_info = {
            'id': -1,
            'username': username,
        }
        self.start_position = start_position
        self.client = UrsinaNetworkingClient(self.ip, self.port)
        self.easy = EasyUrsinaNetworkingClient(self.client)
        self.chatMessage = ChatMessage(username)
        self.player = Player(position=self.start_position, clientCallback=[self.sendSignalShooting, self.printPosOfOtherPlayer, self.getListOtherPlayers,
                             self.getIdPlayers, self.check_player_shot], ignorePosition=self.start_position, player_info=self.player_info,  client=self)
        self.time_start = time.time()
        Audio('asset/static/sound_effect/getready.ogg').play()

        @self.client.event
        def GetID(content):
            self.player_info['id'] = content
            self.player.position = playerRandomPositions[int(content)]
            self.client.send_message(
                'updatePosition', playerRandomPositions[int(content)])

            # Debug: In ra danh sách replicated variables từ server
            print("Dữ liệu replicated từ server:",
                  self.easy.replicated_variables)

            # Xóa danh sách cũ và cập nhật danh sách mới
            self.list_other_players.clear()

            for player_id, data in self.easy.replicated_variables.items():
                if int(player_id) != self.player_info['id']:
                    new_player = OtherPlayer(player_id, Vec3(0, 3.5, 0))
                    new_player.setPos(data.content['position'])
                    # ✅ Chỉ thêm người chơi khác
                    self.list_other_players[player_id] = new_player

            # Debug: Kiểm tra danh sách đã cập nhật
            print("Danh sách người chơi sau khi cập nhật:",
                  self.list_other_players)

        # hàm này chạy được nhưng lỗi nhân bản sau khi reset
        @self.client.event
        def allPlayersData(content):
            print("🔵 Cập nhật lại danh sách người chơi từ server:", content)

            existing_players = set(self.list_other_players.keys())
            print("Danh sách người chơi hiện tại:", self.list_other_players)

            for player_id_str, player_data in content.items():
                player_id = int(player_id_str)  # Luôn ép kiểu về int

                if player_id == self.player_info['id']:
                    print(f"🚫 Bỏ qua chính mình (ID: {player_id})")
                    continue  # Bỏ qua chính mình

                if player_id in existing_players:
                    print(
                        f"🔄 Cập nhật lại vị trí người chơi {player_id}: {player_data['position']}")
                    self.list_other_players[player_id].setPos(
                        player_data['position'])
                else:
                    print(
                        f"✅ Thêm người chơi mới {player_id} tại vị trí {player_data['position']}")
                    new_player = OtherPlayer(
                        player_id, player_data['position'])
                    self.list_other_players[player_id] = new_player

            # ✅ Yêu cầu đồng bộ lại vị trí
            self.client.send_message('requestSyncPositions', {})

        # hàm này kết hợp với "hàm này chạy được nhưng lỗi nhân bản sau khi reset"
        @self.client.event
        def syncPositions(content):
            print("🔄 Đồng bộ vị trí của tất cả người chơi từ server:", content)

            for player_id_str, position in content.items():
                player_id = int(player_id_str)  # Ép kiểu player_id về int

                if player_id == self.player_info['id']:
                    print(
                        f"✅ Cập nhật vị trí của chính mình (ID: {player_id}) thành {position}")
                    self.player.position = position  # Cập nhật trực tiếp vị trí của nhân vật chính
                    continue

                if player_id in self.list_other_players:
                    self.list_other_players[player_id].setPos(position)
                    print(
                        f"✅ Cập nhật vị trí của {player_id} thành {position}")
                else:
                    print(
                        f"⚠️ Không tìm thấy người chơi {player_id} trong danh sách, nhưng không tạo mới vì đó có thể là lỗi!")

        @self.client.event
        def newPlayerLogin(data):
            player_id = data.get('id')
            position = data.get('position', Vec3(0, 3.5, 0))

            # Nếu player ID là chính mình, không tạo model tĩnh
            if player_id == self.player_info['id']:
                print(
                    f"⚠️ Bỏ qua tạo nhân vật {player_id} vì đó là chính mình!")
                return

            if player_id is None or position is None:
                print(f"❌ Lỗi: Dữ liệu không hợp lệ! {data}")
                return

            if player_id in self.list_other_players:
                print(f"⚠️ Người chơi {player_id} đã tồn tại!")
                return

            try:
                new_player = OtherPlayer(player_id, position)
                self.list_other_players[player_id] = new_player
                print(
                    f"✅ Đã tạo người chơi mới: {player_id} tại vị trí {position}")
            except Exception as e:
                print(f"❌ Lỗi khi tạo OtherPlayer: {e}")

        @self.client.event
        def newMessage(content):
            # print(content)
            self.chatMessage.addNewMessage(
                contentMessage=content['message'], usermes=content['username'])
            pass

        @self.client.event
        def existedClientDisConnected(idPlayerLogout):
            # print('----------ndk log - Existed client disconnect----')
            # print('removed id:', idPlayerLogout)
            self.list_other_players[idPlayerLogout].logout()

        @self.client.event
        def decrease_hp(content):
            print("Đã nhận event decrease_hp với content:", content)
            print("Giá trị content nhận được:", content)
            print("Giá trị player id của tôi:", self.player_info['id'])

            # Nếu content là một dictionary, hãy truy cập key chứa id
            if isinstance(content, dict) and 'id' in content:
                target_id = content['id']
            else:
                target_id = content

            # Ép kiểu cho phù hợp nếu cần (ví dụ: ép về int hoặc str)
            try:
                target_id = int(target_id)
                my_id = int(self.player_info['id'])
            except Exception as e:
                print("Lỗi ép kiểu:", e)
                target_id = target_id
                my_id = self.player_info['id']

            if target_id == my_id:
                self.player.healthbar.value -= 20
                print(
                    f"🔥 Tôi bị bắn! Máu còn lại: {self.player.healthbar.value}")
            elif target_id in self.list_other_players:
                new_hp = self.list_other_players[target_id].healthbar.value - 20
                self.list_other_players[target_id].update_health(new_hp)
                print(
                    f"🔥 Người chơi {target_id} bị bắn! Máu còn lại: {new_hp}")

        @self.client.event
        def hearFromOtherClient(content):
            print(content)
            # self.openVoiceChat()

        @self.client.event
        def stopHearFromOtherClient(content):
            print(content)
            self.stopVoiceChat()

        self.endGameMessage = None
        self.allowRestartGame = False

        @self.client.event
        def endGame(content):
            print("Nhận event endGame:", content)
            self.allowRestartGame = True
            self.result = content
            if content['id'] == self.player_info['id']:
                self.endGameMessage = Text(
                    text='Victory',
                    style='bold',
                    parent=camera.ui,
                    position=Vec3(-0.595996, 0.136, 0),
                    scale=Vec3(13.9, 10.6, 5),
                    color=color.rgb(231, 245, 32),
                )
                Audio('asset/static/sound_effect/victory.mp3').play()
            else:
                self.endGameMessage = Text(
                    text='Defeat',
                    style='bold',
                    parent=camera.ui,
                    position=Vec3(-0.595996, 0.136, 0),
                    scale=Vec3(13.9, 10.6, 5),
                    color=color.rgb(57, 45, 89),
                )
                Audio('asset/static/sound_effect/defeat.mp3').play()

        @self.easy.event
        def onReplicatedVariableCreated(Content):
            # print('-------ndk log new syn var created-------')
            # print(Content)
            pass

        @self.easy.event
        def onReplicatedVariableRemoved(Content):
            # print('-------ndk log one syn var remove-------')
            # print(Content)
            pass

        @self.client.event
        def updateOtherPlayerPosition(content):
            player_id = content['id']
            position = content['position']

            if player_id in self.list_other_players:
                self.list_other_players[player_id].setPos(position)
                print(f"🔄 Cập nhật vị trí người chơi {player_id}: {position}")
            else:
                print(
                    f"⚠️ Không tìm thấy người chơi {player_id} để cập nhật vị trí!")

        @self.client.event
        def updateOtherPlayerRotation(content):
            player_id = content['id']
            rotation = content['rotation']
            if player_id in self.list_other_players:
                self.list_other_players[player_id].setRot(rotation)
                print(
                    f"🔄 Cập nhật hướng của người chơi {player_id}: {rotation}")

        @self.client.event
        def updateOtherPlayerStatus(content):
            player_id = content['id']
            status = content['status']
            if player_id in self.list_other_players:
                other_player = self.list_other_players[player_id]
                # Giả sử bạn có các phương thức running() và stand() để chuyển đổi animation
                if status == 'running':
                    other_player.running()
                else:
                    other_player.stand()
                print(
                    f"🔄 Cập nhật trạng thái của người chơi {player_id}: {status}")

        @self.client.event
        def assignNewID(content):
            self.player_info['id'] = content['id']
            self.player.position = content['position']
            print(
                f"Đã nhận ID mới: {self.player_info['id']}, vị trí: {self.player.position}")

        @self.client.event
        def reset_game(content):
            print("Đã nhận event reset_game từ server:", content)
            self.resetGame(content)

            # ✅ Yêu cầu danh sách tất cả người chơi từ server để cập nhật lại
            self.client.send_message('requestAllPlayersData', {})

    def resetGame(self, content):
        print("Dữ liệu content nhận được:", content)
        if not isinstance(content, dict):
            print("⚠️ Content không phải dictionary, bỏ qua:", content)
            return
        if 'id' in content:
            print("ℹ️ Nhận dữ liệu endGame thay vì reset_game, bỏ qua:", content)
            return

        print(f"list other players resettttttt: {self.list_other_players}")
        # Xóa tất cả OtherPlayer cũ
        for player in self.list_other_players.values():
            if hasattr(player, 'character'):
                destroy(player.character.stand_entity)
                destroy(player.character.running_entity)
        self.list_other_players.clear()

        # **Reset nhân vật chính**
        if str(self.player_info['id']) in content:
            player_pos = content[str(self.player_info['id'])]['position']
            self.player.position = player_pos  # Cập nhật vị trí mới
            self.player.healthbar.value = 100  # Reset máu
            print(
                f"Đã reset Player {self.player_info['id']} tại vị trí: {self.player.position}")

    def updateUsername(self, name):
        self.player_info['username'] = name
        self.chatMessage.inputText.y = -.43

    def sendSignalShooting(self, position, direction):
        self.client.send_message('clientShooting', {
            'position': position,
            'direction': direction
        })

    def printPosOfOtherPlayer(self):
        print('---------function: printPosOfOtherPlayer - client.py-------------')
        count = 0  # 🔹 Đặt giá trị ban đầu cho count

        for player_id, player in self.list_other_players.items():  # 🔹 Duyệt dict đúng cách
            if player_id != self.player_info['id']:
                print(f'🟢 Vị trí của người chơi {player_id}: {player.pos}')
            count += 1

    def check_player_shot(self, bullet_pos):
        count = 0
        for player_id, player in self.list_other_players.items():  # 🔹 Duyệt qua dict đúng cách
            if player.pos == bullet_pos:  # ✅ Lúc này player là OtherPlayer
                # player.healthbar.value -= 20
                # Gửi thông tin cho server
                hit_data = {'id': player_id}
                self.client.send_message('player_shot', hit_data)
                # print(f"🔥 Người chơi {player_id} bị trúng đạn! Máu còn lại: {player.healthbar.value}")

                if player.healthbar.value <= 0:
                    self.client.send_message('checkPlayerSurvival', 'reset')
                    player.logout()
            count += 1

    def getListOtherPlayers(self):
        return list(filter(lambda x: self.list_other_players.index(x) != self.player_info['id'], self.list_other_players))

    def getIdPlayers(self):
        return self.player_info['id']

    def input(self, key):

        if key == Keys.enter:
            if self.chatMessage.inputText.position == Vec3(0, -1, 0):
                self.chatMessage.inputText.position = Vec3(0, -0.43, 0)
                self.player.disable()
                self.chatMessage.inputText.active = True

            if self.chatMessage.inputText.text != '' and self.chatMessage.inputText.position == Vec3(0, -0.43, 0):
                self.client.send_message('messageFromClient',
                                         {
                                             'username': self.player_info['username'],
                                             'message': self.chatMessage.inputText.text
                                         }
                                         )
                self.chatMessage.inputText.position = Vec3(0, -1, 0)
                self.chatMessage.inputText.active = False
                self.player.enable()
        if held_keys['a'] or held_keys['s'] or held_keys['d'] or held_keys['w']:
            self.client.send_message(
                'updatePosition', self.player.model.world_position)
            self.client.send_message(
                'updateRotation', self.player.model.world_rotation)
            self.client.send_message('updateStatus', 'running')
        if not held_keys['a'] and not held_keys['s'] and not held_keys['d'] and not held_keys['w']:
            self.client.send_message('updateStatus', 'stand')
        if key == 'v' and self.allowRestartGame:
            print("Client: Gửi yêu cầu resetGameRequest đến server")
            self.allowRestartGame = False  # Ngăn spam yêu cầu

            if self.player_info['id'] == 0:  # Chỉ Player 0 gửi yêu cầu reset
                self.client.send_message('resetGameRequest', {})

            self.client.send_message(
                'registerPlayer', {})  # Yêu cầu cấp ID mới

            if self.endGameMessage:
                destroy(self.endGameMessage)
                self.endGameMessage = None

            self.player.ndk_revival()
