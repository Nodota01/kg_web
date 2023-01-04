from setuptools import find_packages, setup
# 输入[pip install -e .] 安装到本地，[flask -app kgweb run] 到处可运行
setup(
    name='kgweb',
    version='1.0.0',
    author="Nodota",
    author_email="nbdota01@outlook.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'pytest',
        'coverage',
        'pymysql',
        'flask_sqlalchemy',
        'flask_login',
        'openpyxl',
        'pandas',
        'requests',
        'bs4'
    ],
)