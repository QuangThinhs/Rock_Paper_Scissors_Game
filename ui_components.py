import tkinter as tk
from tkinter import ttk

class UIComponents:
    def __init__(self, colors):
        self.colors = colors
    
    def create_modern_button(self, parent, text, command, color=None):
        """Tạo nút hiện đại với hiệu ứng hover và padding tốt hơn"""
        if color is None:
            color = self.colors.get('accent', '#4a90e2') # Fallback color nếu không có trong dict
            
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            font=('Segoe UI', 11, 'bold'), # Giảm size chữ chút cho tinh tế
            relief='flat',
            borderwidth=0,     # Loại bỏ viền 3D cũ
            highlightthickness=0, # Loại bỏ viền focus mặc định
            padx=25,
            pady=10,
            cursor='hand2',
            activebackground=self.lighten_color(color, factor=1.1), # Sáng hơn chút khi nhấn
            activeforeground='white'
        )
        
        # Hiệu ứng Hover mượt mà
        def on_enter(e):
            btn.config(bg=self.lighten_color(color, factor=1.15))
            
        def on_leave(e):
            btn.config(bg=color)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn

    def lighten_color(self, hex_color, factor=1.2):
        """Làm sáng màu linh hoạt hơn"""
        # Xử lý an toàn nếu màu sai định dạng
        try:
            hex_color = hex_color.replace('#', '')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lighter = tuple(min(255, int(c * factor)) for c in rgb)
            return f'#{int(lighter[0]):02x}{int(lighter[1]):02x}{int(lighter[2]):02x}'
        except:
            return hex_color

    def create_modern_entry(self, parent, placeholder, show=None):
        """Tạo ô nhập liệu hiện đại với viền highlight khi focus"""
        
        # Màu nền và màu chữ phụ
        bg_color = '#2d2d44'
        text_sec_color = self.colors.get('text_secondary', '#aaaaaa')
        accent_color = self.colors.get('accent', '#4a90e2')

        entry = tk.Entry(
            parent,
            font=('Segoe UI', 12),
            bg=bg_color,
            fg='white',
            insertbackground='white', # Màu con trỏ chuột
            relief='flat',
            highlightthickness=2,       # Độ dày viền
            highlightbackground=bg_color, # Màu viền khi không focus (ẩn đi)
            highlightcolor=accent_color,  # Màu viền khi focus (hiệu ứng hiện đại)
            show=show
        )
        
        # Tăng chiều cao nội dung (padding trong) cho thoáng
        # Lưu ý: pack/grid sẽ được gọi bên ngoài, nhưng ipady cần config ở đây hoặc khi pack
        # Tuy nhiên tk.Entry không hỗ trợ ipady trong constructor, ta dùng bind để hack nhẹ visual nếu cần
        # Hoặc người dùng gọi pack(ipady=5). Ở đây ta giữ nguyên widget thuần.
        
        entry.insert(0, placeholder)
        entry.config(fg=text_sec_color)
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='white')
            # Không cần đổi màu viền thủ công vì highlightcolor đã lo việc đó
        
        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg=text_sec_color)
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry

    def create_stat_card(self, parent, emoji, label, value, color, row, col):
        """Tạo thẻ thống kê với thiết kế sạch sẽ hơn"""
        # Tạo hiệu ứng đổ bóng nhẹ bằng cách lồng Frame (tùy chọn)
        # Ở đây ta giữ đơn giản nhưng căn chỉnh padding đẹp hơn
        
        card = tk.Frame(parent, bg=color)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew") # sticky nsew để co giãn đều
        
        # Container bên trong để căn giữa nội dung
        inner_frame = tk.Frame(card, bg=color, padx=20, pady=20)
        inner_frame.pack(expand=True, fill='both')
        
        # Emoji icon
        tk.Label(
            inner_frame, 
            text=emoji, 
            font=('Segoe UI Emoji', 36), # Thêm font Emoji nếu có
            bg=color,
            fg='white'
        ).pack(pady=(0, 5))
        
        # Giá trị số (To, đậm)
        tk.Label(
            inner_frame, 
            text=str(value), 
            font=('Segoe UI', 28, 'bold'), 
            fg='white', 
            bg=color
        ).pack()
        
        # Nhãn (Nhỏ hơn, màu nhạt hơn chút)
        tk.Label(
            inner_frame, 
            text=label.upper(), # Chữ in hoa cho tiêu đề
            font=('Segoe UI', 10, 'bold'), 
            fg='#eeeeee', # Trắng hơi đục
            bg=color
        ).pack(pady=(5, 0))

    def setup_styles(self, root):
        """Thiết lập style cho giao diện"""
        style = ttk.Style()
        style.theme_use('clam') # 'clam' hỗ trợ tùy chỉnh màu tốt nhất trong các theme mặc định
        
        # Cấu hình chung cho Frame
        style.configure('TFrame', background=self.colors.get('bg', '#1e1e2e'))
        
        # Cấu hình Label mặc định
        style.configure(
            'TLabel', 
            background=self.colors.get('bg', '#1e1e2e'), 
            foreground=self.colors.get('text', 'white'), 
            font=('Segoe UI', 11)
        )
        
        # Tiêu đề lớn
        style.configure(
            'Title.TLabel', 
            font=('Segoe UI', 24, 'bold'), 
            foreground=self.colors.get('accent', '#4a90e2'),
            background=self.colors.get('bg', '#1e1e2e')
        )
        
        # Tiêu đề phụ
        style.configure(
            'Subtitle.TLabel', 
            font=('Segoe UI', 12), 
            foreground=self.colors.get('text_secondary', '#aaaaaa'),
            background=self.colors.get('bg', '#1e1e2e')
        )
        
        # Cấu hình Treeview (Bảng dữ liệu) cho hiện đại hơn (Bonus)
        style.configure(
            "Treeview",
            background="#2d2d44",
            foreground="white",
            fieldbackground="#2d2d44",
            borderwidth=0,
            font=('Segoe UI', 10),
            rowheight=30
        )
        style.configure(
            "Treeview.Heading",
            background=self.colors.get('accent', '#4a90e2'),
            foreground="white",
            relief="flat",
            font=('Segoe UI', 10, 'bold')
        )
        style.map("Treeview", background=[('selected', self.colors.get('accent', '#4a90e2'))])