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
# service = Service("chromedriver")
# 不自动关闭浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # 无头模式，可不启用界面显示运行
chrome_options.add_argument('--disable-gpu') # 禁用GPU加速
chrome_options.add_argument('--start-maximized')#浏览器最大化
chrome_options.add_argument('--window-size=1280x1024') # 设置浏览器分辨率（窗口大小）
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('--user-agent=""') # 设置请求头的User-Agent
chrome_options.add_argument('--disable-infobars') # 禁用浏览器正在被自动化程序控制的提示
chrome_options.add_argument('--incognito') # 隐身模式（无痕模式）
chrome_options.add_argument('--hide-scrollbars') # 隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('--disable-javascript') # 禁用javascript
chrome_options.add_argument('--blink-settings=imagesEnabled=false') # 不加载图片, 提升速度
chrome_options.add_argument('--ignore-certificate-errors') # 禁用扩展插件并实现窗口最大化
chrome_options.add_argument('-disable-software-rasterizer')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--no-sandbox')  #以最高权限运行
chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=service,options=option)
driver = webdriver.Chrome(options=chrome_options)
# driver=webdriver.Remote(command_executor="http://localhost:4444/wd/hub",options=option)


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
print("Crawler Successfully!")