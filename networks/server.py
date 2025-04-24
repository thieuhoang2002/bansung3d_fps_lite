from ursinanetworking import easyursinanetworking
from ursinanetworking import *
from data.RandomPosition import playerRandomPositions


class MyServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.start_server = True
        self.update_server = False
        self.server = None
        self.easy = None

        self.waiting_list = []  # Danh sách chờ đăng ký ID mới
        self.is_resetting = False  # Cờ để ngăn chặn xử lý nhiều lần

    def handle(self):
        if self.start_server:
            self.server = UrsinaNetworkingServer(self.ip, self.port)
            self.easy = easyursinanetworking.EasyUrsinaNetworkingServer(
                self.server)
            print("Server đã khởi tạo và đăng ký các event.")

            @self.server.event
            def registerPlayer(Client, content):
                if Client.id not in self.waiting_list:
                    self.waiting_list.append(Client.id)

                new_id = self.waiting_list.index(Client.id)

                start_position = playerRandomPositions[new_id]
                self.easy.create_replicated_variable(new_id, {
                    "id": new_id,
                    'position': start_position,
                    'rotation': (0, 0, 0),
                    'status': 'stand',
                    'hp': 100,
                })
                Client.send_message(
                    'assignNewID', {'id': new_id, 'position': start_position})

            @self.server.event
            def endGame(Client, content):
                print(f"Trò chơi kết thúc, người thắng là: {content['id']}")

                # Xóa toàn bộ danh sách người chơi
                self.easy.replicated_variables.clear()
                self.waiting_list = []  # Reset danh sách đăng ký

            @self.server.event
            def onClientConnected(Client):
                print(f"{Client.id} joined game")
                # self.numberOfPlayers += 1
                # Gán vị trí ngẫu nhiên dựa vào ID
                start_position = playerRandomPositions[Client.id]

                # Tạo replicated variable
                self.easy.create_replicated_variable(Client.id,
                                                     {
                                                         "id": Client.id,
                                                         'position': start_position,
                                                         'rotation': (0, 0, 0),
                                                         'status': 'stand',
                                                         'hp': 100,
                                                     }
                                                     )

            # Debug danh sách player trên server
                print("🔵 Danh sách replicated trên server sau khi cập nhật:",
                      self.easy.replicated_variables)

                # Gửi ID và danh sách toàn bộ player về client mới
                Client.send_message('GetID', Client.id)
                # Client.send_message('updatePosition', start_position)
                Client.send_message('allPlayersData', {
                                    pid: data.content for pid, data in self.easy.replicated_variables.items()})

                # Thông báo với các client khác về người chơi mới
                self.server.broadcast(
                    'newPlayerLogin', {'id': Client.id, 'position': start_position})

            @self.server.event
            def onClientDisconnected(Client):
                print(f"{Client} leave game")
                # self.notifycation_content.text += "\n" + f"{Client.id} leave game"
                self.easy.remove_replicated_variable_by_name(Client.id)
                self.server.broadcast('existedClientDisConnected', Client.id)

            @self.server.event
            def messageFromClient(Client, message):
                print(f"{message}")
                # self.notifycation_content.text += "\n" + f"chatmessage feature: {message}"
                self.server.broadcast('newMessage', message)

            @self.server.event
            def updatePosition(Client, content):
                if Client.id in self.easy.replicated_variables:
                    self.easy.update_replicated_variable_by_name(
                        Client.id, 'position', content)
                    self.server.broadcast('updateOtherPlayerPosition', {
                                          'id': Client.id, 'position': content})

            @self.server.event
            def updateRotation(Client, content):
                # Cập nhật biến replicated
                self.easy.update_replicated_variable_by_name(
                    Client.id, 'rotation', content)
                # Broadcast thông tin xoay cho các client
                self.server.broadcast('updateOtherPlayerRotation', {
                                      'id': Client.id, 'rotation': content})

            @self.server.event
            def updateStatus(Client, content):
                self.easy.update_replicated_variable_by_name(
                    Client.id, 'status', content)
                # Broadcast trạng thái (running, stand) cho các client
                self.server.broadcast('updateOtherPlayerStatus', {
                                      'id': Client.id, 'status': content})

            @self.server.event
            def clientShooting(Client, content):
                print('server recieved client shooting signal:', content)
                self.server.broadcast('bulletFromOtherPlayer', {
                    'id': Client.id,
                    'position': tuple(content['position']),
                    'direction': content['direction'],
                })
                print(
                    f"Broadcasting bullet from player {Client.id} at position {content['position']}")

            @self.server.event
            def player_shot(Client, content):
                try:
                    print(
                        f"Danh sách người chơi trên server: {self.easy.replicated_variables}")
                    target_id = content.get('id')
                    # Lấy dữ liệu người chơi từ replicated variables
                    if target_id in self.easy.replicated_variables:
                        current_data = self.easy.replicated_variables[target_id].content
                        # Mặc định là 100 nếu không có hp
                        current_hp = current_data.get('hp', 100)
                        new_hp = current_hp - 20
                        # Cập nhật lại replicated variable cho HP
                        self.easy.update_replicated_variable_by_name(
                            target_id, 'hp', new_hp)
                        print(
                            f"Server: Người chơi {target_id} bị bắn! HP thay đổi từ {current_hp} xuống {new_hp}")
                        # Broadcast kết quả giảm HP cho tất cả client
                        self.server.broadcast(
                            'decrease_hp', {'id': target_id, 'hp': new_hp})
                    else:
                        print(
                            f"Server: Không tìm thấy thông tin cho người chơi {target_id}")
                except Exception as e:
                    print("Lỗi trong player_shot:", e)

            @self.server.event
            def checkPlayerSurvival(Client, content):
                dead_id = content.get('id')
                print('Server: Nhận checkPlayerSurvival từ người chơi', dead_id)

                # Loại bỏ người chơi chết khỏi replicated variables
                self.easy.remove_replicated_variable_by_name(dead_id)

                # Tính lại số người chơi còn sống
                remaining_players = list(self.easy.replicated_variables.keys())
                print("Server: Người chơi còn sống:", remaining_players)

                if len(remaining_players) == 1:
                    winner = int(remaining_players[0])
                    print(f"Server: Đã xác định người thắng là {winner}")
                    self.server.broadcast('endGame', {'id': winner})

            @self.server.event
            def resetGameRequest(Client, content):
                if self.is_resetting:
                    print(f"Server: Đang reset, bỏ qua yêu cầu từ {Client.id}")
                    return

                self.is_resetting = True
                print("Server: Nhận yêu cầu reset game từ Client:", Client.id)

                self.easy.replicated_variables.clear()
                self.waiting_list = []

                new_players_data = {}
                for client in self.server.clients:
                    client_id = client.id
                    start_position = playerRandomPositions[int(client_id)]
                    self.easy.create_replicated_variable(client_id, {
                        "id": client_id,
                        'position': start_position,
                        'rotation': (0, 0, 0),
                        'status': 'stand',
                        'hp': 100
                    })
                    new_players_data[str(client_id)] = {
                        'position': start_position,
                        'hp': 100
                    }

                print("Server: Broadcast reset_game với dữ liệu mới:",
                      new_players_data)
                self.server.broadcast('reset_game', new_players_data)

                # ✅ Gửi lại danh sách toàn bộ người chơi ngay sau khi reset
                self.server.broadcast('allPlayersData', new_players_data)

                from threading import Timer
                Timer(1.0, lambda: setattr(self, 'is_resetting', False)).start()

            @self.server.event
            def requestSyncPositions(Client, content):
                print(f"Server: Nhận yêu cầu đồng bộ vị trí từ {Client.id}")

                sync_data = {pid: data.content['position']
                             for pid, data in self.easy.replicated_variables.items()}
                Client.send_message('syncPositions', sync_data)

            self.start_server = False
            self.update_server = True
