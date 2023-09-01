from fontTools.ttLib import TTFont
import requests
import re
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
}

url = "https://www.qidian.com/all/orderId11/"
response = requests.get(url=url,headers=headers)
response.encoding = 'utf-8'

# print(response.text)
html_data = response.text

#匹配字体文件下载地址
font_url = re.findall("; src: url\('(.*?)'\) format",response.text)[1]
print(font_url)


font_res = requests.get(url=font_url,headers=headers)
with open("fonts.woff",mode="wb") as f:
    f.write(font_res.content)


#
font = TTFont('fonts.woff')
font.saveXML("font.xml")

#获取字体映射关系
font_cmap = font['cmap'].getBestCmap()
print(font_cmap)

f = {'period':'.', 'four': 4, 'three': 3, 'six':6, 'zero': 0,
     'one': 1, 'eight' : 8,'seven': 7,'nine': 9,'five' : 5, 'two': 2}
#更改映射
for key in font_cmap:
    font_cmap[key] = f[font_cmap[key]]

print(font_cmap)

#替换映射
for key in font_cmap:
    html_data = html_data.replace('&#'+str(key)+';',str(font_cmap[key]))
#保存页面
with open("okkk.html","w",encoding="utf-8") as f:
    f.write(html_data)
