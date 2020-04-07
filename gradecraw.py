from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import load_workbook

print("삼성채용 이메일을 입력해주세요")
s_id = input()
print("삼성채용 비밀번호를 입력해주세요(코드 내에서만 사용됩니다)")
s_pa = input()
print("전공명 id를 입력해주세요(예시: 'applyform_tmp_majcd_22XX'\n자세한 사항은 github readme를 참고해주세요)")
majid = input()
print("chromedriver 주소를 입력해주세요. 자세한 사항은 git readme를 참고해주세요.\n(예시:C:\\chromedriver, 맥 예시: /Users/jung/chromedriver_mac/chromedriver)")
driveraddress = input()

#### 삼성 아이디(이메일)와 비밀번호를 적어주세요
# s_id = '여기에 이메일을 적어주세요 삼성아이디(이메일)'
# s_pa = '여기에 비밀번호를 적어주세요'

# data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
#### 전체성적 엑셀파일을 이 파이썬 파일과 같은 위치에 놔둬야합니다.
#### 아니면 "전체성적엑셀파일이 있는 경로"를 적어주세요
#### yes.knu.ac.kr 에 있는 성적 전체엑셀파일 형식만 가능합니다.
#### xls로 되어있다면 xlsx로 업그레이드 해주셔야합니다.
load_wb = load_workbook("전체성적.xlsx", data_only=True)
# 시트 이름으로 불러오기
load_ws = load_wb['Sheet']

# Chrome(' 이 위치에 chromedriver파일 위치를 넣어준다. 밑은 예시로 c드라이브안에 바로 넣었을때') driver connect
#driver = webdriver.Chrome('C:\\chromedriver')
driver = webdriver.Chrome(driveraddress)
cnt = 0

def gr_craw(sam_id, sam_pass):
    driver.get('https://www.samsungcareers.com/rec/apply/ComResumeServlet')
    time.sleep(3)
    tmp = driver.find_element_by_name('email')
    tmp.send_keys(sam_id)
    tmp = driver.find_element_by_name('password')
    tmp.send_keys(sam_pass)
    tmp.send_keys(Keys.RETURN) ## 로긴 버튼 클릭
    time.sleep(2)
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(3)

    driver.find_element_by_xpath(
        '//*[@id="cont"]/div[1]/ul/div/dl/dd[1]/p/span/a'
    ).click() ## 3급신입채용 클릭
    time.sleep(4)

    try:
        tmp = driver.find_element_by_xpath('//*[@id="masTable1"]/tr/td[3]/a')
    except:
        time.sleep(2)
        tmp = driver.find_element_by_xpath('//*[@id="masTable1"]/tr/td[3]/a')

    tmp.click()  ## 작성중 이력서 항목중 1번째 클릭
    time.sleep(4)
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)

    tmp= driver.find_element_by_xpath(
        '//*[@id="cont"]/table[1]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[2]/ul/li[3]/a'
    )
    tmp.click()  ## 이수교과목 클릭
    time.sleep(2)
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)

    multiple_cells = load_ws['A2':'F60']
    while 1:
        try:
            time.sleep(2)
            driver.find_element_by_name('tmp_schlcarrcdView').click()  ## 학사버튼클릭하기
            time.sleep(2)
            driver.find_element_by_id(
                'applyform_tmp_schlcarrcd_5'
            ).click()  ## 버튼클릭하기
            break
        except:
            print('과정선택 에러')
            time.sleep(2)
            continue
    while 1:
        try:
            print(2)
            driver.find_element_by_name(
                'tmp_majcdView'
            ).click()  ## 전공명버튼클릭하기
            time.sleep(1)
            # 콤보박스가 닫혀있으면 display: none; 열려있으면 display: block;
            checkmaj = driver.find_element_by_id('ComboDiv_tmp_majcd').get_attribute('style')
            ########## 전공명 아이디는 개인마다 다름, 입력값으로 해놓으면 좋을
            if "block" in checkmaj:
                driver.find_element_by_id(
                    majid
                ).click()  ## 버튼클릭하기
                break
            else:
                continue
        except:
            print('전공명선택 에러')
            time.sleep(5)
            continue
    while 1:
        try:
            driver.find_element_by_id(
                'tmp_retakeynId'
            ).click()  ## 버튼클릭하기
            time.sleep(2)
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

    for row in multiple_cells:
        list_r = []
        for cell in row:
            list_r.append(cell.value) # 한 row 정보를 임시 list에 저장

        if list_r[0] == None:
            break
        if list_r[4] == '' or list_r[4]== None or list_r[1] == '' or list_r[1]== None:
            continue

        while 1:
            try:
                driver.find_element_by_id(
                    'tmp_regyrId'
                ).click()  ## 수강년도버튼클릭하기
                time.sleep(1)
                st_yr = 'applyform_tmp_regyr_'+ list_r[0][0:4]
                checkre = driver.find_element_by_id('ComboDiv_tmp_regyr').get_attribute('style')
                if 'block' in checkre:
                    driver.find_element_by_id(st_yr).click()  ## 버튼클릭하기
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
                st_semst = ''
                checksemst = driver.find_element_by_id('ComboDiv_tmp_semst').get_attribute('style')
                if 'block' in checksemst:
                    if list_r[0][4] == 'S':
                        st_semst = 'applyform_tmp_semst_여름계절'
                    elif list_r[0][4] == 'W':
                        st_semst = 'applyform_tmp_semst_겨울계절'
                    else:
                        st_semst = 'applyform_tmp_semst_' + list_r[0][4]
                    driver.find_element_by_id(st_semst).click()
                    break
                else:
                    continue
            except:
                print('학기선택 에러')
                time.sleep(1)
                continue
        print(list_r)
        while 1:
            try:
                driver.find_element_by_id(
                    'tmp_majtypecdId'
                ).click()  ## 과목유형버튼클릭하기
                st_matype=''
                time.sleep(1)
                majtype = list_r[1]
                checkmajtype = driver.find_element_by_id('ComboDiv_tmp_majtypecd').get_attribute('style')
                if 'block' in checkmajtype:
                    if '전공' in majtype and '기반' not in majtype:
                        driver.find_element_by_id('applyform_tmp_majtypecd_A').click() ## 전공 클릭
                    else:
                        driver.find_element_by_id('applyform_tmp_majtypecd_C').click() ## 교양 클릭
                    st_name = driver.find_element_by_id('tmp_majcurrinm')
                    if st_name.is_enabled():
                        break
                else:
                    continue
            except:
                print('과목유형선택 에러')
                time.sleep(1)
                continue

        st_name = driver.find_element_by_id('tmp_majcurrinm')
        st_name.send_keys(list_r[3])

        while 1:
            try:
                driver.find_element_by_id(
                    'tmp_obtptId'
                ).click()  ## 버튼클릭하기
                time.sleep(2)
                checkscore = driver.find_element_by_id('ComboDiv_tmp_obtpt').get_attribute('style')
                if 'block' in checkscore:
                    st_obtpt = 'applyform_tmp_obtpt_'+list_r[4]
                    driver.find_element_by_id(st_obtpt).click()  ## 버튼클릭하기
                    break
                else:
                    continue
            except:
                print('학점선택 에러')
                time.sleep(1)
                continue
        print(list_r[0],"중간확인")
        while 1:
            try:
                print('성적확인1')
                driver.find_element_by_id(
                    'tmp_obtpovId'
                ).click()  ## 버튼클릭하기
                print('성적확인2')
                if '0' in list_r[5]:
                    list_r[5]=list_r[5][0:-1]
                elif 'S' in list_r[5]:
                    list_r[5] = 'PASS'
                elif 'U' in list_r[5]:
                    list_r[5] = 'FAIL'

                # st_obtpov = 'applyform_tmp_obtpov_'+list_r[5]
                st_obtpov = list_r[5]
                print('성적확인3',st_obtpov)
                time.sleep(2)
                checkscore = driver.find_element_by_id('ComboDiv_tmp_obtpov').get_attribute('style')
                if 'block' in checkscore:
                    driver.find_element_by_link_text(st_obtpov).click()  ## 버튼클릭하기
                    break
            except:
                print('성적선택 에러')
                time.sleep(1)
                continue
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="budiv_mySheet_AddMajdet"]/a').click() #추가버튼 클릭


gr_craw(s_id, s_pa)
time.sleep(2)
driver.find_element_by_id('abeektgtynId').click()
time.sleep(2)
checkabeek = driver.find_element_by_id('ComboDiv_abeektgtyn').get_attribute('style')
if 'block' in checkabeek:
    driver.find_element_by_id('applyform_abeektgtyn_A').click()
else:
    driver.find_element_by_id('abeektgtynId').click()
    time.sleep(2)
    driver.find_element_by_id('applyform_abeektgtyn_A').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="budiv_mySheet_Save"]/a').click()
print('저장 버튼 클릭 완료. 만일을 대비해 확인 부탁드립니다.')

# f.close()
# driver.close()
# driver.quit()
