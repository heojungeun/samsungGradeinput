# samsungGradeinput
삼성 채용 이력서 작성에 필요한 이수학점 입력을 크롤링으로 해결합니다.

__주의사항__ 
  * 경북대yes에서 제공하는 전체성적파일 양식을 따릅니다. 
  * 파이썬 에디터가 필요합니다. pycharm, idle 상관 없습니다. (pycharm community(무료) 추천합니다)

### 초기 설정
1. gradecraw.py 파일을 다운로드합니다.
2. 본인의 크롬의 버전에 맞는 chromdriver를 원하는 위치에 설치합니다. https://chromedriver.chromium.org/downloads
   * 경로를 기억해두셔야 합니다.
   
   * 윈도우 예시: c 드라이브에 chromedriver_win64 폴더에 chromedriver.exe를 저장했다면, C:\\chromedriver_win64\\chromedriver 입니다.
   
   * 맥 예시: exe 파일을 설치한 곳으로 간 다음, exe파일에 우클릭, 정보 가져오기를 해서, 경로를 복사합니다. 
   만약 사용자 폴더 하에, jung 폴더 하에, chromedriver_mac 폴더 안에 설치했을 경우 끝에 exe 파일의 이름을 붙이면 됩니다.  
   -> /Users/jung/chromedriver_mac/chromedriver
   
3. 경북대 yes에 접속하여 성적 카테고리에 들어가 전체 이수성적 엑셀파일을 다운로드합니다. 파일 이름은 '전체성적' 그대로 놔둡니다.
   * xls 파일 형식일 경우 xlsx로 업그레이드시켜줍니다. (xls는 프로그램에서 다룰 수 없습니다.)
4. 전체성적 엑셀파일을 편의를 위해서 파이썬 파일(gradecraw.py)과 같은 위치에 둡니다.
5. 삼성 전공명이 개개인마다 id가 달라서 직접 메모해두셔야 합니다. 삼성 채용 사이트에 접속해서 이수교과목 적는 칸으로 갑니다.
   * 개발자 도구를 킵니다. ( 자세한 건 구글에 검색하기 )
   
   * applyform_tmp_majcd_ 을 복사해서 개발자 도구 element칸에서 ctrl+f -> 붙여넣기하셔서 id 위치를 찾습니다.
   
   * 'applyform_tmp_majcd_0000'에서 0000은 개개인마다 다릅니다. apply부터 0000까지 복사해서 메모해둡니다.

### 설정이 끝나면
* 파이썬 에디터에서 파이썬 파일을 실행시켜주세요. 입력해주세요가 나오면 메모해둔 것대로 입력하시면 됩니다. 크롬 창이 뜨고 크롤링이 시작됩니다.
* 콘솔 창에 나오는 에러는 확인을 위해 나오는 것입니다. 계속 진행하시면 됩니다.
  * 같은 에러가 계속해서 나오고, 크롤링이 멈춘 것같다면 해당되는 하얀색 칸을(사진 참고) 한번만 클릭해주세요
    <img src="IMG_9209.jpg" width="200px"></img>
  * 다른 에러가 뜬다면 프로그램을 종료시키고, 다시 실행해주세요.
* 파이썬이 실행시킨 크롬창을 최소화하면 안됩니다. 진행이 안됩니다. 
* 이 프로그램은 1회수강을 고정해두고있습니다. 재이수 과목이 있을 경우 (프로그램이 끝나고) 직접 수정해야합니다.

### *프로그램이 끝나면, 총 이수과목 수(직접입력)를 입력하라고 알림이 뜹니다. 입력하시고 꼭꼭 저장하고 창을 끄시면 됩니다.*
