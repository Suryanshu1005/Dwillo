import tkinter as tk
from tkinter import ttk
from pytube import YouTube
import threading
from tkinter import filedialog
from PIL import ImageTk, Image

root = tk.Tk()
root.geometry('700x300')
root.resizable(False, False)
root.title('Your personal Downloader')

video_title_var = tk.StringVar()
progress_var = tk.DoubleVar()
video_path = tk.StringVar()
url_path = tk.StringVar()
progress_bar_label_var = tk.StringVar()
video_size_label = tk.StringVar()
video_size = tk.DoubleVar()
error_label = tk.StringVar()
error_label_var = tk.StringVar()
selected_path_var = tk.StringVar()
selected_path = ""
video_quality_label = tk.StringVar()
loading_label = ttk.Label(root, text="")

selected_path_label = ttk.Label(root, textvariable=selected_path_var)


url = url_path.get()
def update_progress_bar(stream, chunk, bytes_remaining):
    total_bytes = stream.filesize
    bytes_downloaded = total_bytes - bytes_remaining
    percentage = (bytes_downloaded / total_bytes) * 100
    progress_var.set(int(percentage))
    if percentage != 100:
        progress_bar_label_var.set(f"Progress: {int(percentage)}%")
    else:
        progress_bar_label_var.set(f"Progress: Completed")

def choose_directory():
    global selected_path
    selected_path = filedialog.askdirectory(title="Select Save Directory")
    if selected_path:
        selected_path_var.set(selected_path)


def clear_loading_and_error_labels():
    loading_label.destroy()
    error_label_var.set("")

def get_video_details(url):
    try:
        global loading_label
        loading_label = ttk.Label(root ,text="Fetching data, please wait...")
        loading_label.place(relx=0.5, rely=0.1, anchor="center")

        root.update()

        loading_label.destroy()

        video = YouTube(url)
        video_file = video.streams.filter(file_extension="mp4", res="720p").first()

        # resolution =[int(i.split("p")[0]) for i in (list(dict.fromkeys([i.resolution for i in video.streams if i.resolution])))]
        # resolution.sort()
        # print()

        # Clear previous error message

        if video_file:
            loading_label.destroy()
            title_label = ttk.Label(root, text=f"Video Title: {video_file.title}")
            title_label.place(relx=0.318, rely=0.39)

            video_size_label.set(f"Video Size: {video_file.filesize_mb} MB")

            size_label = ttk.Label(root, textvariable=video_size_label)
            size_label.place(relx=0.318, rely=0.44)
        else:
            root.after(3000, clear_loading_and_error_labels)
            error_label_var.set("Video details not available for the selected resolution.")
    except Exception as e:
        root.after(3000, clear_loading_and_error_labels)
        error_label_var.set(f"Error: {str(e)}")


def main():
    global selected_path
    try:
        url = url_path.get()
        if not url:
            raise ValueError("Please enter a valid URL")
        
        video = YouTube(url)
        video_file = video.streams.filter(file_extension="mp4", res="720p").first()
        video.register_on_progress_callback(update_progress_bar)
        if not selected_path:
            raise ValueError("Please select a directory to save the file")
        
        download_thread = threading.Thread(target=video_file.download, args=(selected_path,))
        download_thread.start()

        selected_path_label.place(relx=0.1, rely=0.5)

        progress_bar_percent = ttk.Label(root, textvariable=progress_bar_label_var)
        progress_bar_percent.place(relx=0.32, rely=0.5)

        progress_bar = ttk.Progressbar(root, variable=progress_var, mode='determinate')
        progress_bar.place(relx=0.33, rely=0.6, relwidth=0.5)

        error_label_var.set("")

    except Exception as e:
        error_label_var.set(f"Error: {str(e)}")


original_image = Image.open("D:/Downloads/Dwillo-logos/Dwillo-logos_transparent.png")
resized_image = original_image.resize((200, 200), Image.ADAPTIVE)
img = ImageTk.PhotoImage(resized_image)

# Create a label with the image
panel = tk.Label(root, image=img)
panel.place(relx=0.001, rely= -0.13)

url_area_label = ttk.Label(root, text="Enter you video url", font=("Segoe UI Semibold", 15))
url_area_label.place(relx=0.318, rely=0.1)

url_area = tk.Entry(root, textvariable=url_path, font=('Arial 8'))
url_area.place(relx=0.31, rely=0.26, width=400, x=10)
url_area.focus()

selected_path_label = ttk.Label(root, textvariable=selected_path_var)
selected_path_label.place(relx=0.108, rely=0.5)

error_label = ttk.Label(root, textvariable=error_label_var, foreground="red")
error_label.place(relx=0.1, rely=0.5)

browser_button = ttk.Button(
    root,
    text='Browse',
    command=choose_directory
)
download_button = ttk.Button(
    root,
    text='Download Your Video',
    command=main
)
exit_button = ttk.Button(
    root,
    text='Close',
    command=lambda: root.quit()
)
browser_button.place(relx=0.308, rely=0.8)
download_button.place(relx=0.4, rely=0.8, x=20)
exit_button.place(relx=0.1, rely=0.8)

url_area.bind("<KeyRelease>", lambda event: get_video_details(url_path.get()))

root.mainloop()
