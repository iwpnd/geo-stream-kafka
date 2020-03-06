def test_post_producer(test_app):

    msg = {"name": "AIOmessenger_ONE", "lat": 13, "lon": 37}

    topicname = "geostream"

    with test_app as client:
        response = client.post(f"/producer/{topicname}", json=msg)

    assert response.status_code == 200
