import pandas as pd
# gt 패키지는 Python에서 직접적인 대체재가 다양함 (예: tabulate, PrettyTable, pandas Styler)
# 여기서는 간단한 pandas DataFrame 출력 및 스타일링으로 대체.
# readr은 pandas의 read_csv 등으로 대체.

# 0. 원본 R 코드의 지저분한 부분 (Python으로 유사하게 재현 후 정리)

# 가정: adsl_saf는 이미 로드되어 있다고 가정 (이전 스크립트들에서 사용)
# 여기서는 설명을 위해 다시 로드 (실제로는 한 번만 로드)
try:
    adsl = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
    if 'SAFFL' in adsl.columns:
        adsl_saf_py = adsl[adsl['SAFFL'] == "Y"].copy()
        print("adsl_saf_py 데이터 로드 및 필터링 완료.")
    else:
        print("SAFFL 열이 adsl 데이터에 없습니다.")
        adsl_saf_py = pd.DataFrame()
except Exception as e:
    print(f"ADSL 데이터 읽기 오류: {e}")
    adsl_saf_py = pd.DataFrame()

# --- 원본 R 코드의 지저분한 부분 (Python으로 유사하게 재현) ---
# 이 부분은 R 코드의 스타일 문제를 보여주기 위함이므로, Python으로 직접 번역보다는
# Python에서 유사한 스타일 문제를 가진 코드를 작성하고 정리하는 과정을 보여줌.

# 예시: 지저분한 Python 코드 (R 코드의 문제점 일부 반영)
if not adsl_saf_py.empty:
    BIG_N_CNT_PY = adsl_saf_py.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N') # snake_case, camelCase 혼용

    # 성별 각 범주에 대한 개수 계산 (주석 스타일 R과 유사)
    small_n_cnt_py = adsl_saf_py.groupby(['TRT01AN', 'TRT01A', 'SEX']).size().reset_index(name='n')
    # print(small_n_cnt_py) # 불필요한 print

    adsl_mrg_cnt_py = pd.merge(small_n_cnt_py, BIG_N_CNT_PY, on=['TRT01A', 'TRT01AN'], how='left')
    # 매우 긴 한 줄짜리 연산 (R 코드의 긴 파이프라인 모방)
    adsl_mrg_cnt_py = adsl_mrg_cnt_py.assign(
        perc=lambda x: (x['n'] / x['N'] * 100).round(1),
        perc_char=lambda x: x['perc'].apply(lambda y: f"{y:.1f}")
    ).assign(npct=lambda x: x['n'].astype(str) + " (" + x['perc_char'] + ")") \
     .replace({'SEX': {"M": "Male", "F": "Female"}}) \
     [['TRT01A', 'SEX', 'npct']].pivot_table(index='SEX', columns='TRT01A', values='npct', aggfunc='first').reset_index()
    adsl_mrg_cnt_py.columns.name = None
    print("\n--- 지저분한 코드 실행 결과 (SEX) ---")
    print(adsl_mrg_cnt_py)

    # AGEGR1에 대한 유사한 코드 반복 (DRY 원칙 위반)
    if 'AGEGR1' in adsl_saf_py.columns:
        BIG_N_CNT_PY_AGE = adsl_saf_py.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N') # 변수명 재사용 혼란
        small_n_cnt_py_age = adsl_saf_py.groupby(['TRT01AN', 'TRT01A', 'AGEGR1']).size().reset_index(name='n')
        adsl_mgr_cnt_py_age = pd.merge(small_n_cnt_py_age, BIG_N_CNT_PY_AGE, on=['TRT01A', 'TRT01AN'], how='left')
        # ... (이하 유사한 긴 연산 및 피벗) ...
        # 여기서는 생략하고, 스타일 정리의 중요성을 강조

    # RACE에 대한 유사한 코드 반복
    # ... (생략) ...

# --- 코드 스타일 정리 (Pythonic 하게) ---

# 1. 들여쓰기 및 다시 포맷하기 (RStudio IDE 기능 -> Python IDE 기능)
# Python은 들여쓰기가 문법의 일부이므로 항상 중요.
# 자동 포맷터 (Black, Ruff, autopep8 등) 사용 권장.
# 예: Black 사용 시 일관된 스타일 적용.

# 2. 특정 스타일 문제 - 일관성을 유지하십시오 (Python - PEP 8)
# - 할당: `=` 사용 (Python에서는 `<-` 사용 안 함).
# - 명명 규칙: snake_case (함수, 변수), PascalCase (클래스). (PEP 8 권장)
# - 공백: 연산자 주위, 쉼표 뒤 등 (PEP 8 권장).
# - 줄 바꿈: 가독성을 위해 적절히 사용 (최대 줄 길이 PEP 8 권장 - 79자).
#   - 함수 호출 시 인자가 많으면 줄바꿈.
#   - pandas 메서드 체인 시 각 메서드 호출 후 줄바꿈.

# 예시: 정리된 함수 (DRY 원칙 적용)
def create_summary_table_py(df, group_var_name, value_var_name='npct_col'):
    """ 지정된 그룹 변수에 대해 개수 및 백분율 요약 테이블 생성 """
    if not isinstance(df, pd.DataFrame) or df.empty:
        print(f"create_summary_table_py: 입력 df가 비어있거나 유효하지 않음 ({group_var_name}).")
        return pd.DataFrame()

    required_cols = ['TRT01AN', 'TRT01A', group_var_name]
    if not all(col in df.columns for col in required_cols):
        print(f"create_summary_table_py: 필요한 열이 df에 없음 ({required_cols}) for group_var '{group_var_name}'.")
        return pd.DataFrame()

    # 전체 N 계산 (치료 그룹별)
    big_n = df.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N_total')
    if big_n.empty:
        print(f"create_summary_table_py: big_n 계산 결과가 비어있음 ({group_var_name}).")
        return pd.DataFrame()

    # 지정된 group_var_name에 대한 small n 계산
    small_n_group = df.groupby(['TRT01AN', 'TRT01A', group_var_name]).size().reset_index(name='n_group')
    if small_n_group.empty:
        print(f"create_summary_table_py: small_n_group 계산 결과가 비어있음 ({group_var_name}).")
        return pd.DataFrame()

    # 병합 및 백분율 계산
    merged_df = pd.merge(small_n_group, big_n, on=['TRT01A', 'TRT01AN'], how='left')

    # N_total이 0이거나 NA인 경우 처리
    if 'n_group' not in merged_df.columns or 'N_total' not in merged_df.columns or \
       merged_df['N_total'].isnull().any() or (merged_df['N_total'] == 0).any():
        print(f"create_summary_table_py: 병합된 df에 n_group 또는 N_total 문제 ({group_var_name}).")
        merged_df[value_var_name] = merged_df.get('n_group', pd.Series(dtype='int')).astype(str) + " (N/A)"
    else:
        merged_df['perc'] = (merged_df['n_group'] / merged_df['N_total'] * 100).round(1)
        merged_df['perc_char'] = merged_df['perc'].apply(lambda x: f"{x:.1f}")
        merged_df[value_var_name] = merged_df['n_group'].astype(str) + " (" + merged_df['perc_char'] + ")"

    # group_var_name이 'SEX'인 경우 특별 처리 (재코딩)
    if group_var_name == 'SEX':
        sex_map = {"M": "Male", "F": "Female", "U": "Unknown", "UNDIFFERENTIATED": "Unknown"}
        merged_df[group_var_name] = merged_df[group_var_name].replace(sex_map)

    # 최종 테이블 피벗
    # 피벗 전에 필요한 열만 선택
    pivot_input_df = merged_df[['TRT01A', group_var_name, value_var_name]]
    if pivot_input_df.empty:
        print(f"create_summary_table_py: 피벗 입력 데이터가 비어있음 ({group_var_name}).")
        return pd.DataFrame()

    try:
        summary_pivot = pivot_input_df.pivot_table(
            index=group_var_name,
            columns='TRT01A',
            values=value_var_name,
            aggfunc='first' # 중복이 없다고 가정
        ).reset_index()
        summary_pivot.columns.name = None # 컬럼 인덱스 이름 제거
        return summary_pivot
    except Exception as e:
        print(f"create_summary_table_py 피벗 오류 ({group_var_name}): {e}")
        return pd.DataFrame()

print("\n--- 정리된 함수를 사용한 결과 ---")
if not adsl_saf_py.empty:
    # SEX에 대한 요약 테이블
    summary_sex = create_summary_table_py(adsl_saf_py, 'SEX')
    if not summary_sex.empty:
        print("\nSEX 요약 테이블:")
        print(summary_sex)

    # AGEGR1에 대한 요약 테이블
    if 'AGEGR1' in adsl_saf_py.columns:
        summary_agegr1 = create_summary_table_py(adsl_saf_py, 'AGEGR1')
        if not summary_agegr1.empty:
            print("\nAGEGR1 요약 테이블:")
            print(summary_agegr1)
    else:
        print("\nAGEGR1 열이 없어 요약 테이블을 생성할 수 없습니다.")

    # RACE에 대한 요약 테이블
    if 'RACE' in adsl_saf_py.columns:
        summary_race = create_summary_table_py(adsl_saf_py, 'RACE')
        if not summary_race.empty:
            print("\nRACE 요약 테이블:")
            print(summary_race)
    else:
        print("\nRACE 열이 없어 요약 테이블을 생성할 수 없습니다.")
else:
    print("\n정리된 함수 테스트를 위한 adsl_saf_py 데이터가 비어있습니다.")


# 3. 주석 확인 (Python - docstrings 및 # 주석)
# 함수에는 docstring을 사용하여 목적, 인수, 반환 값 등을 설명.
# 코드 라인에는 `#`를 사용하여 설명 추가.
# R과 마찬가지로 주석은 최신 상태로 유지해야 함.

# 4. 필요한 것보다 많은 라이브러리를 로드하지 마십시오. (Python - 필요한 모듈만 import)
# R과 동일한 원칙. `import pandas as pd` 처럼 필요한 것만 가져옴.
# `from somelib import *` (와일드카드 import)는 피하는 것이 좋음 (네임스페이스 충돌).

# 5. 반복하지 마십시오 - DRY (Don't Repeat Yourself) 원칙
# 위 `create_summary_table_py` 함수가 이 원칙을 적용한 예.
# R 코드의 오타 (`adsl_mgr_cnt` vs `adsl_mrg_cnt`)는 Python에서도 발생 가능.
# 일관된 변수명, 함수 사용, 코드 재사용으로 줄일 수 있음.
# BIG_N_CNT_PY를 반복 계산하는 것은 비효율적. 함수 내에서 한 번만 계산하거나,
# 더 상위 레벨에서 계산하여 인자로 전달하는 것이 좋음 (위 함수에서 개선).

# 추가: R의 gt 패키지 -> Python의 pandas Styler 객체
# pandas Styler는 DataFrame 표시에 다양한 스타일 적용 가능.
# 예: summary_sex.style.set_caption("SEX 요약").hide(axis="index").set_table_styles(...)
# Jupyter Notebook 등에서 HTML로 렌더링될 때 효과적.
if 'summary_sex' in locals() and not summary_sex.empty:
    print("\nSEX 요약 테이블 (Styler 객체로 HTML 출력 가능 - 여기서는 텍스트):")
    # styled_summary_sex = summary_sex.style.set_caption("성별 요약") \
    #                                    .format(precision=1) # 예시: 소수점 1자리
    # print(styled_summary_sex.to_html()) # Jupyter 등에서 HTML로 표시
    print(summary_sex.to_string()) # 콘솔 출력용


# R의 session_info() 또는 {logrx} -> Python의 session-info, platform, 패키지 버전 직접 확인
# import session_info
# session_info.show() # 설치 필요: pip install session-info
# 또는:
import platform
import pandas as pd_version_check # pandas 이름 충돌 피하기 위해 별칭
print(f"\n--- Python 세션 정보 (일부) ---")
print(f"Python 버전: {platform.python_version()}")
print(f"Pandas 버전: {pd_version_check.__version__}")
# 필요한 다른 라이브러리 버전도 유사하게 확인 가능.

# `pip install pandas pyreadstat session-info` 필요할 수 있음.
# 이 스크립트는 R 코드의 스타일 문제를 Python 관점에서 어떻게 해결하고,
# PEP 8 및 DRY 원칙을 적용하여 더 깨끗하고 유지보수하기 쉬운 코드를 작성하는지 보여줌.
# 자동 포맷터(Black, Ruff 등) 사용은 Python 개발에서 매우 일반적.
