# Cấu hình Database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',      
    'password': '',       
    'database': 'rps_game'
}

# Cấu hình Server
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5555

# Cấu hình Client
CLIENT_HOST = 'localhost'
CLIENT_PORT = 5555

# Cấu hình màu sắc
COLORS = {
    'primary': '#0f3460',
    'secondary': '#16213e',
    'accent': '#e94560',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'bg': '#1a1a2e',
    'text': '#ffffff',
    'text_secondary': '#a0a0a0'
}

# Cấu hình game
GAME_CHOICES = {
    'rock': {'emoji': '✊', 'name': 'Búa', 'beats': 'scissors'},
    'paper': {'emoji': '✋', 'name': 'Bao', 'beats': 'rock'},
    'scissors': {'emoji': '✌️', 'name': 'Kéo', 'beats': 'paper'}
}