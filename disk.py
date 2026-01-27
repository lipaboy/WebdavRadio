import webdav.client as wc

def openClientSession(through_proxy: bool) -> wc.Client:
    webdav_pass = ""
    proxy_pass = ""
    options = {
            'webdav_hostname': "https://webdav.yandex.ru",
            'webdav_login':    "supermen-forever",
            'webdav_password': webdav_pass,
            'proxy_hostname':  "",
            'proxy_login':     "",
            'proxy_password':  proxy_pass
        } if through_proxy else  {
            'webdav_hostname': "https://webdav.yandex.ru",
            'webdav_login':    "supermen-forever",
            'webdav_password': webdav_pass
        }  

    client = wc.Client(options)
    return client