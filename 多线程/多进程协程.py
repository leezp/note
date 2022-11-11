# coding:utf-8
#!/usr/bin/env python3
import aiohttp
import asyncio
import aiomultiprocess
import datetime
async def tq(code):
    data = {
        'email': '113811112202@qq.com'
        , 'name': 'co2222ee',
        'password': 'qwerzxcv',
        'passwordagain': 'qwerzxcv',
        'inviteCode': '%s' % str(code),  # (unable to decode value)
        'geetest_challenge': 'ec4384831c8cc9d799b297b49e57f72564',
        'geetest_validate': '3189a9537d4c93811389bdcb75e1811a',
        'geetest_seccode': '3189a9537d4c93811389bdcb75e1811a|jordan'

    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://bithack.io/api?userReg',data=data,ssl=False) as resp:
                res = await resp.read()
                if '邀请码错误'.encode() not in res:
                    print('正确邀请码为:{}'.format(code))
                else:
                    print(code)
    except Exception as e:
        print(e)
async def main():
    tasks = range(800, 1001)
    async with aiomultiprocess.Pool() as pool:
        result = await pool.map(tq,tasks)
    print(result)
if __name__ == '__main__':
    start = datetime.datetime.now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end = datetime.datetime.now()
    print (end - start)  #39s


