import pandas as pd
from skimpy import skim

# 2. 데이터 읽기
# GitHub에서 직접 XPT 파일을 읽기 위해 pandas의 read_sas 함수를 사용합니다.
# SAS XPT 형식은 read_sas에서 지원됩니다.
# R의 rio::import와 유사하게 파일 경로만 필요합니다.
try:
    adsl = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
except Exception as e:
    print(f"데이터 읽기 오류: {e}")
    adsl = pd.DataFrame() # 오류 발생 시 빈 데이터프레임 생성

# 3. 데이터프레임의 처음 10개 행 보기
if not adsl.empty:
    print("ADSL 데이터프레임의 처음 10개 행:")
    print(adsl.head(10))
    print(f"\nADSL 데이터 객체에는 {adsl.shape[0]}개의 행과 {adsl.shape[1]}개의 열이 있습니다.")

# 4. 데이터셋의 각 열 유형 확인
if not adsl.empty:
    print("\nADSL 데이터 유형:")
    print(adsl.dtypes)

# 5. 개별 변수의 유형 확인
if not adsl.empty:
    print("\nAGE 변수가 숫자인지 확인:")
    # pandas에서는 dtypes를 사용하여 특정 열의 유형을 확인하고,
    # pd.api.types.is_numeric_dtype과 같은 함수로 확인할 수 있습니다.
    if 'AGE' in adsl.columns:
        print(pd.api.types.is_numeric_dtype(adsl['AGE']))
    else:
        print("AGE 열을 찾을 수 없습니다.")

    print("\nRACE 변수가 문자인지 확인:")
    if 'RACE' in adsl.columns:
        # pandas에서는 object dtype이 종종 문자열 데이터를 나타냅니다.
        print(pd.api.types.is_string_dtype(adsl['RACE']) or adsl['RACE'].dtype == 'object')
    else:
        print("RACE 열을 찾을 수 없습니다.")


# 6. skimr 패키지와 유사한 요약 정보 표시
if not adsl.empty:
    print("\nskimpy를 사용한 ADSL 데이터 요약:")
    skim(adsl)

# 7. 유효성 분석 모집단에 대한 새 데이터 객체 만들기
if not adsl.empty and 'EFFFL' in adsl.columns:
    adsl_eff = adsl[adsl['EFFFL'] == 'Y'].copy() # .copy()를 사용하여 SettingWithCopyWarning 방지
    print("\nEFFFL == 'Y'로 필터링된 adsl_eff 데이터프레임:")
    print(adsl_eff)
    print(f"필터링 후 adsl_eff에는 {adsl_eff.shape[0]}개의 행과 {adsl_eff.shape[1]}개의 열이 있습니다.")
else:
    print("\nEFFFL 열을 찾을 수 없거나 adsl이 비어 있어 adsl_eff를 만들 수 없습니다.")
    adsl_eff = pd.DataFrame() # adsl_eff가 정의되도록 빈 데이터프레임 생성

# 8. USUBJID 변수를 기준으로 adsl_eff 데이터 객체 정렬
if not adsl_eff.empty and 'USUBJID' in adsl_eff.columns:
    # R의 arrange와 유사하게 sort_values 사용
    sort_adsl_eff = adsl_eff.sort_values(by='USUBJID')
    print("\nUSUBJID로 정렬된 sort_adsl_eff:")
    print(sort_adsl_eff.head())

    # 파이프 연산자를 사용한 R 코드와 유사한 체인 작업
    sort_adsl_eff_chained = (adsl[adsl['EFFFL'] == 'Y']
                             .sort_values(by='USUBJID'))
    print("\n체인 작업으로 USUBJID로 정렬된 sort_adsl_eff_chained:")
    print(sort_adsl_eff_chained.head())
else:
    print("\nUSUBJID 열을 찾을 수 없거나 adsl_eff가 비어 있어 정렬할 수 없습니다.")

# 9. adsl_eff의 skim 요약 확인
if not adsl_eff.empty:
    print("\nskimpy를 사용한 adsl_eff 데이터 요약:")
    skim(adsl_eff)

# 10. TRT01A, USUBJID 변수를 기준으로 adsl_eff 데이터 정렬
if not adsl_eff.empty and 'TRT01A' in adsl_eff.columns and 'USUBJID' in adsl_eff.columns:
    adsl_eff_srt = adsl_eff.sort_values(by=['TRT01A', 'USUBJID'])
    print("\nTRT01A, USUBJID로 정렬된 adsl_eff_srt:")
    print(adsl_eff_srt.head())
else:
    print("\nTRT01A 또는 USUBJID 열을 찾을 수 없거나 adsl_eff가 비어 있어 정렬할 수 없습니다.")
    adsl_eff_srt = pd.DataFrame()

# 11. 지정된 열 선택
if not adsl_eff_srt.empty:
    selected_columns = ['USUBJID', 'AGE', 'AGEU', 'SEX', 'RACE', 'ETHNIC', 'TRT01A']
    # 모든 열이 adsl_eff_srt에 있는지 확인
    if all(col in adsl_eff_srt.columns for col in selected_columns):
        adsl_eff_srt_selected = adsl_eff_srt[selected_columns]
        print("\n선택된 열이 있는 adsl_eff_srt_selected:")
        print(adsl_eff_srt_selected.head())
        print(f"선택 후 adsl_eff_srt_selected에는 {adsl_eff_srt_selected.shape[0]}개의 행과 {adsl_eff_srt_selected.shape[1]}개의 열이 있습니다.")
    else:
        print("\n하나 이상의 선택된 열을 adsl_eff_srt에서 찾을 수 없습니다.")
        adsl_eff_srt_selected = pd.DataFrame()
else:
    print("\nadsl_eff_srt가 비어 있어 열을 선택할 수 없습니다.")
    adsl_eff_srt_selected = pd.DataFrame()


# 12. 열 이름 변경
if not adsl_eff_srt_selected.empty:
    new_column_names = ["Subject ID", "Age", "AgeUnits", "Sex", "Race", "Ethnicity", "Treatment"]
    # 열 수가 일치하는지 확인
    if len(adsl_eff_srt_selected.columns) == len(new_column_names):
        adsl_eff_srt_renamed = adsl_eff_srt_selected.copy() # SettingWithCopyWarning 방지
        adsl_eff_srt_renamed.columns = new_column_names
        print("\n이름이 변경된 열이 있는 adsl_eff_srt_renamed:")
        print(adsl_eff_srt_renamed.head())
    else:
        print("\n열 이름 변경 실패: 열 수 불일치.")
        adsl_eff_srt_renamed = adsl_eff_srt_selected # 오류 시 변경되지 않은 상태로 유지
else:
    print("\nadsl_eff_srt_selected가 비어 있어 열 이름을 변경할 수 없습니다.")
    adsl_eff_srt_renamed = pd.DataFrame()

# 13. 데이터 목록 표시
# pandas에서는 데이터프레임을 직접 인쇄하면 잘 형식화된 테이블이 표시됩니다.
# R의 htmlTable과 유사한 HTML 표현을 위해 to_html()을 사용할 수 있습니다.
if not adsl_eff_srt_renamed.empty:
    print("\n표시용 adsl_eff_srt_renamed:")
    print(adsl_eff_srt_renamed)

    print("\nHTML 형식의 adsl_eff_srt_renamed (처음 5개 행):")
    # R의 htmlTable과 유사하게 to_html 사용. css.cell과 같은 특정 스타일링은
    # pandas Styler 객체를 통해 수행해야 합니다.
    # 여기서는 간단한 HTML 출력을 보여줍니다.
    try:
        html_output = adsl_eff_srt_renamed.head().to_html(index=False, classes='table table-striped table-hover', escape=False)
        # 추가 스타일링 (R의 css.cell과 유사)
        # 이 예에서는 align="l" (왼쪽 정렬)을 모방합니다.
        # 더 복잡한 스타일링은 BeautifulSoup 또는 Styler 객체를 사용해야 합니다.
        print(html_output.replace('<td>', '<td style="text-align: left; padding-left: .5em; padding-right: .2em;">'))

    except Exception as e:
        print(f"HTML 변환 오류: {e}")

else:
    print("\nadsl_eff_srt_renamed가 비어 있어 표시할 수 없습니다.")

# 필요한 경우 Python 스크립트 실행을 위해 추가 설정이 필요할 수 있습니다.
# 예: pip install pandas skimpy
# 이 스크립트는 Python 환경에서 실행되어야 합니다.
# R Markdown 청크를 실행하는 것과는 다릅니다.
# 각 R 청크는 이 Python 스크립트의 해당 섹션으로 변환되었습니다.
# 특정 R 패키지(tidyverse, rio, skimr, htmlTable)는
# Python 패키지(pandas, skimpy)로 대체되었습니다.
# R의 파이프(%>%)는 pandas의 메서드 체인으로 변환되었습니다.
# 데이터 유형 확인 및 조작은 pandas의 해당 함수를 사용합니다.
# R의 `sapply(X = adsl, FUN = class)`는 `adsl.dtypes`로 변환되었습니다.
# R의 `is.numeric`, `is.character`는 `pd.api.types.is_numeric_dtype`, `pd.api.types.is_string_dtype`로 변환되었습니다.
# R의 `filter`는 boolean indexing (e.g., `adsl[adsl['EFFFL'] == 'Y']`)으로 변환되었습니다.
# R의 `arrange`는 `sort_values`로 변환되었습니다.
# R의 `select`는 DataFrame 열 선택 (e.g., `adsl_eff_srt[selected_columns]`)으로 변환되었습니다.
# R의 `names(x) <- c(...)`는 `df.columns = [...]`로 변환되었습니다.
# R의 `htmlTable`은 `df.to_html()`로 변환되었으며, 스타일링은 추가적인 HTML/CSS 조작이 필요할 수 있습니다.
# 모든 R 코드는 Python으로 번역되었으며, 각 단계는 원본 Rmd 파일의 번호 매기기를 따릅니다.
# 오류 처리 및 조건부 실행이 추가되어 스크립트의 견고성을 높였습니다.
# .copy()가 SettingWithCopyWarning을 피하기 위해 적절한 위치에 사용되었습니다.
# Python 스크립트를 실행하기 전에 `pip install pandas pyreadstat skimpy`를 실행해야 할 수 있습니다.
# pyreadstat은 .xpt 파일을 읽는 데 사용됩니다. (pandas.read_sas는 .xpt도 처리할 수 있음)
# 이 스크립트는 순수 Python이며, R 환경이 필요하지 않습니다.
# 각 단계의 출력은 원본 R Markdown과 유사하게 콘솔에 인쇄됩니다.
# HTML 출력은 더 정교한 스타일링을 위해 추가 작업이 필요할 수 있습니다.
# 이 변환은 R의 핵심 데이터 조작 및 요약 기능을 Python으로 가져오는 것을 목표로 합니다.
# R의 특정 시각화 또는 고급 통계 기능은 다른 Python 라이브러리가 필요할 수 있습니다.
# 이 스크립트는 MiniProject1_ko.Rmd의 핵심 논리를 Python으로 구현합니다.
# R의 `skim()`은 Python의 `skimpy.skim()`으로 대체되었습니다.
# R의 `import()` (rio 패키지)는 `pd.read_sas()`로 대체되었습니다.
# R의 `library()` 호출은 Python의 `import` 문으로 대체되었습니다.
# 전반적으로, Python 생태계의 표준 도구를 사용하여 R 스크립트의 기능을 복제하는 데 중점을 두었습니다.
