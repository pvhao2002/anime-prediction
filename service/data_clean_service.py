class DataCleanService:
    def __init__(self):
        self.data_clean = None

    def clean_data(self, data):
        # tien hanh lam sach du lieu bang cach thay bang gia tri trung binh hoac gia tri xuat hien nhieu nhat
        for col in data.columns:
            if data[col].dtype == 'object':
                data[col].fillna(data[col].mode()[0], inplace=True)
            else:
                data[col].fillna(data[col].mean(), inplace=True)
        return data


    def get_count_null_value(self, data):
        return self.data_clean.get_count_null_value(data)
