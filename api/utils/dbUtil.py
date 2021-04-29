import pymysql


def get_def_mysql_db():
    db = pymysql.connect(host="127.0.0.1", user="root", password="1690036618", database="weibo", port=3306)
    return db


if __name__ == "__main__":
    with get_def_mysql_db() as db:
        print(db)
