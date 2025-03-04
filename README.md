# Personal Youtube Converter
This software is a tool designed to easily download youtube audio directly on your device, without the need to rely on ad-filled websites.
The converter supports both single videos and playlists.

## Features
- Download videos in MP3 format (MP4 support planned)
- Supports public playlists
- Easy to use and intuitive
- Add and remove videos from the queue easily
- View each video's length and file size
- View the estimated total download size
- Customize the default download directory
- Change individually download directories for both input and videos already inside the queue

## How to use
### Requirements
This program is intended to run with Python 3.12<br>
You **must** have the "assets" folder inside the same folder as the python file.<br>
You will need the following dependencies:
- customtkinter : ``pip install customtkinter``
- CTkMessagebox : ``pip install CTkMessagebox``
- Pytubefix : ``pip install pytubefix``
- PIL (pillow) : ``pip install pillow``

### PO Tokens
"Proof of Origin (PO) Token is a parameter that YouTube requires to be sent with requests from some clients. Without it, requests for the affected clients' format URLs may return HTTP Error 403, or result in your account or IP address being blocked."

In other words, when converting a video, if you do not have any PO token already cached on your device, the program will ask you one. **This does only apply if you are using the python file, if you use the executable, the token is already included.**

#### How to get your PO Token ?
You can find a guide on how to get PO tokens [here.](https://pytubefix.readthedocs.io/en/latest/user/po_token.html#manually-acquiring-a-po-token-from-a-browser-for-use-when-logged-out) When you have your have your visitorData and your poToken, you can attempt to convert any video and the program will ask you for them in the console.

### Using the program
Simply **get your YouTube video or playlist URL** from your browser (not the URL from the share button or the URL from a single video inside a playlist) and **paste it in the program.**
Then add it to the download queue. This action might take some time, and the program may appear frozen, but patience is key.

Once you've added all the videos you wanted to download to the queue, simply **click the download button** and wait for the queue to download.
Your files should be downloaded inside a "downloads" folder located next to the python file.

#### **IMPORTANT**
Since this program does not connect to your youtube account, it **cannot download private playlists** and auto-generated playlists !<br>
For the same reasons, the program cannot download private and age restricted videos either.

## Note
This program is in its early stages of development and is still unstable. Features will be added, and bugs will be fixed in future versions.

## Support & Feedback
- If you encounter any bugs or errors, please report them [here](https://github.com/Navee84/personal-youtube-converter/issues), it helps me keep this project clean from bugs.

- Have any suggestions for the project ? Feel free to open a discussion and share your ideas.

- **Leave a star** ⭐ on this repository if you find it useful, it encourages me to keep improving this project ! (and it boosts my ego)

## Disclaimer
⚠️ This tool is intended for personal use only ⚠️<br>
Downloading copyrighted material without permission is against YouTube's Terms of Service and may violate copyright law.<br>
By using this tool, you agree that you are entirely sole responsible for any content you download.<br>
I am not affiliated with YouTube, Google, or any other related services.

### Credits
<a href="https://www.flaticon.com/free-icons/tick" title="tick icons">Tick icons created by Pixel perfect - Flaticon</a><br>
<a href="https://www.flaticon.com/free-icons/folder" title="folder icons">Folder icons created by dmitri13 - Flaticon</a><br>
<a href="https://www.flaticon.com/free-icons/trash" title="trash icons">Trash icons created by Freepik - Flaticon</a><br>
<a href="https://www.flaticon.com/free-icons/youtube" title="youtube icons">Youtube icons created by Md Tanvirul Haque - Flaticon</a>