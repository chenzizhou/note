import os
import re
import winreg
import zipfile
import requests
import json
import urllib3
# 避免 InsecureRequestWarning 报错
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = 'https://mirrors.tools.huawei.com/chromedriver/.index.json'
version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本号的正则表达式
def update_json(Driver_version):
    with open(r"./index.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        target_version = Driver_version

        # 自定义函数用于比较版本号
        def compare_versions(version1, version2):
            v1_parts = version1.split(".")
            v2_parts = version2.split(".")
            min_len = min(len(v1_parts), len(v2_parts))
            for i in range(min_len):
                if int(v1_parts[i]) > int(v2_parts[i]):
                    return 1
                elif int(v1_parts[i]) < int(v2_parts[i]):
                    return -1
            if len(v1_parts) > len(v2_parts):
                return 1
            elif len(v1_parts) < len(v2_parts):
                return -1
            return 0

        # 找到与目标版本相近的版本
        closest_version = max(data["chromedriver"], key=lambda x: compare_versions(x, target_version))
    return closest_version, data["chromedriver"][closest_version]["files"][4]


def getChromeVersion():
    """通过注册表查询chrome版本"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Google\\Chrome\\BLBeacon')
        value, t = winreg.QueryValueEx(key, 'version')
        return version_re.findall(value)[0]  # 返回前3位版本号
    except WindowsError as e:
        # 没有安装chrome浏览器
        return "1.1.1"


def getChromeDriverVersion():
    """查询Chromedriver版本"""
    outstd2 = os.popen(r'.\chromedriver-win64\chromedriver.exe --version').read()
    try:
        version = outstd2.split(' ')[1]
        version = ".".join(version.split(".")[:-1])
        return version
    except Exception as e:
        return "0.0.0"


def getLatestChromeDriver(Driver_version):
    Driver_version_url = 'https://mirrors.tools.huawei.com/chromedriver/'
    """获取该chrome版本的最新driver版本号"""
    latest_version = requests.get(base_url, verify=False)
    with open('index.json', "wb") as file:
        file.write(latest_version.content)
    Chrome_Driver_version, Chrome_Driver_version_url = update_json(Driver_version)
    print(f"与当前chrome匹配的最新chromedriver版本为: {Chrome_Driver_version}")
    # 下载chromedriver
    print("开始下载chromedriver...")
    download_url = f"{Driver_version_url}{Chrome_Driver_version_url}"
    file = requests.get(download_url, verify=False)
    with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
    print("下载完成.")
    # 解压
    f = zipfile.ZipFile("chromedriver.zip", 'r')
    for file in f.namelist():
        f.extract(file)
    print("解压完成.")


def checkChromeDriverUpdate():
    chrome_version = getChromeVersion()
    print(f'当前chrome版本: {chrome_version}')
    driver_version = getChromeDriverVersion()
    print(f'当前chromedriver版本: {driver_version}')
    if chrome_version == driver_version:
        print("版本兼容，无需更新.")
        return
    print("chromedriver版本与chrome浏览器不兼容，更新中>>>")
    try:
        getLatestChromeDriver(chrome_version)
        print("chromedriver更新成功!")
    except requests.exceptions.Timeout:
        print("chromedriver下载失败，请检查网络后重试！")
    except Exception as e:
        print(f"chromedriver未知原因更新失败: {e}")



if __name__ == "__main__":
    checkChromeDriverUpdate()
    try:
        os.remove('./chromedriver.zip')
        os.remove('./index.json')
    except FileNotFoundError:
        pass
