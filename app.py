import tkinter as tk
from tkinter import filedialog as fd, StringVar
from tkinter import messagebox

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tksheet import Sheet

from data.csv_helper import CsvHelper
from service.chart_service import show_null_value_chart, show_chart_distribute_episodes, \
    show_chart_top10_by_rating, show_chart_top10_studio, show_chart_release_year, show_chart_scale_chart
from service.data_clean_service import DataCleanService
from service.standard_scaler_service import StandardScalerService


class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Đồ án python")
        # make full screen
        self.root.state('zoomed')
        self.csv_helper = CsvHelper()
        self.data_clean_service = DataCleanService()
        self.standard_scaler_service = StandardScalerService()
        self.sheet = None
        self.current_page_label = None
        self.sort_option = None
        self.search_text = tk.StringVar()
        self.selected_row_index = None
        self.data_after_scaled = None
        self.list_entry_variable = [
            {"name": "Rank", "entry": StringVar()},
            {"name": "Name", "entry": StringVar()},
            {"name": "Japanese_name", "entry": StringVar()},
            {"name": "Type", "entry": StringVar()},
            {"name": "Episodes", "entry": StringVar()},
            {"name": "Studio", "entry": StringVar()},
            {"name": "Release_season", "entry": StringVar()},
            {"name": "Tags", "entry": StringVar()},
            {"name": "Rating", "entry": StringVar()},
            {"name": "Release_year", "entry": StringVar()},
            {"name": "End_year", "entry": StringVar()},
            {"name": "Description", "entry": StringVar()},
            {"name": "Content_Warning", "entry": StringVar()},
            {"name": "Related_Mange", "entry": StringVar()},
            {"name": "Related_anime", "entry": StringVar()},
            {"name": "Voice_actors", "entry": StringVar()},
            {"name": "staff", "entry": StringVar()}
        ]

        self.current_page = 1
        self.data, self.total_pages, self.row_per_page = self.csv_helper.read_csv("data/Anime.csv")

        self.root.grid_rowconfigure(0, weight=7)  # Hàng cho frame_load_data
        self.root.grid_rowconfigure(1, weight=1)  # Hàng cho frame_bottom
        self.root.grid_columnconfigure(0, weight=1)

        self.frame_load_data = self.create_frame_load_data()
        self.frame_bottom = self.create_frame_bottom()
        self.root.mainloop()

    def create_frame_load_data(self):
        frame_load_data = tk.Frame(self.root)
        frame_load_data.grid(row=0, column=0, sticky="nsew")
        frame_load_data.grid_columnconfigure(0, weight=1)
        frame_load_data.grid_rowconfigure(1, weight=1)

        # create frame at top to search and sort
        frame_search_sort = tk.Frame(frame_load_data)
        frame_search_sort.grid(row=0, column=0, columnspan=5, sticky="nsew")
        frame_search_sort.config(bg="gray")

        # create label and entry to search
        lbl_search = tk.Label(frame_search_sort, text="Tìm kiếm:", font=("Arial", 12))
        lbl_search.grid(row=0, column=0, padx=10, pady=10)

        entry_search = tk.Entry(frame_search_sort, textvariable=self.search_text, width=50)
        entry_search.grid(row=0, column=1, padx=10, pady=10)

        btn_search = tk.Button(frame_search_sort, text="Tìm", width=10, height=1, command=self.on_search)
        btn_search.grid(row=0, column=2, padx=10, pady=10)

        # create combox box to sort
        lbl_sort = tk.Label(frame_search_sort, text="Sắp xếp tăng dần theo:", font=("Arial", 12))
        lbl_sort.grid(row=0, column=3, padx=10, pady=10)

        self.sort_option = tk.StringVar(value="Name")
        self.sort_option.trace("w", self.on_sort_option_change)
        menu_sort = tk.OptionMenu(frame_search_sort, self.sort_option, "Name", "Rating", "Rank", "Episodes", "Type")
        menu_sort.config(width=10)
        menu_sort.grid(row=0, column=4, padx=10, pady=10)

        # frame to load data csv
        frame_data = tk.Frame(frame_load_data)
        frame_data.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        frame_data.config(bg="white")
        frame_data.columnconfigure(0, weight=10)
        frame_data.columnconfigure(1, weight=2)
        frame_data.rowconfigure(0, weight=1)

        # create table to load data
        frame_csv = tk.Frame(frame_data)
        frame_csv.grid(row=0, column=0, sticky="nsew")
        frame_csv.config(bg="white")
        frame_csv.columnconfigure(0, weight=1)
        frame_csv.rowconfigure(0, weight=1)

        self.sheet = Sheet(frame_csv, data=self.data.values.tolist(),
                           headers=list(self.data.columns), header_bg="blue",
                           selected_rows_to_end_of_window=True,
                           header_fg="white")
        self.sheet.grid(row=0, column=0, sticky="nsew")
        self.sheet.enable_bindings()
        self.sheet.extra_bindings("cell_select", self.on_sheet_click)

        # create two button to move next and previous page
        frame_button_page = tk.Frame(frame_data)
        frame_button_page.grid(row=1, column=0, columnspan=5, sticky="nsew")

        btn_first = tk.Button(frame_button_page, text="Trang đầu", width=15, height=2, bg="DeepSkyBlue4", fg="white",
                              command=self.move_first_page)
        btn_first.grid(row=1, column=0, padx=5, pady=5)

        btn_previous = tk.Button(frame_button_page, text="Trang trước", width=15, height=2, bg="SkyBlue1", fg="Black",
                                 command=self.move_previous_page)
        btn_previous.grid(row=1, column=1, padx=5, pady=5)

        btn_next = tk.Button(frame_button_page, text="Trang sau", width=15, height=2, bg="SkyBlue1", fg="Black",
                             command=self.move_next_page)
        btn_next.grid(row=1, column=2, padx=5, pady=5)

        btn_last = tk.Button(frame_button_page, text="Trang cuối", width=15, height=2, bg="DeepSkyBlue4", fg="white",
                             command=self.move_last_page)
        btn_last.grid(row=1, column=3, padx=5, pady=5)

        self.current_page_label = tk.Label(frame_button_page, text=f"Trang {self.current_page}/{self.total_pages}",
                                           font=("Arial", 12))
        self.current_page_label.grid(row=1, column=4, padx=5, pady=5)

        # right box to enter data
        frame_right = tk.Frame(frame_data)
        frame_right.grid(row=0, column=1, sticky="nsew")
        frame_right.config(bg="lightblue")
        frame_right.grid_columnconfigure(0, weight=1)
        frame_right.grid_columnconfigure(1, weight=3)
        frame_right.grid_rowconfigure(0, weight=1)
        frame_right.grid_rowconfigure(1, weight=1)
        frame_right.grid_rowconfigure(2, weight=1)
        frame_right.grid_rowconfigure(3, weight=1)
        frame_right.grid_rowconfigure(4, weight=1)
        frame_right.grid_rowconfigure(5, weight=1)
        frame_right.grid_rowconfigure(6, weight=1)
        frame_right.grid_rowconfigure(7, weight=1)
        frame_right.grid_rowconfigure(8, weight=1)
        frame_right.grid_rowconfigure(9, weight=1)
        frame_right.grid_rowconfigure(10, weight=1)
        frame_right.grid_rowconfigure(11, weight=1)
        frame_right.grid_rowconfigure(12, weight=1)
        frame_right.grid_rowconfigure(13, weight=1)
        frame_right.grid_rowconfigure(14, weight=1)
        frame_right.grid_rowconfigure(15, weight=1)
        frame_right.grid_rowconfigure(16, weight=1)

        lb_rank = tk.Label(frame_right, text="Rank:", font=("Arial", 12))
        lb_rank.grid(row=0, column=0, padx=10, pady=10)

        rank_var = next(item["entry"] for item in self.list_entry_variable if item["name"] == "Rank")
        entry_rank = tk.Entry(frame_right, textvariable=rank_var)
        entry_rank.grid(row=0, column=1, padx=10, pady=10)

        lb_name = tk.Label(frame_right, text="Name:", font=("Arial", 12))
        lb_name.grid(row=1, column=0, padx=10, pady=10)

        name_var = next(item["entry"] for item in self.list_entry_variable if item["name"] == "Name")
        entry_name = tk.Entry(frame_right, textvariable=name_var)
        entry_name.grid(row=1, column=1, padx=10, pady=10)

        lb_japanese_name = tk.Label(frame_right, text="Japanese name:", font=("Arial", 12))
        lb_japanese_name.grid(row=2, column=0, padx=10, pady=10)

        entry_japanese_name_var = next(
            item["entry"] for item in self.list_entry_variable if item["name"] == "Japanese_name")
        entry_japanese_name = tk.Entry(frame_right, textvariable=entry_japanese_name_var)
        entry_japanese_name.grid(row=2, column=1, padx=10, pady=10)

        lb_type = tk.Label(frame_right, text="Type:", font=("Arial", 12))
        lb_type.grid(row=3, column=0, padx=10, pady=10)

        entry_type_var = next(item["entry"] for item in self.list_entry_variable if item["name"] == "Type")
        entry_type = tk.Entry(frame_right, textvariable=entry_type_var)
        entry_type.grid(row=3, column=1, padx=10, pady=10)

        lb_episodes = tk.Label(frame_right, text="Episodes:", font=("Arial", 12))
        lb_episodes.grid(row=4, column=0, padx=10, pady=10)

        entry_episodes_var = next(item["entry"] for item in self.list_entry_variable if item["name"] == "Episodes")
        entry_episodes = tk.Entry(frame_right, textvariable=entry_episodes_var)
        entry_episodes.grid(row=4, column=1, padx=10, pady=10)

        lb_studio = tk.Label(frame_right, text="Studio:", font=("Arial", 12))
        lb_studio.grid(row=5, column=0, padx=10, pady=10)

        entry_studio_var = next(item["entry"] for item in self.list_entry_variable if item["name"] == "Studio")
        entry_studio = tk.Entry(frame_right, textvariable=entry_studio_var)
        entry_studio.grid(row=5, column=1, padx=10, pady=10)

        lb_release_season = tk.Label(frame_right, text="Release season:", font=("Arial", 12))
        lb_release_season.grid(row=6, column=0, padx=10, pady=10)

        entry_release_season_var = next(
            item["entry"] for item in self.list_entry_variable if item["name"] == "Release_season")
        entry_release_season = tk.Entry(frame_right, textvariable=entry_release_season_var)
        entry_release_season.grid(row=6, column=1, padx=10, pady=10)

        lb_tags = tk.Label(frame_right, text="Tags:", font=("Arial", 12))
        lb_tags.grid(row=7, column=0, padx=10, pady=10)

        entry_tags_var = next(item["entry"] for item in self.list_entry_variable if item["name"] == "Tags")
        entry_tags = tk.Entry(frame_right, textvariable=entry_tags_var)
        entry_tags.grid(row=7, column=1, padx=10, pady=10)

        lb_rating = tk.Label(frame_right, text="Rating:", font=("Arial", 12))
        lb_rating.grid(row=8, column=0, padx=10, pady=10)

        entry_rating_var = next(item["entry"] for item in self.list_entry_variable if item["name"] == "Rating")
        entry_rating = tk.Entry(frame_right, textvariable=entry_rating_var)
        entry_rating.grid(row=8, column=1, padx=10, pady=10)

        lb_release_year = tk.Label(frame_right, text="Release year:", font=("Arial", 12))
        lb_release_year.grid(row=9, column=0, padx=10, pady=10)

        entry_release_year_var = next(
            item["entry"] for item in self.list_entry_variable if item["name"] == "Release_year")
        entry_release_year = tk.Entry(frame_right, textvariable=entry_release_year_var)
        entry_release_year.grid(row=9, column=1, padx=10, pady=10)

        lb_end_year = tk.Label(frame_right, text="End year:", font=("Arial", 12))
        lb_end_year.grid(row=10, column=0, padx=10, pady=10)

        entry_end_year_var = next(item["entry"] for item in self.list_entry_variable if item["name"] == "End_year")
        entry_end_year = tk.Entry(frame_right, textvariable=entry_end_year_var)
        entry_end_year.grid(row=10, column=1, padx=10, pady=10)

        lb_description = tk.Label(frame_right, text="Description:", font=("Arial", 12))
        lb_description.grid(row=11, column=0, padx=10, pady=10)

        entry_description_var = next(
            item["entry"] for item in self.list_entry_variable if item["name"] == "Description")
        entry_description = tk.Entry(frame_right, textvariable=entry_description_var)
        entry_description.grid(row=11, column=1, padx=10, pady=10)

        lb_content_warning = tk.Label(frame_right, text="Content warning:", font=("Arial", 12))
        lb_content_warning.grid(row=12, column=0, padx=10, pady=10)

        entry_content_warning_var = next(
            item["entry"] for item in self.list_entry_variable if item["name"] == "Content_Warning")
        entry_content_warning = tk.Entry(frame_right, textvariable=entry_content_warning_var)
        entry_content_warning.grid(row=12, column=1, padx=10, pady=10)

        lb_relate_manga = tk.Label(frame_right, text="Relate mange:", font=("Arial", 12))
        lb_relate_manga.grid(row=13, column=0, padx=10, pady=10)

        entry_relate_manga_var = next(
            item["entry"] for item in self.list_entry_variable if item["name"] == "Related_Mange")
        entry_relate_manga = tk.Entry(frame_right, textvariable=entry_relate_manga_var)
        entry_relate_manga.grid(row=13, column=1, padx=10, pady=10)

        lb_relate_anime = tk.Label(frame_right, text="Relate anime:", font=("Arial", 12))
        lb_relate_anime.grid(row=14, column=0, padx=10, pady=10)

        entry_relate_anime_var = next(
            item["entry"] for item in self.list_entry_variable if item["name"] == "Related_anime")
        entry_relate_anime = tk.Entry(frame_right, textvariable=entry_relate_anime_var)
        entry_relate_anime.grid(row=14, column=1, padx=10, pady=10)
        lb_voice_actor = tk.Label(frame_right, text="Voice actor:", font=("Arial", 12))
        lb_voice_actor.grid(row=15, column=0, padx=10, pady=10)

        entry_voice_actor_var = next(
            item["entry"] for item in self.list_entry_variable if item["name"] == "Voice_actors")
        entry_voice_actor = tk.Entry(frame_right, textvariable=entry_voice_actor_var)
        entry_voice_actor.grid(row=15, column=1, padx=10, pady=10)

        lb_staff = tk.Label(frame_right, text="Staff:", font=("Arial", 12))
        lb_staff.grid(row=16, column=0, padx=10, pady=10)

        entry_staff_var = next(
            item["entry"] for item in self.list_entry_variable if item["name"] == "staff")
        entry_staff = tk.Entry(frame_right, textvariable=entry_staff_var)
        entry_staff.grid(row=16, column=1, padx=10, pady=10)

        return frame_load_data

    def create_frame_bottom(self):
        frame_bottom = tk.Frame(self.root)
        frame_bottom.grid(row=1, column=0, sticky="nsew")

        frame_bottom.config(bg="lightblue")

        # Tao list cac button
        list_object_button = [
            {"text": "Chọn file", "width": 10, "command": self.open_file, "bg": "lavender"},
            {"text": "Thêm", "width": 10, "command": self.insert_data, "bg": "light yellow"},
            {"text": "Sửa", "width": 10, "command": self.update_data, "bg": "azure2"},
            {"text": "Xóa", "width": 10, "command": self.delete_data, "bg": "plum3"},
            {"text": "Làm mới", "width": 10, "command": self.reset_entry_fields, "bg": "light green"},
            {"text": "Làm sạch dữ liệu", "width": 15, "command": self.clean_data, "bg": "light coral"},
            {"text": "Trực quan hóa", "width": 15, "command": self.data_visualize, "bg": "khaki2"},
            {"text": "Chuẩn hóa dữ liệu", "width": 15, "command": self.scaled_data, "bg": "khaki2"},
            {"text": "Highlight", "width": 10, "command": self.highlight, "bg": "LightBlue3"},
            {"text": "Mô tả đồ án", "width": 10, "command": self.show_about_project, "bg": "light pink"},
            {"text": "Thoát", "width": 10, "command": self.on_exit, "bg": "pink3"}
        ]

        for index, object_button in enumerate(list_object_button):
            btn = tk.Button(frame_bottom, text=object_button["text"], width=object_button["width"],
                            bg=object_button["bg"],
                            height=2, command=object_button["command"])
            btn.grid(row=0, column=index, padx=10, pady=10)
            frame_bottom.grid_columnconfigure(index, weight=1)

        return frame_bottom

    def scaled_data(self):
        df_scale = self.standard_scaler_service.scale(self.data_clean_service.clean_data(self.csv_helper.get_data()))

        # tao mot cua so moi de hien thi du lieu sau khi chuan hoa
        new_window = tk.Toplevel(self.root)
        new_window.title("Dữ liệu sau khi chuẩn hóa")
        new_window.geometry(self.get_center_window(600, 600))

        # tao 1 sheet de hien thi du lieu sau khi chuan hoa
        sheet = Sheet(new_window, data=df_scale.values.tolist(), headers=list(df_scale.columns), header_bg="blue",
                      selected_rows_to_end_of_window=True, header_fg="white")
        sheet.pack(expand=True, fill=tk.BOTH)
        sheet.enable_bindings()

        fig = show_chart_scale_chart(self.csv_helper.get_data(), df_scale)
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def move_next_page(self):
        self.move_to_page(self.current_page + 1)

    def move_previous_page(self):
        self.move_to_page(self.current_page - 1)

    def move_first_page(self):
        self.move_to_page(1)

    def move_last_page(self):
        self.move_to_page(self.total_pages)

    def move_to_page(self, page):
        if 0 < page <= self.total_pages:
            self.current_page = page
            self.data = self.csv_helper.get_data_per_page(self.current_page)
            self.sheet.set_sheet_data(self.data.values.tolist())
            self.update_paging_label()
            self.clear_highlight()
        else:
            messagebox.showerror("Lỗi", "Trang không tồn tại")

    def on_sort_option_change(self, *args):
        self.data = self.csv_helper.sort_data(self.sort_option.get(), self.current_page)
        self.sheet.set_sheet_data(self.data.values.tolist())

    def on_search(self):
        keyword = self.search_text.get()
        self.data, self.total_pages = self.csv_helper.search_data(keyword, self.current_page)
        self.sheet.set_sheet_data(self.data.values.tolist())
        self.update_paging_label()

    def update_paging_label(self):
        self.current_page_label.config(text=f"Trang {self.current_page}/{self.total_pages}")

    def on_exit(self):
        self.root.destroy()

    def show_about_project(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Thông tin đồ án")
        new_window.geometry(self.get_center_window(600, 600))

        # dua new window ra giua man hinh
        new_window.update_idletasks()
        label = tk.Label(new_window, text="Đồ án cuối kỳ môn Python", font=("Arial", 12))
        label.pack()

        # read file from data/about_project.txt
        with open("data/about_project.txt", "r", encoding="utf-8") as file:
            content = file.read()
            text = tk.Text(new_window, height=10, width=50)
            text.insert(tk.END, content)
            text.pack(expand=True, fill=tk.BOTH)

            # Apply bold formatting
            text.tag_configure("bold", font=("Arial", 10, "bold"))
            text.tag_add("bold", "1.0", "end")

    def insert_data(self):
        # kiem tra trong list entry variable neu co gia tri None thi hien thong bao loi
        for item in self.list_entry_variable:
            if item["entry"].get() == "":
                messagebox.showerror("Lỗi", f"Vui lòng nhập {item['name']}")
                return

        row_data = self.get_dict_data()

        self.data, self.total_pages = self.csv_helper.insert_data(row_data)
        self.sheet.set_sheet_data(self.data.values.tolist())
        self.update_paging_label()

        messagebox.showinfo("Thông báo", "Thêm dữ liệu thành công")
        self.reset_entry_fields()

    def delete_data(self):
        if self.selected_row_index is None:
            messagebox.showerror("Lỗi", "Vui lòng chọn dòng cần xóa")
            return

        self.data, self.total_pages = self.csv_helper.delete_data(self.selected_row_index, self.current_page)
        self.sheet.set_sheet_data(self.data.values.tolist())
        self.update_paging_label()
        self.selected_row_index = None

    def update_data(self):
        if self.selected_row_index is None:
            messagebox.showerror("Lỗi", "Vui lòng chọn dòng cần xóa")
            return

        data = self.get_dict_data()
        self.data, self.total_pages = self.csv_helper.update_data(data, self.selected_row_index, self.current_page)
        self.sheet.set_sheet_data(self.data.values.tolist())
        self.update_paging_label()

    def highlight(self):
        # highlight all row if have value None, null, empty
        for i in range(len(self.data)):
            for j in range(len(self.data.columns)):
                if self.data.iloc[i, j] is None or self.data.iloc[i, j] == "" or pd.isnull(self.data.iloc[i, j]):
                    self.sheet.highlight_cells(row=i, column=j, bg="red")

    def clear_highlight(self):
        for i in range(len(self.data)):
            for j in range(len(self.data.columns)):
                self.sheet.highlight_cells(row=i, column=j, bg="white")

    def open_file(self):
        # open file dialog to choose file
        filetypes = (
            ('Csv files', '*.csv'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if filename:
            self.current_page = 1
            self.data, self.total_pages, self.row_per_page = self.csv_helper.read_csv(filename)
            self.sheet.set_sheet_data(self.data.values.tolist())
            self.update_paging_label()

    # Define the callback function to handle the click event
    def on_sheet_click(self, event):
        selected_row = self.sheet.get_currently_selected()
        if selected_row:
            self.selected_row_index = selected_row[0]
            self.fill_entry_fields(self.data.iloc[self.selected_row_index])

    # Define the function to fill the entry fields with the selected row data
    def fill_entry_fields(self, row_data):
        for item in self.list_entry_variable:
            item["entry"].set(row_data[item["name"]])

    def reset_entry_fields(self):
        self.selected_row_index = None
        for item in self.list_entry_variable:
            item["entry"].set("")
        self.data, self.total_pages, self.row_per_page = self.csv_helper.read_csv("data/Anime.csv")
        self.current_page = 1
        self.sheet.set_sheet_data(self.data.values.tolist())
        self.update_paging_label()
        self.clear_highlight()

    def clean_data(self):
        self.data_clean_service.clean_data(self.csv_helper.get_data())
        self.move_to_page(self.current_page)
        self.clear_highlight()

    def get_dict_data(self):
        row_data = {}
        for item in self.list_entry_variable:
            row_data[item["name"]] = item["entry"].get()
        return row_data

    def data_visualize(self):
        popup = tk.Toplevel(self.root)
        popup.title("Chọn biểu đồ trực quan hóa")

        # để popup nằm giữa màn hình
        popup.geometry(self.get_center_window(600, 600))
        # Add a label to the popup window
        label = tk.Label(popup, text="Chọn:", font=("Arial", 12))
        label.grid(row=0, column=0, pady=10)

        def draw_chart(fig, title):
            new_window = tk.Toplevel(self.root)
            new_window.title(title)  # Tiêu đề cửa sổ mới

            # Tạo canvas và vẽ biểu đồ
            canvas = FigureCanvasTkAgg(fig, master=new_window)  # Sử dụng cửa sổ mới làm master
            canvas.draw()
            canvas.get_tk_widget().pack()

        def on_option_click():
            percent_null = self.csv_helper.get_null_value_df()
            fig = show_null_value_chart(percent_null)

            draw_chart(fig, "Biểu đồ tương quan giữa cột và số lượng giá trị null")

        def episode_distribution():
            fig = show_chart_distribute_episodes(self.csv_helper.get_data())
            draw_chart(fig, "Phân bố số tập phim")

        def show_top10_by_rating():
            fig = show_chart_top10_by_rating(self.csv_helper.get_data())
            draw_chart(fig, "Top 10 Anime Theo Rating")

        def show_top10_by_studio():
            fig = show_chart_top10_studio(self.csv_helper.get_data())
            draw_chart(fig, "Số lượng anime theo Studio (Top 10 Studio)")

        def show_anime_by_release_year():
            fig = show_chart_release_year(self.csv_helper.get_data())
            draw_chart(fig, "Số lượng anime theo năm phát hành (Release_year)")

        def show_outlier():
            df = self.csv_helper.get_data().copy()

            # Tạo Figure và hai trục
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))  # 1 hàng, 2 cột
            # Biểu đồ trước khi xử lý outlier
            sns.boxplot(y='Release_year', data=df, ax=axes[0])
            axes[0].set_title('Trước khi xử lý Outlier', fontsize=14)

            # Xử lý outlier
            IQR = df["Release_year"].quantile(0.75) - df["Release_year"].quantile(0.25)
            lower_release_year_limit = df["Release_year"].quantile(0.25) - (IQR * 1.5)
            upper_release_year_limit = df["Release_year"].quantile(0.75) + (IQR * 1.5)
            df["Release_year"] = np.where(
                df["Release_year"] > upper_release_year_limit,
                upper_release_year_limit,
                np.where(df["Release_year"] < lower_release_year_limit, lower_release_year_limit, df["Release_year"])
            )

            # Biểu đồ sau khi xử lý outlier
            sns.boxplot(y='Release_year', data=df, ax=axes[1])
            axes[1].set_title('Sau khi xử lý Outlier', fontsize=14)

            fig.tight_layout()
            draw_chart(fig, "Biểu đồ sau xử lý outlier")

        # Add a dropdown menu to select different options
        options = [
            {"text": "Biểu đồ tương quan giữa cột và số lượng giá trị null", "bg": "light blue",
             "command": on_option_click},
            {"text": "Phân bố số tập phim", "bg": "light blue", "command": episode_distribution},
            {"text": "Top 10 anime theo Rating", "bg": "light blue", "command": show_top10_by_rating},
            {"text": "Số lượng anime theo Studio (Top 10 Studio)", "bg": "light blue",
             "command": show_top10_by_studio},
            {"text": "Số lượng anime theo năm phát hành (Release_year)", "bg": "light blue",
             "command": show_anime_by_release_year},
            {"text": "Biểu đồ sau xử lý outlier", "command": show_outlier, "bg": "light blue"},
        ]

        for index, opt in enumerate(options):
            button = tk.Button(popup, text=opt["text"], bg=opt["bg"],
                               command=opt["command"])
            button.grid(row=index + 2, column=0, pady=5)
            popup.grid_rowconfigure(index + 2, weight=1)

        # Add a button to close the popup
        close_button = tk.Button(popup, text="Close", command=popup.destroy, bg="red")
        close_button.grid(row=len(options) + 2, column=0, pady=10)

        popup.grid_rowconfigure(len(options) + 2, weight=1)
        popup.grid_columnconfigure(0, weight=1)

    def get_center_window(self, width, height):
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()

        popup_width = width
        popup_height = height

        center_x = main_x + (main_width // 2) - (popup_width // 2)
        center_y = main_y + (main_height // 2) - (popup_height // 2)

        return f"{popup_width}x{popup_height}+{center_x}+{center_y}"


if __name__ == "__main__":
    MainGUI()
