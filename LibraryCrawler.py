import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def formatText(htmlText):
    newStr=''
    sign=0
    for c in htmlText:
        if sign==1:
            if c=='>':
                sign=0
            continue
        if c=='<':
            sign=1
            continue
        # 存入newStr
        newStr += c
    return newStr

waitPath='waitTime'
unPath='username'
pdPath='password'
drvPath='driverPath'

# username=''
# password=''
# waittime=''
with open("./config.txt", "r", encoding='utf8') as file:
    line = file.readline()
    while line:
        line=line.strip()  # 去除行尾的换行符
        if(line.startswith(unPath)):
            username=line[9:]
        elif(line.startswith(pdPath)):
            password=line[9:]
        elif(line.startswith(waitPath)):
            waitTime=int(line[9:])
        elif(line.startswith(drvPath)):
            driverPath=line[11:]
        line = file.readline()

# 填写chromedriver的目录
# 'D:/Code/python/workspace/selenium/chromedriver-win64/chromedriver.exe'
#service = Service(driverPath)
# 不自动关闭浏览器
option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--disable-gpu')
option.add_experimental_option("detach", True)
# driver = webdriver.Chrome(service=service/options=option)
driver=webdriver.Remote(command_executor="http://192.168.2.23:4444/wd/hub",options=driver_options)


driver.get('https://booking.lib.zju.edu.cn/h5/index.html#/SeatScreening/1')


# 隐式等待
driver.implicitly_wait(waitTime)
try:
    # 以form_group的存在为监测点
    driver.find_element(By.CLASS_NAME,'form-group')
except Exception as e:
    print(f'[ERROR] 连接登录界面超时，请检查网络环境或在配置文件中将轮询等待时间{waitPath}调至更长')
    exit()
driver.implicitly_wait(waitTime)
try:
    driver.find_element(By.ID,'username')
except Exception as e:
    print('[ERROR] 连接登录界面超时，请检查网络环境或在配置文件中将轮询等待时间{waitPath}调至更长')
    exit()
#输入用户名密码登录
driver.find_element(By.ID,'username').send_keys(username)
pdInput = driver.find_element(By.ID,'password')
pdInput.send_keys(password)
pdInput.send_keys(Keys.RETURN)
# 获取座位信息
driver.implicitly_wait(waitTime)
try:
    htmllist=driver.find_elements(By.CLASS_NAME,'seatNum')
except Exception as e:
    print('[ERROR] 连接座位获取界面超时，请检查网络环境或在配置文件中将轮询等待时间{waitPath}调至更长')
    exit()
# 防未加载
time.sleep(waitTime)
# <div data-v-a6e3d86e="" class="seatNum"><span data-v-a6e3d86e="">座位 48</span><span data-v-a6e3d86e="">空闲 <b data-v-a6e3d86e="">0</b></span></div>
# 存入 ./data/时间.txt下
localTime = time.strftime("%Y-%m-%d %H_%M_%S %a", time.localtime())
filePath = "./data/"+localTime+".txt"
saveFile = open(filePath,mode='x',encoding='utf8')
# 遍历
for html in htmllist:
    text = formatText(html.text)
    saveFile.write(text+'\n')
# flush buffer to file
saveFile.flush()
saveFile.close()

# close browser
driver.quit()
