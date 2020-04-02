import asyncio
import json
import datetime
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, Item
from . import my_db


class MQTTConsumer(AsyncConsumer):
    """write, show"""
    async def websocket_connect(self,event):
        print("Connected",event)
        await self.send({
            "type":"websocket.accept"
        })

    async def websocket_receive(self,event):
        print("Receive",event)
        front_text = event.get('text',None)
        print(front_text)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            operation = loaded_dict_data.get('operation')
            msg = loaded_dict_data.get('text')
            if operation == "write":
                #my_db.db_write(msg)
                message = "Write Data Success : "+msg
            elif operation == "show":
                #db_data = my_db.db_show(msg)
                message = "All data : \n"+str(msg)
            elif operation == "delete":
                #my_db.db_delete(msg)
                message = "Delete Data Success : "+str(msg)
            elif operation == "ping":
                current_time  = datetime.datetime.now()
                message = "Pong : "+str(current_time)
            else:
                message =  "Unknown response"
            myResponse = {
                    'message' : message
                }
            await self.send({
                "type":"websocket.send",
                "text":json.dumps(myResponse)
            })

    async def websocket_disconnect(self,event):
        print("Disconnected",event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    
    