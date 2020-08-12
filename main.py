import requests
import time
import random
import hashlib
import json
import tkinter


# 将字符串用md5加密
def md5(key):
    hash = hashlib.md5()
    hash.update(key.encode())
    return hash.hexdigest()


def main(fanyi_i):
    # print(fanyi_i)
    # 处理headers
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '261',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-673730215@10.169.0.82; OUTFOX_SEARCH_USER_ID_NCOO=743231293.2018329; UM_distinctid=17393299d0c30e-0f185cd7365b32-1d231c08-1fa400-17393299d0d1a0; JSESSIONID=aaafMzDwjhHJ1hCwEXHpx; ___rl__test__cookies=1597220822100',
        'Host': 'fanyi.youdao.com' ,
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }


    # 处理fanyi_lts
    fanyi_lts = str(time.time())
    fanyi_lts = fanyi_lts.split('.')[0] + fanyi_lts.split('.')[1][0:3]
    # print(fanyi_lts)


    # 处理fanyi_salt
    # i = r + parseInt(10 * Math.random(), 10);
    fanyi_salt = str(int(fanyi_lts) + random.randint(0, 10))
    # print(fanyi_salt)


    # 处理fanyi_bv
    fanyi_bv = md5(user_agent)
    # print(fanyi_bv)


    # 处理fanyi_sign
    fanyi_sign = md5("fanyideskweb" + fanyi_i + fanyi_salt + "]BjuETDhU)zqSxf-=B#7m")
    # print(fanyi_sign)




    data = {
        'i': fanyi_i,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': fanyi_salt,
        'sign': fanyi_sign,
        'lts': fanyi_lts,
        'bv': fanyi_bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }

    r = requests.post('http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule', headers=headers, data=data)
    text = json.loads(r.content.decode())
    # print(text['errorCode'])
    entry1.delete(0, tkinter.END)
    if text['errorCode'] == 0:
        # print('%s的翻译结果为:%s' % (fanyi_i ,text['translateResult'][0][0]['tgt']))
        entry1.insert(0, text['translateResult'][0][0]['tgt'])
    else:
        # print('翻译失败')
        entry1.insert(0, '翻译失败')


if __name__ == "__main__":
    window = tkinter.Tk()
    window.title('有道翻译')
    window.geometry('300x150')
    label1 = tkinter.Label(window, text='文本:')
    label2 = tkinter.Label(window, text='结果:')
    entry = tkinter.Entry(window)
    entry1 = tkinter.Entry(window)
    entry.place(x=80, y=30)
    entry1.place(x=80, y=60)
    label2.place(x=40, y=30)
    label1.place(x=40, y=60)
    button1 = tkinter.Button(window, text='翻译', command=lambda : main(entry.get()))
    button1.place(x=75, y=90)

    window.mainloop()
