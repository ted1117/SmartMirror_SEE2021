from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime, pickle, os.path

def getTodo():
    creds_filename = "\module\client_secret.json"

    #권한 인증 및 토큰 확인 
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    creds = None

    #이미 발급받은 토큰이 있을때
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    #elif not creds or not creds.valid:
    else:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_filename, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # 객체 생성
    service = build("calendar", "v3", credentials=creds)

    # 조회에 사용될 요청 변수 지정
    calendar_id = "primary"
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # 일정을 조회할 날짜
    time_min = today + "T00:00:00+09:00"
    time_max = today + "T23:59:59+09:00"
    max_result = 5
    is_single_events = True
    orderby = "startTime"

    events_result = service.events().list(calendarId = calendar_id,
                                          timeMin = time_min,
                                          timeMax = time_max,
                                          maxResults = max_result,
                                          singleEvents = is_single_events,
                                          orderBy = orderby
                                          ).execute()

    items = events_result.get('items', [])
    todo_list = []

    for item in items:
        todo_dict = {}
        todo_dict["summary"] = item["summary"]  # 일정 제목 가져오기
        todo_dict["start"] = item["start"]["dateTime"][11:16]   # 일정 시작 시각 가져오기
        todo_list.append(todo_dict)

    return todo_list



if __name__ == "__main__":
    print(getTodo())