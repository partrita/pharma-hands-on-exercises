import pandas as pd
import numpy as np
# skimr는 Python의 skimpy로 대체 가능 (이미 다른 파일에서 사용)
from skimpy import skim

# 0. 데이터 로드 (adsl_saf)
try:
    adsl = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
    if 'SAFFL' in adsl.columns:
        adsl_saf = adsl[adsl['SAFFL'] == "Y"].copy()
        print("adsl_saf 데이터 로드 및 필터링 완료.")
    else:
        print("SAFFL 열이 adsl 데이터에 없습니다.")
        adsl_saf = pd.DataFrame()
except Exception as e:
    print(f"ADSL 데이터 읽기 오류: {e}")
    adsl_saf = pd.DataFrame()

# R의 벡터화된 연산 예시
if not adsl_saf.empty and 'SUBJID' in adsl_saf.columns:
    # R: sum(!is.na(SUBJID))
    non_missing_subj_count = adsl_saf['SUBJID'].notna().sum()
    print(f"\nSUBJID 열의 누락되지 않은 값 수: {non_missing_subj_count}")

# 루프를 사용해야 하는 경우 (R 코드 예시의 Python 버전)
if not adsl_saf.empty:
    var_names = adsl_saf.columns.tolist()
    counts_py = {} # Python에서는 딕셔너리가 명명된 벡터와 유사하게 사용될 수 있음

    for col_name in var_names:
        counts_py[col_name] = adsl_saf[col_name].notna().sum()

    print("\n루프를 사용하여 계산된 각 열의 누락되지 않은 값 수 (처음 5개):")
    for i, (k, v) in enumerate(counts_py.items()):
        if i < 5:
            print(f"{k}: {v}")
        else:
            break

    # R의 select(STUDYID) 또는 counts[,"STUDYID"] 와 같은 접근은
    # Python 딕셔너리에서는 counts_py['STUDYID'] 또는 counts_py.get('STUDYID') 사용
    if 'STUDYID' in counts_py:
        print(f"\nSTUDYID의 누락되지 않은 값 수 (딕셔너리에서): {counts_py['STUDYID']}")

    # 루프 내에서 객체 "늘리기" (Python에서는 리스트에 append) - 비효율적일 수 있음
    # R: counts <- NULL; for(...) { counts <- c(counts, sum(!is.na(adsl_saf[i,]))) }
    # Python에서는 일반적으로 미리 크기를 알 수 없으면 리스트에 append 후 DataFrame 변환
    # 여기서는 행별 누락 값 계산 예시 (R 코드의 의도와 다를 수 있음, R은 열별 계산)
    # row_non_missing_counts = []
    # for index, row in adsl_saf.iterrows():
    #     row_non_missing_counts.append(row.notna().sum())
    # print("\n행별 누락되지 않은 값 수 (처음 5개):")
    # print(row_non_missing_counts[:5])


# apply 계열 함수 (R) -> pandas의 apply, applymap, agg 등
# R: nonMissing <- function(vector){ sum(!is.na(vector)) }
def non_missing_py(series):
    return series.notna().sum()

if not adsl_saf.empty:
    # R: lapply(adsl_saf, FUN = nonMissing) 또는 sapply(adsl_saf, FUN = nonMissing)
    # pandas에서는 DataFrame.apply()를 사용하여 열별 또는 행별 함수 적용
    col_non_missing_counts = adsl_saf.apply(non_missing_py) # 기본값 axis=0 (열별)
    print("\napply를 사용하여 계산된 각 열의 누락되지 않은 값 수 (처음 5개):")
    print(col_non_missing_counts.head())

    # R: tapply(adsl_saf$AGE, INDEX = adsl_saf$TRT01A, FUN = nonMissing)
    if 'AGE' in adsl_saf.columns and 'TRT01A' in adsl_saf.columns:
        age_non_missing_by_trt = adsl_saf.groupby('TRT01A')['AGE'].apply(non_missing_py)
        print("\nTRT01A 그룹별 AGE의 누락되지 않은 값 수:")
        print(age_non_missing_by_trt)

    # R: apply(adsl_saf, MARGIN = 2, FUN = function(x)tapply(x, INDEX = adsl_saf$TRT01A, FUN = nonMissing))
    # pandas에서는 각 열에 대해 groupby().apply()를 반복하거나, pivot_table 또는 groupby().agg() 사용
    # 예: 모든 숫자형 열에 대해 그룹별 nonMissing 계산
    if 'TRT01A' in adsl_saf.columns:
        numeric_cols = adsl_saf.select_dtypes(include=np.number).columns
        if not numeric_cols.empty:
            grouped_non_missing_all_numeric = adsl_saf.groupby('TRT01A')[numeric_cols].apply(non_missing_py)
            print("\nTRT01A 그룹별 모든 숫자형 열의 누락되지 않은 값 수 (처음 몇 개):")
            print(grouped_non_missing_all_numeric.head())
        else:
            print("\n숫자형 열이 없어 그룹별 nonMissing 계산을 수행할 수 없습니다.")


# 깔끔한 반복 (tidyverse) -> pandas 메서드 체인 및 기능
# R: across(.cols = everything(), .fns = nonMissing)
if not adsl_saf.empty:
    summary_non_missing_all = adsl_saf.apply(non_missing_py).to_frame(name='non_missing_count').T # .T로 행렬 전치
    print("\nacross와 유사: 모든 열의 누락되지 않은 값 수 요약:")
    print(summary_non_missing_all.iloc[:, :5]) # 처음 5개 열만 표시

    # R: across(.cols = any_of(c("AGE","SEX", "RACE","ETHNIC")), .fns = nonMissing)
    cols_to_summarize = ["AGE", "SEX", "RACE", "ETHNIC", "MIKE"] # "MIKE"는 없는 열 (테스트용)
    actual_cols_present = [col for col in cols_to_summarize if col in adsl_saf.columns]
    if actual_cols_present:
        summary_non_missing_selected = adsl_saf[actual_cols_present].apply(non_missing_py).to_frame(name='non_missing_count').T
        print("\nacross와 유사: 선택된 열의 누락되지 않은 값 수 요약:")
        print(summary_non_missing_selected)
    else:
        print("\n선택된 열이 데이터프레임에 없어 요약을 생성할 수 없습니다.")

    # R: across(.cols = where(is.numeric), .fns = median)
    numeric_cols_df = adsl_saf.select_dtypes(include=np.number)
    if not numeric_cols_df.empty:
        median_of_numeric = numeric_cols_df.median() # median은 Series에 직접 적용
        print("\nacross와 유사: 모든 숫자형 열의 중앙값:")
        print(median_of_numeric.head())

        # 그룹화와 함께 사용
        if 'TRT01A' in adsl_saf.columns:
            median_numeric_by_trt = adsl_saf.groupby('TRT01A').median(numeric_only=True) # numeric_only=True로 경고 방지
            print("\nacross 및 group_by와 유사: TRT01A 그룹별 숫자형 열 중앙값 (처음 몇 개):")
            print(median_numeric_by_trt.iloc[:,:4])
    else:
        print("\n숫자형 열이 없어 중앙값 계산을 수행할 수 없습니다.")

    # R: mutate(across(.cols = where(is.character), .fns = toupper))
    char_cols_df = adsl_saf.select_dtypes(include='object') # object dtype은 종종 문자열
    adsl_saf_upper = adsl_saf.copy()
    for col in char_cols_df.columns:
        # 실제 문자열 타입인지 확인 후 적용 (숫자 등이 object로 읽힐 수 있으므로)
        if pd.api.types.is_string_dtype(adsl_saf_upper[col]):
             # 결측치가 있는 경우 .str 접근자 사용 시 오류 방지를 위해 .astype(str) 사용 후 원래 NaN으로 복원 고려
            adsl_saf_upper[col] = adsl_saf_upper[col].astype(str).str.upper().replace('NAN', np.nan)


    print("\nmutate(across...)와 유사: 모든 문자열 열 대문자화 (USUBJID 처음 5개):")
    if 'USUBJID' in adsl_saf_upper.columns: # USUBJID가 문자열이라고 가정
        print(adsl_saf_upper['USUBJID'].head())


# R: rowwise() 및 c_across() -> pandas의 DataFrame.apply(axis=1)
if not adsl_saf.empty and 'SUBJID' in adsl_saf.columns:
    # 각 행의 숫자형 열에 대해 누락된 값 수 계산
    # numeric_cols는 위에서 정의됨
    if not numeric_cols.empty: # numeric_cols가 정의되었는지 확인
        adsl_saf['missing_numeric_rowwise'] = adsl_saf[numeric_cols].isnull().sum(axis=1)
        print("\nrowwise 및 c_across와 유사: 각 행의 숫자형 열 중 누락된 값 수 (처음 5개):")
        print(adsl_saf[['SUBJID', 'missing_numeric_rowwise']].head())
    else:
        print("\n숫자형 열이 없어 행별 누락 값 계산을 수행할 수 없습니다.")


# map을 사용하여 {purrr} 함수 만들기 -> Python의 map(), list comprehensions, DataFrame.groupby().apply()
if not adsl_saf.empty and 'TRT01A' in adsl_saf.columns:
    # R: adsl_saf %>% split(f = .$TRT01A) %>% purrr::map(.f = skimr::skim)
    # pandas에서는 groupby 객체에 apply를 사용하거나, 그룹별로 반복하여 함수 적용

    print("\npurrr::map과 유사한 그룹별 skimpy.skim 적용:")
    for name, group_df in adsl_saf.groupby('TRT01A'):
        print(f"\nTRT01A 그룹: {name}")
        skim(group_df) # skimpy.skim 함수 사용
        break # 너무 많은 출력을 피하기 위해 첫 그룹만 표시

# 속도 향상, 병렬화 -> Python의 multiprocessing, joblib, dask, pyspark 등
# 이 부분은 환경 설정과 복잡한 코드 구조가 필요하므로, 개념적 설명으로 대체.
# Python에서도 대규모 데이터 처리 시 병렬/분산 처리를 위한 다양한 라이브러리가 존재함.

# 도전 과제: MiniProject 7의 adsl_counts 함수를 각 RACE 값에 대해 적용
# adsl_counts_from_df_py 함수 (MiniProject7_ko.py에서 정의됨 가정) 사용
# 실제로는 해당 함수를 이 파일로 가져오거나 여기서 다시 정의해야 함.
# 여기서는 개념적 구현을 보여주기 위해 함수가 있다고 가정.

def adsl_counts_from_df_py_placeholder(df_saf_group):
    """ MiniProject7_ko.py의 adsl_counts_from_df_py 함수의 플레이스홀더 """
    if df_saf_group.empty or not all(col in df_saf_group.columns for col in ['TRT01AN', 'TRT01A', 'SEX']):
        return pd.DataFrame({'note': [f'Data for group is empty or missing columns']})

    big_n = df_saf_group.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N')
    small_n = df_saf_group.groupby(['TRT01AN', 'TRT01A', 'SEX']).size().reset_index(name='n')

    if small_n.empty or big_n.empty:
        return pd.DataFrame({'note': [f'small_n or big_n is empty for group']})

    merged_df = pd.merge(small_n, big_n, on=['TRT01AN', 'TRT01A'], how='left')

    if 'n' not in merged_df.columns or 'N' not in merged_df.columns or merged_df['N'].isnull().any() or (merged_df['N'] == 0).any():
        merged_df['npct'] = merged_df['n'].astype(str) + " (N/A)"
    else:
        merged_df['perc'] = (merged_df['n'] / merged_df['N'] * 100).round(1)
        merged_df['perc_char'] = merged_df['perc'].apply(lambda x: f"{x:.1f}")
        merged_df['npct'] = merged_df['n'].astype(str) + " (" + merged_df['perc_char'] + ")"

    sex_map = {"M": "Male", "F": "Female"} # 원본 함수에 따라 처리
    if 'SEX' in merged_df.columns:
        merged_df['SEX'] = merged_df['SEX'].replace(sex_map)

    final_df = merged_df[['TRT01A', 'SEX', 'npct']] # 원본 함수에 따라 열 선택

    try:
        pivot_df = final_df.pivot_table(index='SEX', columns='TRT01A', values='npct', aggfunc='first').reset_index()
        pivot_df.columns.name = None
        return pivot_df
    except Exception as e:
        return pd.DataFrame({'error': [f"Pivot error: {e}"]})


if not adsl_saf.empty and 'RACE' in adsl_saf.columns:
    print("\n--- 도전 과제 시작 ---")
    # RACE의 각 고유값에 대해 adsl_counts_from_df_py_placeholder 함수 적용
    # adsl_saf.groupby('RACE').apply(adsl_counts_from_df_py_placeholder)는 다중 인덱스 반환 가능성

    results_by_race = {}
    for race_value, group_df in adsl_saf.groupby('RACE'):
        print(f"\nRACE 그룹: {race_value}에 대한 adsl_counts 결과:")
        # 이 그룹(특정 RACE 값을 가진 부분집합)에 대해 SAFFL='Y' 필터링은 이미 적용됨
        # adsl_counts_from_df_py_placeholder는 이미 필터링된 adsl_saf의 부분집합을 받음
        result_for_race = adsl_counts_from_df_py_placeholder(group_df)
        if not result_for_race.empty:
            print(result_for_race)
            results_by_race[race_value] = result_for_race
        else:
            print(f"RACE 그룹 {race_value}에 대한 결과가 비어있습니다.")
            results_by_race[race_value] = pd.DataFrame({'note': ['empty result']}) # 빈 결과도 저장
    print("--- 도전 과제 종료 ---")
else:
    print("\nadsl_saf 데이터가 비어있거나 RACE 열이 없어 도전 과제를 수행할 수 없습니다.")

# `pip install pandas pyreadstat numpy skimpy` 필요할 수 있음.
# 이 스크립트는 R의 반복 관련 함수 및 개념을 Python의 pandas 기능과 매핑.
# R의 apply 계열 함수는 pandas의 .apply(), .agg(), .transform() 등으로,
# tidyverse의 across()는 .select_dtypes().apply() 또는 특정 열 선택 후 .apply() 등으로,
# purrr의 map()은 .groupby().apply() 또는 Python의 map()/list comprehension으로 유사하게 구현.
# 병렬 처리는 Python에서도 중요한 주제이며, 다양한 라이브러리로 지원됨.
# 도전 과제는 groupby().apply() 패턴을 사용하여 그룹별로 함수를 적용하는 방법을 보여줌.
# 실제 함수(adsl_counts_from_df_py)는 MiniProject7_ko.py에서 가져와야 완전한 실행 가능.
