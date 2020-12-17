import subprocess
import datetime
import requests

# Test compatibility with requests library for various requests
def checkValidResponse(r):
    assert "connection" in r.headers
    assert r.headers["Connection"].lower() == "close"
    assert "Date" in r.headers
    date = datetime.datetime.strptime(r.headers["Date"], '%a, %d %b %Y %H:%M:%S GMT')
    assert (date - datetime.datetime.utcnow()).total_seconds() < 5

# Test an index of main folder is returned
def test_valid_get_nopath_requestslib():
    r = requests.get('http://localhost:64321/')
    checkValidResponse(r)
    assert r.status_code == 200
    assert "<a href=" in r.text # encoded as links
    assert "folder" in r.text
    assert "webserver_tests.py" in r.text
    print("Succeded: test_valid_get_nopath_requestslib")
    
# Test an index of subfolder is returned
def test_valid_get_subfolder_requestslib():
    r = requests.get('http://localhost:64321/folder1/')
    checkValidResponse(r)
    print(r.status_code)
    assert r.status_code == 200
    assert "<a href=" in r.text # encoded as links
    assert "testfile.txt" in r.text
    print("Succeded: test_valid_get_subfolder_requestslib")

# Test a file in subfolder
def test_valid_get_ressource_requestslib():
    r = requests.get('http://localhost:64321/folder1/testfile.txt')
    checkValidResponse(r)
    assert r.status_code == 200
    assert "This is a test" == r.text 

# Test with invalid ressource path
def test_invalid_patch_requestslib():
    r = requests.patch('http://localhost:64321/filethatdoesnotexist')
    checkValidResponse(r)
    assert r.status_code == 404 # wrong file

# spawn web server for all tests
server = subprocess.Popen(["python3", "../Code/webserver.py"])
import time
time.sleep(1)
try:
    test_valid_get_nopath_requestslib()
    test_valid_get_subfolder_requestslib()
    test_valid_get_ressource_requestslib()
    test_invalid_patch_requestslib()
finally:
    server.terminate()
