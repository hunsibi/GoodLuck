import requests
import random
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from copy import copy

old_lotto_numbers = []
my_lotto_numbers = []
sampleing_arr = []
sampling_numbers = []
#동행복권 회차 prtest
selectTime =1066


def sendEmail(lottNumbers):
    sendEmail = "hunsibi77@naver.com"
    password = "ruathsgo77@#@"
    recvEmail = "hunsibi77@naver.com"
    smtpName = "smtp.naver.com"
    smtpPort = 587

    lottotext = ("\n".join(map(str,lottNumbers)))
    msg = MIMEText(lottotext)

    msg['Subject'] = f'!!!!!!! 제{selectTime+1}회차 로또번호!!!!!!!'
    msg['From'] = sendEmail
    msg['To'] = recvEmail
    print(msg.as_string())

    s = smtplib.SMTP(smtpName, smtpPort)  # 메일 서버 연결
    s.starttls()  # TLS 보안 처리
    s.login(sendEmail, password)  # 로그인
    s.sendmail(sendEmail, recvEmail, msg.as_string())  # 메일 전송, 문자열로 변환하여 보냅니다.
    s.close()  # smtp 서버 연결을 종료합니다.


def get_lotto_numbers(episode):
    params = {
        'method':'getLottoNumber',
        'drwNo':episode
    }

    request = requests.get('https://www.dhlottery.co.kr/common.do',
                           params=params)
    response = request.json()
    print(response)
    num_arr = []
    for i in range(1,7):
        num_arr.append(response["drwtNo" + str(i)])
    # 1등 번호 넣는다.
    old_lotto_numbers.append(num_arr)
    # 보너스 번호를 이용하여 필터 번호 확장
    bnus_arr = []
    for i in range(0,6):
        bnus_arr = copy(num_arr)
        bnus_arr[i] = response['bnusNo']
        old_lotto_numbers.append(bnus_arr)

def makeLottoNumber():
    oldLottDF = pd.read_csv("oldLottoNumber.csv", header=None)
    old_lotto_list = oldLottDF.values.tolist()

    # #1. 필터링에 없는 것을 랜덤으로 샘플링 한다.
    while len(my_lotto_numbers) < 5:
        list_of_numbers = list(range(1,46))
        random.shuffle(list_of_numbers)
        numbers = random.sample(list_of_numbers,6)

        if numbers not in old_lotto_list or numbers not in my_lotto_numbers:
            numbers.sort()
            my_lotto_numbers.append(numbers)
    #2. 랜덤으로 만들어진 번호들 중에 샘플링 6개해서 5쌍 번호를 만든다.
    sampleing_arr = []
    for i in range(0,5):
       sampleing_arr =  sampleing_arr + my_lotto_numbers[i]

    sampleTemp = []
    while len(sampleTemp) < 3:
        random.shuffle(sampleing_arr)
        samplenumbers = random.sample(sampleing_arr,6)
        # 중복 제거
        if len(set(samplenumbers)) <6:
            continue

        if samplenumbers not in old_lotto_list or samplenumbers not in my_lotto_numbers:
            samplenumbers.sort()
            sampleTemp.append(samplenumbers)
            my_lotto_numbers.append(samplenumbers)

    # #3. 1에서 만들어진 번호를 제외한 것을 만든다
    lotto_num = []
    sampleing_arr2 = []
    sampleing_arr = []
    for i in range(0,5):
       sampleing_arr2 =  sampleing_arr2 + my_lotto_numbers[i]

    sampleTemp2 = []
    while len(sampleTemp2) < 2:
        lotto_num.clear()
        while len(lotto_num) < 6:
            random.seed(random.random())
            tempNum = random.randrange(1, 46)
            if tempNum in lotto_num or tempNum in sampleing_arr2:
                continue
            lotto_num.append(tempNum)

        lotto_num.sort()
        sampleTemp2.append(lotto_num.copy())
        my_lotto_numbers.append(lotto_num.copy())

    for num in my_lotto_numbers:
        print(num)

def makeResult():
    f = open("numbers.text", 'w')
    i = 1
    for nums in my_lotto_numbers:
        f.write(str(sorted(nums)) + "\n")
        if i % 5 == 0:
            f.write("\n")
        i = i + 1

    f.close()

def copyCsvFile():
    # 예전 로또 번호 즉 필터링 정보를  csv에 저장한다.
    df = pd.DataFrame(old_lotto_numbers)
    if not os.path.exists('oldLottoNumber.csv'):
        df.to_csv("oldLottoNumber.csv", header=False, index=False, mode='w', encoding='cp949')
    else:
        df.to_csv("oldLottoNumber.csv", header=False, index=False, mode='a', encoding='cp949')

selectTime += 1

# for i in range(1,selectTime):
#    print(f'{i} 번째 로또 진행 중...')
#    get_lotto_numbers(i)
# get_lotto_numbers(selectTime)

# copyCsvFile()
makeLottoNumber()
makeResult()
sendEmail(my_lotto_numbers)




