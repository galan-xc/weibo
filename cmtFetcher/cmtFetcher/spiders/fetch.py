import ujson
import warnings

from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str

from cmtFetcher.items import CmtfetcherItem


class FetchSpider(RedisSpider):
    name = 'fetch'
    allowed_domains = ['weibo.cm']
    redis_key = "cmt:start_urls"
    cookie_list = []

    def make_request_from_data(self, data):
        """Returns a Request instance from data coming from Redis.

        By default, ``data`` is an encoded URL. You can override this method to
        provide your own message decoding.

        Parameters
        ----------
        data : bytes
            Message from redis.

        """
        self.logger.debug("recv data-> {}({})".format(data, type(data)))
        data = ujson.loads(bytes_to_str(data, self.redis_encoding))
        self.logger.debug("trans data-> {}({})".format(data, type(data)))
        url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(data["id"], data["id"])
        if data["comments_count"] > 0:
            return self.make_requests_from_url(url, data)

    def make_requests_from_url(self, url, data):
        return Request(url, meta=data, dont_filter=True)

    def parse(self, response):
        rsp_date = ujson.loads(response.body)
        rsp_meta = response.meta
        # self.logger.debug("parse:rsp_date-> {}".format(rsp_date))
        # self.logger.debug("parse:response.meta-> {}".format(response.meta))
        if rsp_date["ok"] != 1:
            return

        if "data" in rsp_date["data"]:
            for ctitm in rsp_date["data"]["data"]:
                # self.logger.debug("ctitm-> {}".format(ctitm))
                item = CmtfetcherItem()
                item["wid"] = response.meta["id"]
                item["comment_id"] = ctitm["id"]
                item["comment_create"] = ctitm["created_at"]
                item["comment_text"] = ctitm["text"]
                item["user_name"] = ctitm["user"]["screen_name"]
                item["user_id"] = ctitm["user"]["id"]
                item["user_profile"] = ctitm["user"]["profile_url"]
                item["user_verified"] = ctitm["user"]["verified"]
                item["user_verified_reason"] = ctitm["user"].get("verified_reason", "")
                item["user_description"] = ctitm["user"]["description"]
                yield Request(
                    "https://m.weibo.cn/profile/info?uid={}".format(ctitm["user"]["id"]),
                    meta={
                        "item": item
                    },
                    callback=self.more_info,
                    dont_filter=True,
                )
            max_id = rsp_date["data"].get("max_id", "0")
            if int(max_id) > 0:
                url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0".format(
                    response.meta["id"], response.meta["id"], max_id)
                yield Request(
                    url,
                    meta={
                        'id': response.meta["id"],
                    },
                    callback=self.parse)

    def more_info(self, response):
        # self.logger.debug("parse:response.body: {}".format(response.body))
        rsp_data = ujson.loads(response.body)
        rsp_meta = response.meta
        item = rsp_meta["item"]
        is_ok = rsp_data.get("ok", -1)
        if is_ok != 1 or "data" not in rsp_data:
            return
        statuses = rsp_data["data"].get("statuses")
        user = rsp_data["data"].get("user")
        item["source"] = ""
        item["gender"] = "x"
        item["statuses_count"] = -1
        if statuses and len(statuses) > 0:
            item["source"] = statuses[0].get("source", "")
        if user:
            item["gender"] = user.get("gender", "x")
            item["statuses_count"] = user.get("statuses_count", -1)

        yield item
