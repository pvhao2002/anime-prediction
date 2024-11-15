class DataCleanService:
    def __init__(self):
        self.data_clean = None

    def clean_data(self, data):
        return self.data_clean.clean_data(data)

    def get_count_null_value(self, data):
        return self.data_clean.get_count_null_value(data)