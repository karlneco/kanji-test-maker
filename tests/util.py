import pytest
def login(client,username,password):
    return client.post('/',data=dict(username=username,password=password), follow_redirects=True)

def logout(client):
    return client.get('/users/logout',follow_redirects=True)
