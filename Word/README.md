# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 한혁님
- 리뷰어 : 조은별

# PRT(Peer Review Template)
- [Y]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 문제에서 요구하는 최종 결과물이 첨부되었는지 확인
        - 중요! 해당 조건을 만족하는 부분을 캡쳐해 근거로 첨부

1. 텍스트 전처리 수행하기
import re
# - Avengers.txt 파일을 불러온다.
with open("Avengers.txt", "r", encoding="utf-8") as f:
    text = f.read()
    # - 모든 문자는 소문자로 변환한다.
    text = text.lower()
    # - 모든 기호를 제거한다
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # - 단어 단위로 분리한다.
    clean_text = clean_text.split()
# - 결과: " I am hungry.. very.. much" -> ['i', 'am', 'hungry', 'very', 'much']
print(clean_text[:50])

2. 각 단어 별 빈도수를 딕셔너리 형태로 저장한다.
words = clean_text
word_count = {}
for word in words:
  word_count[word] = word_count.get(word, 0) + 1
print(word_count)

3. 딕셔너리를 빈도수순으로 내림차순 정렬하고, 정렬 순서대로 정수 인덱스를 부여한다.

def create_word_to_index(word_count):
    # 빈도수 기준 내림차순 정렬 (빈도수가 같으면 알파벳 순)
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))

    # 정수 인덱스 부여 (0부터 시작)
    word_to_index = {}
    for idx, (word, freq) in enumerate(sorted_words):
        word_to_index[word] = idx
    print(type(word_to_index))
    return word_to_index
wordtoindex = create_word_to_index(word_count)
print(wordtoindex)

4. 텍스트를 input()으로 입력받아서 정수를 return하는 함수를 만든다.
def print_value_by_input(d):
    """
    사용자로부터 키(문자열)를 입력받아 딕셔너리 d에서 값을 출력.
    키가 없으면 에러 메시지 출력.
    """
    key = input("키를 입력하세요: ")
    print(key)
    print(d[key])
    # if key in d:
    #     print(d.items())
    # else:
    #     print(f"키 '{key}'가 딕셔너리에 없습니다.")
print_value_by_input(wordtoindex)
    
- [Y]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 해당 코드 블럭을 왜 핵심적이라고 생각하는지 확인
    - 해당 코드 블럭에 doc string/annotation이 달려 있는지 확인
    - 해당 코드의 기능, 존재 이유, 작동 원리 등을 기술했는지 확인
    - 주석을 보고 코드 이해가 잘 되었는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부
        
이해 잘 되게끔 주석도 잘 달아주신 거 같아요!
그 중에서 이제 핵심 블럭이라고 생각되는 부분은 아래에 남겨드릴게요!!!

3. 딕셔너리를 빈도수순으로 내림차순 정렬하고, 정렬 순서대로 정수 인덱스를 부여한다.
def create_word_to_index(word_count):
    # 빈도수 기준 내림차순 정렬 (빈도수가 같으면 알파벳 순)
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))

    # 정수 인덱스 부여 (0부터 시작)
    word_to_index = {}
    for idx, (word, freq) in enumerate(sorted_words):
        word_to_index[word] = idx
    print(type(word_to_index))
    return word_to_index
wordtoindex = create_word_to_index(word_count)
print(wordtoindex)

이 부분은 '빈도 내림차순, 동률 시 단어 오름차순'으로 문제에 제시된 기준보다
좀 더 기준을 구체화하여서, 동률일 때 어떻게 하겠다라는 가이드라인까지 세워주시고
그렇게 하신 걸 코드에도 반영을 해주셔서 좋은 거 같습니다!!!!! 배워갑니다!

- [N]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 문제 원인 및 해결 과정을 잘 기록하였는지 확인
    - 프로젝트 평가 기준에 더해 추가적으로 수행한 나만의 시도, 
    실험이 기록되어 있는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부
        
에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남기거나
새로운 시도 또는 추가 실험을 수행한 과정이 기록되어 있지는 않습니다!
     
그래서 추천드리는 문제풀이 방식이 있어요!
문제 해결의 과정은 아래와 같이 작성해야 제대로 문제를 뜯어봤다고 볼 수 있습니다.
1. 말로써, 자기의 언어로써 입력-처리-출력 과정 및 여타 조건을 만족하는 코드들을  
   먼저 표현해보기(한국어/영어 혹은 의사코드 작성 가능)
2. 노가다로 구현부터 해보기
   (알고리즘 문제라면, 브루트포스 방식을 사용한다거나, 아예 자료구조부터 직접 구현해보는 방식)
3. 그 다음 파이썬 고유의 함수 등을 적용하여, 
   다시 같은 의미의 코드를 재구성(리팩토링, 최적화 + 간결화)하기
4. 그 다음 적용해본 방식들 비교 & 시간/공간 복잡도 분석

매번 이렇게까지는 하지 않아도 되는데, 각 의미 단위의 코드블럭을 짜주실 때 여러가지 방식을
생각해보신다면, 정말 많이 성장할 수 있을 거 같습니다!!!

저희 팀도 촉박하게 문제푸느라 완벽하지는 않지만, 참고용으로 첨부드립니다!

# 2번 과정 시작(각 단어별 빈도수를 딕셔너리에 저장)
# 나중에 해볼 방법
# for문 써서 word count
# list.count "딕셔너리 형태로 저장방법?"
# 지금 사용 방법
# Counter "리스트에서 바로 사용가능한지? -> 문자열 리스트가 아니라 지금 "리스트의 리스트" 상태여서? 조치가 필요"
# 그 전 쉘에서 형태 수정

from collections import Counter
word_count = Counter(words_list)

- [N]  **4. 회고를 잘 작성했나요?**
    - 주어진 문제를 해결하는 완성된 코드 내지 프로젝트 결과물에 대해
    배운점과 아쉬운점, 느낀점 등이 기록되어 있는지 확인
    - 전체 코드 실행 플로우를 그래프로 그려서 이해를 돕고 있는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부

회고가 작성되어 있지는 않지만, 회고하실 때 도움이 되셨으면 좋겠는 바람에서
1번 파트에서 수정할 만한 거 알려드릴게요!

1. 텍스트 전처리 수행하기
import re
# - Avengers.txt 파일을 불러온다.
with open("Avengers.txt", "r", encoding="utf-8") as f:
    text = f.read()
    # - 모든 문자는 소문자로 변환한다.
    text = text.lower()
    # - 모든 기호를 제거한다
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)    <- 여기
    # - 단어 단위로 분리한다.
    clean_text = clean_text.split()
# - 결과: " I am hungry.. very.. much" -> ['i', 'am', 'hungry', 'very', 'much']
print(clean_text[:50])

모든 기호를 제거하시는 부분에서 일단 for 문으로 특정 기호 몇개를 제거하는 코드보다
정규표현식을 쓰신점은 너무 칭찬드립니다, 리스트 컴프리헨션으로 코드를 재구성해보셔도 좋을 거 같아요

참고용으로 리스트 컴프리헨션 이용해서 작성한 코드 첨부드릴게요

# 특수문자 제거(은별 버전)
clean_lines = [
    ''.join(
      ch if (ch.islower() or ch.isdigit() or ch.isspace()) else ' '
      for ch in line
    )
    for line in data_lower
]

또한 1번 파트에서 주의하셨으면 좋겠는게, 
re.sub(..., '', text)로 기호를 빈 문자열로 제거하면 hello,world → helloworld 처럼 단어가 붙어버리게 됩니다
그래서 반드시 공백 " "으로 치환하는 걸 기억해주셨으면 좋겠어요!
      
- [Y]  **5. 코드가 간결하고 효율적인가요?**
    - 파이썬 스타일 가이드 (PEP8) 를 준수하였는지 확인
    - 코드 중복을 최소화하고 범용적으로 사용할 수 있도록 함수화/모듈화했는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부

혁님 팀이 작성하신 코드는 모듈화가 굉장히 잘되어 있습니다
문제 해결 과정이 4단계로 주어진 만큼 작성하신 코드도 셸을 4개만 사용하셨는데, 
이는 모듈화가 잘되어 있어서 어느 파트가 어떤 걸 의미하고,
코드를 수정하려면 어디서 고쳐야 하는지 파악하기가 쉬워요.

# 1. 텍스트 전처리 수행하기
import re
# - Avengers.txt 파일을 불러온다.
with open("Avengers.txt", "r", encoding="utf-8") as f:
    text = f.read()
    # - 모든 문자는 소문자로 변환한다.
    text = text.lower()
    # - 모든 기호를 제거한다
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # - 단어 단위로 분리한다.
    clean_text = clean_text.split()
# - 결과: " I am hungry.. very.. much" -> ['i', 'am', 'hungry', 'very', 'much']
print(clean_text[:50])
     
반면, 저희 팀이 1번 전처리 파트에서 작성한 코드는 코랩에서 진행하는 만큼
원하는 코드를 찍어보고 바로 결과를 육안으로 볼 수 있는 장점을 살려서 
여러 셸로 나눠서 코드를 작성하고, 코드라인 별로 print를 찍어보는 방법을 택했습니다

그래서 결론적으로는, 특히 전처리 파트에서 추천드리는 방법은 코드라인 별로 작성 후
print를 찍어보시면서, 원하는 결과가 나오는지 확인하고 나서
전처리 파트를 작성을 다 하시면 그 후에 지금처럼 한 셸에 모으고 관리하시는 게
제일 베스트인 거 같습니다! 만약에 이미 그런 방식으로 하신 거라면 완전 칭찬드립니다!!!

# 회고(참고 링크 및 코드 개선)
```
# 리뷰어의 회고를 작성합니다.
# 코드 리뷰 시 참고한 링크가 있다면 링크와 간략한 설명을 첨부합니다.
# 코드 리뷰를 통해 개선한 코드가 있다면 코드와 간략한 설명을 첨부합니다.
```
