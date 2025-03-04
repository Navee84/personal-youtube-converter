try:
    import customtkinter as tk
    import os
    from CTkMessagebox import CTkMessagebox
    from pytubefix import YouTube, Playlist
    from PIL import Image, ImageTk
except Exception as e:
    print(e)
    input("")
    exit()

version = "0.2.0"
DEBUG = False

tk.set_default_color_theme("dark-blue")
tk.set_appearance_mode("dark")

###################################
#  ____ _                         #
# / ___| | __ _ ___ ___  ___  ___ #
#| |   | |/ _` / __/ __|/ _ \/ __|#
#| |___| | (_| \__ \__ \  __/\__ \#
# \____|_|\__,_|___/___/\___||___/#
###################################

class Utils():
    def textbox_show_error(self,title:str,message:str)->None:
        error = CTkMessagebox(title=title, message=message, icon="cancel", sound=True, fade_in_duration=100, header=True, topmost=False)
    
    def textbox_show_info(self,title:str,message:str)->None:
        info = CTkMessagebox(title=title, message=message, icon="info", sound=True, fade_in_duration=100, header=True, topmost=False)

    def textbox_confirmation(self,title:str,message:str,icon:str)->bool:
        confirmation = CTkMessagebox(title=title, message=message, icon=icon, sound=True, fade_in_duration=100, header=True, topmost=False, option_1="Yes", option_2="No")
        response = confirmation.get()

        if response == "Yes":
            return True
        return False

    def convert_time(self,original_time:int)->str:
        h = str(original_time//3600)
        m = str((original_time%3600)//60)
        s = str(original_time%60)
        return h+"h"+m+"m"+s+"s"
    
    def convert_size(self,original_size:int)->str:
        size = original_size//1000  # B into KB
        if size < 10**3:
            return str(round(size,1))+"KB"
        
        size = size/1000    # KB into MB
        if size < 10**3:
            return str(round(size,1))+"MB"
        
        return str(round((size/1000),1))+"GB"

    def openfolder(self):
        return tk.filedialog.askdirectory()


class App(tk.CTk,Utils):
    def __init__(self,window_height:int,window_width:int):
        super().__init__()
        self.starting_prompt = CTkMessagebox(title="Opening", message="Starting personal youtube converter, please wait...", icon="info", sound=False, fade_in_duration=200, header=True, topmost=True)
        
        # icons import
        self.folder_icon = tk.CTkImage(dark_image=Image.open("assets/folder_light.png"),light_image=Image.open("assets/folder_dark.png"))
        self.confirm_icon = tk.CTkImage(dark_image=Image.open("assets/check_light.png"),light_image=Image.open("assets/check_dark.png"))
        self.trash_icon = tk.CTkImage(dark_image=Image.open("assets/bin_light.png"),light_image=Image.open("assets/bin_dark.png"))
        self.download_icon = tk.CTkImage(dark_image=Image.open("assets/download_light.png"),light_image=Image.open("assets/download_dark.png"))

        # app paramaters
        self.title("Personal Youtube Converter")
        self.geometry(str(window_height)+"x"+str(window_width))
        self.minsize(window_height,window_width)
        self.icon = ImageTk.PhotoImage(file="assets/youtube_color.png")
        self.after(200, lambda: self.iconphoto(False,self.icon))

        for i in range(3):
            self.grid_rowconfigure(i,weight=1)
            self.grid_columnconfigure(i,weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=0)


        # Default download path
        if not os.path.exists("./download_directory.txt"):
            os.mkdir("./downloads")
            with open("./download_directory.txt","w") as download_directory_file:
                download_directory_file.write("./downloads")

        with open("./download_directory.txt","r") as download_directory_file:
            self.default_download_directory_path = self.check_path(download_directory_file.read())


        # Initializing the download queue
        self.download_queue = Queue(self)

        # initiating all classes
        self.queue_global_frame = QueueGlobalFrame(self)
        self.queue_global_frame.grid(row=1, column=1, sticky="nsew")

        self.input_frame = InputFrame(self)
        self.input_frame.grid(row=2, column=1, sticky="ew")

        self.misc_frame = MiscFrame(self)
        self.misc_frame.grid(row=1,column=2,sticky="nsew")



    def entry_freeze(self,value:bool)->None:
        self.input_frame.input_entry_freeze(value)
    
    def visual_update(self)->None:
        print("UPDATING VISUAL")
        self.queue_global_frame.queue_refresh(self.download_queue.get_videos_properties())
        self.misc_frame.update_infos()
    
    def check_path(self,path:str)->str:
        if not os.path.exists(path):
            self.textbox_show_error(title="Default path error", message="The default download directory path does not exists, please change it.\nUsing default path instead.")
            return "./downloads"
        return path
    
    def set_default_download_directory_path(self,new_path:str)->None:
        print(f"setting path : {new_path}")
        with open("./download_directory.txt","w") as file:
            file.write(new_path)
        

    
    # debug functions
    def debug_insert_playlist(self):
        self.input_frame.url_entry.insert(0,"https://www.youtube.com/playlist?list=PLLWxffLzEPlKwfDR3QgYu-yBeEtGE6Fw3")
        self.input_frame.send_to_queue()
    
    def debug_insert(self):
        self.input_frame.url_entry.insert(0,"https://www.youtube.com/watch?v=4JWANCA-Pbw")
        self.input_frame.send_to_queue()
    
    def debug_download_queue(self):
        self.download_queue.start_download()


class Video(Utils):
    def __init__(self,url:str,arg_type:int,arg_path):
        self.ObjVideo = YouTube(url,use_po_token=True)
        self.title = self.ObjVideo.title
        self.type = arg_type # 0 = audio; 1 = video+audio

        if self.type > 0:
            self.video_stream = self.ObjVideo.streams.get_highest_resolution(True)
            self.size = self.video_stream.filesize # In Bytes
        else:
            self.audio_stream = self.ObjVideo.streams.get_audio_only()
            self.size = self.audio_stream.filesize # In Bytes

        self.length = self.ObjVideo.length # In seconds

        self.path = arg_path

    def set_title(self,new_title):
        self.title = new_title
    
    def set_path(self,new_path):
        self.path = new_path

    def get_properties(self):
        return [self.title,self.length,self.size,self.type,self.path]
    
    def download(self):
        if self.type > 0:
            self.video_stream.download(self.path, self.title, max_retries=2)
        else:
            try :
                self.audio_stream.download(self.path, self.title+".mp3", max_retries=2)
            except Exception as e:
                self.textbox_show_error("Error",e)


class Queue():
    def __init__(self,parent:App):
        self.parent = parent
        self.queue = [] # Only Video() objects are allowed in this list...
    
    def add(self,elem:Video):
        self.queue.append(elem)
        print("added 1 video to queue")
    
    def remove(self,index):
        self.queue.pop(index)
        self.parent.visual_update()
    
    def empty_queue(self):
        self.queue = []
        self.parent.visual_update()

    def list(self):
        print(self.queue)
    
    def get_queue_length(self):
        return len(self.queue)

    def get(self):
        return self.queue
    
    def get_videos_properties(self):
        properties = []
        for element in self.queue:
            properties.append(element.get_properties()) # ...because of this line
        
        return properties
    
    def start_download(self):
        print("starting downloading queue....")
        while len(self.queue) > 0:
            print("downloading")
            self.queue[0].download() # ...because of this line
            self.remove(0)
        
        print("finished downloading queue")


class QueueGlobalFrame(tk.CTkFrame):
    def __init__(self, parent:App):
        super().__init__(parent)

        self.parent = parent

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)

        self.queue_header_frame = QueueHeaderFrame(self)
        self.queue_header_frame.grid(row=0,column=0,sticky="ew")
        
        self.queue_frame = QueueFrame(self)
        self.queue_frame.grid(row=1, column=0, sticky="nsew")
    
    def queue_refresh(self,video_properties):
        self.queue_frame.clear_queue()
        idx = 0
        for video in video_properties:
            self.queue_frame.new_element(idx,video)
            idx += 1


class QueueHeaderFrame(tk.CTkFrame):
    def __init__(self,parent:QueueGlobalFrame):
        super().__init__(parent,height=60)

        self.parent = parent
        font = tk.CTkFont(size=16,weight="bold")


        self.grid_columnconfigure(0,weight=3)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.grid_columnconfigure(3,weight=1)

        # header title
        self.header_title = tk.CTkLabel(self, fg_color="transparent", width=170, height=40,font=font, text="Title")
        self.header_title.configure()
        self.header_title.grid(row=0, column=0, padx=(5,5), sticky="ew")

        # header length
        self.header_length = tk.CTkLabel(self, fg_color="transparent", width=60, height=40, font=font, text="Length")
        self.header_length.grid(row=0, column=1, sticky="ew")

        # header size
        self.header_size = tk.CTkLabel(self, fg_color="transparent", width=60, height=40, font=font, text="Size")
        self.header_size.grid(row=0, column=2, sticky="ew")

        # header format
        self.header_format = tk.CTkLabel(self, fg_color="transparent", width=60, height=40, font=font, text="Format")
        self.header_format.grid(row=0, column=3, sticky="ew", padx=(0,110))


class QueueFrame(tk.CTkScrollableFrame):
    def __init__(self,parent:QueueGlobalFrame):
        super().__init__(parent)
        self.parent = parent
        self.grid_columnconfigure(0,weight=1)
    
    def clear_queue(self):
        for element in self.grid_slaves():
            element.grid_forget()

    def new_element(self,index,properties):
        frame_element = QueueElement(self,index,properties[0],properties[1],properties[2])
        frame_element.grid(row=index, column=0, sticky="ew",pady=3)


class QueueElement(tk.CTkFrame,Utils):
    def __init__(self,parent:QueueFrame,index,title:str,length:str,size:str):
        super().__init__(parent)
        self.parent = parent
        self.index = index

        font = tk.CTkFont(size=14)

        self.grid_columnconfigure(0,weight=4)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.grid_columnconfigure(3,weight=1)
        self.grid_columnconfigure(4,weight=0)

        # element title
        element_title = tk.CTkTextbox(self,font=font, activate_scrollbars=True, height=80, width=180, fg_color="transparent")
        element_title.insert("0.0",title)
        element_title.configure(state="disabled",wrap="word")
        element_title.grid(row=0, column=0, sticky="ew",padx=5,pady=5)

        # element length
        element_length = tk.CTkTextbox(self,font=font, activate_scrollbars=False, height=35, width=80)
        element_length.insert("0.0",self.convert_time(length))
        element_length.configure(state="disabled",wrap="none")
        element_length.grid(row=0, column=1, pady=20, sticky="ew")

        # element size
        element_length = tk.CTkTextbox(self,font=font, activate_scrollbars=False, height=35, width=60)
        element_length.insert("0.0",self.convert_size(size))
        element_length.configure(state="disabled",wrap="none")
        element_length.grid(row=0, column=2, pady=20, sticky="ew")

        # element format button
        element_format_button = tk.CTkSegmentedButton(self,values=["MP3","MP4"],height=35,width=60)
        element_format_button.set("MP3")
        element_format_button.configure(state="disabled")
        element_format_button.grid(row=0, column=3,sticky="ew")

        # element directory button
        directory_button = tk.CTkButton(self,image=parent.parent.parent.folder_icon,text="",width=45,height=35, command=self.set_download_path)
        directory_button.grid(row=0,column=4, sticky="ew")

        # element remove button
        element_removre_button = tk.CTkButton(self,image=parent.parent.parent.trash_icon,text="",width=45,height=35, command=self.remove_self_from_queue)
        element_removre_button.grid(row=0,column=5, sticky="ew")
    
    def remove_self_from_queue(self):
        self.parent.parent.parent.download_queue.remove(self.index)
    
    def set_download_path(self):
        new_folder = self.openfolder()
        self.parent.parent.parent.download_queue.queue[self.index].path = new_folder


class InputFrame(tk.CTkFrame, Utils):
    def __init__(self, parent:App):
        super().__init__(parent,fg_color="transparent")      
        self.parent = parent
        self.grid_rowconfigure(0,weight=0)

        self.grid_columnconfigure(0,weight=4)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=0)
        self.grid_columnconfigure(3,weight=0)

        # url entry
        self.url_entry = tk.CTkEntry(self,placeholder_text="Video URL",height=35)
        self.url_entry.grid(row=0, column=0, sticky="ew")

        # format button
        self.format_button = tk.CTkSegmentedButton(self,values=["MP3","MP4"],height=35)
        self.format_button.set("MP3")
        self.format_button.configure(state="disabled")
        self.format_button.grid(row=0, column=1, sticky="ew")

        # directory button
        self.directory_button = tk.CTkButton(self,image=parent.folder_icon,text="",width=50,height=35, command=self.select_path)
        self.directory_button.grid(row=0,column=2,padx=10)

        # confirm button
        self.confirm_button = tk.CTkButton(self,image=parent.confirm_icon,text="",width=50,height=35, command=self.send_to_queue)
        self.confirm_button.grid(row=0,column=3)

        self.selected_path = parent.default_download_directory_path
    
    def input_entry_freeze(self,state:bool):
        # /!\ REMEMBER TO ADD FORMAT BUTTON WHEN IMPLEMENTING MP4 SUPPORT /!\
        if state == True:
            self.url_entry.configure(state="disabled")
            self.directory_button.configure(state="disabled")
            self.confirm_button.configure(state="diabled")

        else:
            self.url_entry.configure(state="normal")
            self.directory_button.configure(state="normal")
            self.confirm_button.configure(state="normal")
    
    def clean_entry(self):
        print("cleared entry")
        self.url_entry.delete(0,tk.END)

    def select_path(self):
        self.select_path = self.openfolder()

    def get_selected_format(self)->int:
        match self.format_button.get():
            case "MP3" :
                return 0

            case "MP4" :
                return 1

    def get_selected_path(self):
        if not os.path.exists(self.selected_path):
            self.textbox_show_error(title="Path error", message="The selected download path does not exists\nUsing default path instead.")
            return "./downloads"
        return self.selected_path


    def url_is_correct(self,url:str)->bool:
        generic_video_url = "https://www.youtube.com/watch?"
        generic_playlist_url = "https://www.youtube.com/playlist?"
        if generic_video_url in url or generic_playlist_url in url:
            return True
        else:
            return False

    def url_is_video(self,url):
        # allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        idx_start = url.find("watch?v=")+8
        video_id = url[idx_start:]
        if len(video_id) == 11:
            return True
        else:
            return False

    def send_to_queue(self):
        self.parent.entry_freeze(True)
        url = self.url_entry.get()
            
        if not self.url_is_correct(url):
            self.textbox_show_error(title="Uncorrect URL",message="The Youtube url given cannot be read.")

        else:
            try:
                if self.url_is_video(url):
                    self.textbox_show_info("Converting...","Converting video, don't close the program...")
                    video = Video(url,self.get_selected_format(),self.get_selected_path())
                    self.parent.download_queue.add(video)
                    self.parent.visual_update()

                else:
                    pl = Playlist(url)
                    self.textbox_show_info("Converting...","Converting playlist, this might take some time.\nPlease be patient...")
                    for url in pl.video_urls:
                        video = Video(url,self.get_selected_format(),self.get_selected_path())
                        self.parent.download_queue.add(video)
                        self.parent.visual_update()
            except Exception as e:
                self.textbox_show_error("Error",str(e)+"\nplease try again")


        self.parent.entry_freeze(False)
        self.clean_entry()


class MiscFrame(tk.CTkFrame,Utils):
    def __init__(self, parent:App):
        super().__init__(parent,fg_color="transparent")
        self.parent = parent

        self.grid_columnconfigure(0,weight=1)

        for i in range(5):
            self.grid_rowconfigure(i, weight=1)

        # download button
        self.download_button = tk.CTkButton(self, width=80, height=35, text="", image=parent.download_icon, command=self.download)
        self.download_button.grid(row=0, column=0 ,padx=10)


        # deflault folder button
        self.default_directory_button = tk.CTkButton(self,image=parent.folder_icon,text="",width=80,height=35, command=self.set_default_download_directory)
        self.default_directory_button.grid(row=1 ,column=0,padx=10)

        # empty queue button
        self.empty_queue = tk.CTkButton(self,image=parent.trash_icon,text="",width=80,height=35, command=self.empty_queue)
        self.empty_queue.grid(row=2,column=0,padx=10)

        # queue length
        self.queue_length_frame = tk.CTkFrame(self,height=35)
        self.queue_length_frame.grid(row=3,column=0,sticky="ew",pady=30,padx=10)

        self.queue_length_text = tk.CTkLabel(self.queue_length_frame,text="Queue length : "+str(parent.download_queue.get_queue_length()))
        self.queue_length_text.grid(padx=20)

        # queue size
        self.queue_size_frame = tk.CTkFrame(self,height=35)
        self.queue_size_frame.grid(row=4,column=0,sticky="ew",padx=10)

        self.queue_size_text = tk.CTkLabel(self.queue_size_frame,text="Queue size : "+self.convert_size(self.get_total_queue_size()))
        self.queue_size_text.grid(padx=20)
    
    def download(self):
        if self.parent.download_queue.get_queue_length() > 0:
            self.parent.download_queue.start_download()
        else:
            self.textbox_show_error("Error","Cannot download empty queue.")

    def set_default_download_directory(self):
        if not self.textbox_confirmation(title="Default diretory", message="Change the default directory for downloaded files ?", icon="question"):
            return None

        new_path = self.openfolder()

        if not os.path.exists(new_path):
            return None

        self.parent.set_default_download_directory_path(new_path)

    
    def empty_queue(self):
        if self.textbox_confirmation(title="Empty queue",message="Are you sure you want to empty the queue ?",icon="warning"):
            self.parent.download_queue.empty_queue()
    
    def get_total_queue_size(self):
        total_size = 0
        for video_properties in self.parent.download_queue.get_videos_properties():
            total_size += video_properties[2]
        return total_size
    
    def update_infos(self):
        self.queue_length_text.configure(text="Queue length : "+str(self.parent.download_queue.get_queue_length()))
        self.queue_size_text.configure(text="Queue size : "+self.convert_size(self.get_total_queue_size()))

################################################
# __  __       _          ____          _      #
#|  \/  | __ _(_)_ __    / ___|___   __| | ___ #
#| |\/| |/ _` | | '_ \  | |   / _ \ / _` |/ _ \#
#| |  | | (_| | | | | | | |__| (_) | (_| |  __/#
#|_|  |_|\__,_|_|_| |_|  \____\___/ \__,_|\___|#
################################################

app = App(800,600)

if DEBUG :

    import threading
    import code

    def start_console():
        code.interact(local=globals())

    thread_console = threading.Thread(target=start_console, daemon=True)
    thread_console.start()

app.starting_prompt.destroy()
app.mainloop()