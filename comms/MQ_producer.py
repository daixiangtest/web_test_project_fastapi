"""
MQ 生产者操作封装
"""
import json
from comms.settings import MQ_CONFIG
import pika


class MQProducer:
    """
    MQ 生产者操作封装
    """
    def __init__(self):
        # 连接到RabbitMQ服务器
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_CONFIG["host"], port=MQ_CONFIG["port"]))
        # 创建一个频道
        self.channel = self.connection.channel()
        # 声明一个队列
        self.channel.queue_declare(queue=MQ_CONFIG['queue_name'])

    def send_test_task(self,env_config, test_case):
        """
        发送测试任务
        """

        data={
            "env_config":env_config,
            "test_case":test_case
        }
        msg=json.dumps(data).encode("utf-8")
        self.channel.basic_publish(exchange='', routing_key=MQ_CONFIG['queue_name'], body=msg)

    def __del__(self):
        """
        销毁对象时断开连接
        """
        self.connection.close()

