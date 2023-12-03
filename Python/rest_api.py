import requests

#서버와 통신을 처리하는 py입니다.

#서버 주소 설정 (제가 운영하는 서버 주소로 되어있습니다.)
server_url = 'http://118.67.131.187:3000/file/'

#서버에서 해당 FileName의 File을 가져오는 메서드입니다.
# GET 기능을 합니다.
#파일의 내용을 return 합니다.
def getFile(fileName):
    end_point = "getFile"
    try:
        #JSON으로 fileName을 전달합니다.
        response = requests.get(server_url + end_point, params={"fileName":fileName})
        # 응답이 성공했을 경우
        if response.status_code == 200:
            text = response.text  # 텍스트 추출
            return text
        else:
            print(f"Error: {response.status_code}")  # 에러 처리
            return None
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None

#서버에 존재하는 파일 목록을 보여주는 메서드입니다.
#파일 목록을 텍스트로 return 합니다.
def getFileList():
    end_point = "getFileList"
    try:
        response = requests.get(server_url + end_point)
        # 응답이 성공했을 경우
        if response.status_code == 200:
            text = response.text  # 텍스트 추출
            return text
        else:
            print(f"Error: {response.status_code}")  # 에러 처리
            return None
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None
    

#서버에 파일을 저장하는 메서드입니다.
# POST 기능을 합니다.
# _data 에 fileName, text를 id로 갖는 value들을 저장합니다.
# 해당 정보를 json으로 서버에 전달합니다.
#성공 시 OK를 return 합니다.
def saveFile(fileName, text):
    try:
        print('save file')
        end_point = "saveFile"
        _data = {"fileName":fileName, "text":text}
        
        response = requests.post(server_url + end_point, json = _data)
        # 응답이 성공했을 경우
        if response.status_code == 200:
            return "OK"
        else:
            print(f"Error: {response.status_code}")  # 에러 처리
            return "Err"
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None
    

#서버에 fileName에 해당하는 파일을 삭제합니다.
# GET 기능으로 처리합니다.
#params 로 fileName을 전달합니다.
#성공시 OK를 return 합니다.
def deleteFile(fileName):
    end_point = 'deleteFile'
    try:
        response = requests.get(server_url + end_point, params={"fileName":fileName})
        # 응답이 성공했을 경우
        if response.text == "OK":
            return "OK"
        else:
            print(f"Error: {response.status_code}")  # 에러 처리
            return None
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None