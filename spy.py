from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re



def connect_to_cl():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    # print(driver.title)
    return driver


def new_que(driver, times):
    for i in range(times):
        print('='*50)
        print(f'正在第 {i+1}/{times} 次进入题库')
        driver.get('https://wlkc.ouc.edu.cn/webapps/assessment/take/launch.jsp?course_assessment_id=_30548_1&course_id=_13487_1&content_id=_641343_1&step=null')


        print('开始新的提交')
        new_ti = driver.find_element_by_xpath('//*[@id="containerdiv"]/div[2]/a[3]')

        new_ti.click()  # 开始新提交，进入第一题
        time.sleep(2.5)

        print('到最后一题')
        end = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div/div/div[2]/form/div[3]/div[3]/ul/li['
                                           '1]/button[2]')
        end.click()
        time.sleep(2.5)

        print("提交")
        sub = driver.find_element_by_xpath('//*[@id="dataCollectionContainer"]/p[1]/input')
        sub.click()
        altt = driver.switch_to.alert
        altt.accept()

        driver.get('https://wlkc.ouc.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_13487_1&content_id=_641337_1&mode=reset')


def analyse_que(driver, titou='总题头.txt', tiku='总题库.txt'):
    print('正在进入题库')
    driver.get('https://wlkc.ouc.edu.cn/webapps/assessment/take/launch.jsp?course_assessment_id=_30548_1&course_id=_13487_1&content_id=_641343_1&step=null')

    print("正在拉取题目列表")
    all_q = driver.find_element_by_css_selector('#containerdiv > div.attemptNavigation > a:nth-child(2)')
    all_q.click()

    time.sleep(2)
    links = driver.find_element_by_css_selector('#containerdiv > div.columnStep.clearfix > div > table > tbody')
    links = links.find_elements_by_xpath('//a')
    lin = []

    for i in links:
        if i.text in list('1234567890'):
            lin.append(i.get_attribute('href'))

    print(f"本次共有{lin.__len__()}次考试记录")
    for kkk in lin:
        driver.get(kkk)
        ques = driver.find_element_by_css_selector('#content_listContainer')
        ques = ques.find_elements_by_class_name('details')  # 15个题
        with open(titou, 'r', encoding='utf-8') as f1:
            tt_list = f1.read()

        tt_list = eval(tt_list)
        print(f'题库中已有{tt_list.__len__()}题，本次为第 {lin.index(kkk)+1}/{lin.__len__()} 次考试')  

        for qq1 in ques:  # qq1为一个题目
            title = qq1.get_attribute('innerHTML')
            title = re.findall('<div class="vtbegenerated inlineVtbegenerated">(.*?)</div>', title, re.S)
            if 'span' in title[0]:
                title = re.findall('>(.*?)<', title[0], re.S)[0]
            else:
                title = title[0]

            answers = qq1.find_elements_by_class_name('reviewQuestionsAnswerDiv')
            an_cont = {}
            for answer in answers:
                an_cont[answer.text] = ('correctAnswerFlag' in answer.get_attribute('innerHTML'))
            # print(an_cont)
            anss = '\n'.join([i+'  '+str(an_cont[i]) for i in an_cont.keys() if i != '[未给定]']).replace('False', '')

            anss.replace('[未给定]', '')

            for_write = title + '\n' + anss + '\n\n'

            if title not in tt_list:  # 一题一题的循环写入
                tt_list.append(title)
                with open(tiku, 'a+', encoding='utf-8') as f2:
                    f2.write(for_write)

                with open(titou, 'w+', encoding='utf-8') as f1:
                    f1.write(str(tt_list))


"""
reviewQuestionsAnswerDiv 选项
vtbegenerated inlineVtbegenerated 题目（首个）

"""


if __name__ == '__main__':
    driver = connect_to_cl()
    analyse_que(driver, titou='总/真的总题头.txt', tiku='总/真的总题库.txt')
    # new_que(driver, 200)








