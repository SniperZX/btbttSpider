from multiprocessing import Pool
from channel_extact  import channel_list
from pages_parsing   import get_links_from
from pages_parsing import get_item_info
import pymongo


client = pymongo.MongoClient('localhost', 27017)
ceshi = client['ceshi']
url_list = ceshi['url_list']


def get_all_links_from(channel):
    for i in range(1051,2000):
        get_links_from(channel,i)





if __name__ == '__main__':
    pool = Pool()
    # pool = Pool(processes=6)
    # pool.map(get_all_links_from,channel_list.split())
    list = url_list.find({},{'url': 1})
    # for i in list:
    #     get_item_info(i)
    pool.map(get_item_info,list)

