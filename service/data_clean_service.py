import pandas as pd


class DataCleanService:
    def __init__(self):
        pass

    def clean_data(self, data):
        """
           Làm sạch dữ liệu bằng cách thay thế giá trị thiếu (NaN) bằng:
           - Giá trị xuất hiện nhiều nhất (mode) cho cột kiểu chuỗi (object).
           - Giá trị trung bình (được chuyển thành số nguyên nếu cần) cho cột kiểu số.
           """
        for col in data.columns:
            if data[col].dtype == 'object':
                # Thay thế NaN bằng mode (giá trị xuất hiện nhiều nhất)
                data[col] = data[col].fillna(data[col].mode()[0])  # Đảm bảo thay đổi cột này trong DataFrame
            else:
                # Tính giá trị trung bình
                mean_value = data[col].mean()
                # Nếu cột là Int64, chuyển giá trị trung bình thành số nguyên
                if pd.api.types.is_integer_dtype(data[col].dtype):
                    mean_value = int(mean_value)
                # Thay thế NaN bằng giá trị trung bình
                data[col] = data[col].fillna(mean_value)  # Đảm bảo thay đổi cột này trong DataFrame
        return data
