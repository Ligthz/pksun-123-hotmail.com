from django.urls import path, re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from mysite.core.consumers import MQTTConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    #re_path(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer),
                    re_path(r"^MQTT/", MQTTConsumer),
                    re_path(r"", MQTTConsumer),
                ]
            )
        )
    )
})