import tkinter as tk
from tkinter import ttk, messagebox, filedialog, StringVar
import yt_dlp
from urllib.parse import urlparse, parse_qs

class YouTubeDownloader:
    def __init__(self):
        self.links = []
        self.root = tk.Tk()
        self.root.title("YouTube Music Downloader")

        # Entry for adding links
        self.link_entry = tk.Entry(self.root, width=40)
        self.link_entry.grid(row=0, column=0, padx=10, pady=10)

        # Button to add links
        add_button = tk.Button(self.root, text="Add Link", command=self.add_link)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        # Button to clear the link input
        clear_button = tk.Button(self.root, text="Clear Input", command=self.clear_input)
        clear_button.grid(row=0, column=2, padx=10, pady=10)

        # Listbox to display links with order number
        self.link_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=10, width=50)
        self.link_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Button to remove selected link
        remove_button = tk.Button(self.root, text="Remove", command=self.remove_link)
        remove_button.grid(row=2, column=0, padx=10, pady=10)

        # Button to download all links
        download_button = tk.Button(self.root, text="Download All", command=self.download_all)
        download_button.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        # StringVar to store the selected location
        self.location_var = StringVar()

        # Entry for specifying download location
        self.location_entry = tk.Entry(self.root, textvariable=self.location_var, width=40)
        self.location_entry.grid(row=3, column=0, padx=10, pady=10)

        # Button to specify download location using file dialog
        location_button = tk.Button(self.root, text="Select Location", command=self.choose_location)
        location_button.grid(row=3, column=1, padx=10, pady=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=4, column=0, columnspan=3, pady=10)

        self.root.mainloop()

    def add_link(self):
        full_link = self.link_entry.get()
        video_id = self.get_video_id(full_link)
        if video_id:
            order_number = len(self.links) + 1
            self.links.append(f"https://www.youtube.com/watch?v={video_id}")
            self.link_listbox.insert(tk.END, f"{order_number}. https://www.youtube.com/watch?v={video_id}")
            self.link_entry.delete(0, tk.END)

    def remove_link(self):
        selected_index = self.link_listbox.curselection()
        if selected_index:
            self.links.pop(selected_index[0])
            self.link_listbox.delete(selected_index[0])
            self.update_order_numbers()

    def download_all(self):
        location = self.location_var.get()
        if location and self.links:
            self.progress_bar["maximum"] = len(self.links)
            for i, link in enumerate(self.links):
                options = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': f'{location}/{i + 1}.%(ext)s',
                }
                with yt_dlp.YoutubeDL(options) as ydl:
                    try:
                        ydl.download([link])
                    except Exception as e:
                        messagebox.showerror("Error", f"Error downloading {link}: {str(e)}")
                        continue
                self.progress_bar["value"] = i + 1
                self.progress_bar.update()
            messagebox.showinfo("Download Complete", "All Music downloaded successfully!")
            self.progress_bar["value"] = 0
            self.progress_bar.update()

    def get_video_id(self, link):
        query = urlparse(link)
        if query.hostname == 'www.youtube.com' and query.path == '/watch':
            params = parse_qs(query.query)
            return params['v'][0] if 'v' in params else None
        elif query.hostname == 'youtu.be':
            return query.path.lstrip('/')
        return None

    def choose_location(self):
        location = filedialog.askdirectory()
        if location:
            self.location_var.set(location)

    def clear_input(self):
        self.link_entry.delete(0, tk.END)

    def update_order_numbers(self):
        self.link_listbox.delete(0, tk.END)
        for i, link in enumerate(self.links, start=1):
            self.link_listbox.insert(tk.END, f"{i}. {link}")

if __name__ == "__main__":
    downloader = YouTubeDownloader()
