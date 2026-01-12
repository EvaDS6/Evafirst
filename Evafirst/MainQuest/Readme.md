## ✨ 피쳐엔지니어링 실험 ( 1/11일 두번째 실험, 5개피쳐 추가)
- 실험 파일명 (data_prepro3.ipynb, autoint_mlp4_train.ipynb, autointmlp3,py, show_st_plus3.py)

1. 영화 인기도(**movie_pop**), 유저 활동성(**user_act**)을 추가하여 Cold-start 문제를 완화
2. 개봉 후 경과 기간(**release_lag**)을 추가하여 최신성 트렌드를 반영
3. **age_gender**(예시 : 20대_남성), **age_genre**(예시 : 20대 코미디)와 같이 유의미한 그룹 정보를 명시적으로 결합
4. 랜덤영화를 추출해서 학습하던 부분을 **Hard Negative**(인기는 많은데 안 본 영화)와 무작위를 5:5 비율로 섞어서 학습.
5. 학습시 하이퍼 파라미터 추가 튜닝
  - 임베딩 차원 16 -> 64
  - Dropout 0.4 -> 0.5로 강화시켜 과적합 방지     

### ✨ 실험 결과
  - ndcg : 0.77703 ( 0.66142 기존대비 11.5%개선)
  - hitrate : 0.70698 ( 0.62982 기존대비 7.7%개선)

### - 품질 비교
  - ID 10번의 2001년 1월 시청한 영화 목록으로 비교
  - ID 10번 유저는 1980~90년대 코미디, 드라마, 액션 장르 순서로 영화를 많이 시청한것으로 파악된다.

  - <img width="1082" height="663" alt="image" src="https://github.com/user-attachments/assets/27ab99e4-96f5-46d4-8d77-de7dac670f01" />
  - 첫번째 실험과 다르게 조금더 시청자의 선호도를 폭넓게 반영한 것으로 보인다.
  - 기존 선호도 (80,90년대 코미디, 드라마장르)도 치우치지않고, 70년대 영화, animation, 스릴러등 다른 시간대과 장르의 선호도도 반영되어서
    성능지표 개선과 더불어 품질 향상도 된것으로 확인했다.




## ✨ 파라미터 튜닝 실험 ( 1/9일 첫번째 실험)
- 실험 파일명 (autoint_mlp2_train.ipynb, autointmlp2,py, show_st_plusplus.py)

1. AutoIntMLPModel call 메서드에 training인자를 전달하여, 과적합방지
2. 임베딩 레이어 초기화 수정 (FeaturesEmbedding) build함수 대신 표준 keras방식으로 변경
3. Layer Nomalization 추가. Self-Attention구조 (Transformer계열)에서는 성능개선 가능
4. 활성화 함수 relu에서 gelu로 변경

### ✨ 실험 결과
  - ndcg : 0.66381 ( 0.66142 기존대비 0.2%개선)
  - hitrate : 0.63184 ( 0.62982 기존대비 0.2%개선)

### - 품질 비교
  - ID 10번의 2001년 1월 시청한 영화 목록으로 비교
  - ID 10번 유저는 1980~90년대 코미디, 드라마, 액션 장르 순서로 영화를 많이 시청한것으로 파악된다.
    - <img width="569" height="597" alt="1" src="https://github.com/user-attachments/assets/a9dbd0a2-0b57-48d8-b163-a761558948c3" />

  - 기존 코드에서는 장르에 주목해서 드라마, 코미디 장르 위주 영화를 추천해주었다.
  - 반면 실험 코드에서는 영화 제작년도에 주목해서 1990년도 영화 위주로 추천해주었다.
 
- 실험코드
  - <img width="558" height="343" alt="1_추천" src="https://github.com/user-attachments/assets/2e95db82-ad44-47fa-b7d5-28c361fd124f" />
- 기존코드
  - <img width="560" height="347" alt="2_추천" src="https://github.com/user-attachments/assets/16b592a4-e9ee-4a52-8881-8da88f24f35c" />
