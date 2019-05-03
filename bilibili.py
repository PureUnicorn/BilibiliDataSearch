from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time


from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def demo(myurl, max_page, endurl=""):
    # 初始化浏览器
    browser = webdriver.Chrome("E:\Source\chromedriver_win32\chromedriver.exe")

    # base_url = "https://search.bilibili.com/all?keyword=%E5%8F%A3%E7%BA%A2&from_source=banner_search&spm_id_from=333.334.b_62616e6e65725f6c696e6b.1&order=click&duration=0&tids_1=0&page={page}"
    base_url = myurl+"{page}"
    end_url = endurl
    with open("bilibili.txt","w")as f:
        for i in range(1, max_page+1):
            url = base_url.format(page=i)+end_url
            browser.get(url)
            bs4 = BeautifulSoup(browser.page_source, 'lxml')
            titles = bs4.find_all('div', {'class': 'tags'})
            for title in titles:
                title_content = title.get_text().strip('\n')
                try:
                    f.write(title_content)
                    f.write("|\n")
                except:
                    continue


def serchData(name,browser):
    # browser = webdriver.Chrome("E:\Source\chromedriver_win32\chromedriver.exe")
    # browser.get(url)
    print("开始检索%s"%name)
    pageNum = 0
    with open("data_bilibili_"+name+".txt","w")as f:
        while(True):
            time.sleep(1)
            pageNum += 1
            js = "var q=document.documentElement.scrollTop=10000"
            browser.execute_script(js)
            time.sleep(0.1)
            js = "var q=document.documentElement.scrollTop=10000"
            browser.execute_script(js)

            bs4 = BeautifulSoup(browser.page_source, 'lxml')
            # 寻找下一页按钮
            # print("bs4")

            # print("next")

            tags = bs4.find_all('div', {'class': 'tags'})
            for tag in tags:
                # print("tag",tag)
                # for x in tag:
                #     print("x",x)
                # print(tag.span.text.strip("\n").replace(" ",""),end="")
                f.write(re.sub(r"\..", "", tag.span.text.replace("万","0000").replace(" ", "").replace("亿", "00000000")))
            # 进入下一页
            try:
                next = browser.find_element_by_class_name("icon-arrowdown3").click()
                print("第%d页"%(pageNum),end=", ")
            except TimeoutException:
                browser.refresh()
                time.sleep(5)
                next = browser.find_element_by_class_name("icon-arrowdown3").click()
                print("第%d页" % (pageNum),end=", ")
            except:
                try:
                    browser.refresh()
                    time.sleep(5)
                    next = browser.find_element_by_class_name("icon-arrowdown3").click()
                except NoSuchElementException:
                    print()
                    print(name+"Complete!")
                    break
                except:
                    print("第%d页" % (pageNum),end=", ")
                    # if(not next):
                    # browser.close()
                    break


def resolve(name):
    with open("E:\\Users\\Administrator\\PycharmProjects\\bilibili_Selenuim\\data_bilibili_"+name+".txt","r")as f:
        line = f.readline()
        guankan = 0
        danmu = 0
        while(True):
            if(line =="\n"):
                line = f.readline()
                continue
            elif(line):
                list = line.split(",")
                guankan += int(list[0].replace("\n",""))
                # danmu += int(list[1].replace("\n",""))
                line = f.readline()
            else:
                break
        print("|"+str(guankan)+"|")

def controller():
    # a = ['口红品牌','口红性价比','口红润泽','冷白皮','黄皮','口红秋冬色','春夏口红','哑光口红','口红色号','香奈儿口红','圣罗兰口红','迪奥口红','tf口红','李佳琪','mac口红']
    a = ['口红秋冬色','春夏口红','哑光口红','口红色号','香奈儿口红','圣罗兰口红','迪奥口红','tf口红','李佳琪','mac口红']
    browser = webdriver.Chrome("E:\Source\chromedriver_win32\chromedriver.exe")
    browser.get("https://search.bilibili.com/all?keyword=%E5%8F%A3%E7%BA%A2%E6%80%A7%E4%BB%B7%E6%AF%94&order=pubdate&duration=0&tids_1=0")
    for key_words in a:
        time.sleep(1)
        # 置顶
        js = "var q=document.documentElement.scrollTop=0"
        browser.execute_script(js)
        time.sleep(0.1)
        js = "var q=document.documentElement.scrollTop=0"
        browser.execute_script(js)
        # 输入搜索词
        search = browser.find_element_by_id("search-keyword")
        time.sleep(0.1)
        search.send_keys(Keys.CONTROL, 'a')
        search.send_keys(Keys.BACK_SPACE)
        search.send_keys(key_words)

        time.sleep(0.1)
        browser.find_element_by_class_name("search-button").click()
        # 获取数据
        serchData(key_words, browser)

        # 统计数据
        print("%s开始统计数据"%key_words)
        resolve(key_words)
        print("%s统计结束"%key_words)

if __name__ == "__main__":
    '''
    从B站抓取数据，并统计求和
    '''
    controller()
    # demo("https://search.bilibili.com/all?keyword=%E5%8F%A3%E7%BA%A2&from_source=banner_search&spm_id_from=333.334.b_62616e6e65725f6c696e6b.1&order=click&duration=0&tids_1=0&page=", 3)
    # resolve()


    # # time(1)
    # # time(3)
    # serchData("冷白皮", browser)
