import pandas as pd


class CollectionService:
    def __init__(self):
        self.file_path = './data/collection.csv'
        try:
            self.data = pd.read_csv(self.file_path)
        except pd.errors.EmptyDataError:
            self.data = pd.DataFrame()

    def insert_data(self, data):
        try:
            new_row = pd.DataFrame([data])  # Tạo DataFrame mới từ dữ liệu

            self.data = pd.concat([self.data, new_row], ignore_index=True)  # Nối dữ liệu mới vào dữ liệu cũ
            self.data.to_csv(self.file_path, index=False)
            return True
        except:
            return False

    def delete_data(self, index):
        if 0 <= index < len(self.data):
            self.data = self.data.drop(index)
            self.data.to_csv(self.file_path, index=False)
        return self.data

    def get(self):
        try:
            self.data = pd.read_csv(self.file_path)
            self.format_year_int()
        except pd.errors.EmptyDataError:
            self.data = pd.DataFrame()
        return self.data

    def format_year_int(self):
        # Duyệt qua các cột cần chuyển đổi
        for column in ['Release_year', 'End_year', "Episodes"]:
            if column in self.data.columns:
                # Chuyển sang số nguyên Pandas Int64 (cho phép NaN)
                self.data[column] = pd.to_numeric(self.data[column], errors='coerce').astype('Int64')
