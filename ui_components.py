import tkinter as tk
from tkinter import ttk

class UIComponents:
    def __init__(self, colors):
        self.colors = colors
    
    def create_modern_button(self, parent, text, command, color=None):
        """Tạo nút hiện đại"""
        if color is None:
            color = self.colors['accent']
            
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground=self.lighten_color(color),
            activeforeground='white'
        )
        
        btn.bind('<Enter>', lambda e: btn.config(bg=self.lighten_color(color)))
        btn.bind('<Leave>', lambda e: btn.config(bg=color))
        
        return btn

    def lighten_color(self, hex_color):
        """Làm sáng màu"""
        rgb = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f'#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}'

    def create_modern_entry(self, parent, placeholder, show=None):
        """Tạo ô nhập liệu hiện đại"""
        entry = tk.Entry(
            parent,
            font=('Segoe UI', 12),
            bg='#2d2d44',
            fg='white',
            insertbackground='white',
            relief='flat',
            show=show
        )
        entry.insert(0, placeholder)
        entry.config(fg=self.colors['text_secondary'])
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='white')
        
        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg=self.colors['text_secondary'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry

    def create_stat_card(self, parent, emoji, label, value, color, row, col):
        """Tạo thẻ thống kê"""
        card = tk.Frame(parent, bg=color, padx=30, pady=20)
        card.grid(row=row, column=col, padx=10, pady=10)
        
        tk.Label(card, text=emoji, font=('Segoe UI', 40), bg=color).pack()
        tk.Label(card, text=str(value), font=('Segoe UI', 32, 'bold'), fg='white', bg=color).pack()
        tk.Label(card, text=label, font=('Segoe UI', 12), fg='white', bg=color).pack()

    def setup_styles(self, root):
        """Thiết lập style cho giao diện"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['text'], font=('Segoe UI', 11))
        style.configure('Title.TLabel', font=('Segoe UI', 28, 'bold'), foreground=self.colors['accent'])
        style.configure('Subtitle.TLabel', font=('Segoe UI', 14), foreground=self.colors['text_secondary'])