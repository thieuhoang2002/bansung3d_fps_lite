from cProfile import label
from tkinter import Tk,Canvas,messagebox
from PIL import Image,ImageTk
from tkinter import Label,Entry,Text, Button,PhotoImage,Checkbutton,IntVar

class LoginForm:
    def __init__(self, callback):
        self.callback =callback
        self.win = Tk()
        self.win.title("Ursina")
        # Kích thước cửa sổ
        self.win.update_idletasks()  # Cập nhật để lấy kích thước chính xác

        win_width = 1280
        win_height = 720

        # Lấy kích thước màn hình
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        # Tính toán vị trí để căn giữa
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        self.win.after(10, lambda: self.win.geometry(f"{win_width}x{win_height}+{x}+{y}"))

        # Đặt kích thước và vị trí cửa sổ
        # Màu nền
        self.win.configure(bg="#202227")

        canvas = Canvas(self.win, width=win_width, height=win_height, highlightthickness=0, bg="#202227")
        canvas.place(x=0, y=0)

        img = Image.open("asset/static/login_gui/2151138370.jpg")
        img = img.resize((int(win_width * 0.7), win_height))
        bg_photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor='nw', image=bg_photo)
        canvas.image = bg_photo

        logo_x = int(win_width * 0.7) + 50
        logo_y = 20  # Cùng với vị trí của tên label
        img_logo = Image.open("asset/static/login_gui/flaticon.png")
        img_logo = img_logo.resize((290,190))
        bg_logo = ImageTk.PhotoImage(img_logo)
        canvas.create_image(logo_x, logo_y, anchor='nw', image=bg_logo)

        # Tọa độ bắt đầu bên phải ảnh
        right_x = int(win_width * 0.7) + 50
        label_y = 200
        entry_y = label_y + 50  

        # Label "Nhập tên người chơi"
        name_label = Label(self.win, text="Welcome", fg="white", bg="#202227", font=("Arial", 22))
        name_label.place(x=right_x + 70, y=label_y)

        # Entry để nhập tên
        self.name_entry = Entry(self.win, font=("Arial", 16), width=24, bg="#32353c", fg="#d7d7da")  # Màu chữ khi chưa nhập
        self.name_entry.insert(0, "Nhập tên người chơi")  # Đặt placeholder ban đầu
        self.name_entry.place(x=right_x, y=entry_y, height=40)  # hoặc dùng ipady với .pack() / .grid()

        #icon facebook
        icon_facebook = Image.open("asset/static/login_gui/facebook.png")
        icon_facebook = icon_facebook.resize((50,25))
        facebook_photo = ImageTk.PhotoImage(icon_facebook)

        facebook_button = Button(self.win,image=facebook_photo,bg ="#202227",border=0, highlightthickness=0, relief="flat")
        facebook_button.place(x=right_x, y=entry_y + 60)

        #icon google
        icon_google = Image.open("asset/static/login_gui/google.png")
        icon_google = icon_google.resize((50,25))
        google_photo = ImageTk.PhotoImage(icon_google)

        google_button = Button(self.win,image=google_photo,bg= "#202227",border=0, highlightthickness=0, relief="flat")
        google_button.place(x=right_x + 60,y=entry_y+ 60)

        #icon apple
        icon_apple = Image.open("asset/static/login_gui/apple.png")
        icon_apple = icon_apple.resize((50,25))
        apple_photo = ImageTk.PhotoImage(icon_apple)

        apple_button = Button(self.win,image = apple_photo, bg= "#202227",border=0, highlightthickness=0, relief="flat")
        apple_button.place(x=right_x + 120,y=entry_y + 60)

        #icon xbox 
        icon_xbox = Image.open("asset/static/login_gui/xbox.png")
        icon_xbox = icon_xbox.resize((50,25))
        xbox_photo = ImageTk.PhotoImage(icon_xbox)

        xbox_button = Button(self.win,image=xbox_photo,bg= "#202227",border=0, highlightthickness=0, relief="flat")
        xbox_button.place(x=right_x + 180, y= entry_y +60)

        #icon sony
        icon_sony = Image.open("asset/static/login_gui/playstation.png")
        icon_sony = icon_sony.resize((50,25))
        sony_photo = ImageTk.PhotoImage(icon_sony,)

        sony_button = Button(self.win, image= sony_photo,bg= "#202227",border=0, highlightthickness=0, relief="flat")
        sony_button.place(x=right_x + 240,y=entry_y + 60)

        #checkbox
        remember_var = IntVar()
        remember_check = Checkbutton(
            self.win,
            text="Ghi nhớ đăng nhập",
            variable=remember_var,
            fg="white",
            bg="#202227",
            font=("Arial", 12),
            activebackground="#202227",
            activeforeground="white",
            selectcolor="#202227",  # màu nền khi được tick
            highlightthickness=0,
            bd=0
        )
        remember_check.place(x=right_x, y=entry_y + 100)  # Điều chỉnh vị trí cho đẹp

        login_button =Button (
            self.win,
            text ="Sign in",
            font=("Arial", 14),
            fg="white",
            bg="#0eafff",
            activebackground="#0c99dd",
            activeforeground="white",
            border=0,
            width=18,
            relief="flat",
            padx=20,
            pady=5,
            command=self.sign_in_clicked,
        )
        login_button.place(x=right_x + 30, y=entry_y + 140)
        self.name_entry.bind("<FocusIn>", self.on_entry_click)
        self.name_entry.bind("<FocusOut>", self.on_focus_out)

        # ... Các phần còn lại (ảnh icon, button...) giữ nguyên, nhớ đổi từ win → self.win nếu cần
        self.win.mainloop()

        # Hàm khi click vào Entry (FocusIn)
        
        
    def on_entry_click(self, event):
        if self.name_entry.get() == "Nhập tên người chơi":
            self.name_entry.delete(0, "end")
            self.name_entry.config(fg="white")

    def on_focus_out(self, event):
        if self.name_entry.get() == "":
            self.name_entry.insert(0, "Nhập tên người chơi")
            self.name_entry.config(fg="#d7d7da")
    
    def sign_in_clicked(self):
        # Kiểm tra nếu người dùng đã nhập tên người dùng
        username = self.name_entry.get().strip()
        if username.strip():
            # Gọi hàm callback và truyền tên người dùng và IP room (có thể là chuỗi rỗng)
            self.win.destroy()  # Đóng cửa sổ sau khi nhấn nút "Submit"
            self.callback[0](username)
        else:
            # Hiển thị cảnh báo nếu tên người dùng không được nhập
            messagebox.showwarning("Warning", "Vui lòng nhập tên người chơi.")
