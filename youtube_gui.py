import tkinter as tk
import urllib.request
from io import BytesIO
from tkinter import BOTTOM, X, RIGHT, Y

from PIL import Image, ImageTk


class YoutubeGUI:
    def __init__(self, json_data, geometry):
        self.json = json_data["result"]  # Access the nested "result" array
        self.image_cache = []  # Cache for ImageTk.PhotoImage to avoid garbage collection

        self.root = tk.Toplevel()
        self.root.title("YouTube Videos")
        self.root.geometry(geometry)
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        h = tk.Scrollbar(self.root, orient='horizontal')
        h.pack(side=BOTTOM, fill=X)

        v = tk.Scrollbar(self.root)
        v.pack(side=RIGHT, fill=Y)

        # Create frame with list div videos
        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.frame, bg="white", xscrollcommand=h.set, yscrollcommand=v.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        h.config(command=self.canvas.xview)
        v.config(command=self.canvas.yview)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.frame2 = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.frame2, anchor="nw")
        self.create_video()
        self.root.mainloop()

    def create_video(self):
        for video in self.json:
            frame = tk.Frame(self.frame2, bg="white", highlightbackground="black", highlightthickness=1)
            frame.pack(pady=5, padx=5, fill="x", expand=True)

            # Fetch and display the video thumbnail
            image_url = video["thumbnails"][0]["url"]
            with urllib.request.urlopen(image_url) as u:
                raw_data = u.read()
            image_data = Image.open(BytesIO(raw_data))
            # Resize the image to fit the frame
            image_data.thumbnail((200, 200))
            img = ImageTk.PhotoImage(image_data)

            # Cache the image to prevent garbage collection
            self.image_cache.append(img)

            thumbnail_label = tk.Label(master=frame, image=img, bg="white")
            thumbnail_label.pack(side="left", padx=5)

            # Video title
            title_label = tk.Label(frame, text=video["title"], bg="white", font=("Arial", 12), wraplength=400,
                                   justify="left")
            title_label.pack(side="top", anchor="w", padx=5)

            # Video duration
            duration_label = tk.Label(frame, text=video["duration"], bg="white", font=("Arial", 10), justify="left")
            duration_label.pack(side="bottom", anchor="w", padx=5)

            # Video link
            link_label = tk.Label(frame, text=video["link"], bg="white", font=("Arial", 10), fg="blue", cursor="hand2",
                                  wraplength=400)
            link_label.pack(side="bottom", anchor="w", padx=5)
            link_label.bind("<Button-1>", lambda e, url=video["link"]: self.open_url(url))

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
