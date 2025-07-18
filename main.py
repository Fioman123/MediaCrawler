# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


import asyncio
import sys
from typing import Optional

import cmd_arg
import config
import db
from base.base_crawler import AbstractCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.tieba import TieBaCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.xhs import XiaoHongShuCrawler
from media_platform.zhihu import ZhihuCrawler

# 爬虫工厂类，根据平台名创建对应的爬虫对象
class CrawlerFactory:
    CRAWLERS = {
        "xhs": XiaoHongShuCrawler,   # 小红书
        "dy": DouYinCrawler,         # 抖音
        "ks": KuaishouCrawler,       # 快手
        "bili": BilibiliCrawler,     # 哔哩哔哩
        "wb": WeiboCrawler,          # 微博
        "tieba": TieBaCrawler,       # 贴吧
        "zhihu": ZhihuCrawler        # 知乎
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        # 根据平台名获取对应的爬虫类
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError("Invalid Media Platform Currently only supported xhs or dy or ks or bili ...")
        return crawler_class()

# 主异步函数，负责整个爬虫流程的调度
async def main():
    # 解析命令行参数，初始化配置
    await cmd_arg.parse_cmd()

    # 如果需要保存到数据库，则初始化数据库
    if config.SAVE_DATA_OPTION in ["db", "sqlite"]:
        await db.init_db()

    # 创建对应平台的爬虫对象
    crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
    # 启动爬虫主流程
    await crawler.start()

    # 爬虫结束后关闭数据库连接
    if config.SAVE_DATA_OPTION in ["db", "sqlite"]:
        await db.close()

# 程序入口
if __name__ == '__main__':
    try:
        # 启动主异步流程
        # 这里使用 asyncio.get_event_loop().run_until_complete(main()) 是为了兼容 Python 3.6/3.7 及更早版本，
        # 因为 asyncio.run() 是从 Python 3.7 开始引入的更简洁的写法。
        # get_event_loop() 会获取当前线程的事件循环，如果没有则自动创建一个，然后用 run_until_complete() 执行 main() 协程直到完成。
        # 适用于需要手动管理事件循环，或在某些老版本/嵌入式环境下无法直接用 asyncio.run() 的场景。
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
