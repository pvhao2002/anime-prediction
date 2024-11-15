import pandas as pd


class CsvHelper:
    def __init__(self):
        self.data = None
        self.total_pages = None
        self.row_per_page = None
        self.data_per_page = None

    def read_csv(self, file_path, page=1):
        self.row_per_page = 30
        self.data = pd.read_csv(file_path)
        self.get_total_pages()
        self.data_per_page = self.data[(page - 1) * self.row_per_page:page * self.row_per_page]
        return self.data_per_page, self.total_pages, self.row_per_page

    def insert_data(self, data):
        self.data = self.data.append(data, ignore_index=True)
        self.data.to_csv('data/data.csv', index=False)
        return self.data_per_page, self.get_total_pages()

    def update_data(self, data, index, page=1):
        # the row need to update is index in the data_per_page list then update it row in the data list
        self.data.loc[self.data_per_page.index[index]] = data
        self.data.to_csv('data/data.csv', index=False)

        # update data_per_page list
        self.data_per_page = self.data[(page - 1) * self.row_per_page:page * self.row_per_page]
        return self.data_per_page, self.get_total_pages()

    def delete_data(self, index, page=1):
        # the row need to delete is index in the data_per_page list then delete it row in the data list
        self.data = self.data.drop(self.data_per_page.index[index])
        self.data.to_csv('data/data.csv', index=False)

        # update data_per_page list
        self.data_per_page = self.data[(page - 1) * self.row_per_page:page * self.row_per_page]
        return self.data_per_page, self.get_total_pages()

    def sort_data(self, column_name, page=1):
        self.data = self.data.sort_values(by=column_name)
        self.data_per_page = self.data[(page - 1) * self.row_per_page:page * self.row_per_page]
        return self.data_per_page

    def search_data(self, keyword, page=1):
        # Search for keyword in Name, Description, type, tags no matter the case
        data_search = self.data[self.data['Name'].str.contains(keyword, case=False) |
                                self.data['Description'].str.contains(keyword, case=False) |
                                self.data['Type'].str.contains(keyword, case=False) |
                                self.data['Tags'].str.contains(keyword, case=False)]
        self.data_per_page = data_search[(page - 1) * self.row_per_page:page * self.row_per_page]
        self.total_pages = len(data_search) // self.row_per_page + (
            1 if len(data_search) % self.row_per_page != 0 else 0)
        return self.data_per_page, self.total_pages

    def get_total_pages(self):
        self.total_pages = len(self.data) // self.row_per_page + (1 if len(self.data) % self.row_per_page != 0 else 0)
        return self.total_pages

    def get_data(self):
        return self.data.isnull().sum()

    def get_null_value_df(self):
        return self.data.isnull().sum()
