from app import app # Flask instance of the API

def test_index_route():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert 'eat good food' in response.data.decode('utf-8')

def test_request_add():
    response = app.test_client().post("/add", data={
        "todo_item": "Test flask application",
    }, follow_redirects=True)
    assert response.status_code == 200