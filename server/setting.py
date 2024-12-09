from server import PromptServer
from aiohttp import web
from ..common import g_settings, clear_s3_client

@PromptServer.instance.routes.patch("/saveimages3/setting")
async def new_setting(request):
    try:
        settings = await request.json()
        if 'url' in settings is not None and 'bucket' in settings is not None \
            and 'accessKey' in settings is not None and'secretKey' in settings is not None:
            url = settings['url']
            bucket = settings['bucket']
            accessKey = settings['access']
            secretKey = settings['secret']

            if type(url) is not str:
                raise Exception('url must be string')
            if type(bucket) is not str:
                raise Exception('bucket must be string')
            if type(accessKey) is not str:
                raise Exception('accessKey must be string')
            if type(secretKey) is not str:
                raise Exception('secretKey must be string')
            
            g_settings.url = url
            g_settings.access_key = accessKey
            g_settings.secret_key = secretKey
            g_settings.bucket = bucket
            clear_s3_client()

            return web.Response(status=200)
    except Exception as e:
        return web.Response(status=400, text=str(e))
    
@PromptServer.instance.routes.patch("/saveimages3/setting/url")
async def update_url(request):
    try:
        settings = await request.json()
        if 'url' in settings is not None:
            url = settings['url']
            if type(url) is not str:
                raise Exception('url must be string')
            
            g_settings.url = url
            clear_s3_client()


            return web.Response(status=200)
    except Exception as e:
        return web.Response(status=400, text=str(e))
    

    
@PromptServer.instance.routes.patch("/saveimages3/setting/bucket")
async def update_bucket(request):
    try:
        settings = await request.json()
        if 'bucket' in settings is not None:
            bucket = settings['bucket']
            if type(bucket) is not str:
                raise Exception('bucket must be string')
            g_settings.bucket = bucket
            clear_s3_client()


            return web.Response(status=200)
    except Exception as e:
        return web.Response(status=400, text=str(e))
    

@PromptServer.instance.routes.patch("/saveimages3/setting/access")
async def update_access(request):
    try:
        settings = await request.json()
        if 'access' in settings is not None:
            accessKey = settings['access']
            if type(accessKey) is not str:
                raise Exception('bucket must be string')
            g_settings.access_key = accessKey
            clear_s3_client()

            return web.Response(status=200)
    except Exception as e:
        return web.Response(status=400, text=str(e))


@PromptServer.instance.routes.patch("/saveimages3/setting/secret")
async def update_secret(request):
    try:
        settings = await request.json()
        if 'secret' in settings is not None:
            secretKey = settings['secret']
            if type(secretKey) is not str:
                raise Exception('bucket must be string')
            g_settings.secret_key = secretKey
            clear_s3_client()

            return web.Response(status=200)
    except Exception as e:
        return web.Response(status=400, text=str(e))