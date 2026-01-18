import mysql.connector
import hashlib

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.init_database()

    def init_database(self):
        """Khởi tạo cơ sở dữ liệu và bảng"""
        try:
            conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password']
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS rps_game")
            cursor.close()
            conn.close()

            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            # Bảng người dùng
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    wins INT DEFAULT 0,
                    losses INT DEFAULT 0,
                    draws INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Bảng lịch sử trận đấu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS match_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    player1_id INT,
                    player2_id INT,
                    player1_choice VARCHAR(10),
                    player2_choice VARCHAR(10),
                    winner_id INT,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (player1_id) REFERENCES users(id),
                    FOREIGN KEY (player2_id) REFERENCES users(id)
                )
            ''')
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✓ Database initialized successfully")
        except Exception as e:
            print(f"✗ Database error: {e}")

    def hash_password(self, password):
        """Mã hóa mật khẩu"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, email):
        """Đăng ký người dùng mới"""
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                (username, password_hash, email)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Registration successful"
        except mysql.connector.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def login_user(self, username, password):
        """Đăng nhập người dùng"""
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            password_hash = self.hash_password(password)
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password_hash=%s",
                (username, password_hash)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                return True, user
            return False, "Invalid credentials"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_user_stats(self, user_id):
        """Lấy thống kê người chơi"""
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT wins, losses, draws FROM users WHERE id=%s", (user_id,))
            stats = cursor.fetchone()
            cursor.close()
            conn.close()
            return stats
        except Exception as e:
            return None

    def save_match(self, p1_id, p2_id, p1_choice, p2_choice, winner_id):
        """Lưu kết quả trận đấu"""
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO match_history 
                   (player1_id, player2_id, player1_choice, player2_choice, winner_id)
                   VALUES (%s, %s, %s, %s, %s)""",
                (p1_id, p2_id, p1_choice, p2_choice, winner_id)
            )
            
            # Cập nhật thống kê
            if winner_id == p1_id:
                cursor.execute("UPDATE users SET wins=wins+1 WHERE id=%s", (p1_id,))
                cursor.execute("UPDATE users SET losses=losses+1 WHERE id=%s", (p2_id,))
            elif winner_id == p2_id:
                cursor.execute("UPDATE users SET wins=wins+1 WHERE id=%s", (p2_id,))
                cursor.execute("UPDATE users SET losses=losses+1 WHERE id=%s", (p1_id,))
            else:
                cursor.execute("UPDATE users SET draws=draws+1 WHERE id=%s", (p1_id,))
                cursor.execute("UPDATE users SET draws=draws+1 WHERE id=%s", (p2_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error saving match: {e}")