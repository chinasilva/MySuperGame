import urllib.request, sys,base64,json,os,time,string,re
import subprocess
import os
import sys
from PIL import Image
from aip import AipOcr
from aitext import Ai

try:
    import configparser
except:
    from six.moves import configparser


CF = configparser.ConfigParser()
CF.read("config.conf","utf-8-sig")

Devices=CF.get("Devices", "Devices")

GAME_NAME=CF.get("GAME_NAME", "GAME_NAME")

GAME_TYPE=CF.get("GAME_TYPE", "GAME_TYPE")

APP_ID=CF.get("BD_OCR", "APP_ID")
API_KEY=CF.get("BD_OCR", "API_KEY")
SECRET_KEY=CF.get("BD_OCR", "SECRET_KEY")
API_VERSION=CF.get("BD_OCR", "API_VERSION")

IMG_TOP=CF.getint("CROP_IMG", "TOP")
IMG_LEFT=CF.getint("CROP_IMG", "LEFT")
IMG_RIGHT=CF.getint("CROP_IMG", "RIGHT")
IMG_BOTTON=CF.getint("CROP_IMG", "BOTTON")

# 芝士超人
# 西瓜视频
# 冲顶大会

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def main():
    start = time.time()
    '''
    截图方法一
    '''
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    end = time.time()
    print('截图用时：' + str(end - start) + '秒')
    os.system("adb pull /sdcard/screenshot.png .")
    end = time.time()
    print('拉图用时：' + str(end - start) + '秒')


    '''
    截图方法二
    '''
    # process = subprocess.Popen('adb shell screencap -p ',shell=True, stdout=subprocess.PIPE)
    # binary_screenshot = process.stdout.read()
    # binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
    # f = open('screencap.png', 'wb')
    # f.write(binary_screenshot)
    # f.close()
    # end = time.time()
    # print('截图用时：' + str(end - start) + '秒')
    '''
    截图方法三
    '''
    # outfile = open("screenshot.png", "wb")
    # proc = subprocess.Popen("adb shell screencap -p ", stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=True)
    # for line in proc.stdout:
    #     outfile.write(line)
    # outfile.close()
    # end = time.time()
    # print('截图用时：' + str(end - start) + '秒')

    '''
    截图方式四
    '''

    # p = subprocess.Popen('adb shell screencap -p /sdcard/screenshot.png',shell=True)
    # out, err = p.communicate()
    # end = time.time()
    # print('截图用时：' + str(end - start) + '秒')
    # p2 = subprocess.Popen('adb pull /sdcard/screenshot.png .',shell=True)
    # out, err = p2.communicate()
    # end = time.time()
    # print('拉图用时：' + str(end - start) + '秒')
    # im = Image.open(r"./screenshot.png")

    '''
    对图片进行切分
    img_size = im.size
    w = im.size[0]
    h = im.size[1]
    1010=1080-70
    '''
    # 裁剪的区域
    # if  Devices=='模拟器':
    #     if GAME_NAME=='芝士超人':
    #         region = im.crop((0, 120, 1080, 600))
    #     else :
    #         # if GAME_NAME=='西瓜视频' or GAME_NAME=='冲顶大会':
    #         region = im.crop((70, 200, 1010, 800))
    # else:
    #     region = im.crop((70, 200, 1010, 800))
    # 芝士超人
    # region = im.crop((0, 120, 1080, 600))


    # 华为手机第九题奖励金新玩法

    # if GAME_TYPE=='NEW9':
    #     region = im.crop((70, 300, 1010, 1200))
    # else:
    #     region = im.crop((70, 400, 1010, 1300))
    
    region = im.crop((IMG_LEFT, IMG_TOP, IMG_RIGHT, IMG_BOTTON))
        
    '''
    # 华为手机旧玩法
    '''
    # region = im.crop((70, 400, 1010, 1300))

    region.save(r"./cropimg.png")

    end = time.time()


    options = {}
    options["language_type"] = "CHN_ENG"
    timeout = 3
    image_data = get_file_content('./cropimg.png')
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    client.setConnectionTimeoutInMillis(timeout * 1000)
    if API_VERSION == 1:
        response = client.basicAccurate(image_data, options)
    else:
        response = client.basicGeneral(image_data, options) # 用完500次后可改 respon = client.basicAccurate(image) 这个还可用50次
    titles = response['words_result']  # 获取问题
    issue = ''
    answer = ['', '', '', '', '', '']
    countone = 0
    answercount = 0
    for title in titles:
        countone += 1
        if (countone >= len(titles) - 2):
            answer[answercount] = title['words']
            answercount += 1
        else:
            issue = issue + title['words']

    # 去掉题目索引
    if GAME_NAME=='西瓜视频' or GAME_NAME=='冲顶大会':
        tissue = issue[1:2]
        if str.isdigit(tissue):
            issue = issue[3:]
        else:
            issue = issue[2:]


    print(issue)  # 打印问题
    print('  A:' + answer[0] + ' B:' + answer[1] + ' C:' + answer[2])  # 打印答案


    keyword = issue  # 识别的问题文本

    ai = Ai(issue, answer)

    ai.search()
    #
    end = time.time()
    print('程序用时：' + str(end - start) + '秒')

""" 读取图片 """
def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()


def yes_or_no(prompt, true_value='y', false_value='n', default=True):
    """
    检查是否已经为启动程序做好了准备
    """
    default_value = true_value if default else false_value
    prompt = '{} {}/{} [{}]: '.format(prompt, true_value,
        false_value, default_value)
    i = input(prompt)
    if not i:
        return default
    while True:
        if i == true_value:
            return True
        elif i == false_value:
            return False
        prompt = 'Please input {} or {}: '.format(true_value, false_value)
        i = input(prompt)


def gameBegin():
    
   
    while True:
        op = yes_or_no('回车继续')
        print (time.time())
        if not op:
            print('bye')
            return
        main()
if __name__ == '__main__':
    gameBegin()

