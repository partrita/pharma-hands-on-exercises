import pandas as pd
import pytest # testthat 대신 Python의 표준 테스트 프레임워크 pytest 사용

# 0. 테스트 대상 함수 정의 (MiniProject12_Example의 R 코드에 해당)
#    Python에서는 이러한 함수들을 별도의 .py 파일 (예: my_functions.py)에 저장하고 import.
#    여기서는 설명을 위해 이 파일에 직접 정의.

# wrangle_data 함수
def wrangle_data_py(input_df):
    if not isinstance(input_df, pd.DataFrame):
        # raise TypeError("입력값은 pandas DataFrame이어야 합니다.")
        print("wrangle_data_py: 입력값은 pandas DataFrame이어야 합니다.")
        return pd.DataFrame()

    # 실제 R 코드의 로직을 따라야 함. 여기서는 예시로 SAFFL 필터링 및 열 선택 가정.
    # MiniProject12_Example/R/functions.R 의 wrangle_data 와 유사하게
    if 'SAFFL' not in input_df.columns:
        print("wrangle_data_py: SAFFL 열이 없습니다.")
        return pd.DataFrame()

    processed_df = input_df[input_df['SAFFL'] == 'Y'].copy()

    # MiniProject12_Example에서는 특정 열을 선택하지 않음.
    # 만약 선택한다면:
    # required_cols = ["STUDYID", "USUBJID", "SEX", "TRT01A", "TRT01AN", "SAFFL"]
    # if not all(col in processed_df.columns for col in required_cols):
    #     print("wrangle_data_py: 선택할 열 중 일부가 없습니다.")
    #     # 필요한 열만 선택하거나, 오류 처리
    #     cols_to_select = [col for col in required_cols if col in processed_df.columns]
    #     if not cols_to_select: return pd.DataFrame()
    #     return processed_df[cols_to_select]

    return processed_df

# calculate_Big_N_cnt 함수
def calculate_big_n_cnt_py(adsl_data_df):
    if not isinstance(adsl_data_df, pd.DataFrame) or adsl_data_df.empty:
        print("calculate_big_n_cnt_py: 입력 데이터프레임이 비어있거나 유효하지 않습니다.")
        return pd.DataFrame()
    if not all(col in adsl_data_df.columns for col in ['TRT01AN', 'TRT01A']):
        print("calculate_big_n_cnt_py: TRT01AN 또는 TRT01A 열이 없습니다.")
        return pd.DataFrame()

    big_n_df = adsl_data_df.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N')
    return big_n_df

# calculate_small_n_cnt 함수
def calculate_small_n_cnt_py(adsl_data_df):
    if not isinstance(adsl_data_df, pd.DataFrame) or adsl_data_df.empty:
        print("calculate_small_n_cnt_py: 입력 데이터프레임이 비어있거나 유효하지 않습니다.")
        return pd.DataFrame()
    if not all(col in adsl_data_df.columns for col in ['TRT01AN', 'TRT01A', 'SEX']):
        print("calculate_small_n_cnt_py: TRT01AN, TRT01A 또는 SEX 열이 없습니다.")
        return pd.DataFrame()

    small_n_df = adsl_data_df.groupby(['TRT01AN', 'TRT01A', 'SEX']).size().reset_index(name='n')
    return small_n_df

# adsl_counts 함수 (MiniProject12의 Rmd에서 단순화된 버전)
# 이 함수는 Big_N_cnt와 small_n_cnt를 인자로 받도록 수정됨 (Rmd와 동일)
def adsl_counts_py(big_n_df, small_n_df): # adsl_data 인자 제거
    if not isinstance(big_n_df, pd.DataFrame) or big_n_df.empty or \
       not isinstance(small_n_df, pd.DataFrame) or small_n_df.empty:
        print("adsl_counts_py: big_n_df 또는 small_n_df가 비어있거나 유효하지 않습니다.")
        return pd.DataFrame()

    if not all(col in big_n_df.columns for col in ['TRT01AN', 'TRT01A', 'N']) or \
       not all(col in small_n_df.columns for col in ['TRT01AN', 'TRT01A', 'SEX', 'n']):
        print("adsl_counts_py: 필요한 열이 big_n_df 또는 small_n_df에 없습니다.")
        return pd.DataFrame()

    adsl_mrg_df = pd.merge(small_n_df, big_n_df, on=['TRT01A', 'TRT01AN'], how='left')

    if 'n' not in adsl_mrg_df.columns or 'N' not in adsl_mrg_df.columns or \
       adsl_mrg_df['N'].isnull().any() or (adsl_mrg_df['N'] == 0).any():
        print("adsl_counts_py: 병합 후 n 또는 N 열 문제로 백분율 계산 불가.")
        adsl_mrg_df['perc'] = 0.0 # 또는 np.nan 처리
    else:
        adsl_mrg_df['perc'] = (adsl_mrg_df['n'] / adsl_mrg_df['N'] * 100).round(1)

    # SEX 재코딩 (Rmd 예제에 있음)
    if 'SEX' in adsl_mrg_df.columns:
        sex_map = {"M": "Male", "F": "Female", "U": "Unknown", "UNDIFFERENTIATED":"Unknown"} # 예시 맵
        # 원본 R 코드에는 Female, Male만 있었으나, test_data_py에는 U, UNDIFFERENTIATED도 있음
        adsl_mrg_df['SEX'] = adsl_mrg_df['SEX'].replace(sex_map)


    # 최종 열 선택
    if not all(col in adsl_mrg_df.columns for col in ['TRT01A', 'SEX', 'perc']):
        print("adsl_counts_py: 최종 선택할 열(TRT01A, SEX, perc) 중 일부가 없습니다.")
        return adsl_mrg_df # 가능한 부분 결과 반환

    return adsl_mrg_df[['TRT01A', 'SEX', 'perc']]


# 테스트 데이터 준비
# PHUSE 데이터 로드 (실제 테스트 시에는 고정된 테스트 파일 사용 권장)
try:
    phuse_data_py = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
except Exception as e:
    print(f"PHUSE 데이터 읽기 오류: {e}")
    phuse_data_py = pd.DataFrame()

# MiniProject12_Rmd에서 사용된 테스트 데이터 (Python DataFrame으로)
test_data_py = pd.DataFrame({
    'STUDYID': ["CDISCPILOT01"] * 8,
    'TRT01AN': [1, 1, 2, 1, 1, 2, 2, 1],
    'TRT01A': ["Treatment A", "Treatment A", "Treatment B", "Treatment A",
               "Treatment A", "Treatment B", "Treatment B", "Treatment A"],
    'SEX': ['Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
    'SAFFL': ['Y'] * 8, # wrangle_data_py 테스트용
    'USUBJID': [f"01-701-101{i}" for i in range(5,13)] # 고유 ID 추가
})
# 테스트 데이터에 UNDIFFERENTIATED, U 추가 (Rmd의 test-adsl_counts.R 참고)
test_data_u = pd.DataFrame({
    'STUDYID': ["CDISCPILOT01"]*2, 'TRT01AN': [3,3], 'TRT01A': ["Treatment C"]*2,
    'SEX': ['U', 'UNDIFFERENTIATED'], 'SAFFL': ['Y']*2, 'USUBJID': ["01-701-1013", "01-701-1014"]
})
test_data_py_extended = pd.concat([test_data_py, test_data_u], ignore_index=True)


# 테스트 함수 (pytest 스타일: test_*.py 파일에 test_* 함수로 정의)
# 이 파일이 test_mini_project12.py 라면 pytest 실행 시 자동 발견됨.

# --- wrangle_data_py 테스트 ---
def test_wrangle_data_output_saffl():
    """wrangle_data_py 결과 SAFFL 열은 'Y' 값만 가져야 함"""
    if phuse_data_py.empty:
        pytest.skip("PHUSE 원본 데이터 로드 실패")
    adsl_data_processed = wrangle_data_py(phuse_data_py)
    if adsl_data_processed.empty:
        # 함수 내에서 이미 print로 경고했을 수 있음, 추가적인 assert로 실패 명시
        assert False, "wrangle_data_py가 빈 데이터프레임을 반환했습니다 (SAFFL 테스트용)."

    assert adsl_data_processed['SAFFL'].unique().tolist() == ['Y'], "SAFFL 열에 'Y' 이외의 값이 포함됨"
    assert adsl_data_processed['SAFFL'].isnull().sum() == 0, "SAFFL 열에 NA 값이 포함됨"

def test_wrangle_data_output_columns():
    """wrangle_data_py 결과는 특정 수의 열을 가져야 함 (Rmd 예제에서는 6개, 여기서는 원본 유지 가정)"""
    if phuse_data_py.empty:
        pytest.skip("PHUSE 원본 데이터 로드 실패")
    adsl_data_processed = wrangle_data_py(phuse_data_py)
    if adsl_data_processed.empty:
         assert False, "wrangle_data_py가 빈 데이터프레임을 반환했습니다 (컬럼 수 테스트용)."
    # MiniProject12_Example/R/functions.R의 wrangle_data는 열을 선택하지 않음.
    # 따라서 원본 phuse_data_py와 동일한 열 수를 기대 (SAFFL='Y' 필터링만)
    expected_cols = phuse_data_py.columns.tolist() # 모든 열
    assert len(adsl_data_processed.columns) == len(expected_cols)
    # 특정 열 존재 여부 테스트 (Rmd의 expected_vars와 유사)
    expected_vars_py = ["TRT01AN", "TRT01A", "SEX"] # 예시
    assert all(col in adsl_data_processed.columns for col in expected_vars_py)


# --- calculate_Big_N_cnt_py 테스트 ---
def test_calculate_big_n_cnt_output_structure():
    """calculate_big_n_cnt_py 결과 구조 테스트"""
    big_n_result = calculate_big_n_cnt_py(test_data_py)
    if big_n_result.empty and not test_data_py.empty : # 입력이 있는데 결과가 비면 문제
        assert False, "calculate_big_n_cnt_py가 빈 데이터프레임을 반환했습니다."
    elif test_data_py.empty and big_n_result.empty: # 입력이 비어서 결과도 비면 정상
        return

    assert list(big_n_result.columns) == ["TRT01AN", "TRT01A", "N"]
    # 행 수: 고유 (TRT01AN, TRT01A) 조합 수
    expected_rows = len(test_data_py[['TRT01AN', 'TRT01A']].drop_duplicates())
    assert len(big_n_result) == expected_rows
    assert pd.api.types.is_integer_dtype(big_n_result['N'])

def test_calculate_big_n_cnt_calculation():
    """calculate_big_n_cnt_py 계산 정확성 테스트"""
    big_n_result = calculate_big_n_cnt_py(test_data_py)
    if big_n_result.empty and not test_data_py.empty:
        assert False, "calculate_big_n_cnt_py가 빈 데이터프레임을 반환했습니다 (계산 테스트용)."
    elif test_data_py.empty and big_n_result.empty:
        return

    # test_data_py에서 Treatment A (TRT01AN=1)는 5개, Treatment B (TRT01AN=2)는 3개
    # 결과는 TRT01AN 순서대로 정렬된다고 가정 (groupby 기본 동작)
    # 실제 값 확인 (더 견고한 방식은 TRT01A 값으로 필터링하여 확인)
    val_A = big_n_result[big_n_result['TRT01A'] == 'Treatment A']['N'].iloc[0]
    val_B = big_n_result[big_n_result['TRT01A'] == 'Treatment B']['N'].iloc[0]
    assert val_A == 5
    assert val_B == 3


# --- calculate_small_n_cnt_py 테스트 ---
def test_calculate_small_n_cnt_output_structure():
    """calculate_small_n_cnt_py 결과 구조 테스트"""
    small_n_result = calculate_small_n_cnt_py(test_data_py)
    if small_n_result.empty and not test_data_py.empty:
         assert False, "calculate_small_n_cnt_py가 빈 데이터프레임을 반환했습니다."
    elif test_data_py.empty and small_n_result.empty:
        return

    assert list(small_n_result.columns) == ["TRT01AN", "TRT01A", "SEX", "n"]
    expected_rows = len(test_data_py[['TRT01AN', 'TRT01A', 'SEX']].drop_duplicates())
    assert len(small_n_result) == expected_rows
    assert pd.api.types.is_integer_dtype(small_n_result['n'])

def test_calculate_small_n_cnt_calculation():
    """calculate_small_n_cnt_py 계산 정확성 테스트"""
    small_n_result = calculate_small_n_cnt_py(test_data_py)
    if small_n_result.empty and not test_data_py.empty:
        assert False, "calculate_small_n_cnt_py가 빈 데이터프레임을 반환했습니다 (계산 테스트용)."
    elif test_data_py.empty and small_n_result.empty:
        return

    # 예: Treatment A, Female
    val_A_F = small_n_result[(small_n_result['TRT01A'] == 'Treatment A') & (small_n_result['SEX'] == 'Female')]['n'].iloc[0]
    assert val_A_F == 2 # test_data_py에서 (A, Female)은 2건
    # 예: Treatment B, Male
    val_B_M = small_n_result[(small_n_result['TRT01A'] == 'Treatment B') & (small_n_result['SEX'] == 'Male')]['n'].iloc[0]
    assert val_B_M == 1 # test_data_py에서 (B, Male)은 1건

def test_big_n_equals_sum_of_small_n():
    """Big_N 값은 해당 치료 그룹의 small_n 값들의 합과 같아야 함"""
    big_n_df = calculate_big_n_cnt_py(test_data_py)
    small_n_df = calculate_small_n_cnt_py(test_data_py)

    if (big_n_df.empty or small_n_df.empty) and not test_data_py.empty:
        assert False, "big_n 또는 small_n 계산 결과가 비어있습니다."
    elif test_data_py.empty and big_n_df.empty and small_n_df.empty:
        return

    sum_small_n_by_trt = small_n_df.groupby(['TRT01AN', 'TRT01A'])['n'].sum().reset_index(name='sum_n')

    merged_check_df = pd.merge(big_n_df, sum_small_n_by_trt, on=['TRT01AN', 'TRT01A'])
    assert (merged_check_df['N'] == merged_check_df['sum_n']).all()


# --- adsl_counts_py 테스트 (도전 과제) ---
def test_adsl_counts_percentage_calculation():
    """adsl_counts_py의 백분율 계산 정확성 테스트"""
    # test_data_py_extended 사용 (U, UNDIFFERENTIATED 포함)
    big_n_res = calculate_big_n_cnt_py(test_data_py_extended)
    small_n_res = calculate_small_n_cnt_py(test_data_py_extended)

    if big_n_res.empty or small_n_res.empty:
        pytest.fail("adsl_counts_py 테스트를 위한 big_n 또는 small_n 생성 실패")

    counts_result = adsl_counts_py(big_n_res, small_n_res)
    if counts_result.empty:
        pytest.fail("adsl_counts_py가 빈 결과를 반환했습니다.")

    # Treatment A (N=5), Female (n=2) -> perc = (2/5)*100 = 40.0
    perc_A_F = counts_result[
        (counts_result['TRT01A'] == 'Treatment A') & (counts_result['SEX'] == 'Female')
    ]['perc'].iloc[0]
    assert perc_A_F == 40.0

    # Treatment B (N=3), Male (n=1) -> perc = (1/3)*100 = 33.3 (round(1))
    perc_B_M = counts_result[
        (counts_result['TRT01A'] == 'Treatment B') & (counts_result['SEX'] == 'Male')
    ]['perc'].iloc[0]
    assert perc_B_M == 33.3

    # Treatment C (N=2), Unknown (U, n=1) -> perc = (1/2)*100 = 50.0
    # adsl_counts_py 내부에서 U, UNDIFFERENTIATED가 "Unknown"으로 매핑됨
    perc_C_U = counts_result[
        (counts_result['TRT01A'] == 'Treatment C') & (counts_result['SEX'] == 'Unknown')
    ]['perc']
    # Unknown 그룹이 두 행일 수 있으므로 (원래 U, UNDIFFERENTIATED), 둘 다 50.0인지 확인
    assert len(perc_C_U) >= 1 # 최소 하나는 있어야 함
    assert (perc_C_U == 50.0).all() # 모든 Unknown 그룹의 perc가 50.0인지 확인

def test_adsl_counts_sex_recode():
    """adsl_counts_py에서 SEX 값 재코딩 확인"""
    big_n_res = calculate_big_n_cnt_py(test_data_py_extended)
    small_n_res = calculate_small_n_cnt_py(test_data_py_extended)
    counts_result = adsl_counts_py(big_n_res, small_n_res)

    if counts_result.empty:
        pytest.fail("adsl_counts_py가 빈 결과를 반환했습니다 (SEX 재코딩 테스트용).")

    # 재코딩된 SEX 값 확인 (Male, Female, Unknown 만 있어야 함)
    expected_sex_values = {'Male', 'Female', 'Unknown'}
    actual_sex_values = set(counts_result['SEX'].unique())
    assert actual_sex_values.issubset(expected_sex_values)
    # 원래 U, UNDIFFERENTIATED가 있었던 Treatment C 그룹이 Unknown으로 매핑되었는지 확인
    assert 'Unknown' in counts_result[counts_result['TRT01A'] == 'Treatment C']['SEX'].unique()


# pytest 실행 방법:
# 1. 터미널에서 `pip install pytest pandas pyreadstat` 실행.
# 2. 이 파일을 `test_mini_project12.py`와 같이 `test_`로 시작하는 이름으로 저장.
# 3. 터미널에서 이 파일이 있는 디렉터리로 이동 후 `pytest` 명령어 실행.

# 참고:
# - R의 testthat::expect_equal()은 Python의 assert a == b 와 유사.
# - testthat::expect_length()는 assert len(obj) == expected_len 과 유사.
# - testthat::expect_named()는 assert list(df.columns) == expected_names 와 유사.
# - testthat::expect_type()은 assert isinstance(obj, expected_type) 또는 pd.api.types 확인 함수와 유사.
# - testthat::expect_success(), expect_failure()는 pytest에서 예외 발생 여부 테스트 등으로 구현 가능.
#   (예: with pytest.raises(ExpectedError): ... )
# - 테스트 구성 및 실행: R 패키지 구조와 유사하게, Python 프로젝트에서도 테스트용 폴더(예: tests/)를 만들고
#   그 안에 test_*.py 파일을 넣어 구성. pytest는 이러한 파일을 자동으로 찾아 실행.
# - MiniProject12_Example 폴더 구조는 Python에서도 유사하게 구성 가능.
#   R 스크립트 -> Python 모듈 (.py 파일)
#   tests/testthat/ -> tests/ (pytest는 tests 폴더를 기본으로 인식)
#   test-*.R -> test_*.py
#   testthat.R (test_dir 실행) -> pytest 명령어 (자동으로 tests 폴더 내 테스트 실행)

# 이 스크립트는 MiniProject12_ko.Rmd의 핵심 테스트 로직을 Python과 pytest를 사용하여 변환한 예시입니다.
# 실제 프로젝트에서는 함수 정의와 테스트 코드를 별도 파일로 분리하는 것이 일반적입니다.
