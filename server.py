import socket
import threading
import json
import secrets
from database import DatabaseManager
from game_logic import GameLogic

class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.waiting_room = []
        self.active_games = {}
        
        # Khởi tạo database
        self.db_config = {
            'host': 'localhost',
            'user': 'root',     
            'password': '',       
            'database': 'rps_game'
        }
        self.db = DatabaseManager(self.db_config)
        self.game_logic = GameLogic()

    def handle_client(self, client_socket, addr):
        """Xử lý kết nối từ client"""
        print(f"[NEW CONNECTION] {addr} connected")
        session_token = secrets.token_hex(16)
        self.clients[session_token] = {
            'socket': client_socket,
            'addr': addr,
            'user': None,
            'in_game': False
        }

        try:
            while True:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                message = json.loads(data)
                action = message.get('action')

                if action == 'register':
                    self.handle_register(client_socket, message)
                elif action == 'login':
                    self.handle_login(client_socket, session_token, message)
                elif action == 'find_match':
                    self.handle_find_match(session_token)
                elif action == 'make_choice':
                    self.handle_make_choice(session_token, message)

        except Exception as e:
            print(f"[ERROR] {addr}: {e}")
        finally:
            self.cleanup_client(session_token, client_socket, addr)

    def handle_register(self, client_socket, message):
        """Xử lý đăng ký"""
        success, msg = self.db.register_user(
            message['username'],
            message['password'],
            message.get('email', '')
        )
        response = {'action': 'register_response', 'success': success, 'message': msg}
        client_socket.send(json.dumps(response).encode('utf-8'))

    def handle_login(self, client_socket, session_token, message):
        """Xử lý đăng nhập"""
        success, result = self.db.login_user(message['username'], message['password'])
        if success:
            self.clients[session_token]['user'] = result
            response = {
                'action': 'login_response',
                'success': True,
                'user': {
                    'id': result['id'],
                    'username': result['username'],
                    'wins': result['wins'],
                    'losses': result['losses'],
                    'draws': result['draws']
                },
                'token': session_token
            }
        else:
            response = {'action': 'login_response', 'success': False, 'message': result}
        client_socket.send(json.dumps(response).encode('utf-8'))

    def handle_find_match(self, session_token):
        """Xử lý tìm trận đấu"""
        if session_token not in self.waiting_room:
            self.waiting_room.append(session_token)
            if len(self.waiting_room) >= 2:
                p1 = self.waiting_room.pop(0)
                p2 = self.waiting_room.pop(0)
                game_id = secrets.token_hex(8)
                self.active_games[game_id] = {
                    'player1': p1,
                    'player2': p2,
                    'choices': {}
                }
                self.clients[p1]['in_game'] = True
                self.clients[p2]['in_game'] = True
                
                self.clients[p1]['socket'].send(json.dumps({
                    'action': 'match_found',
                    'game_id': game_id,
                    'opponent': self.clients[p2]['user']['username']
                }).encode('utf-8'))
                
                self.clients[p2]['socket'].send(json.dumps({
                    'action': 'match_found',
                    'game_id': game_id,
                    'opponent': self.clients[p1]['user']['username']
                }).encode('utf-8'))

    def handle_make_choice(self, session_token, message):
        """Xử lý lựa chọn trong game"""
        game_id = message['game_id']
        choice = message['choice']
        
        if game_id not in self.active_games:
            return
        
        game = self.active_games[game_id]
        if session_token == game['player1']:
            game['choices']['player1'] = choice
        elif session_token == game['player2']:
            game['choices']['player2'] = choice
        
        if len(game['choices']) == 2:
            self.process_game_result(game_id, game)

    def process_game_result(self, game_id, game):
        """Xử lý kết quả trận đấu"""
        result = self.game_logic.determine_winner(
            game['choices']['player1'],
            game['choices']['player2']
        )
        
        p1_user = self.clients[game['player1']]['user']
        p2_user = self.clients[game['player2']]['user']
        
        winner_id = None
        if result == 'player1':
            winner_id = p1_user['id']
        elif result == 'player2':
            winner_id = p2_user['id']
        
        # Lưu kết quả vào database
        self.db.save_match(
            p1_user['id'], p2_user['id'],
            game['choices']['player1'],
            game['choices']['player2'],
            winner_id
        )
        
        # ✨ CÂP NHẬT THỐNG KÊ NGAY LẬP TỨC ✨
        # Lấy thống kê mới từ database
        p1_stats = self.db.get_user_stats(p1_user['id'])
        p2_stats = self.db.get_user_stats(p2_user['id'])
        
        # Cập nhật thống kê trong bộ nhớ server
        if p1_stats:
            self.clients[game['player1']]['user']['wins'] = p1_stats['wins']
            self.clients[game['player1']]['user']['losses'] = p1_stats['losses']
            self.clients[game['player1']]['user']['draws'] = p1_stats['draws']
        
        if p2_stats:
            self.clients[game['player2']]['user']['wins'] = p2_stats['wins']
            self.clients[game['player2']]['user']['losses'] = p2_stats['losses']
            self.clients[game['player2']]['user']['draws'] = p2_stats['draws']
        
        # Gửi kết quả cho player 1 (kèm stats mới)
        result_data = {
            'action': 'game_result',
            'your_choice': game['choices']['player1'],
            'opponent_choice': game['choices']['player2'],
            'result': result,
            'updated_stats': {
                'wins': p1_stats['wins'] if p1_stats else p1_user['wins'],
                'losses': p1_stats['losses'] if p1_stats else p1_user['losses'],
                'draws': p1_stats['draws'] if p1_stats else p1_user['draws']
            }
        }
        self.clients[game['player1']]['socket'].send(
            json.dumps(result_data).encode('utf-8')
        )
        
        # Gửi kết quả cho player 2 (kèm stats mới)
        result_data['your_choice'] = game['choices']['player2']
        result_data['opponent_choice'] = game['choices']['player1']
        if result == 'player1':
            result_data['result'] = 'player2'
        elif result == 'player2':
            result_data['result'] = 'player1'
        result_data['updated_stats'] = {
            'wins': p2_stats['wins'] if p2_stats else p2_user['wins'],
            'losses': p2_stats['losses'] if p2_stats else p2_user['losses'],
            'draws': p2_stats['draws'] if p2_stats else p2_user['draws']
        }
        
        self.clients[game['player2']]['socket'].send(
            json.dumps(result_data).encode('utf-8')
        )
        
        self.clients[game['player1']]['in_game'] = False
        self.clients[game['player2']]['in_game'] = False
        del self.active_games[game_id]

    def cleanup_client(self, session_token, client_socket, addr):
        """Dọn dẹp khi client ngắt kết nối"""
        if session_token in self.waiting_room:
            self.waiting_room.remove(session_token)
        if session_token in self.clients:
            del self.clients[session_token]
        client_socket.close()
        print(f"[DISCONNECTED] {addr}")

    def start(self):
        """Khởi động server"""
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.host}:{self.port}")
        
        while True:
            client_socket, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    server = GameServer()
    server.start()