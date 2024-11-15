import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tksheet import Sheet

from data.csv_helper import CsvHelper
from model.moive import Movie
from service.chart_service import show_null_value_chart


class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Đồ án python")
        # make full screen
        self.root.state('zoomed')
        self.csv_helper = CsvHelper()
        self.sheet = None
        self.current_page_label = None
        self.sort_option = None
        self.search_text = tk.StringVar()
        self.movie_value = Movie()

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
        lbl_sort = tk.Label(frame_search_sort, text="Sắp xếp:", font=("Arial", 12))
        lbl_sort.grid(row=0, column=3, padx=10, pady=10)

        self.sort_option = tk.StringVar(value="Name")
        self.sort_option.trace("w", self.on_sort_option_change)
        menu_sort = tk.OptionMenu(frame_search_sort, self.sort_option, "Name", "Rating")
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

        entry_rank = tk.Entry(frame_right)
        entry_rank.grid(row=0, column=1, padx=10, pady=10)
        entry_rank.bind("<KeyRelease>", lambda event: self.update_movie_value("rank", entry_rank.get()))

        lb_name = tk.Label(frame_right, text="Name:", font=("Arial", 12))
        lb_name.grid(row=1, column=0, padx=10, pady=10)

        entry_name = tk.Entry(frame_right)
        entry_name.grid(row=1, column=1, padx=10, pady=10)
        entry_name.bind("<KeyRelease>", lambda event: self.update_movie_value("name", entry_name.get()))

        lb_japanese_name = tk.Label(frame_right, text="Japanese name:", font=("Arial", 12))
        lb_japanese_name.grid(row=2, column=0, padx=10, pady=10)

        entry_japanese_name = tk.Entry(frame_right)
        entry_japanese_name.grid(row=2, column=1, padx=10, pady=10)
        entry_japanese_name.bind("<KeyRelease>", lambda event: self.update_movie_value("japanese_name",
                                                                                       entry_japanese_name.get()))

        lb_type = tk.Label(frame_right, text="Type:", font=("Arial", 12))
        lb_type.grid(row=3, column=0, padx=10, pady=10)

        entry_type = tk.Entry(frame_right)
        entry_type.grid(row=3, column=1, padx=10, pady=10)
        entry_type.bind("<KeyRelease>", lambda event: self.update_movie_value("type", entry_type.get()))

        lb_episodes = tk.Label(frame_right, text="Episodes:", font=("Arial", 12))
        lb_episodes.grid(row=4, column=0, padx=10, pady=10)

        entry_episodes = tk.Entry(frame_right)
        entry_episodes.grid(row=4, column=1, padx=10, pady=10)
        entry_episodes.bind("<KeyRelease>",
                            lambda event: self.update_movie_value("episodes", entry_episodes.get()))

        lb_studio = tk.Label(frame_right, text="Studio:", font=("Arial", 12))
        lb_studio.grid(row=5, column=0, padx=10, pady=10)

        entry_studio = tk.Entry(frame_right)
        entry_studio.grid(row=5, column=1, padx=10, pady=10)
        entry_studio.bind("<KeyRelease>", lambda event: self.update_movie_value("studio", entry_studio.get()))

        lb_release_season = tk.Label(frame_right, text="Release season:", font=("Arial", 12))
        lb_release_season.grid(row=6, column=0, padx=10, pady=10)

        entry_release_season = tk.Entry(frame_right)
        entry_release_season.grid(row=6, column=1, padx=10, pady=10)
        entry_release_season.bind("<KeyRelease>", lambda event: self.update_movie_value("release_season",
                                                                                        entry_release_season.get()))

        lb_tags = tk.Label(frame_right, text="Tags:", font=("Arial", 12))
        lb_tags.grid(row=7, column=0, padx=10, pady=10)

        entry_tags = tk.Entry(frame_right)
        entry_tags.grid(row=7, column=1, padx=10, pady=10)
        entry_tags.bind("<KeyRelease>", lambda event: self.update_movie_value("tags", entry_tags.get()))

        lb_rating = tk.Label(frame_right, text="Rating:", font=("Arial", 12))
        lb_rating.grid(row=8, column=0, padx=10, pady=10)

        entry_rating = tk.Entry(frame_right)
        entry_rating.grid(row=8, column=1, padx=10, pady=10)
        entry_rating.bind("<KeyRelease>", lambda event: self.update_movie_value("rating", entry_rating.get()))

        lb_release_year = tk.Label(frame_right, text="Release year:", font=("Arial", 12))
        lb_release_year.grid(row=9, column=0, padx=10, pady=10)

        entry_release_year = tk.Entry(frame_right)
        entry_release_year.grid(row=9, column=1, padx=10, pady=10)
        entry_release_year.bind("<KeyRelease>", lambda event: self.update_movie_value("release_year",
                                                                                      entry_release_year.get()))

        lb_end_year = tk.Label(frame_right, text="End year:", font=("Arial", 12))
        lb_end_year.grid(row=10, column=0, padx=10, pady=10)

        entry_end_year = tk.Entry(frame_right)
        entry_end_year.grid(row=10, column=1, padx=10, pady=10)
        entry_end_year.bind("<KeyRelease>",
                            lambda event: self.update_movie_value("end_year", entry_end_year.get()))

        lb_description = tk.Label(frame_right, text="Description:", font=("Arial", 12))
        lb_description.grid(row=11, column=0, padx=10, pady=10)

        entry_description = tk.Entry(frame_right)
        entry_description.grid(row=11, column=1, padx=10, pady=10)
        entry_description.bind("<KeyRelease>",
                               lambda event: self.update_movie_value("description", entry_description.get()))

        lb_content_warning = tk.Label(frame_right, text="Content warning:", font=("Arial", 12))
        lb_content_warning.grid(row=12, column=0, padx=10, pady=10)

        entry_content_warning = tk.Entry(frame_right)
        entry_content_warning.grid(row=12, column=1, padx=10, pady=10)
        entry_content_warning.bind("<KeyRelease>", lambda event: self.update_movie_value("content_warning",
                                                                                         entry_content_warning.get()))

        lb_relate_manga = tk.Label(frame_right, text="Relate mange:", font=("Arial", 12))
        lb_relate_manga.grid(row=13, column=0, padx=10, pady=10)

        entry_relate_manga = tk.Entry(frame_right)
        entry_relate_manga.grid(row=13, column=1, padx=10, pady=10)
        entry_relate_manga.bind("<KeyRelease>", lambda event: self.update_movie_value("related_manga",
                                                                                      entry_relate_manga.get()))

        lb_relate_anime = tk.Label(frame_right, text="Relate anime:", font=("Arial", 12))
        lb_relate_anime.grid(row=14, column=0, padx=10, pady=10)

        entry_relate_anime = tk.Entry(frame_right)
        entry_relate_anime.grid(row=14, column=1, padx=10, pady=10)
        entry_relate_anime.bind("<KeyRelease>", lambda event: self.update_movie_value("related_anime",
                                                                                      entry_relate_anime.get()))
        lb_voice_actor = tk.Label(frame_right, text="Voice actor:", font=("Arial", 12))
        lb_voice_actor.grid(row=15, column=0, padx=10, pady=10)

        entry_voice_actor = tk.Entry(frame_right)
        entry_voice_actor.grid(row=15, column=1, padx=10, pady=10)
        entry_voice_actor.bind("<KeyRelease>",
                               lambda event: self.update_movie_value("voice_actors", entry_voice_actor.get()))

        lb_staff = tk.Label(frame_right, text="Staff:", font=("Arial", 12))
        lb_staff.grid(row=16, column=0, padx=10, pady=10)

        entry_staff = tk.Entry(frame_right)
        entry_staff.grid(row=16, column=1, padx=10, pady=10)
        entry_staff.bind("<KeyRelease>", lambda event: self.update_movie_value("staff", entry_staff.get()))

        return frame_load_data

    def create_frame_bottom(self):
        frame_bottom = tk.Frame(self.root)
        frame_bottom.grid(row=1, column=0, sticky="nsew")

        # fill color background for frame_bottom
        frame_bottom.config(bg="lightblue")

        # create buttons is: "Chọn file", "Thêm", "Sửa", "Xóa", "Thoát", Trực quan hóa
        btn_choose_file = tk.Button(frame_bottom, text="Chọn file", width=10, height=2, command=self.open_file)
        btn_choose_file.grid(row=0, column=0, padx=10, pady=10)

        btn_add = tk.Button(frame_bottom, text="Thêm", width=10, height=2, command=self.insert_data)
        btn_add.grid(row=0, column=1, padx=10, pady=10)

        btn_edit = tk.Button(frame_bottom, text="Sửa", width=10, height=2)
        btn_edit.grid(row=0, column=2, padx=10, pady=10)

        btn_delete = tk.Button(frame_bottom, text="Xóa", width=10, height=2, command=self.delete_data)
        btn_delete.grid(row=0, column=3, padx=10, pady=10)

        btn_visualize = tk.Button(frame_bottom, text="Trực quan hóa", width=15, height=2)
        btn_visualize.grid(row=0, column=4, padx=10, pady=10)

        btn_highlight = tk.Button(frame_bottom, text="Highlight", width=10, height=2, command=self.highlight)
        btn_highlight.grid(row=0, column=5, padx=10, pady=10)

        btn_clean = tk.Button(frame_bottom, text="Làm sạch dữ liệu", width=20, height=2, command=self.clean_data)
        btn_clean.grid(row=0, column=6, padx=10, pady=10)

        btn_exit = tk.Button(frame_bottom, text="Thoát", width=10, height=2, command=self.on_exit)
        btn_exit.grid(row=0, column=7, padx=10, pady=10)

        # make buttons is center
        frame_bottom.grid_columnconfigure(0, weight=1)
        frame_bottom.grid_columnconfigure(1, weight=1)
        frame_bottom.grid_columnconfigure(2, weight=1)
        frame_bottom.grid_columnconfigure(3, weight=1)
        frame_bottom.grid_columnconfigure(4, weight=1)
        frame_bottom.grid_columnconfigure(5, weight=1)

        return frame_bottom

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
            self.data, _, _ = self.csv_helper.read_csv("data/Anime.csv", self.current_page)
            self.sheet.set_sheet_data(self.data.values.tolist())
            self.update_paging_label()
        else:
            messagebox.showerror("Lỗi", "Trang không tồn tại")

    def update_movie_value(self, attribute, value):
        setattr(self.movie_value, attribute, value)

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

    def insert_data(self):
        data = self.movie_value.to_dict()

        # validate data if have empty value then alert to fill full
        if "" in data.values() or None in data.values():
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
            return

        self.data, self.total_pages = self.csv_helper.insert_data(data)
        self.sheet.set_sheet_data(self.data.values.tolist())
        self.update_paging_label()

    def delete_data(self):
        row_data = self.sheet.get_currently_selected()
        if not row_data:
            messagebox.showerror("Lỗi", "Vui lòng chọn dòng cần xóa")
            return

        index = row_data[0][0]
        self.data, self.total_pages = self.csv_helper.delete_data(index, self.current_page)
        self.sheet.set_sheet_data(self.data.values.tolist())
        self.update_paging_label()

    def update_data(self):
        row_data = self.sheet.get_currently_selected()
        if not row_data:
            messagebox.showerror("Lỗi", "Vui lòng chọn dòng cần sửa")
            return

        index = row_data[0][0]
        data = self.movie_value.to_dict()
        self.data, self.total_pages = self.csv_helper.update_data(data, index, self.current_page)
        self.sheet.set_sheet_data(self.data.values.tolist())
        self.update_paging_label()

    def highlight(self):
        # highlight all row if have value None, null, empty
        for i in range(len(self.data)):
            for j in range(len(self.data.columns)):
                if self.data.iloc[i, j] is None or self.data.iloc[i, j] == "":
                    self.sheet.highlight_cells(row=i, column=j, bg="red")

    def clean_data(self):
        # clean data and reload data
        percent_null = self.csv_helper.get_null_value_df()
        fig = show_null_value_chart(percent_null)

        new_window = tk.Toplevel(self.root)
        new_window.title("Null Value Chart")  # Tiêu đề cửa sổ mới

        # Tạo canvas và vẽ biểu đồ
        canvas = FigureCanvasTkAgg(fig, master=new_window)  # Sử dụng cửa sổ mới làm master
        canvas.draw()
        canvas.get_tk_widget().pack()

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
            self.sheet.set_headers(list(self.data.columns))
            self.update_paging_label()


if __name__ == "__main__":
    MainGUI()
