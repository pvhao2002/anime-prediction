from tkinter import messagebox

from tksheet import Sheet

from service.collection_service import CollectionService


class CollectionGUI:
    def __init__(self, root, data, geo):
        self.selected_row_index = None
        self.sheet = None
        self.data = data
        self.root = root
        self.setup_gui(geo)
        self.service = CollectionService()

    def setup_gui(self, geo):
        # Tạo giao diện cơ bản
        self.root.title("Bộ sưu tập")
        self.root.geometry(geo)
        self.root.rowconfigure(0, weight=1)  # Cấu hình dòng đầu tiên mở rộng
        self.root.columnconfigure(0, weight=1)  # Cấu hình cột đầu tiên mở rộng
        self.sheet = Sheet(self.root, data=self.data.values.tolist(),
                           headers=list(self.data.columns), header_bg="blue",
                           selected_rows_to_end_of_window=True,
                           header_fg="white")
        self.sheet.enable_bindings("single_select",
                                   "drag_select",
                                   "select_all",
                                   "column_select",
                                   "row_select",
                                   "column_width_resize",
                                   "double_click_column_resize",
                                   "arrowkeys",
                                   "row_height_resize",
                                   "double_click_row_resize",
                                   "right_click_popup_menu",
                                   "rc_select")
        self.sheet.grid(row=0, column=0, sticky="nsew")
        self.sheet.popup_menu_add_command("Xóa khỏi bộ sưu tập", self.remove_collection, table_menu=False,
                                          header_menu=False, empty_space_menu=False)

    def remove_collection(self):
        selected_row = self.sheet.get_currently_selected()
        if selected_row:
            result = self.service.delete_data(selected_row[0])
            messagebox.showinfo('Thành công', 'Thành công')
            self.sheet.set_sheet_data(self.service.get().values.tolist())
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn dòng cần xóa")
