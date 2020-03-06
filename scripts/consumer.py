from pykafka import KafkaClient

client = KafkaClient(hosts="127.0.0.1:9092")


def get_messages(topicname):
    def events():
        for i in client.topics[topicname].get_simple_consumer():
            yield "data:{0}\n\n".format(i.value.decode())

    return events()


for x in get_messages("geostream"):
    print(x)
