from bs4 import BeautifulSoup
import requests
import time
import pymongo
import json

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['ceshi']
url_list = ceshi['url_list']
item_info = ceshi['movie_detial']

home = 'http://www.btbtt.co/'
host = 'http://www.btbtt.co'
qinuhost = 'http://ogepgo3ck.bkt.clouddn.com/'


# 在最左边是在python 中对象的名称，后面的是在数据库中的名称
# spider 1
def get_links_from(channel, pages):
    # td.t 没有这个就终止
    try:

        list_view = '{}-page-{}.htm'.format(channel, str(pages))
        print(list_view)
        wb_data = requests.get(list_view, timeout=30)
        # time.sleep(1)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        tmp = soup.select('div.page a')
        if tmp[-1].text == '▶':
            for item in soup.select('td.subject a.subject_link'):
                title = item.get('title')
                url = home + item.get('href')
                from_url = list_view
                url_list.insert_one({'title': title, 'url': url, "from": from_url})
        else:
            print("nnnn")
            pass
    except Exception as e:
        print('Error:', e)





# spider 2
def get_item_info(item):
    # url = item.get('url')
    url = item
    print(url)
    try:
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        details = soup.select('td.post_td p')
        title = soup.title.text
        images = soup.select('p > img')
        imagesurl = ''
        downloadUrl = ''
        for image in images:

            print(image.get('src').find('http'))
            if image.get('src') and image.get('src').find('http') > -1:
                print(image.get('src'))
                imagesurl = qinuhost + image.get('src').split('/')[-1]
                downloadImageFile(image.get('src'))
            else:
                print(home + image.get('src'))
                imagesurl += qinuhost + image.get('src').split('/')[-1]+'\n'
                downloadImageFile(host + image.get('src'))
        attchs = soup.select('div.attachlist a')
        for attch in attchs:
            print(attch.get('href'))
            href = attch.get('href')
            href = href.replace('dialog','download')
            downloadFile(home+href,attch.get_text())
            downloadUrl += qinuhost +attch.get_text()+"\n"
            print(href)

        print(attch)
        item_info.insert_one({'title': title, 'detail': str(details), 'image': imagesurl,  'url': item, 'download':downloadUrl})
        print(title)
    except Exception as e:
        print('Error:', e)


    # no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')
    # if no_longer_exist:
    #     pass
    # else:
    #     title = soup.title.text
    #     price = soup.select('span.price.c_f50')[0].text
    #     date = soup.select('.time')[0].text
    #     area = list(soup.select('.c_25d a')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None
    #     item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})
    #     print({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})

def downloadImageFile(imgUrl):
    local_filename = imgUrl.split('/')[-1]
    print("Download Image File=", local_filename)
    print(imgUrl)
    r = requests.get(imgUrl, stream = True, timeout=30) # here we need to set stream = True parameter
    with open("H:/btbttimg/"+local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    return local_filename


def downloadFile(fileUrl,file_name):
    local_filename = file_name
    print("Download torrent File=", local_filename)
    print(fileUrl)
    r = requests.get(fileUrl, stream = True, timeout=30) # here we need to set stream = True parameter
    with open("H:/bttorrent/"+local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    return local_filename

get_item_info('http://www.btbtt.co/thread-index-fid-950-tid-4346742.htm')