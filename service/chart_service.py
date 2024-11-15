import matplotlib.pyplot as plt


def show_null_value_chart(data):
    # Get the column names and null counts
    column_name = data.index
    count_null = data.values

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(column_name, count_null, color='skyblue')
    ax.set_xlabel('Số dòng null')
    ax.set_title('Số dòng null của mỗi cột')
    ax.invert_yaxis()

    return fig
