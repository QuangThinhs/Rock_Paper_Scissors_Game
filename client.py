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
        self.root.geometry("1000x750") # Tăng kích thước một chút cho thoáng
        self.root.resizable(False, False)
        
        # Bảng màu Modern Cyberpunk
        self.colors = {
            'primary': '#0f3460',
            'secondary': '#16213e', 
            'accent': '#e94560',
            'success': '#00b894', # Xanh mint hiện đại hơn
            'warning': '#fdcb6e', # Vàng dịu
            'bg': '#1a1a2e',
            'card_bg': '#252a41', # Màu nền cho các khung card
            'text': '#ffffff',
            'text_secondary': '#b2bec3',
            'input_bg': '#303a52'
        }
        self.root.configure(bg=self.colors['bg'])
        
        # Vẫn giữ khởi tạo logic cũ
        self.ui = UIComponents(self.colors)
        self.network = NetworkHandler(self.handle_server_message)
        
        self.ui.setup_styles(self.root)
        
        # Căn giữa cửa sổ khi mở
        self.center_window()
        self.show_login_screen()

    def center_window(self):
        """Hàm phụ trợ để căn giữa màn hình"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    # --- Helper tạo Widget đẹp (Thay thế cho các hàm UI cơ bản để control giao diện tốt hơn) ---
    def create_styled_button(self, parent, text, command, bg_color, width=15, font_size=12):
        btn = tk.Button(parent, text=text, command=command,
                       font=('Segoe UI', font_size, 'bold'),
                       bg=bg_color, fg='white',
                       activebackground=self.colors['text'], activeforeground=bg_color,
                       relief='flat', cursor='hand2', borderwidth=0,
                       width=width, pady=10)
        
        # Hiệu ứng Hover
        def on_enter(e): btn.config(bg=self.ui.lighten_color(bg_color) if hasattr(self.ui, 'lighten_color') else '#ffffff', fg=bg_color)
        def on_leave(e): btn.config(bg=bg_color, fg='white')
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn

    def create_styled_entry(self, parent, placeholder, show=None):
        container = tk.Frame(parent, bg=self.colors['card_bg'], pady=2)
        container.pack(fill='x', pady=10)
        
        lbl = tk.Label(container, text=placeholder, font=('Segoe UI', 10), 
                      fg=self.colors['text_secondary'], bg=self.colors['card_bg'], anchor='w')
        lbl.pack(fill='x')
        
        entry = tk.Entry(container, font=('Segoe UI', 12), bg=self.colors['input_bg'], 
                        fg='white', relief='flat', insertbackground='white')
        if show: entry.config(show=show)
        entry.pack(fill='x', ipady=8, ipadx=5)
        
        # Viền dưới focus
        border = tk.Frame(container, height=2, bg=self.colors['primary'])
        border.pack(fill='x')
        
        def on_focus_in(e): border.config(bg=self.colors['accent'])
        def on_focus_out(e): border.config(bg=self.colors['primary'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry

    # ---------------- LOGIC GIỮ NGUYÊN 100% ----------------
    
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
        """Hiển thị màn hình đăng nhập - Thiết kế dạng Card"""
        self.clear_screen()
        
        # Container chính căn giữa
        center_frame = tk.Frame(self.root, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo Area
        tk.Label(center_frame, text="✊✋✌️", font=('Segoe UI', 70), bg=self.colors['bg']).pack()
        tk.Label(center_frame, text="KÉO BÚA BAO", font=('Segoe UI', 36, 'bold'), 
                 fg=self.colors['text'], bg=self.colors['bg']).pack(pady=(0, 5))
        tk.Label(center_frame, text="Đấu trường trực tuyến", font=('Segoe UI', 14), 
                 fg=self.colors['accent'], bg=self.colors['bg']).pack(pady=(0, 30))
        
        # Form Card
        card = tk.Frame(center_frame, bg=self.colors['card_bg'], padx=40, pady=40)
        card.pack(ipadx=20)
        
        # Giả lập Shadow cho Card (Optional, đơn giản bằng border)
        card.config(highlightbackground=self.colors['secondary'], highlightthickness=1)

        tk.Label(card, text="ĐĂNG NHẬP", font=('Segoe UI', 16, 'bold'), 
                 fg=self.colors['text'], bg=self.colors['card_bg']).pack(pady=(0, 20), anchor='w')
        
        # Inputs
        self.login_username = self.create_styled_entry(card, "Tên đăng nhập")
        self.login_password = self.create_styled_entry(card, "Mật khẩu", show='*')
        
        # Buttons Area
        btn_frame = tk.Frame(card, bg=self.colors['card_bg'])
        btn_frame.pack(pady=(30, 0), fill='x')
        
        login_btn = self.create_styled_button(btn_frame, "ĐĂNG NHẬP", self.login, self.colors['accent'], width=20)
        login_btn.pack(fill='x', pady=(0, 10))
        
        reg_btn = tk.Button(btn_frame, text="Chưa có tài khoản? Đăng ký ngay", 
                           command=self.show_register_screen,
                           font=('Segoe UI', 10), bg=self.colors['card_bg'], fg=self.colors['text_secondary'],
                           relief='flat', activebackground=self.colors['card_bg'], activeforeground='white', bd=0)
        reg_btn.pack()

    def show_register_screen(self):
        """Hiển thị màn hình đăng ký - Thiết kế đồng bộ"""
        self.clear_screen()
        
        center_frame = tk.Frame(self.root, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(center_frame, text="📝", font=('Segoe UI', 50), bg=self.colors['bg']).pack()
        tk.Label(center_frame, text="TẠO TÀI KHOẢN", font=('Segoe UI', 28, 'bold'), 
                 fg=self.colors['text'], bg=self.colors['bg']).pack(pady=(0, 20))
        
        card = tk.Frame(center_frame, bg=self.colors['card_bg'], padx=40, pady=30)
        card.pack(ipadx=20)
        
        self.reg_username = self.create_styled_entry(card, "Tên đăng nhập")
        self.reg_email = self.create_styled_entry(card, "Email (tùy chọn)")
        self.reg_password = self.create_styled_entry(card, "Mật khẩu", show='*')
        self.reg_password_confirm = self.create_styled_entry(card, "Xác nhận mật khẩu", show='*')
        
        btn_frame = tk.Frame(card, bg=self.colors['card_bg'])
        btn_frame.pack(pady=(30, 0), fill='x')
        
        reg_btn = self.create_styled_button(btn_frame, "HOÀN TẤT ĐĂNG KÝ", self.register, self.colors['success'])
        reg_btn.pack(fill='x', pady=(0, 10))
        
        back_btn = tk.Button(btn_frame, text="Quay lại đăng nhập", command=self.show_login_screen,
                            font=('Segoe UI', 10), bg=self.colors['card_bg'], fg=self.colors['text_secondary'],
                            relief='flat', bd=0, cursor='hand2')
        back_btn.pack()

    def login(self):
        """Logic giữ nguyên"""
        username = self.login_username.get()
        password = self.login_password.get()
        
        if not username or not password:
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
        """Logic giữ nguyên"""
        username = self.reg_username.get()
        email = self.reg_email.get()
        password = self.reg_password.get()
        password_confirm = self.reg_password_confirm.get()
        
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if password != password_confirm:
            messagebox.showwarning("Cảnh báo", "Mật khẩu xác nhận không khớp!")
            return
        
        if not self.network.connect_to_server():
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến server!")
            return
        
        self.network.send_message({
            'action': 'register',
            'username': username,
            'password': password,
            'email': email
        })

    def handle_register_response(self, message):
        if message['success']:
            messagebox.showinfo("Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
            self.show_login_screen()
        else:
            messagebox.showerror("Lỗi", message['message'])

    def handle_login_response(self, message):
        if message['success']:
            self.user = message['user']
            self.network.token = message['token']
            self.show_main_menu()
        else:
            messagebox.showerror("Lỗi", message['message'])

    def show_main_menu(self):
        """Màn hình chính - Dashboard style"""
        self.clear_screen()
        
        # Header Bar
        header = tk.Frame(self.root, bg=self.colors['secondary'], padx=30, pady=20)
        header.pack(fill='x')
        
        welcome_lbl = tk.Label(header, text=f"Xin chào, {self.user['username']}", 
                              font=('Segoe UI', 16, 'bold'), fg='white', bg=self.colors['secondary'])
        welcome_lbl.pack(side='left')
        
        logout_btn = tk.Button(header, text="Đăng xuất 🚪", command=self.logout,
                              bg=self.colors['secondary'], fg=self.colors['accent'],
                              relief='flat', font=('Segoe UI', 10, 'bold'), bd=0, cursor='hand2')
        logout_btn.pack(side='right')

        # Main Content
        content = tk.Frame(self.root, bg=self.colors['bg'])
        content.pack(expand=True, fill='both', padx=50, pady=20)

        # Title
        tk.Label(content, text="THỐNG KÊ CÁ NHÂN", font=('Segoe UI', 24, 'bold'), 
                 fg=self.colors['text'], bg=self.colors['bg']).pack(pady=(20, 30))

        # Stats Cards Container (Flex row)
        stats_frame = tk.Frame(content, bg=self.colors['bg'])
        stats_frame.pack(pady=20)
        
        self.stats_labels = {} # Khởi tạo dict lưu label để update
        
        def create_stat_box(parent, icon, title, key, color):
            box = tk.Frame(parent, bg=self.colors['card_bg'], width=200, height=150)
            box.pack_propagate(False)
            box.pack(side='left', padx=20)
            
            # Decoration line
            tk.Frame(box, bg=color, height=4).pack(fill='x')
            
            tk.Label(box, text=icon, font=('Segoe UI', 30), bg=self.colors['card_bg']).pack(pady=(20, 5))
            tk.Label(box, text=title, font=('Segoe UI', 12), fg=self.colors['text_secondary'], bg=self.colors['card_bg']).pack()
            
            # Label giá trị
            val_lbl = tk.Label(box, text=str(self.user[key]), font=('Segoe UI', 24, 'bold'), 
                             fg='white', bg=self.colors['card_bg'])
            val_lbl.pack(pady=5)
            
            self.stats_labels[key] = val_lbl
            
        create_stat_box(stats_frame, "🏆", "CHIẾN THẮNG", 'wins', self.colors['success'])
        create_stat_box(stats_frame, "❌", "THẤT BẠI", 'losses', self.colors['accent'])
        create_stat_box(stats_frame, "🤝", "HÒA", 'draws', self.colors['warning'])

        # Action Buttons
        action_area = tk.Frame(content, bg=self.colors['bg'])
        action_area.pack(pady=50)
        
        play_btn = self.create_styled_button(action_area, "🎮 TÌM TRẬN ĐẤU NGAY", self.find_match, self.colors['accent'], width=25, font_size=16)
        play_btn.config(pady=15) # Nút to hơn
        play_btn.pack()

        self.root.after(100, self.refresh_stats)

    def find_match(self):
        """Màn hình loading đẹp hơn"""
        self.clear_screen()
        
        center = tk.Frame(self.root, bg=self.colors['bg'])
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        # Radar/Scan effect visualization (Static text for now)
        tk.Label(center, text="📡", font=('Segoe UI', 80), bg=self.colors['bg'], fg=self.colors['success']).pack(pady=20)
        
        tk.Label(center, text="ĐANG QUÉT MẠNG LƯỚI...", font=('Segoe UI', 20, 'bold'), 
                 fg='white', bg=self.colors['bg']).pack()
        
        self.loading_label = tk.Label(center, text="● ○ ○ ○ ○", font=('Segoe UI', 24), 
                                    fg=self.colors['text_secondary'], bg=self.colors['bg'])
        self.loading_label.pack(pady=20)
        self.animate_loading()
        
        cancel_btn = tk.Button(center, text="HỦY BỎ", command=self.show_main_menu,
                              font=('Segoe UI', 12), bg=self.colors['bg'], fg=self.colors['accent'],
                              relief='flat', bd=0, cursor='hand2')
        cancel_btn.pack(pady=20)
        
        self.network.send_message({'action': 'find_match'})

    def animate_loading(self, dots=0):
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            patterns = ["● ○ ○ ○ ○", "○ ● ○ ○ ○", "○ ○ ● ○ ○", "○ ○ ○ ● ○", "○ ○ ○ ○ ●"]
            self.loading_label.config(text=patterns[dots % 5])
            self.root.after(200, lambda: self.animate_loading(dots + 1))

    def handle_match_found(self, message):
        self.game_id = message['game_id']
        opponent = message['opponent']
        self.show_game_screen(opponent)

    def show_game_screen(self, opponent):
        """Màn hình chơi game - Tập trung vào UX"""
        self.clear_screen()
        
        # Header VS
        header = tk.Frame(self.root, bg=self.colors['secondary'], pady=15)
        header.pack(fill='x')
        
        vs_container = tk.Frame(header, bg=self.colors['secondary'])
        vs_container.pack()
        
        # Player 1
        tk.Label(vs_container, text="👤 BẠN", font=('Segoe UI', 10), fg=self.colors['text_secondary'], bg=self.colors['secondary']).grid(row=0, column=0)
        tk.Label(vs_container, text=self.user['username'], font=('Segoe UI', 18, 'bold'), fg=self.colors['success'], bg=self.colors['secondary']).grid(row=1, column=0, padx=20)
        
        # VS Icon
        tk.Label(vs_container, text="⚔️", font=('Segoe UI', 24), bg=self.colors['secondary']).grid(row=0, column=1, rowspan=2, padx=20)
        
        # Player 2
        tk.Label(vs_container, text="ĐỐI THỦ 👤", font=('Segoe UI', 10), fg=self.colors['text_secondary'], bg=self.colors['secondary']).grid(row=0, column=2)
        tk.Label(vs_container, text=opponent, font=('Segoe UI', 18, 'bold'), fg=self.colors['accent'], bg=self.colors['secondary']).grid(row=1, column=2, padx=20)
        
        # Game Area
        game_area = tk.Frame(self.root, bg=self.colors['bg'])
        game_area.pack(expand=True)
        
        tk.Label(game_area, text="HÃY RA ĐÒN QUYẾT ĐỊNH!", font=('Segoe UI', 20, 'bold'), 
                 fg='white', bg=self.colors['bg']).pack(pady=(0, 40))
        
        # Choice Buttons (Large)
        choices_frame = tk.Frame(game_area, bg=self.colors['bg'])
        choices_frame.pack()
        
        choices = [
            ('✊', 'rock', 'BÚA', '#e17055'),
            ('✋', 'paper', 'BAO', '#0984e3'),
            ('✌️', 'scissors', 'KÉO', '#fdcb6e')
        ]
        
        for emoji, choice, name, color in choices:
            btn_frame = tk.Frame(choices_frame, bg=self.colors['bg'], padx=20)
            btn_frame.pack(side='left')
            
            # Nút tròn to
            btn = tk.Button(btn_frame, text=emoji, font=('Segoe UI', 50),
                           bg=self.colors['card_bg'], fg=color,
                           relief='flat', bd=0, cursor='hand2',
                           width=3, height=1,
                           command=lambda c=choice: self.make_choice(c))
            btn.pack()
            
            # Hover effect đổi màu nền
            def on_e(e, b=btn, c=color): b.config(bg=c, fg='white')
            def on_l(e, b=btn, c=color): b.config(bg=self.colors['card_bg'], fg=c)
            btn.bind('<Enter>', on_e)
            btn.bind('<Leave>', on_l)
            
            tk.Label(btn_frame, text=name, font=('Segoe UI', 14, 'bold'), 
                     fg=color, bg=self.colors['bg']).pack(pady=10)

    def make_choice(self, choice):
        self.network.send_message({
            'action': 'make_choice',
            'game_id': self.game_id,
            'choice': choice
        })
        
        self.clear_screen()
        center = tk.Frame(self.root, bg=self.colors['bg'])
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(center, text="⏳", font=('Segoe UI', 60), bg=self.colors['bg']).pack(pady=20)
        tk.Label(center, text="ĐANG CHỜ ĐỐI THỦ...", font=('Segoe UI', 20, 'bold'), 
                 fg=self.colors['text_secondary'], bg=self.colors['bg']).pack()

    def handle_game_result(self, message):
        """Màn hình kết quả ấn tượng"""
        self.clear_screen()
        
        center = tk.Frame(self.root, bg=self.colors['bg'])
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        result = message['result']
        your_choice = message['your_choice']
        opponent_choice = message['opponent_choice']
        
        choice_emoji = {'rock': '✊', 'paper': '✋', 'scissors': '✌️'}
        
        if result == 'player1':
            emoji, text, color = "🏆", "CHIẾN THẮNG!", self.colors['success']
        elif result == 'player2':
            emoji, text, color = "💀", "THẤT BẠI...", self.colors['accent']
        else:
            emoji, text, color = "🤝", "HÒA NHAU!", self.colors['warning']
        
        # Result Title
        tk.Label(center, text=emoji, font=('Segoe UI', 80), bg=self.colors['bg']).pack()
        tk.Label(center, text=text, font=('Segoe UI', 40, 'bold'), fg=color, bg=self.colors['bg']).pack(pady=10)
        
        # Detail Matchup
        match_frame = tk.Frame(center, bg=self.colors['card_bg'], padx=30, pady=20)
        match_frame.pack(pady=30)
        
        tk.Label(match_frame, text="BẠN", font=('Segoe UI', 12), fg=self.colors['text_secondary'], bg=self.colors['card_bg']).grid(row=0, column=0)
        tk.Label(match_frame, text=choice_emoji[your_choice], font=('Segoe UI', 40), bg=self.colors['card_bg'], fg='white').grid(row=1, column=0, padx=20)
        
        tk.Label(match_frame, text="VS", font=('Segoe UI', 20, 'bold'), fg=self.colors['text_secondary'], bg=self.colors['card_bg']).grid(row=1, column=1)
        
        tk.Label(match_frame, text="ĐỐI THỦ", font=('Segoe UI', 12), fg=self.colors['text_secondary'], bg=self.colors['card_bg']).grid(row=0, column=2)
        tk.Label(match_frame, text=choice_emoji[opponent_choice], font=('Segoe UI', 40), bg=self.colors['card_bg'], fg='white').grid(row=1, column=2, padx=20)
        
        # Back Button
        self.create_styled_button(center, "QUAY VỀ MENU", self.show_main_menu, self.colors['primary'], width=20).pack(pady=20)

    def logout(self):
        self.network.close()
        self.user = None
        self.show_login_screen()

    def refresh_stats(self):
        if self.user and self.network:
            self.network.send_message({'action': 'refresh_stats'})

    def handle_stats_refreshed(self, message):
        if 'stats' in message:
            self.user['wins'] = message['stats']['wins']
            self.user['losses'] = message['stats']['losses']
            self.user['draws'] = message['stats']['draws']
            self.update_stats_display()

    def update_stats_display(self):
        # Cập nhật an toàn dựa trên dict đã tạo
        if hasattr(self, 'stats_labels') and self.user:
            for key in ['wins', 'losses', 'draws']:
                if key in self.stats_labels and self.stats_labels[key].winfo_exists():
                    self.stats_labels[key].config(text=str(self.user[key]))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RockPaperScissorsClient()
    app.run()