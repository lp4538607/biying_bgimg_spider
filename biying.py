# -*- coding: utf-8 -*-
# 每天定时抓取bing搜索的壁纸并保存到本地
# 1。分析bing搜索的页面结构
# 2. 分析bing搜索的壁纸接口
# 3. 根据分析结果编码实现壁纸爬虫

# 技术：http组件：urllib； json解析； 文件操作； 生成时间戳

#面向对象写法，设计python爬虫类
#"startdate":"20180820","fullstartdate":"201808201600","enddate":"20180821",
# "url":"/az/hprichbg/rb/ChrisFabregas_ZH-CN11030716797_1920x1080.jpg",
# "urlbase":"/az/hprichbg/rb/ChrisFabregas_ZH-CN11030716797",
# "copyright":"加利福尼亚州的圣莫尼卡码头 (© Chris Fabregas)",
# "copyrightlink":"/search?q=%e5%9c%a3%e8%8e%ab%e5%b0%bc%e5%8d%a1%e7%a0%
# 81%e5%a4%b4&form=hpcapt&mkt=zh-cn",
# "quiz":"/search?q=Bing+homepage+quiz&filters=WQOskey:%22HPQuiz_20180820_Chri
# sFabregas%22&FORM=HPQUIZ","wp":true,
# "hsh":"bf4f0105be5b5214700c82fc74a42b16","drk":1,"top":1,"bot":1,"hs":[]

import urllib
import urllib.request
import ssl
import time
import json
import os.path

class BingBgDownloader(object):
    _bing_interface = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=%d&nc=%d&pid=hp'
    _bing_url = 'https://cn.bing.com'
    _img_filename = '[%s%s][%s].%s'

    ssl._create_default_https_context = ssl._create_unverified_context
    # 下载壁纸图片
    def download(self, num=1, local_path='./'):
        # 容错
        if num < 1:
            num = 1
        url = self._bing_interface%(num, int( time.time() ))
        img_info = self._get_img_infos(url)
        for info in img_info:
            print(self._get_imgurl(info))
            print(self._get_img_filename(info))
            self._down_img(self._bing_url+self._get_imgurl(info), self._get_img_filename(info))

    # 从接口获取图片资源信息
    def _get_img_infos(self, url):
        request = urllib.request.urlopen(url).read()
        bgObjs = json.loads( bytes.decode(request) )
        return bgObjs['images']

    # 从接口数据得到图片文件名
    def _get_img_filename(self, img_info):
        zh_name = ''
        #find 替代index进行查找
        pos = img_info['copyright'].find('(')
        #没有英文括号时排查中文小括号（统一名称格式）
        if pos<0:
            pos = img_info['copyright'].find('（')

        if pos<0:
            zh_name = img_info['copyright']
        else :
            zh_name = img_info['copyright'][0:pos]
        #英文名
        entmp = img_info['url']
        #从后往前找 rindex
        en_name = entmp[entmp.rindex('/')+1 : entmp.rindex('_ZH')]
        #后缀
        ex_name = entmp[entmp.rindex('.')+1:len(entmp)]
        #分辨率
        pix = entmp[entmp.rindex("_")+1:entmp.rindex('.')]
        img_name = self._img_filename%( zh_name,en_name,pix,ex_name )
        return img_name

    # 得到图片资源的URL
    def _get_imgurl(self, img_info):
        return img_info['url']

    # 下载图片
    def _down_img(self, img_url, img_pathname):
        #urlopen中参数需要是完整url路径
        img_data = urllib.request.urlopen(img_url).read()
        f = open(img_pathname, 'wb')
        f.write(img_data)
        f.close()
        print('success saved image:', img_url)

if __name__ == '__main__':
    dl = BingBgDownloader()
    #下载图片数 最多为8
    dl.download(8)