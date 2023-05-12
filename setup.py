from setuptools import find_packages, setup
# 输入python setup.py install 安装必要包
# 输入[pip install -e .] 安装到本地，[flask --app kgweb run] 到处可运行
setup(
    name='kgweb',
    version='1.0.0',
    author="Nodota",
    author_email="nbdota01@outlook.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
)