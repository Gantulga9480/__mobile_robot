from mqtt_base import PahoMqtt


class Mqtt(PahoMqtt):

    def __init__(self, broker, info, port=1883,
                 raw_msg=False, c_msg="", d_msg=""):
        super().__init__(broker, info, port=port, raw_msg=raw_msg,
                         c_msg=c_msg, d_msg=d_msg)
        self.run = True
        self.msg = ''

    def stream_init(self, path):
        pass

    def stream_stop(self):
        pass

    def _on_connect(self, client, userdata, level, buf):
        print(f"{self.info} connected")
        self.publish(topic='robot/motor_cmd', msg=f'{self.info} connected')

    def _on_message(self, client, userdata, msg):
        msg = msg.payload.decode('utf-8')
        print(msg)
        self.msg = msg