import requests
from lxml import etree
import datetime
import js2py
import json


class ahnu:
    __mainUrl = 'https://ids.ahnu.edu.cn/authserver/login?service=https%3A%2F%2Fahnu.campusphere.net%2Fiap%2FloginSuccess%3FsessionToken%3D47d427053a574a0b9b27262412b8949e%23%2Fmanagement'
    __execution = ''
    __aeskey = ''
    __headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://ids.ahnu.edu.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://ids.ahnu.edu.cn/authserver/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def __init__(self):
        self.__session = requests.Session()
        self.__session.headers = self.__headers
        response = self.__session.get(url=self.__mainUrl)
        tree = etree.HTML(response.text)
        self.__execution = tree.xpath('//*[@id="execution"]/@value')[0]
        self.__aeskey = tree.xpath('//*[@id="pwdEncryptSalt"]/@value')[0]

    def getCaptcha(self, username):
        timestamp = int(datetime.datetime.now().timestamp())
        url = f"https://ids.ahnu.edu.cn/authserver/checkNeedCaptcha.htl?username={username}&_={timestamp}"
        response = self.__session.get(url=url)
        isneed = json.loads(response.text)
        if not isneed['isNeed']:
            return False
        capurl = f"https://ids.ahnu.edu.cn/authserver/getCaptcha.htl?{timestamp}"
        ans = self.__session.get(url=capurl).content
        with open("pic/captcha.png", "wb") as f:
            f.write(ans)
        return True

    def login(self, username, password, captcha):
        with open("encrypt.js", "r", encoding='UTF-8') as f:
            js_code = f.read()
        context = js2py.EvalJs()
        context.execute(js_code)
        password = context.encryptPassword(password, self.__aeskey)  # 调用js加密密码
        data = dict()
        data['username'] = username
        data['password'] = password
        data['captcha'] = captcha
        # data['rememberMe'] = 'true'
        data['_eventId'] = 'submit'
        data['cllt'] = 'userNameLogin'
        data['dllt'] = 'generalLogin'
        data['lt'] = ''
        data['execution'] = self.__execution
        response = self.__session.post(url=self.__mainUrl, data=data)
        if '<span id="showErrorTip"><span>验证码错误</span></span>' in response.text:
            return '验证码错误'
        if '<span id="showErrorTip"><span>您提供的用户名或者密码有误</span></span>' in response.text:
            return '账号密码错误'
        return '登录成功'

    def openCat(self):
        url = ('https://ahnu.campusphere.net/wec-counselor-apps/counselor/index.html?uagRedirectTrans=1&code'
               '=mxxQa0nQqvDbRne4raN71662022008&state=counsellor')
        self.__session.get(url=url)
        # url = 'https://ahnu.campusphere.net/wec-counselor-extend-apps/homepage/index.html'
        # self.__session.get(url=url)
        # for x in self.__session.cookies:
        #     print(x.name + ' : ' + x.value)

    def __makeStuList(self, data, num):
        ans = []
        for i in range(num):
            temp = data['datas']['rows'][i]
            namet = temp['name']
            numt = temp['userId']
            anst = dict()
            anst['name'] = namet
            anst['num'] = numt
            ans.append(anst)
        return ans

    def getStudent(self):
        json_data = {
            'pageSize': 50,
            'pageNumber': 1,
            'grade': '',
            'deptName': '计算机与信息学院',
            'majorWid': '78330',
            'classWid': '1058863',
            'wid': '149392',
            'content': '',
            'sex': '',
            'isHandled': 0,
            'isRead': -1,
            'sortColumn': '',
            'instanceWid': '',
        }
        cookies = {
            'SECKEY_ABVK': 'p076bzYj2qnAOBPFdHqz1jZ0XoCPckbURrfSICPQAtE%3D',
            'BMAP_SECKEY': '38elzjmy_IdeeXn0_Z5MzKxHcQJl9cUepzNvKvu8P-0PCk1ndeQ502b-6Rc2shLhyU0rRghNppC1rBd1s6WGbhByb4sd1rwfC1KmDaVpsu9IBtkbLHaYMNmH75vkdCtS2qEp0eIIEndjpjJOi12E2IhgvlyifgFqgHmHcXvT65Is9uP2ogAXyCWmArojfOZu'
        }
        for x in self.__session.cookies:
            if x.name == 'HWWAFSESID':
                cookies[x.name] = x.value
            if x.name == 'HWWAFSESTIME':
                cookies[x.name] = x.value
            if x.name == 'MOD_AUTH_CAS':
                cookies[x.name] = x.value
        url = 'https://ahnu.campusphere.net/wec-counselor-collector-apps/collector/teacher/queryLoopDailyDetailDate'  # get instanceWid
        response = requests.post(url=url, cookies=cookies, json={'taskWid' : "149392"})
        data = json.loads(response.text)
        json_data['instanceWid'] = data['datas']['rows'][0]['instanceWid']
        url = 'https://ahnu.campusphere.net/wec-counselor-collector-apps/collector/notice/queryAllTarget'
        response = requests.post(url=url, cookies=cookies, json=json_data)
        json_ans = json.loads(response.text)
        num_student = json_ans['datas']['unHandledSize']
        if num_student <= 50:
            un_ok_student = self.__makeStuList(json_ans, num_student)
        else:
            un_ok_student = self.__makeStuList(json_ans, 50)
            json_data['pageNumber'] = 2
            url = 'https://ahnu.campusphere.net/wec-counselor-collector-apps/collector/notice/queryAllTarget'
            response = requests.post(url=url, cookies=cookies, json=json_data)
            json_ans = json.loads(response.text)
            un_ok_student.extend(self.__makeStuList(json_ans, num_student-50))
        return un_ok_student

    def isOline(self):
        url = 'https://ahnu.campusphere.net/wec-counselor-extend-apps/homepage/index.html'
        response = self.__session.get(url=url)
        if '辅导猫' in response.text:
            return True
        return False

