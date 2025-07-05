import pandas as pd

# 0. 데이터 로드 및 초기 필터링 (adsl_saf)
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

# 1. 소개에서 R 코드 예제 (Python으로 변환)
if not adsl_saf.empty and all(col in adsl_saf.columns for col in ['TRT01AN', 'TRT01A', 'SEX']):
    Big_N_cnt = adsl_saf.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N')
    print("\nBig_N_cnt:")
    print(Big_N_cnt)

    small_n_cnt = adsl_saf.groupby(['TRT01AN', 'TRT01A', 'SEX']).size().reset_index(name='n')
    print("\nsmall_n_cnt:")
    print(small_n_cnt)

    if not small_n_cnt.empty and not Big_N_cnt.empty:
        adsl_mrg_cnt_df = pd.merge(small_n_cnt, Big_N_cnt, on=['TRT01AN', 'TRT01A'], how='left')
        if 'n' in adsl_mrg_cnt_df.columns and 'N' in adsl_mrg_cnt_df.columns:
            adsl_mrg_cnt_df['perc'] = (adsl_mrg_cnt_df['n'] / adsl_mrg_cnt_df['N'] * 100).round(1)
            adsl_mrg_cnt_df['perc_char'] = adsl_mrg_cnt_df['perc'].apply(lambda x: f"{x:.1f}")
            adsl_mrg_cnt_df['npct'] = adsl_mrg_cnt_df['n'].astype(str) + " (" + adsl_mrg_cnt_df['perc_char'] + ")"

            sex_map = {"M": "Male", "F": "Female"}
            adsl_mrg_cnt_df['SEX'] = adsl_mrg_cnt_df['SEX'].replace(sex_map)

            adsl_mrg_cnt_final = adsl_mrg_cnt_df[['TRT01A', 'SEX', 'npct']]

            try:
                adsl_mrg_pivot = adsl_mrg_cnt_final.pivot_table(index='SEX', columns='TRT01A', values='npct', aggfunc='first').reset_index()
                adsl_mrg_pivot.columns.name = None
                print("\n최종 adsl_mrg_pivot:")
                print(adsl_mrg_pivot)
            except Exception as e:
                print(f"피벗 오류: {e}")
        else:
            print("병합된 데이터에 n 또는 N 열이 없습니다.")
    else:
        print("small_n_cnt 또는 Big_N_cnt가 비어있어 병합/계산 불가.")
else:
    print("adsl_saf 데이터가 비어있거나 필요한 열이 없습니다 (TRT01AN, TRT01A, SEX).")


# 2. 함수 특징 설명 - Python 함수 구조와 유사점/차이점
# Python 함수: def function_name(arguments): body return value
# R 함수와 유사하게 인수, 본문, 반환 값을 가짐.
# Python의 함수 이름은 R과 마찬가지로 설명적이어야 함.
# Python의 인수는 기본값을 가질 수 있음.
# Python의 함수 본문은 들여쓰기로 구분됨.
# Python의 반환 값은 return 문으로 명시.

# 예시 myFunction1, myFunction2, myFunction3 (Python 버전)
my_data_py = pd.DataFrame({
    'Treatment': ['Placebo', 'Placebo', 'Active', 'Active'],
    'value': [1, 2, 3, 4]
})

def my_function1_py(data):
    # 이 함수는 아무것도 반환하지 않음 (R의 예시와 동일)
    output = data.groupby('Treatment').size().reset_index(name='n')
    # print(output) # R처럼 암시적으로 인쇄되지 않음

def my_function2_py(data):
    output = data.groupby('Treatment').size().reset_index(name='n')
    return output # 명시적 반환

def my_function3_py(data):
    output = data.groupby('Treatment').size().reset_index(name='n')
    try:
        output.to_csv("output_py.csv", index=False)
        print("\noutput_py.csv 파일 저장됨.")
    except Exception as e:
        print(f"CSV 파일 저장 오류: {e}")
    return output

print("\nmyFunction 예시 실행:")
my_function1_py(my_data_py) # 아무것도 출력/반환하지 않음
print("myFunction2_py 결과:")
print(my_function2_py(my_data_py))
print("myFunction3_py 결과:")
print(my_function3_py(my_data_py))


# 3. 함수 만들기 (adsl_counts Python 버전)
def adsl_counts_py(data_file_path):
    try:
        df = pd.read_sas(data_file_path)
    except Exception as e:
        print(f"데이터 파일 읽기 오류 ({data_file_path}): {e}")
        return pd.DataFrame()

    if 'SAFFL' not in df.columns or not all(col in df.columns for col in ['TRT01AN', 'TRT01A', 'SEX']):
        print("입력 데이터에 필요한 열(SAFFL, TRT01AN, TRT01A, SEX)이 없습니다.")
        return pd.DataFrame()

    df_saf = df[df['SAFFL'] == "Y"].copy()
    if df_saf.empty:
        print("SAFFL == 'Y' 조건에 맞는 데이터가 없습니다.")
        return pd.DataFrame()

    big_n = df_saf.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N')
    small_n = df_saf.groupby(['TRT01AN', 'TRT01A', 'SEX']).size().reset_index(name='n')

    if small_n.empty or big_n.empty:
        print("big_n 또는 small_n 계산 결과가 비어있습니다.")
        return pd.DataFrame()

    merged_df = pd.merge(small_n, big_n, on=['TRT01AN', 'TRT01A'], how='left')

    if 'n' not in merged_df.columns or 'N' not in merged_df.columns or merged_df['N'].isnull().any() or (merged_df['N'] == 0).any():
        print("병합된 데이터에 n 또는 N 열이 없거나, N에 null 또는 0 값이 있어 백분율 계산이 불가합니다.")
        # N이 0인 경우를 대비하여 npct만이라도 생성하도록 시도
        merged_df['npct'] = merged_df['n'].astype(str) + " (N/A)" # 백분율 계산 불가 표시
    else:
        merged_df['perc'] = (merged_df['n'] / merged_df['N'] * 100).round(1)
        merged_df['perc_char'] = merged_df['perc'].apply(lambda x: f"{x:.1f}")
        merged_df['npct'] = merged_df['n'].astype(str) + " (" + merged_df['perc_char'] + ")"

    sex_map = {"M": "Male", "F": "Female"}
    merged_df['SEX'] = merged_df['SEX'].replace(sex_map)

    final_df = merged_df[['TRT01A', 'SEX', 'npct']]

    try:
        pivot_df = final_df.pivot_table(index='SEX', columns='TRT01A', values='npct', aggfunc='first').reset_index()
        pivot_df.columns.name = None
        return pivot_df
    except Exception as e:
        print(f"최종 피벗 오류: {e}")
        return pd.DataFrame() # 피벗 실패 시 빈 데이터프레임 반환 또는 final_df 반환 고려

# 4. 함수를 CDISC 데이터셋에 적용
print("\nadsl_counts_py 함수 테스트:")
input_file_path = "https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt"
result_table_py = adsl_counts_py(input_file_path)
if not result_table_py.empty:
    print("adsl_counts_py 결과:")
    print(result_table_py)
else:
    print("adsl_counts_py 함수가 빈 결과를 반환했습니다.")

# 5. 방어적 프로그래밍
# Python에서는 try-except 블록, isinstance(), assert 등을 사용하여 방어적 프로그래밍 구현
# 함수 내부에 이미 일부 방어적 코드 (열 존재 확인, 빈 데이터프레임 처리 등) 추가됨
# 예: 파일 이름 확인
import os
def check_filename(file_path_str, expected_substring="adsl"):
    # os.path.basename을 사용하여 파일 이름만 추출
    file_name = os.path.basename(file_path_str)
    if expected_substring not in file_name:
        # R의 stop과 유사하게 예외 발생 또는 경고 출력
        # raise ValueError(f"입력 파일 이름 '{file_name}'에 '{expected_substring}'이 포함되어 있지 않습니다.")
        print(f"경고: 입력 파일 이름 '{file_name}'에 '{expected_substring}'이 포함되어 있지 않습니다.")
        return False
    return True

print("\n파일 이름 확인 테스트:")
check_filename(input_file_path) # adsl 포함, True 반환 (경고 없음)
check_filename("my_data.csv", "adsl") # adsl 미포함, False 반환 및 경고 출력

# 인수 이름 변경: Python에서도 명확한 인수 이름 사용이 중요.
# RStudio의 "범위 내에서 이름 바꾸기"와 유사한 기능은 Python IDE (VSCode, PyCharm)에서도 제공.

# 6. 자주 검토하고 리팩터링하십시오.
# 데이터 읽기를 함수 외부로 분리하는 것은 Python에서도 좋은 관행.
def adsl_counts_from_df_py(df_saf): # 이제 데이터프레임을 직접 받음
    if not isinstance(df_saf, pd.DataFrame) or df_saf.empty:
        print("입력 데이터프레임이 비어있거나 유효하지 않습니다.")
        return pd.DataFrame()

    if not all(col in df_saf.columns for col in ['TRT01AN', 'TRT01A', 'SEX']):
        print("입력 데이터에 필요한 열(TRT01AN, TRT01A, SEX)이 없습니다.")
        return pd.DataFrame()

    # 나머지 로직은 adsl_counts_py와 유사 (df_saf를 직접 사용)
    big_n = df_saf.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N')
    small_n = df_saf.groupby(['TRT01AN', 'TRT01A', 'SEX']).size().reset_index(name='n')

    if small_n.empty or big_n.empty:
        return pd.DataFrame()

    merged_df = pd.merge(small_n, big_n, on=['TRT01AN', 'TRT01A'], how='left')

    if 'n' not in merged_df.columns or 'N' not in merged_df.columns or merged_df['N'].isnull().any() or (merged_df['N'] == 0).any():
        merged_df['npct'] = merged_df['n'].astype(str) + " (N/A)"
    else:
        merged_df['perc'] = (merged_df['n'] / merged_df['N'] * 100).round(1)
        merged_df['perc_char'] = merged_df['perc'].apply(lambda x: f"{x:.1f}")
        merged_df['npct'] = merged_df['n'].astype(str) + " (" + merged_df['perc_char'] + ")"

    sex_map = {"M": "Male", "F": "Female"}
    merged_df['SEX'] = merged_df['SEX'].replace(sex_map)
    final_df = merged_df[['TRT01A', 'SEX', 'npct']]

    try:
        pivot_df = final_df.pivot_table(index='SEX', columns='TRT01A', values='npct', aggfunc='first').reset_index()
        pivot_df.columns.name = None
        return pivot_df
    except Exception as e:
        print(f"리팩터링된 함수 피벗 오류: {e}")
        return pd.DataFrame()


print("\n리팩터링된 adsl_counts_from_df_py 함수 테스트:")
if not adsl_saf.empty: # 위에서 로드한 adsl_saf 사용
    table1_py = adsl_counts_from_df_py(adsl_saf)
    if not table1_py.empty:
        print("adsl_counts_from_df_py 결과:")
        print(table1_py)
    else:
        print("adsl_counts_from_df_py 함수가 빈 결과를 반환했습니다.")
else:
    print("adsl_saf 데이터가 비어있어 리팩터링된 함수를 테스트할 수 없습니다.")

# 7. 함수 문제 해결 및 디버깅
# Python에서는 pdb (Python Debugger), IDE의 디버거, print() 문 등을 사용.
# R의 debugonce(), browser()와 유사한 기능 제공.
# R의 traceback()은 Python의 traceback 모듈과 유사.
# R의 options(error = recover)는 pdb.pm() (post-mortem debugging)과 유사.

# 8. 모든 인수를 지정할 필요는 없습니다 - *args, **kwargs (Python의 생략 부호)
# R의 ... 와 유사하게, Python에서는 *args (위치 인수)와 **kwargs (키워드 인수)를 사용.
def my_summary_py(my_data, *args, **kwargs): # **kwargs로 round의 digits 인수 등을 받음
    if not isinstance(my_data, pd.DataFrame) or 'AGE' not in my_data.columns or \
       not all(col in my_data.columns for col in ['TRT01AN', 'TRT01A']):
        print("my_summary_py: 입력 데이터가 유효하지 않거나 필요한 열이 없습니다.")
        return pd.DataFrame()

    # round 함수에 kwargs 전달
    # pandas round는 Series.round(**kwargs) 형태로 사용 가능
    # 여기서는 mean 계산 후 Python의 round()에 digits 전달
    digits_to_round = kwargs.get('digits', 0) # 기본값 0

    summary = my_data.groupby(['TRT01AN', 'TRT01A'])['AGE'].mean() \
                     .apply(lambda x: round(x, digits_to_round)) \
                     .reset_index(name='mean_age')
    return summary

print("\nmy_summary_py 함수 테스트:")
if not adsl_saf.empty:
    print("기본값 (digits=0):")
    print(my_summary_py(adsl_saf))
    print("\ndigits=1:")
    print(my_summary_py(adsl_saf, digits=1))
else:
    print("adsl_saf 데이터가 비어있어 my_summary_py를 테스트할 수 없습니다.")

# 도전 과제: MiniProject6의 플롯 함수를 Python으로 변환하고, 축 레이블 등을 인수로 받도록.
# 이 부분은 MiniProject6_ko.py에서 다루는 것이 적절.
# 기본 아이디어: matplotlib/seaborn 플롯 함수를 만들고,
# x_label, y_label, title 등의 인수를 추가하여 사용자가 지정할 수 있도록 함.

# `pip install pandas pyreadstat` 필요할 수 있음.
# 이 스크립트는 R의 함수 작성 및 사용과 관련된 개념을 Python으로 변환/설명.
# R의 tidyverse 스타일 함수 작성 (데이터 우선, 파이프 사용)은 Python에서
# pandas 데이터프레임을 첫 인수로 받고 메서드 체인을 사용하는 함수로 유사하게 구현 가능.
# R의 ... (생략 부호)는 Python의 *args 및 **kwargs로 대체.
# 오류 처리 및 방어적 프로그래밍은 양쪽 언어 모두에서 중요.
# Python의 함수는 객체이므로 변수에 할당하고 다른 함수에 전달 가능 (R과 동일).
# 전반적으로, R의 함수 관련 기능을 Python의 해당 기능과 매핑하여 설명.
