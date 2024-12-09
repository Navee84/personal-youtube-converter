import customtkinter as tk
from PIL import Image

#MAIN WINDOOW
main_window = tk.CTk()
WINDOW_SIZE = "800x600"

main_window.minsize(800,600)

main_window.title("Youtube converter")
main_window.geometry(WINDOW_SIZE)
for i in range(3):
    main_window.grid_rowconfigure(i, weight=1)
    main_window.grid_columnconfigure(i, weight=1)
main_window.grid_columnconfigure(1, weight=2)

# ICONS IMPORT
folder_icon = tk.CTkImage(dark_image=Image.open("assets/folder_light.png"),light_image=Image.open("assets/folder_dark.png"))
confirm_icon = tk.CTkImage(dark_image=Image.open("assets/check_light.png"),light_image=Image.open("assets/check_dark.png"))
trash_icon = tk.CTkImage(dark_image=Image.open("assets/bin_light.png"),light_image=Image.open("assets/bin_dark.png"))

# QUEUE FRAME
queue_frame =tk.CTkScrollableFrame(main_window)
queue_frame.grid(row=1, column=1, sticky="nsew")

# INPUT FRAME
input_frame = tk.CTkFrame(main_window,fg_color="transparent")
input_frame.grid(row=2, column=1, sticky="ew")

input_frame.grid_rowconfigure(0,weight=0)

input_frame.grid_columnconfigure(0,weight=4)
input_frame.grid_columnconfigure(1,weight=1)
input_frame.grid_columnconfigure(2,weight=0)
input_frame.grid_columnconfigure(3,weight=0)


# url entry
url_entry = tk.CTkEntry(input_frame,placeholder_text="Video URL",height=35)
url_entry.grid(row=0, column=0, sticky="ew")

# format button
format_button = tk.CTkSegmentedButton(input_frame,values=["MP3","MP4"],height=35)
format_button.set("MP3")
format_button.configure(state="disabled")
format_button.grid(row=0, column=1, sticky="ew")

# directory button
directory_button = tk.CTkButton(input_frame,image=folder_icon,text="",width=50,height=35)
directory_button.grid(row=0,column=2,padx=10)

# confirm button
confirm_button = tk.CTkButton(input_frame,image=confirm_icon,text="",width=50,height=35)
confirm_button.grid(row=0,column=3)

# SETTINGS FRAME
settings_frame = tk.CTkFrame(main_window,fg_color="transparent")
settings_frame.grid(row=1,column=2,sticky="nsew")

settings_frame.grid_columnconfigure(0,weight=1)

for i in range(5):
    settings_frame.grid_rowconfigure(i, weight=1)

# deflault folder button
default_directory_button = tk.CTkButton(settings_frame,image=folder_icon,text="",width=70,height=35)
default_directory_button.grid(row=0,column=0,padx=10)

# default format button
default_format_button = tk.CTkSegmentedButton(settings_frame,values=["MP3","MP4"],height=35)
default_format_button.set("MP3")
default_format_button.configure(state="disabled")
default_format_button.grid(row=1, column=0, sticky="ew",pady=30,padx=10)

# empty queue button
empty_queue = tk.CTkButton(settings_frame,image=trash_icon,text="",width=70,height=35)
empty_queue.grid(row=2,column=0,padx=10)

# queue size
queue_size_frame = tk.CTkFrame(settings_frame,height=35)
queue_size_frame.grid(row=3,column=0,sticky="ew",pady=30,padx=10)

queue_size_text = tk.CTkLabel(queue_size_frame,text="Queue size : "+"0")
queue_size_text.grid(padx=20)

# queue weight
queue_weight_frame = tk.CTkFrame(settings_frame,height=35)
queue_weight_frame.grid(row=4,column=0,sticky="ew",padx=10)

queue_weight_text = tk.CTkLabel(queue_weight_frame,text="Queue weight : "+"0"+" Mo")
queue_weight_text.grid(padx=20)

main_window.mainloop()