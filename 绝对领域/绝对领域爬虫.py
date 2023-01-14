import requests
import parsel
import os

user_page = input("请输入需要批量爬取第几页的所有相册内的图片:")
os.mkdir(f'绝对领域（第{user_page}页）')
url = f'https://www.jdlingyu.com/tuji/page/{user_page}'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
    'referer': 'https://www.jdlingyu.com/tuji'
}
html_text = requests.get(url=url, headers=headers).text
selector = parsel.Selector(html_text)  # 解析网页
title_list = selector.css('.post-info h2 a::text').getall()  # 每个相册的标题
link_list = selector.css('.post-info h2 a::attr(href)').getall()  # 每个相册的链接
for title, link in zip(title_list, link_list):
    if not os.path.exists(f'绝对领域（第{user_page}页）/{title}'):
        os.mkdir(f'绝对领域（第{user_page}页）/{title}')
    response = requests.get(url=link, headers=headers)
    html_text = response.text  # 获取网页源代码
    selector = parsel.Selector(html_text)
    photo_list = selector.css('.entry-content img::attr(src)').getall()
    print(f'---------正在下载{title}相册---------')
    for photo in photo_list:  # 获取图片链接
        photo_link = requests.get(photo, headers=headers).content  # 访问图片链接
        photo_name = photo.split('/')[-1]  # 图片名称
        with open(f'绝对领域（第{user_page}页）/{title}/{photo_name}', mode='wb')as f:
            f.write(photo_link)
            print(f'{photo_name}下载完成')