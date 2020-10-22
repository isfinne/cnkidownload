from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import tkinter
import tkinter.messagebox
from tkinter.filedialog import askopenfilename

driver = webdriver.Chrome()
root = tkinter.Tk()
root.withdraw()  # ****实现主窗口隐藏

def get_url(name):
    site = 'https://chn.oversea.cnki.net/kns/DefaultResult/Index?dbcode=SCDB&kw=&korder=TI'
    driver.get(site)
    blank_ISSN = driver.find_element_by_class_name('search-input')
    blank_ISSN.send_keys(name)
    button_search = driver.find_element_by_class_name('search-btn')  # 找到搜索按钮
    button_search.click()  # 点击搜索
    time.sleep(2)  # 停一小会儿
    driver.switch_to.default_content()  # 找到子页面
    try:
        order = driver.find_element_by_css_selector('#orderList > li:nth-child(1)')  # 按相关度排序按钮
    except:
        return ""  # 搜索不到论文
    order.click()
    time.sleep(2)
    driver.switch_to.default_content()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for i in soup.find_all('tr'):
        paper = str(i)
        re_title = re.findall(r'Mark">.*</font>', paper)
        if re_title:
            tittle = re_title[0].strip('Mark">').strip('</font>')
            if tittle == name:
                match = re.findall(r'icon-download" href=".*;', paper)
                try:
                    download_url = 'https://chn.oversea.cnki.net/' + match[0].strip('icon-download" href="').strip(';')
                except IndexError:
                    tkinter.messagebox.showinfo('提示', '未连接到校园网，无法下载！')
                    driver.quit()
                    raise
                else:
                    return download_url
    return ""


def main():
    tkinter.messagebox.showinfo('提示', '请选择包含文章名的txt文件')
    address = askopenfilename()
    file = open(address, 'r', encoding='UTF-8')
    for line in file.readlines():
        name = re.search(r',[^,.]*\.', line).group(0).strip(',').strip('.').strip()
        url = get_url(name)
        if url == '':
            with open('unread.txt', "a") as f:
                f.write(line)
        else:
            driver.get(url)

    file.close()
    driver.close()


if __name__ == '__main__':
    main()
