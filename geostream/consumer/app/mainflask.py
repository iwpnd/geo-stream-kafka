from flask import Flask
from flask import Response
from flask_cors import CORS
from flask_cors import cross_origin
from pykafka import KafkaClient


def get_kafka_client():
    return KafkaClient(hosts="127.0.0.1:9092")


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


# Consumer API
@app.route("/consumer/<topicname>")
@cross_origin()
def get_messages(topicname):
    client = get_kafka_client()

    def events():
        for i in client.topics[topicname].get_simple_consumer():
            yield "data:{0}\n\n".format(i.value.decode())

    return Response(events(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
