from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy import log
from scrapy.conf import settings


class RetryChangeProxyMiddleware(RetryMiddleware):
    '''
    use tor and polipo to change proxy
    '''

    def _retry(self, request, reason, spider):
        log.msg('Changing proxy')
        request.meta['proxy'] = settings.get('HTTP_PROXY')
        return RetryMiddleware._retry(self, request, reason, spider)


class ProxyMiddleware(object):
    ''' just for testing
    '''

    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')
