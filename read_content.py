import os

# 指定要读取的文件夹路径
folder_path = r"E:\大四上\python\BJSTNews\v2\BJSTNews\BJSTComments"  # 替换成你的文件夹路径

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    if file_name.endswith(".py"):  # 仅处理以.py结尾的文件
        file_path = os.path.join(folder_path, file_name)

        # 打开文件并读取其内容
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        # 将文件名和内容打印出来
        print(f"File: {file_name}")
        print("----")
        print(file_content)
        print("----")
