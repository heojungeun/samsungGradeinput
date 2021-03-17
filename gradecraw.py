from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import load_workbook
import xlrd
print("삼성채용 이메일을 입력해주세요")
s_id = input()
print("삼성채용 비밀번호를 입력해주세요(코드 내에서만 사용됩니다)")
s_pa = input()
print("chromedriver 주소를 입력해주세요. 자세한 사항은 git readme를 참고해주세요.\n(예시:C:\\chromedriver, 맥 예시: /Users/jung/chromedriver_mac/chromedriver)")
driveraddress = input()
print("abeek 이수: 이수완료했다면 1, 이수예정이라면 2, 비대상이라면 3 입력해주세요.(나중에 수정가능)")
abeekVar = input()

### 삼성 아이디(이메일)와 비밀번호를 적어주세요
# data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
#### 전체성적 엑셀파일을 이 파이썬 파일과 같은 위치에 놔둬야합니다.
#### 아니면 "전체성적엑셀파일이 있는 경로"를 적어주세요
#### yes.knu.ac.kr 에 있는 성적 전체엑셀파일 형식만 가능합니다.
#### xls로 되어있다면 xlsx로 업그레이드 해주셔야합니다.
#load_wb = load_workbook("전체성적.xlsx", data_only=True)
load_wb = xlrd.open_workbook("전체성적.xlsx")
# 시트 이름으로 불러오기
#load_ws = load_wb['Sheet']
load_ws = load_wb.sheet_by_index(0)

# Chrome(' 이 위치에 chromedriver파일 위치를 넣어준다. 밑은 예시로 c드라이브안에 바로 넣었을때') driver connect
#driver = webdriver.Chrome('C:\\chromedriver')
#webdriver.Chrome('/Users/jung/chromedriver2')

driver = webdriver.Chrome(driveraddress)
cnt = 0
nrow = load_ws.nrows

def gr_craw(sam_id, sam_pass):
    scoreDict = {'A+': 'A+', 'A0': 'A', 'A-': 'A-', 'B+': 'B+', 'B0': 'B', 'C-': 'C-', 'C0': 'C', 'C+': 'C+',
                 'D+': 'D+', 'D0': 'D', 'D-': 'D-', 'S': 'PASS', 'U': 'FAIL'}
    driver.implicitly_wait(10)  # seconds
    driver.get('https://www.samsungcareers.com/rec/apply/ComResumeServlet')
    time.sleep(3)
    tmp = driver.find_element_by_name('email')
    tmp.send_keys(sam_id)
    tmp = driver.find_element_by_name('password')
    tmp.send_keys(sam_pass)
    tmp.send_keys(Keys.RETURN) ## 로긴 버튼 클릭
    time.sleep(4)
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(3)

    # class insecure-form
    try:
        driver.find_element_by_id('proceed-button').click()
        time.sleep(1)
    except:
        print('no proceed-button')

    driver.find_elements_by_class_name('applybtn')[0].click()
    time.sleep(3)

    driver.find_elements_by_class_name('viewNotice')[0].click()
    time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(1)

    driver.execute_script('''
        javascript:hidePopupDiv()
    ''')
    time.sleep(1)
    driver.execute_script('''
            javascript:MoveTo('rsmStep3');
    ''')
    time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)

    while 1:
        try:
            driver.find_element_by_id('tmp_schlcarrcdId').click()  ## 학사버튼클릭하기
            time.sleep(1)
            checkmaj = driver.find_element_by_id('ComboDiv_tmp_schlcarrcd').get_attribute('style')
            if "block" in checkmaj:
                driver.find_element_by_id(
                    'applyform_tmp_schlcarrcd_5'
                ).click()  ## 버튼클릭하기
                break
            else:
                continue
        except:
            print('과정선택 에러')
            time.sleep(2)
            continue
    time.sleep(1)
    while 1:
        try:
            driver.find_element_by_id(
                'tmp_majcdId'
            ).click()  ## 전공명버튼클릭하기
            time.sleep(1)
            # 콤보박스가 닫혀있으면 display: none; 열려있으면 display: block;
            checkmaj = driver.find_element_by_id('ComboDiv_tmp_majcd').get_attribute('style')
            # 전공명 아이디는 개인마다 다름
            if "block" in checkmaj:
                # driver.find_element_by_id(
                #     'ComboDiv_tmp_majcd_List'
                # ).find_elements_by_css_selector('ol > li')[0].find_element_by_tag_name('a').click()  ## 버튼클릭하기
                # break
                maj = driver.find_element_by_name('c_majcd').get_attribute('value')
                st_maj = 'document.getElementById("applyform_tmp_majcd_' + maj + '").click();hidePopupDiv();'
                driver.execute_script(st_maj)
                # driver.find_element_by_id('applyform_tmp_majcd_' + maj).click()
                break
            else:
                continue
        except:
            print('전공명선택 에러')
            time.sleep(2)
            continue
    time.sleep(1)
    while 1:
        try:
            driver.find_element_by_id(
                'tmp_retakeynId'
            ).click()  ## 버튼클릭하기
            time.sleep(1)
            checkre = driver.find_element_by_id('ComboDiv_tmp_retakeyn').get_attribute('style')
            if 'block' in checkre:
                driver.find_element_by_id('applyform_tmp_retakeyn_N').click()  ## 버튼클릭하기
                break
            else:
                continue
        except:
            print('재수강여부 에러')
            time.sleep(1)
            continue
    global cnt
    for i in range(1, nrow):
        row = load_ws.row(i)
        list_r = []
        for cell in row:
            list_r.append(cell.value)# 한 row 정보를 임시 list에 저장
        # if list_r[0] == None:
        #     break
        if list_r[4] == '' or list_r[4] == None or list_r[1] == '' or list_r[1] == None:
            continue

        cnt = cnt + 1
        while 1:
            try:
                driver.find_element_by_id(
                    'tmp_regyrId'
                ).click()  ## 수강년도버튼클릭하기
                time.sleep(1)
                #st_yr = 'applyform_tmp_regyr_'+ list_r[0][0:4]
                checkre = driver.find_element_by_id('ComboDiv_tmp_regyr').get_attribute('style')
                if 'block' in checkre:
                    #driver.find_element_by_id(st_yr).click()  ## 버튼클릭하기
                    st_yr = 'document.getElementById("applyform_tmp_regyr_' + list_r[0][0:4] + '").click();hidePopupDiv();'
                    driver.execute_script(st_yr)
                    break
                else:
                    continue
            except:
                print('수강년도선택 에러')
                time.sleep(1)
                continue
        while 1:
            try:
                driver.find_element_by_id(
                    'tmp_semstId'
                ).click()  ## 버튼클릭하기
                time.sleep(1)
                checksemst = driver.find_element_by_id('ComboDiv_tmp_semst').get_attribute('style')
                if 'block' in checksemst:
                    if list_r[0][4] == 'S':
                        st_semst = 'applyform_tmp_semst_여름계절'
                        driver.find_element_by_id(st_semst).click()
                    elif list_r[0][4] == 'W':
                        st_semst = 'applyform_tmp_semst_겨울계절'
                        driver.find_element_by_id(st_semst).click()
                    else:
                        #st_semst = 'applyform_tmp_semst_' + list_r[0][4]
                        st_semst = 'document.getElementById("applyform_tmp_semst_' + list_r[0][4] + '").click();hidePopupDiv();'
                        driver.execute_script(st_semst)
                    break
                else:
                    continue
            except:
                print('학기선택 에러')
                time.sleep(1)
                continue
        time.sleep(1)
        while 1:
            try:
                driver.find_element_by_id(
                    'tmp_majtypecdId'
                ).click()  ## 과목유형버튼클릭하기
                time.sleep(1)
                majtype = list_r[1]
                checkmajtype = driver.find_element_by_id('ComboDiv_tmp_majtypecd').get_attribute('style')
                if 'block' in checkmajtype:
                    if '전공' in majtype and '기반' not in majtype:
                        driver.find_element_by_id('applyform_tmp_majtypecd_A').click() ## 전공 클릭
                    else:
                        driver.find_element_by_id('applyform_tmp_majtypecd_C').click() ## 교양 클릭
                    # st_name = driver.find_element_by_id('tmp_majcurrinm')
                    # if st_name.is_enabled():
                    #     break
                    break
                else:
                    continue
            except:
                print('과목유형선택 에러')
                time.sleep(1)
                continue
        time.sleep(1)
        st_name = driver.find_element_by_id('tmp_majcurrinm')
        st_name.send_keys(list_r[3])
        time.sleep(1)
        while 1:
            try:
                driver.find_element_by_id(
                    'tmp_obtptId'
                ).click()  ## 버튼클릭하기
                time.sleep(2)
                checkscore = driver.find_element_by_id('ComboDiv_tmp_obtpt').get_attribute('style')
                if 'block' in checkscore:
                    # st_obtpt = 'applyform_tmp_obtpt_'+list_r[4]
                    # driver.find_element_by_id(st_obtpt).click()  ## 버튼클릭하기
                    st_obtpt = 'document.getElementById("applyform_tmp_obtpt_' + list_r[4] + '").click();hidePopupDiv();'
                    driver.execute_script(st_obtpt)
                    break
                else:
                    continue
            except:
                print('학점선택 에러')
                time.sleep(1)
                continue
        time.sleep(1)
        while 1:
            try:
                driver.find_element_by_id(
                    'tmp_obtpovId'
                ).click()  ## 버튼클릭하기
                if '0' in list_r[5]:# A0 -> A 로 변환
                    list_r[5]=list_r[5][0:-1]
                elif 'S' in list_r[5]:
                    list_r[5] = 'PASS'
                elif 'U' in list_r[5]:
                    list_r[5] = 'FAIL'
                #st_obtpov = 'applyform_tmp_obtpov_' + scoreDict[list_r[5]]
                time.sleep(1)
                checkscore = driver.find_element_by_id('ComboDiv_tmp_obtpov').get_attribute('style')
                if 'block' in checkscore:
                    time.sleep(1)
                    #driver.find_element_by_id("applyform_tmp_obtpov_" + scoreDict[list_r[5]]).click()  ## 버튼클릭하기
                    st_obtpov = 'document.getElementById("applyform_tmp_obtpov_' + list_r[5] + '").click();hidePopupDiv();'
                    driver.execute_script(st_obtpov)
                    break
            except:
                print('성적선택 에러')
                time.sleep(1)
                continue
        time.sleep(2)
        driver.find_element_by_css_selector('#budiv_mySheet_AddMajdet > a').click() #추가버튼 클릭


gr_craw(s_id, s_pa)
time.sleep(2)
driver.find_element_by_id('abeektgtynId').click()
time.sleep(2)
checkabeek = driver.find_element_by_id('ComboDiv_abeektgtyn').get_attribute('style')
if 'block' in checkabeek:
    if abeekVar == '1':
        driver.find_element_by_id('applyform_abeektgtyn_A').click()
    elif abeekVar == '1':
        driver.find_element_by_id('applyform_abeektgtyn_B').click()
    else:
        driver.find_element_by_id('applyform_abeektgtyn_N').click()
else:
    driver.find_element_by_id('abeektgtynId').click()
    time.sleep(2)
    if abeekVar == '1':
        driver.find_element_by_id('applyform_abeektgtyn_A').click()
    elif abeekVar == '1':
        driver.find_element_by_id('applyform_abeektgtyn_B').click()
    else:
        driver.find_element_by_id('applyform_abeektgtyn_N').click()
time.sleep(2)
totalCnt = driver.find_element_by_name('majmancnt')
totalCnt.send_keys(str(cnt))
# time.sleep(1)
# driver.find_element_by_css_selector('#budiv_mySheet_Save > a').click()
print('저장 버튼을 클릭하세요. 저장하고 페이지 확인 후 창을 끄셔도 됩니다.')

# f.close()
