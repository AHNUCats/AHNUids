import matplotlib.pyplot as plt
import matplotlib


def draw(data, filename):
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # 创建一个图形对象，并设置大小
    fig = plt.figure(figsize=(2.8, 4.7))
    # 添加一个子图，并设置位置
    ax = fig.add_subplot(111, position=[0.1, 0.1, 0.8, 0.8])

    # 绘制表格
    table = ax.table(cellText=data, loc='center', cellLoc='center')

    # 调整表格大小和位置
    table.scale(0.5, 2)
    ax.axis('off')

    # 设置表格的字体大小、列宽、边框颜色和宽度
    table.set_fontsize(14)
    table.auto_set_font_size(False)
    table.auto_set_column_width(col=list(range(len(data[0]))))
    # 设置表格的边框颜色和宽度
    table.edgecolor = 'black'
    table.linewidth = 1

    # 调整子图的位置和大小
    plt.tight_layout()

    # 保存图像到本地，文件名为pic.png，并去掉图片周围的白边
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()
