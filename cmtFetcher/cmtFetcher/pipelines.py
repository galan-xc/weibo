# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import ujson
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class CmtfetcherPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def create_database(self, mysql_config):
        """创建MySQL数据库"""
        import pymysql
        sql = """CREATE DATABASE IF NOT EXISTS %s DEFAULT
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""" % settings.get(
            'MYSQL_DATABASE', 'weibo')
        db = pymysql.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute(sql)
        db.close()

    def create_table(self):
        """创建MySQL表"""
        sql = """CREATE TABLE `cmt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wid` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `comment_id` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `comment_create` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment_text` varchar(1200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_profile` varchar(600) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_verified` smallint(6) DEFAULT '0',
  `user_verified_reason` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_description` varchar(450) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `statuses_count` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
        self.cursor.execute(sql)

    def open_spider(self, spider):
        try:
            import pymysql
            mysql_config = {
                'host': settings.get('MYSQL_HOST', 'localhost'),
                'port': settings.get('MYSQL_PORT', 3306),
                'user': settings.get('MYSQL_USER', 'root'),
                'password': settings.get('MYSQL_PASSWORD', '123456'),
                'charset': 'utf8mb4'
            }
            spider.logger.info("mysql_config-> {}".format(mysql_config))
            self.create_database(mysql_config)
            mysql_config['db'] = settings.get('MYSQL_DATABASE', 'weibo')
            self.db = pymysql.connect(**mysql_config)
            self.cursor = self.db.cursor()
            self.create_table()
        except ImportError as e:
            spider.pymysql_error = True
            spider.logger.error("import error-> {}".format(e))
        except pymysql.OperationalError as e:
            spider.mysql_error = True
            spider.logger.error("OperationalError-> {}".format(e))

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = """INSERT INTO {table}({keys}) VALUES ({values})""".format(table='cmt',
                                                                         keys=keys,
                                                                         values=values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
        except Exception as e:
            spider.logger.error("process_item-> {}".format(e))
            self.db.rollback()
        return item

    def close_spider(self, spider):
        try:
            self.db.close()
        except Exception:
            pass


class AutoSendPipeline(object):
    '''
    自动将uid添加到redis 队列
    废弃！！！
    后续分析后由脚本分析后，将发送内容推送至redis
    '''
    def open_spider(self, spider):
        try:
            import redis
        except ModuleNotFoundError:
            spider.redis_error = True
        # 第一个参数是settings.py里的属性，第二个参数是获取不到值的时候的替代值
        self.redis_key = "send:msg"
        host = spider.settings.get("REDIS_HOST", "localhost")
        port = spider.settings.get("REDIS_PORT", 6379)
        db_index = spider.settings.get("REDIS_DB_INDEX", 0)
        db_psd = spider.settings.get("REDIS_PASSWORD", "")
        # 连接数据库
        self.db_conn = redis.StrictRedis(host=host, port=port, db=db_index, password=db_psd)

    def process_item(self, item, spider):
        item_dict = dict(item)
        print("*************")
        print(item_dict)
        print(type(item_dict))
        data = {
            "wid": item_dict["wid"],
            "uid": item["user_id"],
        }
        cds = ujson.dumps(data)
        self.db_conn.rpush(self.redis_key, cds)
        return item

    def close_spider(self, spider):
        # 关闭连接
        self.db_conn.connection_pool.disconnect()