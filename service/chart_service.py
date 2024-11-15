import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def show_null_value_chart(data):
    # Get the column names and null counts
    column_name = data.index
    count_null = data.values

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(column_name, count_null, color='skyblue')
    ax.set_xlabel('Số dòng null')
    ax.set_title('Số dòng null của mỗi cột')
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


def show_histogram_chart(data):
    all_columns = data.columns  # Lấy tất cả các cột từ dataframe

    # Tính toán số hàng và cột cho layout dựa trên số lượng biến
    num_rows = int(np.ceil(len(all_columns) / 2))  # Làm tròn lên số hàng
    num_cols = 2  # Giữ nguyên 2 cột

    # Thiết lập kích thước biểu đồ và dpi (dots per inch)
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 20), dpi=100)

    # Vẽ biểu đồ histograms cho tất cả các biến, sử dụng axes đã tạo
    for i, col in enumerate(all_columns):
        row = i // num_cols  # Tính toán hàng dựa trên index
        col_num = i % num_cols  # Tính toán cột dựa trên index
        data[col].hist(ax=axes[row, col_num], bins=10)  # Vẽ trên subplot tương ứng
        axes[row, col_num].set_title(col, fontsize=12)  # Đặt tiêu đề cho subplot, điều chỉnh fontsize
        axes[row, col_num].set_xlabel(col, fontsize=10)  # Đặt nhãn trục x, điều chỉnh fontsize
        axes[row, col_num].set_ylabel("Frequency", fontsize=10)  # Đặt nhãn trục y, điều chỉnh fontsize

    return fig


def show_chart_distribute_episodes(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    data['Episodes'].dropna().plot(kind='hist', bins=20, edgecolor='black', ax=ax)
    ax.set_title('Phân bố số tập phim')
    ax.set_xlabel('Số tập phim')
    ax.set_ylabel('Số lượng anime')
    fig.tight_layout()
    return fig


def show_chart_top10_by_rating(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    top_rated_anime = data.nlargest(10, 'Rating')[['Name', 'Rating']]
    ax.barh(top_rated_anime['Name'], top_rated_anime['Rating'], color='skyblue')
    ax.set_title('Top 10 Anime Theo Rating')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Tên Anime')
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


def show_chart_top10_studio(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    top_studios = data['Studio'].value_counts().head(10)
    top_studios.plot(kind='bar', color='salmon', edgecolor='black')
    ax.set_title('Số lượng anime theo Studio (Top 10 Studio)')
    ax.set_xlabel('Studio')
    ax.set_ylabel('Số lượng anime')
    fig.tight_layout()
    return fig


def show_chart_release_year(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    data['Release_year'].dropna().astype(int).value_counts().sort_index().plot(kind='line', marker='o')
    ax.set_title('Số lượng anime theo năm phát hành')
    ax.set_xlabel('Năm phát hành')
    ax.set_ylabel('Số lượng anime')
    fig.tight_layout()
    return fig


def show_chart_scale_chart(before_data, after_data):
    # Tạo Figure và hai trục
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))  # 1 hàng, 2 cột
    # Biểu đồ trước khi xử lý outlier
    sns.histplot(before_data['Release_year'], kde=True, element="step", ax=axes[0])
    axes[0].set_title('Trước khi scale', fontsize=14)
    axes[0].set_title('Trước khi scale Release_year')
    axes[0].set_xlabel('Năm phát hành')

    sns.histplot(before_data['Release_year'], kde=True, element="step", ax=axes[1])
    axes[1].set_title('Trước khi scale', fontsize=14)
    axes[1].set_title('Trước khi scale Release_year')
    axes[1].set_xlabel('Năm phát hành')

    fig.tight_layout()
    return fig

