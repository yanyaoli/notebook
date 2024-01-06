import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os

def save_to_file():
    content = text_entry.get("1.0", "end-1c")
    if content.strip() == "":
        show_notification("请输入内容！", duration=1000)
        return

    current_datetime = datetime.now().strftime("%Y年%m月%d日%H点%M分%S秒")
    file_name = f"{current_datetime}.txt"
    file_path = os.path.join("notes", file_name)

    if not os.path.exists("notes"):
        os.makedirs("notes")

    with open(file_path, "w") as file:
        file.write(content)

    show_notification(f"保存成功！", duration=1000)

def show_notification(message, duration):
    notification_label.config(text=message)
    notification_label.place(relx=0.5, rely=0.4, anchor='n')
    root.after(duration, hide_notification)

def hide_notification():
    notification_label.place_forget()

def toggle_pin():
    if pin_var.get():
        root.attributes('-topmost', False)
        pin_var.set(False)
        pin_button.config(text="置顶")
        update_button_text()
    else:
        root.attributes('-topmost', True)
        pin_var.set(True)
        pin_button.config(text="取消置顶")
        update_button_text()

def update_button_text():
    if pin_var.get():
        pin_button.config(text="取消置顶")
    else:
        pin_button.config(text="置顶")

def minimize():
    root.wm_overrideredirect(False)
    root.iconify()

def restore(event=None):
    root.deiconify()
    root.wm_overrideredirect(True)

root = tk.Tk()
root.title("Notebook")
root.resizable(False, False)
root.overrideredirect(True)

root.bind("<Map>", restore)
root.protocol("WM_DELETE_WINDOW", minimize)

style = ttk.Style()
style.theme_use("clam")

button_font = ("黑体", 10)
button_color = "white"  
button_font_color = "black"
style.configure('TButton', font=button_font, foreground=button_font_color, background=button_color, borderwidth=1, relief='groove')
style.configure("TScale", background="grey", troughcolor="white", sliderlength=10, sliderthickness=5, sliderrelief="groove", sliderround=True)

pin_var = tk.BooleanVar()
pin_var.set(True)  # 窗口默认置顶

frame_label = tk.Frame(root, bg='grey',height=10)
frame_label.pack(side=tk.TOP, fill=tk.X)

def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    dx = event.x - root.x
    dy = event.y - root.y
    x = root.winfo_x() + dx
    y = root.winfo_y() + dy
    root.geometry(f"+{x}+{y}")

def update_transparency(val):
    root.attributes('-alpha', float(val))


title_label = tk.Label(frame_label, text="Notebook", bg='grey', fg='white',font=("黑体", 10, "bold"))
title_label.pack(side=tk.LEFT, padx=5)

transparency_scale = ttk.Scale(frame_label, from_=0.3, to=1, orient=tk.HORIZONTAL, command=update_transparency, style="TScale")
transparency_scale.set(1)  # 默认透明度为100%
transparency_scale.pack(side=tk.RIGHT, padx=10)

text_entry = tk.Text(root, height=12, width=45,font=("黑体", 10), highlightbackground="grey", highlightcolor="grey", highlightthickness=1)
text_entry.pack(padx=5,pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(side=tk.BOTTOM, padx=5, pady=5)

close_button = ttk.Button(frame_buttons, text='关闭', command=root.quit)
close_button.pack(side=tk.LEFT, padx=5)

pin_button = ttk.Button(frame_buttons, text="取消置顶", command=toggle_pin)
pin_button.pack(side=tk.LEFT, padx=5)

save_button = ttk.Button(frame_buttons, text="保存", command=save_to_file)
save_button.pack(side=tk.LEFT, padx=5)


for widget in [frame_label, title_label]:
    widget.bind("<ButtonPress-1>", start_move)
    widget.bind("<ButtonRelease-1>", stop_move)
    widget.bind("<B1-Motion>", do_move)
    
notification_label = tk.Label(root, text="", fg="black", bg="white")

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口应该出现的位置
x = screen_width - root.winfo_reqwidth() - 120
y = 10

# 设置窗口的位置
root.geometry("+%d+%d" % (x, y))

# 窗口置顶
root.attributes('-topmost', True)

root.mainloop()
