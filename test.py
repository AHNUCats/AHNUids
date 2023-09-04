from AHNU import ahnu
import makeChart
import os
if os.path.isdir('pic'):
    pass
else:
    path = os.path.join('./', 'pic')
    os.mkdir(path)
fudaomao = ahnu()
username = input("请输入用户名：")
password = input("请输入密码：")

captcha = ''
if fudaomao.getCaptcha(username):
    captcha = input("请输入验证码:")
ans = fudaomao.login(username, password, captcha)
print(ans)
if not ans == '登录成功':
    exit(0)
fudaomao.openCat()  # 打开辅导猫，获取cookies
# 以上是辅导猫登录代码
ans = fudaomao.getStudent()
# 生成图表 10人一张
cnt = 0
temp = 0
data = [['姓名', '学号']]
for x in ans:
    data.append([x['name'], x['num']])
    cnt += 1
    if cnt == 10:
        cnt = 0
        # print(data)
        makeChart.draw(data, f"pic/{temp}.png")
        print(f"已生成第{temp}张图")
        data = [['姓名', '学号']]
        temp += 1
    makeChart.draw(data, f"pic/{temp}.png")
print("生成完毕")

