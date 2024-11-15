import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

class StandardScalerService:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def scale(self, data):
        df = data.copy()

        for column in df.select_dtypes(include=['object']).columns:
            df[column] = self.label_encoder.fit_transform(df[column].astype(str))

        # Chuẩn hóa dữ liệu
        df_scaled = self.scaler.fit_transform(df)

        # Chuyển kết quả từ numpy array thành DataFrame
        df_scaled = pd.DataFrame(df_scaled, columns=data.columns)

        return df_scaled
