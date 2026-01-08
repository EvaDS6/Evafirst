
✨ 파라미터 튜닝 실험

1. AutoIntMLPModel call 메서드에 training인자를 전달하여, 과적합방지
2. 임베딩 레이어 초기화 수정 (FeaturesEmbedding) build함수 대신 표준 keras방식으로 변경
3. Layer Nomalization 추가. Self-Attention구조 (Transformer계열)에서는 성능개선 가능
4. 활성화 함수 relu에서 gelu로 변경

✨ 실험 결과
  - ndcg : 0.66381 ( 0.66142 기존대비 0.3%개선)
  - hitrate : 0.63184 ( 0.62982 기존대비 0.3%개선)

- 품질 비교
  - ID 10번의 2001년 1월 시청한 영화 목록으로 비교
  - ID 10번 유저는 1980~90년대 코미디, 드라마, 액션 장르 순서로 영화를 많이 시청한것으로 파악된다.
     <img width="569" height="597" alt="1" src="https://github.com/user-attachments/assets/a9dbd0a2-0b57-48d8-b163-a761558948c3" />

  - 기존 코드에서는 장르에 주목해서 드라마, 코미디 장르 위주 영화를 추천해주었다.
  - 반면 실험 코드에서는 영화 제작년도에 주목해서 1990년도 영화 위주로 추천해주었다.
 
- 실험코드
   <img width="558" height="343" alt="1_추천" src="https://github.com/user-attachments/assets/2e95db82-ad44-47fa-b7d5-28c361fd124f" />
- 기존코드
   <img width="560" height="347" alt="2_추천" src="https://github.com/user-attachments/assets/16b592a4-e9ee-4a52-8881-8da88f24f35c" />
