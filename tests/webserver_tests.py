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
def test_valid_get_nopath():
    r = requests.get('http://localhost:64321/')
    checkValidResponse(r)
    assert r.status_code == 200
    assert "<a href=" in r.text # encoded as links
    assert "folder" in r.text
    assert "webserver_tests.py" in r.text
    print("Succeded: test_valid_get_nopath")
    
# Test an index of subfolder is returned
def test_valid_get_subfolder():
    r = requests.get('http://localhost:64321/folder1/')
    checkValidResponse(r)
    print(r.status_code)
    assert r.status_code == 200
    assert "<a href=" in r.text # encoded as links
    assert "testfile.txt" in r.text
    print("Succeded: test_valid_get_subfolder")

# Test a file in subfolder
def test_valid_get_ressource():
    r = requests.get('http://localhost:64321/folder1/testfile.txt')
    checkValidResponse(r)
    assert r.status_code == 200
    assert "This is a test" == r.text 
    print("Succeded: test_valid_get_ressource")


# Test with invalid ressource path
def test_invalid_get():
    r = requests.patch('http://localhost:64321/filethatdoesnotexist')
    checkValidResponse(r)
    assert r.status_code == 404 # wrong file
    print("Succeded: test_invalid_get")

# Test with non-implemented
def test_nonimplemented_patch():
    r = requests.patch('http://localhost:64321/')
    checkValidResponse(r)
    assert r.status_code == 501 # wrong file
    print("Succeded: test_invalid_patch_requestslib")


# spawn web server for all tests
server = subprocess.Popen(["python3", "../Code/webserver.py"])
import time
time.sleep(1)
try:
    import os
    os.system("curl -v http://localhost:64321")
    test_valid_get_nopath()
    test_valid_get_subfolder()
    test_valid_get_ressource()
    test_invalid_get()
    test_nonimplemented_patch()
finally:
    server.terminate()
