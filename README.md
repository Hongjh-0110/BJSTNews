# 安分守己组

#### 本文件为华为云服务器适配版，如果在IDE上运行出现问题，请尝试修改一下settings.py配置static和media路径

#### 记得改DATABASE

##### Python版本：

- Python 3.8

##### 需要下载的包：

- Django==4.2.7
- django-haystack==3.2.1
- django-simpleui==2023.12.12
- jieba==0.42.1
- Markdown==3.5
- mysqlclient==2.2.0
- Pillow==10.0.1
- Whoosh==2.7.4



#### 如果啥都不会就看下面：



### 项目部署

##### 文件解压后进入项目文件夹`BJSTNews`

##### 运行虚拟环境

> 使用Python 3.8

- 打开`Anaconda Navigator`

- 左侧的`Environments`

- 下方点击`Create`，任意命名

- 选择Python 3.8版本并确认

- 在终端中输入

  ```shell
  conda env list
  ```

  可以看到刚刚创建的环境

- 在终端中输入

  ```shell
  conda activate bjstnews # 此处为虚拟环境的名称
  ```

  此时命令行前出现虚拟环境的名称


##### 安装项目依赖环境

- 在项目根目录下，终端中输入

  ```shell
  pip install -r requirements.txt
  ```

##### 数据库迁移

- 打开`BJSTNews/settings.py`，找到`DATABASE`设置数据库

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql', # 数据库引擎
          'NAME': 'bjstnew', # 数据库名称
          'HOST': 'localhost', # 数据库地址
          'PORT': 3306, # 端口
          'USER': 'root', # 数据库用户名
          'PASSWORD': 'root', # 数据库密码
      }
  }
  ```

- 回到项目根目录，终端中输入

  ```shell
  python manage.py makemigrations
  python manage.py migrate
  ```

- 看到`OK`字样表示数据库迁移成功

##### 建立索引

- 由于含有搜索功能，重新构建索引确保搜索功能正常工作

- 终端中输入

  ```shell
  python manage.py rebuild_index
  ```

- 看到`Prefix dict has been built successfully.`表示索引重建成功

##### 项目运行

- 终端中输入

  ```shell
  python manage.py runserver
  ```

- 点击链接即可进入项目首页，其中已经填充了默认的内容，并创建了超级管理员`root`，密码为`anfenshouji`
