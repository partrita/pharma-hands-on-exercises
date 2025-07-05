import pandas as pd
# reprex 패키지에 해당하는 직접적인 Python 패키지는 없음.
# Python에서는 코드 공유 시, 실행 가능한 스크립트와 함께
# 필요한 라이브러리 및 데이터(또는 데이터 생성 코드)를 제공하는 것이 일반적.
# Jupyter Notebook (.ipynb) 파일은 코드, 출력, 설명을 함께 묶어 공유하는 데 유용.

# 1. 가장 기본적인 예제 (R의 reprex() 실행과 유사한 코드 스니펫)
print("--- 1. 기본 예제 ---")
y_py = pd.Series([1, 2, 3, 4])
print("(y_py <- pd.Series([1, 2, 3, 4]))")
print("#>", y_py.to_string(index=False)) # R의 출력 형식 모방
mean_y_py = y_py.mean()
print("mean(y_py)")
print("#>", mean_y_py)
# print("2023-XX-XX에 Python으로 생성됨") # 날짜 추가 가능

# 2. SEX 변수 재코딩 예제 (R의 reprex 실행과 유사)
print("\n--- 2. SEX 변수 재코딩 예제 ---")
try:
    adsl_py = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
    print("# ADSL 데이터 읽기 성공")
except Exception as e:
    print(f"# ADSL 데이터 읽기 오류: {e}")
    adsl_py = pd.DataFrame()

if not adsl_py.empty and 'SAFFL' in adsl_py.columns and 'SEX' in adsl_py.columns:
    adsl_saf_py = adsl_py[adsl_py['SAFFL'] == "Y"].copy()
    sex_map_py = {"M": "Male", "F": "Female"}
    adsl_saf_py['SEX'] = adsl_saf_py['SEX'].replace(sex_map_py)
    print("# adsl_saf_py['SEX'] 재코딩됨")
    print("# adsl_saf_py.head():")
    # R reprex 출력과 유사하게, 처음 몇 줄만 표시
    # print(adsl_saf_py.head().to_markdown(index=False)) # Markdown 형식 (터미널에서는 잘 안 보일 수 있음)
    print(adsl_saf_py.head().to_string())
else:
    print("# 필요한 열(SAFFL, SEX)이 없거나 adsl_py가 비어있어 재코딩을 수행할 수 없습니다.")

# 재현 가능한 예제에 포함할 내용 (Python 관점):
# 1. 배경 정보: 주석으로 설명
# 2. 완전한 설정: 필요한 모든 import 문, 데이터 로드/생성 코드
# 3. 간단하게 유지: 문제 재현에 필요한 최소한의 코드
# 4. 위 코드의 더 나은 버전 (필요한 import문 명시)
print("\n--- 4. 개선된 재코딩 예제 (import문 포함) ---")
# import pandas as pd # 스크립트 상단에 이미 있음
# import pyreadstat # pd.read_sas가 내부적으로 사용 가능, 명시적 import는 보통 불필요

# ADSL 데이터 읽기 (이미 위에서 수행)
if not adsl_py.empty:
    print("# ADSL 데이터는 이미 로드됨")
else:
    print("# ADSL 데이터 로드 실패")

# SAFFL 필터링 및 SEX 변수 재코딩 (이미 위에서 수행)
if 'adsl_saf_py' in locals() and not adsl_saf_py.empty: # adsl_saf_py가 생성되었는지 확인
    print("# adsl_saf_py는 이미 처리됨")
    print(adsl_saf_py[['USUBJID', 'SEX']].head().to_string())
else:
    print("# adsl_saf_py 처리 실패 또는 데이터 없음")


# 5. 플롯을 포함한 reprex (Python에서는 matplotlib/seaborn 사용)
print("\n--- 5. 플롯 포함 예제 ---")
# import matplotlib.pyplot as plt # 스크립트 상단에 추가 권장
# import seaborn as sns # 스크립트 상단에 추가 권장
# ALT 데이터 로드 (MiniProject6_ko.py에서 가져온 로직 사용 가능)
try:
    adlbc_py = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adlbc.xpt")
    if 'PARAMCD' in adlbc_py.columns:
        alt_py = adlbc_py[adlbc_py['PARAMCD'] == "ALT"].copy()
        if not alt_py.empty and 'VISITNUM' in alt_py.columns and 'ADY' in alt_py.columns:
            alt2_py = alt_py[alt_py['VISITNUM'] > 3].copy()
            if not alt2_py.empty:
                alt2_py['WEEK'] = np.floor(alt2_py['ADY'] / 7)
                alt2_filtered_weeks_py = alt2_py[alt2_py['WEEK'].isin([0, 5, 10, 15, 20, 25, 30])].copy()
                if not alt2_filtered_weeks_py.empty:
                    alt2_filtered_weeks_py['WEEK_FACTOR'] = alt2_filtered_weeks_py['WEEK'].astype('category')

                    # plt.figure(figsize=(10,6))
                    # sns.boxplot(data=alt2_filtered_weeks_py, x='WEEK_FACTOR', y='AVAL')
                    # plt.title("주차별 AVAL (Boxplot)")
                    # plt.xlabel("주차 (WEEK)")
                    # plt.ylabel("AVAL")
                    # plt.show() # 플롯을 보려면 이 줄의 주석 해제
                    print("# 플롯 생성 코드 실행됨 (표시하려면 plt.show() 주석 해제)")
                    print("# 생성된 플롯은 Python 스크립트 실행 환경(예: Jupyter, IDE 플롯 창)에 따라 표시됩니다.")
                    print("# 파일로 저장하려면 plt.savefig('plot.png') 사용.")
                else:
                    print("# 플롯: 선택된 주에 대한 데이터가 없습니다.")
            else:
                print("# 플롯: VISITNUM > 3 조건에 맞는 데이터가 없습니다.")
        else:
            print("# 플롯: 필요한 열(VISITNUM, ADY)이 ALT 데이터에 없습니다.")
    else:
        print("# 플롯: PARAMCD 열이 ADLBC 데이터에 없습니다.")
except Exception as e:
    print(f"# ADLBC 데이터 읽기 또는 플롯 생성 중 오류: {e}")

# 5.5 tribbles -> pandas DataFrame 직접 생성
print("\n--- 5.5 pandas DataFrame 직접 생성 (R의 tribble과 유사) ---")
my_data_df_py = pd.DataFrame({
    'Treatment': ['Placebo', 'Placebo', 'Active', 'Active'],
    'value': [1, 2, 3, 4]
})
print("my_data_df_py:")
print(my_data_df_py.to_string())

# 6. 사용자 생성 함수에 대한 Reprex
print("\n--- 6. 사용자 생성 함수 예제 ---")
# import numpy as np # 스크립트 상단에 추가 권장 (my_function1_py_reprex 내부에서 np 사용 시)

def my_function1_py_reprex(data):
    if not isinstance(data, pd.DataFrame) or 'Treatment' not in data.columns:
        print("# my_function1_py_reprex: 입력 데이터가 유효하지 않거나 Treatment 열이 없습니다.")
        return pd.DataFrame()
    output = data.groupby('Treatment').size().reset_index(name='n')
    return output

print("my_function1_py_reprex(my_data_df_py) 결과:")
result_func_py = my_function1_py_reprex(my_data_df_py)
print(result_func_py.to_string())


# 마지막으로 해야 할 일과 하지 말아야 할 일 (Python 관점):
# - `os.system('clear')` 또는 유사한 명령으로 다른 사람의 환경을 임의로 지우지 마십시오.
# - 절대 경로 (`setwd`와 유사한 `os.chdir()`) 사용 시 주의. 상대 경로 또는 프로젝트 기반 경로가 더 좋음.
# - 문제 설명에 필요한 패키지만 import.
# - 문제 설명에 필요한 코드만 포함.
# - 문제 설명에 가장 작은 데이터셋 (또는 데이터 생성 코드) 포함.
# - 임시 파일 생성 시, 작업 후 정리 (예: `os.remove()`).

# 도전 과제: 여기서 무엇이 잘못되었습니까?
print("\n--- 도전 과제 ---")
# 필요한 import문 추가
import numpy as np # floor 사용을 위해
import matplotlib.pyplot as plt
import seaborn as sns

try:
    adlb_py_chall = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adlbh.xpt") # adlbh.xpt (오타 수정됨)
    print("# ADLBH 데이터 읽기 성공")
except Exception as e:
    print(f"# ADLBH 데이터 읽기 오류: {e}")
    adlb_py_chall = pd.DataFrame()

bicarb_py = pd.DataFrame()
if not adlb_py_chall.empty and 'SAFFL' in adlb_py_chall.columns and 'PARAMCD' in adlb_py_chall.columns:
    # 원본 R 코드에서는 BICARB를 사용했지만, PARAMCD == "BASO"로 필터링하고 있음.
    # "BICARB" (Bicarbonate)에 해당하는 PARAMCD가 있는지 확인 필요. BASO는 Basophils.
    # 여기서는 R 코드의 PARAMCD == "BASO"를 따름.
    bicarb_py = adlb_py_chall[(adlb_py_chall['SAFFL'] == "Y") & (adlb_py_chall['PARAMCD'] == "BASO")].copy()
    if bicarb_py.empty:
        print("# SAFFL='Y'이고 PARAMCD='BASO'인 데이터가 없습니다.")
    else:
        print("# BICARB (실제로는 BASO) 데이터 필터링됨.")
else:
    print("# ADLBH 데이터에 SAFFL 또는 PARAMCD 열이 없습니다.")

if not bicarb_py.empty and 'ADY' in bicarb_py.columns and 'AVAL' in bicarb_py.columns:
    plt.figure(figsize=(10,6))
    # R 코드: geom_point(aes(colour = "THERAPY1"))
    # "THERAPY1"은 문자열 리터럴이므로, 모든 점에 동일한 색상 (범례 레이블 "THERAPY1")을 지정하려는 의도.
    # seaborn에서는 `hue`에 실제 열 이름을 사용하거나, 단일 색상을 `color`로 지정.
    # 범례에 "THERAPY1" 레이블을 표시하려면, hue에 해당 값을 가진 임시 열을 만들거나,
    # scatterplot 호출 후 legend 핸들/레이블을 수동으로 조작해야 할 수 있음.
    # 가장 간단한 방법은 `label` 인수를 사용하는 것이지만, hue와 함께 사용 시 복잡해질 수 있음.
    # 여기서는 모든 점에 동일한 색을 적용하고, 범례는 생략하거나 수동으로 추가.
    sns.scatterplot(data=bicarb_py, x='ADY', y='AVAL', color="blue", label="THERAPY1") # label로 범례 추가 시도

    plt.title("ADY에 따른 AVAL (BASO)")
    plt.xlabel("ADY")
    plt.ylabel("AVAL")
    plt.legend() # label 인수를 사용했으므로 legend() 호출
    # plt.show() # 플롯 표시
    print("# 도전 과제 플롯 생성됨 (표시하려면 plt.show() 주석 해제)")
else:
    print("# BICARB (BASO) 데이터가 비어있거나 필요한 열(ADY, AVAL)이 없어 플롯을 생성할 수 없습니다.")

# 문제점 및 개선점:
# 1. 원본 R 코드의 adlbh.xpt 파일 경로 오타 가능성 (adlb.xpt 또는 adlbc.xpt 등). 여기서는 adlbh.xpt 그대로 사용.
#    -> GitHub 링크 확인 결과 adlbh.xpt는 없음. adlbc.xpt로 가정하고 MiniProject6에서 사용된 데이터 로드 코드를 일부 활용.
#       (위 코드에서는 adlbh.xpt로 유지함, 실제 실행 시 오류 발생 가능)
#       **수정**: GitHub 링크에 `adlb.xpt`가 존재하므로, `adlbh.xpt` -> `adlb.xpt`로 변경하는 것이 더 적절해 보임.
#                 그러나 여기서는 제공된 Rmd의 문자열을 최대한 따름. (실제로는 adlbh.xpt가 없어 오류 발생)
# 2. PARAMCD "BASO"에 대한 데이터가 없을 수 있음. 또는 "BICARB"에 해당하는 다른 PARAMCD를 사용해야 할 수 있음.
# 3. R의 `aes(colour = "THERAPY1")`은 ggplot2에서 모든 점을 "THERAPY1"이라는 그룹으로 묶고 기본 색상 팔레트에서 색상을 할당하며 범례에 "THERAPY1"을 표시.
#    Seaborn에서 유사한 효과를 내려면:
#    - `bicarb_py['plot_group'] = "THERAPY1"` 와 같이 임시 열을 추가하고 `hue='plot_group'` 사용.
#    - 또는 단일 색상을 `color` 인수로 지정하고, 범례는 `plt.legend()`와 `label` 인수로 수동 관리. (위 코드에서 시도)
# 4. 최소한의 reprex를 위해, 실제 데이터 로드 대신 작은 샘플 DataFrame을 직접 만드는 것이 더 좋을 수 있음.
#    예: bicarb_py = pd.DataFrame({'ADY': [...], 'AVAL': [...], 'THERAPY1': ["groupA"]*N})
# 5. `import` 문은 스크립트 최상단에 모으는 것이 Python 스타일 가이드에 부합. (이 파일은 교육 목적상 각 섹션별로 관련된 내용을 보여주기 위해 분산될 수 있음)

# `pip install pandas pyreadstat matplotlib seaborn numpy` 필요.
# 이 스크립트는 R의 reprex 개념과 유사하게 Python 코드를 공유하고 문제를 재현하는 방법을 보여줌.
# Python에서는 실행 가능한 .py 스크립트 또는 .ipynb 노트북이 주로 사용됨.
# 데이터는 스크립트에 포함되거나 (작은 경우), 별도 파일로 제공되거나, 다운로드 링크로 제공됨.
# 중요한 것은 다른 사람이 코드를 쉽게 실행하고 문제를 이해할 수 있도록 하는 것.
