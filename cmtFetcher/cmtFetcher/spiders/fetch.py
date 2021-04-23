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
        """ This method is deprecated. """
        warnings.warn(
            "Spider.make_requests_from_url method is deprecated: "
            "it will be removed and not be called by the default "
            "Spider.start_requests method in future Scrapy releases. "
            "Please override Spider.start_requests method instead."
        )
        return Request(url, meta=data, dont_filter=True)

    def parse(self, response):
        recv_data = ujson.loads(response.body)
        self.logger.debug("recv_data-> {}".format(recv_data))
        self.logger.debug("response.meta-> {}".format(response.meta))
        if recv_data["ok"] == 1:
            if "data" in recv_data["data"]:
                for ctitm in recv_data["data"]["data"]:
                    self.logger.debug("ctitm-> {}".format(ctitm))
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
                    yield item

                max_id = recv_data["data"].get("max_id", "0")
                if int(max_id) > 0:
                    url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0".format(
                        response.meta["id"], response.meta["id"], max_id)
                    yield Request(url,
                                  meta={
                                      'id': response.meta["id"],
                                  },
                                  callback=self.parse)
            else:
                url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(
                    response.meta["id"], response.meta["id"])
                yield Request(url, meta={
                    'id': response.meta["id"],
                }, callback=self.parse, dont_filter=False)
