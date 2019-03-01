# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import urllib.request,time,_thread,urllib.parse
import ctypes,sys

# STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
# STD_ERROR_HANDLE = -12

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
FOREGROUND_RED = 0x0c # red.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_BLUE = 0x09 # blue.

class Ai:

    def biggest(self,a,b,c):  #获取出现次数最多的答案
         if a>b:
             maxnum = a
         else:
             maxnum = b
         if c>maxnum:
             maxnum=c
         return maxnum

    def __init__(self,issue,answer): # 注意前后各两个下划线
        self.start = time.time()
        self.issue = issue
        self.answer = answer
        self.a = 0
        self.b = 0
        self.c = 0
        self.count = 0
        # self.rate_a=0
        # self.rate_b=0
        # self.rate_c=0
        
    def gethtml(self,url):
     headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')

     opener = urllib.request.build_opener()
     opener.addheaders = [headers]
     date = opener.open(url).read()
     if "zhidao.baidu.com" in url:
        str1=date.decode('gbk').encode('utf-8').decode('utf-8')
     else:
        str1=str(date,"utf-8")
     self.count += 1
     self.a += str1.count(self.answer[0].replace('A', ''))
     self.b += str1.count(self.answer[1].replace('B', ''))
     self.c += str1.count(self.answer[2].replace('C', ''))
    #  self.rate_a += fuzz.fuzzyfinder(self.answer[0].replace('A', ''), str(str1))
    #  self.rate_b += fuzz.partial_token_set_ratio(self.answer[1].replace('B', ''), str(str1)) 
    #  self.rate_c += fuzz.partial_token_set_ratio(self.answer[2].replace('C', ''), str(str1)) 

    #  print('a {}'.format(len(fuzz.fuzzyfinder(self.answer[0].replace('A', ''), str(str1)))))
    #  print('b {}'.format(fuzz.partial_token_set_ratio(self.answer[1].replace('A', ''), str1) ))
    #  print('c {}'.format(fuzz.partial_token_set_ratio(self.answer[2].replace('A', ''), str1) ))
    def threhtml(self,url):    #开线程获得网页
        _thread.start_new_thread(self.gethtml,(url,))

    def search(self):           #要搜索的引擎
        
		 #可以自己添加搜索接口  self.threhtml(网址) 并在58行代码加一个数
         baidu = self.threhtml("https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word="+urllib.parse.quote(self.issue,encoding='gbk'))

         sousou = self.threhtml("http://wenwen.sogou.com/s/?w="+urllib.parse.quote(self.issue)+"&ch=ww.header.ssda")

         iask = self.threhtml("https://iask.sina.com.cn/search?searchWord="+urllib.parse.quote(self.issue)+"&record=1")

         so360 = self.threhtml("https://wenda.so.com/search/?q="+urllib.parse.quote(self.issue))

        #  wukong= self.threhtml("https://www.wukong.com/search/?keyword="+urllib.parse.quote(self.issue,encoding='gbk'))
        #  print('myAsk{}'.format(urllib.parse.quote(self.issue,encoding='gbk')))
    


         while 1:
           if(self.count == 4):       #这里是58行代码，如果你自己增加搜索接口(4改5)
               break

         dict = {self.a: 'A', self.b: 'B', self.c: 'C'}

         listselect = [self.a,self.b,self.c]

         print('---------------------------------')
         print(' 选项    出现次数')
         print('  A：     {}'.format(str(self.a)))
         print('  B：     {}'.format(str(self.b)))
         print('  C：     {}'.format(str(self.c)))
         print('---------------------------------')
         if self.issue:
            printRed('  推荐答案：{}{}'.format(dict[self.biggest(self.a,self.b,self.c)],'\n'))
         print('---------------------------------')
         print()
         


        #  print('---------------------------------')
        #  print(' 选项    出现次数')
        #  print('  A：     {}'.format(str(self.a)))
        #  print('  B：     {}'.format(str(self.b)))
        #  print('  C：     {}'.format(str(self.c)))
        #  print('---------------------------------')
        #  print('  推荐答案：{}'.format(dict[self.biggest(self.a,self.b,self.c)]))
        #  print('---------------------------------')
        #  print()

         end = time.time()
         print('搜索用时：{}'.format(str(end-self.start)+'秒'))

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

#红色
#red
def printRed(mess):
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()

#reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
