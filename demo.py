import pandas as pd
import os
from functools import wraps
import numpy as np
from matplotlib import pyplot as plt

class CSVDataProcess:
    def __init__(self, csv_file=None, output=None):
        self.csv_file = csv_file
        self.csv = pd.read_csv(self.csv_file)
        self.output = output
        if os.path.exists(self.output):
            os.remove(self.output)
    
    def get_header_types(self):
        types = self.csv.dtypes
        print(types)

    def split_func_A(self):
        # 分组
        g = self.csv.groupby("Country_Region")
        # 按列聚合
        col_list = ["Confirmed", "Deaths", "Recovered", "Active"]
        data = g[col_list].sum()
        # 按某列倒序取top10
        data = data.sort_values("Confirmed", ascending=False)[:10]
        # 还原数字index
        data.reset_index(inplace=True)
        data.to_csv(self.output)

    def split_func_B(self):
        # 按某个标准的bool过滤(dataframe格式)
        cond = self.csv["Country_Region"]=='US'
        data = self.csv[cond]

        # 按照数字范围过滤
        # cond = (self.csv["Deaths"] > 1000 ) | (self.csv["Deaths"] < 500)
        # data = self.csv[cond]

        # 按照字符串过滤
        # cond = self.csv["Country_Region"].str.contains("Bangladesh")
        # data = self.csv[cond]
        
        data.reset_index(inplace=True, drop=True)
        data.to_csv(self.output)

    def split_func_C(self):
        # 列运算操作
        data = self.csv
        new_col = data["Deaths"] / data["Confirmed"]
        # 插入首尾列
        # data.insert(0, "xxx", new_col)
        data["Death_Rate"] = new_col
        # 取行index
        n = data.columns.tolist().index("Confirmed")
        # 取列index
        n = data["Country_Region"].tolist().index("Germany")
        # 取值（Series）
        data.iloc[:,1]
        data.loc[:,"FIPS"]
        data.iloc[1,[3,4]]
        data.iloc[[3,4],4]
        # count某列的数据出现的次数（series）
        data.value_counts("Country_Region", ascending=True)

        # 保留某列重定向文件
        data.to_csv(self.output, index=0, columns=["Country_Region", "Confirmed", "Deaths", "Death_Rate"])

    def plt_plot_func(self):
        data = self.csv
        data = data.groupby("Country_Region")
        data = data[["Confirmed", "Deaths", "Recovered", "Active"]].sum()

        cond = data["Deaths"] > 100000
        data = data[cond]

        data = data.reset_index()

        x = data["Country_Region"]
        plt.figure(figsize=(20,10), dpi=80)
        plt.plot(x, data["Confirmed"], marker='o', color="green", label="Confirmed")
        plt.plot(x, data["Deaths"], marker='o', color="blue", label="Deaths")
        plt.plot(x, data["Recovered"], marker='o', color="black", label="Recovered")
        plt.plot(x, data["Active"], marker='o', color="red", label="Active")

        plt.grid(alpha=0.3)
        plt.xticks(rotation=90)
        plt.legend(loc="upper right")  # 防止label和图像重合显示不出来
        plt.show()

    def plt_bar_func(self):
        data = self.csv
        data = data[data["Country_Region"] == "Germany"]
        x = data["Province_State"]
    
        offset = np.arange(len(x))
        limit = 0.13
        width = 0.12


        plt.figure(figsize=(20,10), dpi=80)

        plt.bar(offset, data["Confirmed"], color="blue", label="Confirmed", width=width, alpha=0.6)
        plt.bar(offset + limit, data["Deaths"], color="red", label="Deaths", tick_label=x, width=width, alpha=0.6)
        plt.bar(offset + limit * 2, data["Recovered"], color='green', label="Recovered", width=width, alpha=0.6)
        plt.bar(offset + limit * 3, data["Active"], color="purple", label="Active", width=width, alpha=0.6)

        plt.xticks(rotation=90)
        plt.legend(loc="upper right")  # 防止label和图像重合显示不出来
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.show()

    def example_A(self):
        """
          分组， 聚合， 恢复index， 添加列，取部分数据， 条件过滤， 导表
        """

        data = self.csv.groupby("Country_Region")

        col_list = ["Confirmed", "Deaths", "Recovered", "Active"]
        data = data[col_list].sum()

        data.reset_index(inplace=True)

        data["Death_Rate"] = data["Deaths"] / data["Confirmed"]

        data = data[["Country_Region", "Confirmed", "Deaths", "Death_Rate"]]

        cond = data["Death_Rate"] > 0.1
        data = data[cond]
        
        data.to_csv(self.output)

    def example_B(self):
        pass
    
    def __call__(self, exmaple):
        try:
            target_func = getattr(self, exmaple)
            target_func()
        except Exception as e:
            print("execute error", e)

if __name__ == "__main__":
    csv = r'E:\document\12-19-2020.csv'
    output = r'C:\Users\Administrator\Desktop\data.csv'

    csv = CSVDataProcess(csv, output)
    csv("plt_plot_func")




