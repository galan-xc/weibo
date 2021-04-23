# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class WeibosenderPipeline:
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
        sql = """CREATE TABLE `send` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `msg` varchar(800) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ret` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
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
            self.create_database(mysql_config)
            mysql_config['db'] = settings.get('MYSQL_DATABASE', 'weibo')
            self.db = pymysql.connect(**mysql_config)
            self.cursor = self.db.cursor()
            self.create_table()
        except ImportError:
            spider.pymysql_error = True
        except pymysql.OperationalError as e:
            spider.logger.error("pymysql.OperationalError-> {}".format(e))
            spider.mysql_error = True

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = """INSERT INTO {table}({keys}) VALUES ({values})""".format(table='send',
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
        except Exception as e:
            spider.logger.error("close_spider-> {}".format(e))
            pass
