import tkinter as tk
from tkinter import messagebox
from ui_components import UIComponents
from network_handler import NetworkHandler

class RockPaperScissorsClient:
    def __init__(self):
        self.user = None
        self.game_id = None
        self.root = tk.Tk()
        self.root.title("🎮 Kéo - Búa - Bao Online")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        self.colors = {
            'primary': '#0f3460',
            'secondary': '#16213e',
            'accent': '#e94560',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'bg': '#1a1a2e',

            'text': '#ffffff',
            'text_secondary': '#a0a0a0'
        }
        self.root.configure(bg=self.colors['bg'])
        
        self.ui = UIComponents(self.colors)
        self.network = NetworkHandler(self.handle_server_message)
        
        self.ui.setup_styles(self.root)
        self.show_login_screen()
        
    def handle_server_message(self, message):
        """Xử lý tin nhắn từ server"""
        action = message.get('action')
        
        if action == 'register_response':
            self.root.after(0, lambda: self.handle_register_response(message))
        elif action == 'login_response':
            self.root.after(0, lambda: self.handle_login_response(message))
        elif action == 'match_found':
            self.root.after(0, lambda: self.handle_match_found(message))
        elif action == 'game_result':
            self.root.after(0, lambda: self.handle_game_result(message))
        elif action == 'stats_refreshed':
            self.root.after(0, lambda: self.handle_stats_refreshed(message))

    def clear_screen(self):
        """Xóa tất cả widget"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Hiển thị màn hình đăng nhập"""
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both')
        
        # Logo và tiêu đề
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])

        title_frame.pack(pady=(50, 30))
        
        emoji_label = tk.Label(title_frame, text="✊✋✌️", font=('Segoe UI', 60), bg=self.colors['bg'])
        emoji_label.pack()
        
        title = tk.Label(title_frame, text="KÉO - BÚA - BAO", font=('Segoe UI', 32, 'bold'), 
                        fg=self.colors['accent'], bg=self.colors['bg'])
        title.pack(pady=(10, 5))
        
        subtitle = tk.Label(title_frame, text="Chơi trực tuyến với bạn bè", font=('Segoe UI', 14), 
                           fg=self.colors['text_secondary'], bg=self.colors['bg'])
        subtitle.pack()
        
        # Form đăng nhập
        form_frame = tk.Frame(main_frame, bg=self.colors['secondary'], padx=50, pady=40)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="ĐĂNG NHẬP", font=('Segoe UI', 18, 'bold'), 
                fg='white', bg=self.colors['secondary']).pack(pady=(0, 30))
        
        self.login_username = self.ui.create_modern_entry(form_frame, "Tên đăng nhập")
        self.login_username.pack(pady=10, ipady=10, ipadx=10, fill='x')
        
        self.login_password = self.ui.create_modern_entry(form_frame, "Mật khẩu", show='*')
        self.login_password.pack(pady=10, ipady=10, ipadx=10, fill='x')
        
        btn_frame = tk.Frame(form_frame, bg=self.colors['secondary'])
        btn_frame.pack(pady=(20, 0))
        
        login_btn = self.ui.create_modern_button(btn_frame, "ĐĂNG NHẬP", self.login, self.colors['success'])
        login_btn.pack(side='left', padx=5)
        
        register_btn = self.ui.create_modern_button(btn_frame, "ĐĂNG KÝ", self.show_register_screen, self.colors['warning'])
        register_btn.pack(side='left', padx=5)

    def show_register_screen(self):
        """Hiển thị màn hình đăng ký"""
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both')
        
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.pack(pady=(50, 30))
        
        emoji_label = tk.Label(title_frame, text="📝", font=('Segoe UI', 60), bg=self.colors['bg'])
        emoji_label.pack()
        
        title = tk.Label(title_frame, text="TẠO TÀI KHOẢN", font=('Segoe UI', 28, 'bold'), 

                        fg=self.colors['accent'], bg=self.colors['bg'])
        title.pack(pady=(10, 5))
        
        form_frame = tk.Frame(main_frame, bg=self.colors['secondary'], padx=50, pady=40)
        form_frame.pack(pady=20)
        
        self.reg_username = self.ui.create_modern_entry(form_frame, "Tên đăng nhập")
        self.reg_username.pack(pady=10, ipady=10, ipadx=10, fill='x')
        
        self.reg_email = self.ui.create_modern_entry(form_frame, "Email (tùy chọn)")
        self.reg_email.pack(pady=10, ipady=10, ipadx=10, fill='x')
        
        self.reg_password = self.ui.create_modern_entry(form_frame, "Mật khẩu", show='*')
        self.reg_password.pack(pady=10, ipady=10, ipadx=10, fill='x')
        
        self.reg_password_confirm = self.ui.create_modern_entry(form_frame, "Xác nhận mật khẩu", show='*')
        self.reg_password_confirm.pack(pady=10, ipady=10, ipadx=10, fill='x')
        
        btn_frame = tk.Frame(form_frame, bg=self.colors['secondary'])
        btn_frame.pack(pady=(20, 0))
        
        register_btn = self.ui.create_modern_button(btn_frame, "ĐĂNG KÝ", self.register, self.colors['success'])
        register_btn.pack(side='left', padx=5)
        
        back_btn = self.ui.create_modern_button(btn_frame, "QUAY LẠI", self.show_login_screen, self.colors['primary'])
        back_btn.pack(side='left', padx=5)

    def login(self):
        """Xử lý đăng nhập"""
        username = self.login_username.get()
        password = self.login_password.get()
        
        if username in ["Tên đăng nhập", ""] or password in ["Mật khẩu", ""]:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if not self.network.connect_to_server():
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến server!")
            return
        
        self.network.send_message({
            
            'action': 'login',
            'username': username,
            'password': password
        })

    def register(self):
        """Xử lý đăng ký"""
        username = self.reg_username.get()
        email = self.reg_email.get()
        password = self.reg_password.get()
        password_confirm = self.reg_password_confirm.get()
        
        if username in ["Tên đăng nhập", ""] or password in ["Mật khẩu", ""]:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if password != password_confirm:
            messagebox.showwarning("Cảnh báo", "Mật khẩu xác nhận không khớp!")
            return
        
        if not self.network.connect_to_server():
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến server!")
            return
        
        if email == "Email (tùy chọn)":
            email = ""
        
        self.network.send_message({
            'action': 'register',
            'username': username,
            'password': password,
            'email': email
        })

    def handle_register_response(self, message):
        """Xử lý phản hồi đăng ký"""
        if message['success']:
            messagebox.showinfo("Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
            self.show_login_screen()
        else:
            messagebox.showerror("Lỗi", message['message'])

    def handle_login_response(self, message):
        """Xử lý phản hồi đăng nhập"""
        if message['success']:
            self.user = message['user']
            self.network.token = message['token']
            self.show_main_menu()
        else:
            messagebox.showerror("Lỗi", message['message'])

    def show_main_menu(self):
        """Hiển thị menu chính"""
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both')
        
        # Header
        header = tk.Frame(main_frame, bg=self.colors['secondary'], height=100)
        header.pack(fill='x', pady=(0, 30))
        header.pack_propagate(False)
        
        welcome_label = tk.Label(header, text=f"👋 Xin chào, {self.user['username']}!", 
                                font=('Segoe UI', 20, 'bold'), fg='white', bg=self.colors['secondary'])
        welcome_label.pack(pady=20)
        
        # Stats
        stats_frame = tk.Frame(main_frame, bg=self.colors['secondary'], padx=40, pady=30)
        stats_frame.pack(pady=20)
        
        tk.Label(stats_frame, text="THỐNG KÊ CỦA BẠN", font=('Segoe UI', 16, 'bold'), 
                fg='white', bg=self.colors['secondary']).pack(pady=(0, 20))
        
        stats_grid = tk.Frame(stats_frame, bg=self.colors['secondary'])
        stats_grid.pack()
        
        self.ui.create_stat_card(stats_grid, "🏆", "Thắng", self.user['wins'], self.colors['success'], 0, 0)
        self.ui.create_stat_card(stats_grid, "❌", "Thua", self.user['losses'], self.colors['accent'], 0, 1)
        self.ui.create_stat_card(stats_grid, "🤝", "Hòa", self.user['draws'], self.colors['warning'], 0, 2)
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=30)
        
        play_btn = self.ui.create_modern_button(btn_frame, "🎮 TÌM TRẬN ĐẤU", self.find_match, self.colors['success'])
        play_btn.config(font=('Segoe UI', 16, 'bold'), padx=50, pady=20)
        play_btn.pack(pady=10)
        
        logout_btn = self.ui.create_modern_button(btn_frame, "🚪 ĐĂNG XUẤT", self.logout, self.colors['accent'])
        logout_btn.pack(pady=10)
        
        # 🔄 Tự động làm mới stats sau khi hiển thị menu
        self.root.after(100, self.refresh_stats)

    def find_match(self):
        """Tìm trận đấu"""
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both')
        
        tk.Label(main_frame, text="🔍", font=('Segoe UI', 80), bg=self.colors['bg']).pack(pady=(100, 20))
        tk.Label(main_frame, text="Đang tìm đối thủ...", font=('Segoe UI', 24, 'bold'), 
                fg='white', bg=self.colors['bg']).pack(pady=10)
        
        # Loading animation
        self.loading_label = tk.Label(main_frame, text="●○○○○", font=('Segoe UI', 20), 
                                     fg=self.colors['accent'], bg=self.colors['bg'])
        self.loading_label.pack(pady=20)
        self.animate_loading()
        
        cancel_btn = self.ui.create_modern_button(main_frame, "HỦY", self.show_main_menu, self.colors['accent'])
        cancel_btn.pack(pady=30)
        
        self.network.send_message({'action': 'find_match'})

    def animate_loading(self, dots=0):
        """Animation loading"""
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            patterns = ["●○○○○", "○●○○○", "○○●○○", "○○○●○", "○○○○●"]
            self.loading_label.config(text=patterns[dots % 5])
            self.root.after(200, lambda: self.animate_loading(dots + 1))

    def handle_match_found(self, message):
        """Xử lý khi tìm thấy trận đấu"""
        self.game_id = message['game_id']
        opponent = message['opponent']
        self.show_game_screen(opponent)

    def show_game_screen(self, opponent):
        """Hiển thị màn hình chơi game"""
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both')
        
        # Header
        header = tk.Frame(main_frame, bg=self.colors['secondary'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        vs_frame = tk.Frame(header, bg=self.colors['secondary'])
        vs_frame.pack(expand=True)
        
        tk.Label(vs_frame, text=self.user['username'], font=('Segoe UI', 16, 'bold'), 
                fg=self.colors['success'], bg=self.colors['secondary']).pack(side='left', padx=20)
        tk.Label(vs_frame, text="⚔️ VS ⚔️", font=('Segoe UI', 16, 'bold'), 
                fg='white', bg=self.colors['secondary']).pack(side='left', padx=20)
        tk.Label(vs_frame, text=opponent, font=('Segoe UI', 16, 'bold'), 
                fg=self.colors['accent'], bg=self.colors['secondary']).pack(side='left', padx=20)
        
        # Instruction
        tk.Label(main_frame, text="CHỌN LỰA CHỌN CỦA BẠN!", font=('Segoe UI', 24, 'bold'), 
                fg='white', bg=self.colors['bg']).pack(pady=(50, 30))
        
        # Choice buttons
        choice_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        choice_frame.pack(pady=30)
        
        choices = [
            ('✊', 'rock', 'Búa', self.colors['accent']),
            ('✋', 'paper', 'Bao', self.colors['success']),
            ('✌️', 'scissors', 'Kéo', self.colors['warning'])
        ]
        
        for emoji, choice, name, color in choices:
            btn_container = tk.Frame(choice_frame, bg=self.colors['bg'])
            btn_container.pack(side='left', padx=20)
            
            btn = tk.Button(
                btn_container,
                text=emoji,
                font=('Segoe UI', 60),
                bg=color,
                fg='white',
                relief='flat',
                padx=40,
                pady=20,
                cursor='hand2',
                command=lambda c=choice: self.make_choice(c),
                activebackground=self.ui.lighten_color(color)
            )
            btn.pack()
            
            tk.Label(btn_container, text=name, font=('Segoe UI', 14, 'bold'), 
                    fg='white', bg=self.colors['bg']).pack(pady=(10, 0))

    def make_choice(self, choice):
        """Thực hiện lựa chọn"""
        self.network.send_message({
            'action': 'make_choice',
            'game_id': self.game_id,
            'choice': choice
        })
        
        self.clear_screen()
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both')
        
        tk.Label(main_frame, text="⏳", font=('Segoe UI', 80), bg=self.colors['bg']).pack(pady=(150, 20))
        tk.Label(main_frame, text="Đang chờ đối thủ...", font=('Segoe UI', 24, 'bold'), 
                fg='white', bg=self.colors['bg']).pack()

    def handle_game_result(self, message):
        """Xử lý kết quả trận đấu"""
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both')
        
        result = message['result']
        your_choice = message['your_choice']
        opponent_choice = message['opponent_choice']
        
        choice_emoji = {
            'rock': '✊',
            'paper': '✋',
            'scissors': '✌️'
        }
        
        if result == 'player1':
            emoji = "🎉"
            text = "BẠN THẮNG!"
            color = self.colors['success']
        elif result == 'player2':
            emoji = "😢"
            text = "BẠN THUA!"
            color = self.colors['accent']
        else:
            emoji = "🤝"
            text = "HÒA!"
            color = self.colors['warning']
        
        tk.Label(main_frame, text=emoji, font=('Segoe UI', 100), bg=self.colors['bg']).pack(pady=(80, 20))
        tk.Label(main_frame, text=text, font=('Segoe UI', 32, 'bold'), 
                fg=color, bg=self.colors['bg']).pack(pady=10)
        
        # Hiển thị lựa chọn
        result_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        result_frame.pack(pady=40)
        
        tk.Label(result_frame, text=f"Bạn: {choice_emoji[your_choice]}", 
                font=('Segoe UI', 24), fg='white', bg=self.colors['bg']).pack(side='left', padx=30)
        tk.Label(result_frame, text="VS", font=('Segoe UI', 20, 'bold'), 
                fg=self.colors['text_secondary'], bg=self.colors['bg']).pack(side='left', padx=20)
        tk.Label(result_frame, text=f"Đối thủ: {choice_emoji[opponent_choice]}", 
                font=('Segoe UI', 24), fg='white', bg=self.colors['bg']).pack(side='left', padx=30)
        
        back_btn = self.ui.create_modern_button(main_frame, "QUAY LẠI MENU", self.show_main_menu, self.colors['primary'])
        back_btn.config(font=('Segoe UI', 14, 'bold'))
        back_btn.pack(pady=30)

    def logout(self):
        """Đăng xuất"""
        self.network.close()
        self.user = None
        self.show_login_screen()

    def refresh_stats(self):
        """Làm mới thống kê từ server"""
        if self.user and self.network:
            self.network.send_message({'action': 'refresh_stats'})

    def handle_stats_refreshed(self, message):
        """Xử lý khi nhận thống kê mới"""
        if 'stats' in message:
            self.user['wins'] = message['stats']['wins']
            self.user['losses'] = message['stats']['losses']
            self.user['draws'] = message['stats']['draws']
            # Cập nhật lại giao diện nếu đang ở menu
            self.update_stats_display()

    def update_stats_display(self):
        """Cập nhật hiển thị thống kê"""
        if hasattr(self, 'stats_labels') and self.user:
            if 'wins' in self.stats_labels:
                self.stats_labels['wins'].config(text=str(self.user['wins']))
            if 'losses' in self.stats_labels:
                self.stats_labels['losses'].config(text=str(self.user['losses']))
            if 'draws' in self.stats_labels:
                self.stats_labels['draws'].config(text=str(self.user['draws']))

    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()

if __name__ == "__main__":
    app = RockPaperScissorsClient()
    app.run()