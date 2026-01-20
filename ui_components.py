import tkinter as tk
from tkinter import ttk

class UIComponents:
    def __init__(self, colors):
        self.colors = colors
    
    def create_modern_button(self, parent, text, command, color=None):
        """Tạo nút hiện đại: Tăng padding, font chữ thanh thoát hơn"""
        if color is None:
            color = self.colors.get('accent', '#4a90e2')
            
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            # Thay đổi: Font nhỏ hơn xíu nhưng spacing rộng hơn để sang trọng
            font=('Segoe UI', 10, 'bold'), 
            relief='flat',
            borderwidth=0,
            highlightthickness=0,
            # Thay đổi: Tăng padding ngang để nút trông "dài" và cân đối hơn
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground=self.lighten_color(color, factor=1.1),
            activeforeground='white'
        )
        
        # Hiệu ứng Hover giữ nguyên logic nhưng màu mượt hơn
        def on_enter(e):
            btn.config(bg=self.lighten_color(color, factor=1.15))
            
        def on_leave(e):
            btn.config(bg=color)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn

    def lighten_color(self, hex_color, factor=1.2):
        """Logic giữ nguyên: Làm sáng màu"""
        try:
            hex_color = hex_color.replace('#', '')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lighter = tuple(min(255, int(c * factor)) for c in rgb)
            return f'#{int(lighter[0]):02x}{int(lighter[1]):02x}{int(lighter[2]):02x}'
        except:
            return hex_color

    def create_modern_entry(self, parent, placeholder, show=None):
        """Tạo ô nhập liệu: Thêm chiều sâu màu nền và con trỏ nổi bật"""
        
        # Thay đổi: Màu nền tối hơn màu form chính một chút để tạo độ sâu (input depth)
        bg_color = '#252535' 
        text_sec_color = self.colors.get('text_secondary', '#888888')
        accent_color = self.colors.get('accent', '#4a90e2')

        entry = tk.Entry(
            parent,
            font=('Segoe UI', 11), # Font size vừa phải
            bg=bg_color,
            fg='white',
            insertbackground=accent_color, # Con trỏ chuột cùng màu accent (rất hiện đại)
            relief='flat',
            highlightthickness=1,       # Viền mỏng 1px tinh tế hơn 2px
            highlightbackground='#3a3a4e', # Viền khi không focus (nhẹ nhàng)
            highlightcolor=accent_color,
            show=show
        )
        
        entry.insert(0, placeholder)
        entry.config(fg=text_sec_color)
        
        # Logic focus giữ nguyên
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='white')
                # Bonus: Đổi nền sáng hơn chút xíu khi focus
                entry.config(bg='#2a2a3a') 
        
        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg=text_sec_color)
                entry.config(bg=bg_color)
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry

    def create_stat_card(self, parent, emoji, label, value, color, row, col):
        """Tạo thẻ thống kê: Thêm border mỏng, căn chỉnh typography"""
        
        # Thay đổi: Card có thêm viền mỏng (highlightthickness) để tách biệt khỏi nền
        card = tk.Frame(
            parent, 
            bg=color, 
            highlightthickness=1, 
            highlightbackground=self.lighten_color(color, 1.2) # Viền sáng hơn màu nền card
        )
        # Giữ grid logic
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew") 
        
        inner_frame = tk.Frame(card, bg=color, padx=25, pady=25)
        inner_frame.pack(expand=True, fill='both')
        
        # Emoji icon
        tk.Label(
            inner_frame, 
            text=emoji, 
            font=('Segoe UI Emoji', 32), # Giảm nhẹ size để đỡ thô
            bg=color,
            fg='white'
        ).pack(pady=(0, 10))
        
        # Giá trị số
        tk.Label(
            inner_frame, 
            text=str(value), 
            font=('Segoe UI', 30, 'bold'), # Số to, rõ ràng
            fg='white', 
            bg=color
        ).pack()
        
        # Nhãn: Dùng font nhỏ, spacing rộng (letter-spacing giả lập bằng space)
        spaced_label = "  ".join(label.upper()) 
        tk.Label(
            inner_frame, 
            text=spaced_label, 
            font=('Segoe UI', 9, 'bold'), 
            fg=self.lighten_color(color, 1.5), # Màu chữ nhạt hơn nền nhưng độ tương phản cao
            bg=color
        ).pack(pady=(5, 0))

    def setup_styles(self, root):
        """Thiết lập style: Treeview phẳng, Header nổi bật, Scrollbar ẩn (nếu hỗ trợ)"""
        style = ttk.Style()
        style.theme_use('clam') 
        
        bg_default = self.colors.get('bg', '#1e1e2e')
        accent = self.colors.get('accent', '#4a90e2')
        
        # Frame & Label
        style.configure('TFrame', background=bg_default)
        style.configure(
            'TLabel', 
            background=bg_default, 
            foreground=self.colors.get('text', '#e0e0e0'), # Trắng hơi xám đỡ chói mắt
            font=('Segoe UI', 11)
        )
        
        # Titles
        style.configure(
            'Title.TLabel', 
            font=('Segoe UI', 26, 'bold'), # To hơn chút
            foreground='white',
            background=bg_default
        )
        
        style.configure(
            'Subtitle.TLabel', 
            font=('Segoe UI', 11), 
            foreground=self.colors.get('text_secondary', '#9ea0a6'),
            background=bg_default
        )
        
        # --- Treeview (Bảng) Modern ---
        # Header: Nền đậm, chữ trắng đậm
        style.configure(
            "Treeview.Heading",
            background="#33334d", # Màu header riêng biệt, tối hơn bg một chút hoặc theo accent
            foreground="white",
            relief="flat",
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0
        )
        
        # Body: Row cao hơn để dễ đọc
        style.configure(
            "Treeview",
            background="#252535", # Nền bảng
            foreground="#dddddd",
            fieldbackground="#252535",
            borderwidth=0,
            font=('Segoe UI', 10),
            rowheight=35 # Row cao 35px tạo cảm giác thoáng đãng
        )
        
        # Màu khi hover hoặc select vào hàng
        style.map(
            "Treeview", 
            background=[('selected', accent)],
            foreground=[('selected', 'white')]
        )
        
        # Hiệu ứng hover cho Header (chỉ hoạt động ở một số OS)
        style.map(
            "Treeview.Heading",
            background=[('active', self.lighten_color(accent, 0.8))] 
        )