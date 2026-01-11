import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import os

import joblib
from autointmlp3 import AutoIntMLPModel, predict_model
from tensorflow.keras.models import load_model

# streamlit run show_st.py 

@st.cache_resource
@st.cache_resource
def load_data():
    project_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(project_path, 'data')
    model_path = os.path.join(project_path, 'model')
    movielens_path = os.path.join(data_path, 'ml-1m')
    
    # 1. 데이터 로드 (최신 파일 사용)
    field_dims = np.load(os.path.join(data_path, 'field_dims2.npy'))
    
    ratings_df = pd.read_csv(os.path.join(movielens_path, 'ratings_prepro.csv'))
    movies_df = pd.read_csv(os.path.join(movielens_path, 'movies_prepro.csv'))
    user_df = pd.read_csv(os.path.join(movielens_path, 'users_prepro.csv'))
    
    label_encoders = joblib.load(os.path.join(data_path, 'label_encoders2.pkl'))

    # --------------------------------------------------------------------------
    # [추가] 통계 피처 매핑 생성 (학습 코드와 동일 로직)
    # --------------------------------------------------------------------------
    movie_grp = ratings_df.groupby('movie_id')['rating']
    movie_pop_bins = pd.qcut(movie_grp.count().apply(np.log1p), 10, labels=False, duplicates='drop').to_dict()
    movie_rate_bins = pd.qcut(movie_grp.mean(), 10, labels=False, duplicates='drop').to_dict()
    
    user_grp = ratings_df.groupby('user_id')['rating']
    user_act_bins = pd.qcut(user_grp.count().apply(np.log1p), 10, labels=False, duplicates='drop').to_dict()
    user_rate_bins = pd.qcut(user_grp.mean(), 10, labels=False, duplicates='drop').to_dict()
    
    stats_maps = {
        'movie_pop': movie_pop_bins, 'movie_rate': movie_rate_bins,
        'user_act': user_act_bins, 'user_rate': user_rate_bins
    }

    # 2. 모델 파라미터 수정 (학습 설정과 일치시키기)
    embed_dim = 64
    dropout = 0.5
    dnn_hidden_units = (32, 32) # (32, 32) -> (128, 64)로 변경

    model = AutoIntMLPModel(
        field_dims=field_dims, 
        embedding_size=embed_dim, 
        att_layer_num=3, 
        att_head_num=2, 
        att_res=True, 
        dnn_hidden_units=dnn_hidden_units, 
        dnn_activation='gelu', # activation 확인
        l2_reg_dnn=0, 
        l2_reg_embedding=1e-5, 
        dnn_use_bn=True, 
        dnn_dropout=dropout, 
        init_std=0.0001
    )
    
    # Build
    model(tf.zeros((1, len(field_dims)), dtype=tf.int64))

    # 가중치 로드
    weights_path = os.path.join(model_path, 'autoIntMLP_model5_weights.weights.h5')
    try:
        model.load_weights(weights_path)
    except Exception as e:
        st.error(f"가중치 로드 실패: {e}")
    
    # [변경] stats_maps 반환 추가
    return user_df, movies_df, ratings_df, model, label_encoders, stats_maps


def get_user_seen_movies(ratings_df):
    '''
    사용자가 과거에 보았던 영화 리스트를 가져옵니다.
    '''
    user_seen_movies = ratings_df.groupby('user_id')['movie_id'].apply(list).reset_index()
    return user_seen_movies

def get_user_non_seed_dict(movies_df, user_df, user_seen_movies):
    '''
    사용자가 보지 않았던 영화 리스트를 가져옵니다.
    '''
    unique_movies = movies_df['movie_id'].unique()
    unique_users = user_df['user_id'].unique()
    user_non_seen_dict = dict()

    for user in unique_users:
        user_seen_movie_list = user_seen_movies[user_seen_movies['user_id'] == user]['movie_id'].values[0]
        user_non_seen_movie_list = list(set(unique_movies) - set(user_seen_movie_list))
        # user_non_seen_dict[user] = user_non_seen_movie_list
        
    return user_non_seen_dict


def get_user_info(user_id):
    '''
    사용자 정보를 가져옵니다.
    '''
    return users_df[users_df['user_id'] == user_id]

def get_user_past_interactions(user_id):
    '''
    사용자 평점 데이터 중 4점 이상(선호했다는 정보)만 가져옵니다. 
    '''
    return ratings_df[ (ratings_df['user_id'] == user_id) & (ratings_df['rating'] >= 4)].merge(movies_df, on='movie_id')


def get_recom(user_id, user_non_seen_dict, users_df, movies_df, r_year, r_month, model, label_encoders, stats_maps):
    # 1. 입력된 user_id를 무조건 문자열로 변환
    user_id = str(user_id)
    
    # 안 본 영화 리스트 (즉석 계산 로직)
    if user_id in user_non_seen_dict:
        user_non_seen_movie = user_non_seen_dict[user_id]
    else:
        # movies_df의 movie_id도 문자열로 변환 후 집합 생성
        all_movies = set(movies_df['movie_id'].astype(str).unique())
        try:
            # ratings_df의 user_id/movie_id도 문자열 기준 필터링
            # (주의: ratings_df는 함수 인자로 넘어오지 않고 전역변수를 참조중입니다. 
            #  이 경우 load_data에서 이미 str로 로드했으므로 괜찮지만 안전을 위해 처리)
            seen = set(ratings_df[ratings_df['user_id'].astype(str) == user_id]['movie_id'].astype(str))
            user_non_seen_movie = list(all_movies - seen)
        except:
            user_non_seen_movie = list(all_movies)
            
    if not user_non_seen_movie:
        return pd.DataFrame()

    # --------------------------------------------------------------------------
    # [핵심 수정] Merge 에러 방지를 위한 강제 형변환 (모두 문자열로 통일)
    # --------------------------------------------------------------------------
    
    # 1. 영화 데이터 병합 준비
    candidate_movies = pd.DataFrame({'movie_id': user_non_seen_movie})
    candidate_movies['movie_id'] = candidate_movies['movie_id'].astype(str) # 강제 문자열 변환
    movies_df['movie_id'] = movies_df['movie_id'].astype(str)               # 강제 문자열 변환
    
    candidate_movies = pd.merge(candidate_movies, movies_df, on='movie_id')
    
    # 2. 유저 데이터 병합 준비 (에러 발생했던 지점 해결)
    user_id_list = [user_id] * len(candidate_movies) # candidate_movies 길이에 맞춤
    user_info = pd.DataFrame({'user_id': user_id_list})
    
    user_info['user_id'] = user_info['user_id'].astype(str) # 강제 문자열 변환
    users_df['user_id'] = users_df['user_id'].astype(str)   # 강제 문자열 변환
    
    user_info = pd.merge(user_info, users_df, on='user_id')
    
    # --------------------------------------------------------------------------
    
    # 3. 데이터 병합 (Concat)
    # 인덱스 리셋을 해줘야 엉뚱한 행끼리 붙지 않음
    candidate_movies.reset_index(drop=True, inplace=True)
    user_info.reset_index(drop=True, inplace=True)
    
    # 메타 데이터 생성
    user_info['rating_year'] = r_year
    user_info['rating_month'] = r_month
    
    merge_data = pd.concat([candidate_movies, user_info], axis=1)
    merge_data.fillna('no', inplace=True)
    
    # 4. 피처 엔지니어링 (통계/시간/교차)
    # map을 할 때도 key가 문자열이어야 함
    merge_data['movie_pop'] = merge_data['movie_id'].map(stats_maps['movie_pop']).fillna(0).astype(int)
    merge_data['movie_rate'] = merge_data['movie_id'].map(stats_maps['movie_rate']).fillna(5).astype(int)
    merge_data['user_act'] = merge_data['user_id'].map(stats_maps['user_act']).fillna(0).astype(int)
    merge_data['user_rate'] = merge_data['user_id'].map(stats_maps['user_rate']).fillna(5).astype(int)
    
    if merge_data['movie_year'].dtype == object:
        merge_data['movie_year'] = pd.to_numeric(merge_data['movie_year'], errors='coerce').fillna(2000).astype(int)
    merge_data['release_lag'] = (merge_data['rating_year'] - merge_data['movie_year']).apply(lambda x: max(0, x)//5)
    
    merge_data['age_gender'] = merge_data['age'].astype(str) + "_" + merge_data['gender'].astype(str)
    merge_data['age_genre'] = merge_data['age'].astype(str) + "_" + merge_data['genre1'].astype(str)
    
    # (구버전 호환)
    merge_data['movie_decade'] = merge_data['movie_year'].apply(lambda x: str(x - (x % 10)) + 's')
    
    # 5. 컬럼 선택
    target_columns = [
        'user_id', 'movie_id', 
        'movie_decade', 'movie_year', 
        'rating_year', 'rating_month', 
        'genre1', 'genre2', 'genre3', 
        'gender', 'age', 'occupation', 'zip',
        'age_gender', 'age_genre',
        'movie_pop', 'user_act', 'release_lag'
    ]
    
    final_cols = [col for col in target_columns if col in merge_data.columns]
    merge_data = merge_data[final_cols]
    
    # 6. Label Encoding Transform
    for col, le in label_encoders.items():
        if col in merge_data.columns:
            merge_data[col] = merge_data[col].astype(str)
            mapping = dict(zip(le.classes_, le.transform(le.classes_)))
            merge_data[col] = merge_data[col].map(mapping).fillna(0).astype(int)

    # 7. Predict
    recom_top = predict_model(model, merge_data)
    
    recom_movie_indices = [r[0] for r in recom_top]
    origin_m_id = label_encoders['movie_id'].inverse_transform(recom_movie_indices)
    
    # 결과 반환 (이때도 movie_id는 문자열이어야 함)
    return movies_df[movies_df['movie_id'].astype(str).isin(origin_m_id)]

# 데이터 로드
users_df, movies_df, ratings_df, model, label_encoders, stats_maps = load_data()
user_seen_movies = get_user_seen_movies(ratings_df)
user_non_seen_dict = {}

# 타이틀
st.title("영화 추천 결과 살펴보기")

st.header("사용자 정보를 넣어주세요.")
user_id = st.number_input("사용자 ID 입력", min_value=users_df['user_id'].min(), max_value=users_df['user_id'].max(), value=users_df['user_id'].min())
r_year = st.number_input("추천 타겟 연도 입력", min_value=ratings_df['rating_year'].min(), max_value=ratings_df['rating_year'].max(), value=ratings_df['rating_year'].min())
r_month = st.number_input("추천 타겟 월 입력", min_value=ratings_df['rating_month'].min(), max_value=ratings_df['rating_month'].max(), value=ratings_df['rating_month'].min())
 

# streamlit run show_st.py --client.showErrorDetails=false
if st.button("추천 결과 보기"):
    st.write("사용자 기본 정보")
    user_info = get_user_info(user_id)
    st.dataframe(user_info)

    st.write("샤용자가 과거에 봤던 이력(평점 4점 이상)")
    user_interactions = get_user_past_interactions(user_id)
    st.dataframe(user_interactions)

    st.write("추천 결과")
    recommendations = get_recom(user_id, user_non_seen_dict, users_df, movies_df, r_year, r_month, model, label_encoders, stats_maps)
    
    st.dataframe(recommendations)
