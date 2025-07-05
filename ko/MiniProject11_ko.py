import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # plot_mpg 예시용
import seaborn as sns # plot_mpg 예시용
# rlang 패키지 기능은 Python에서 직접적인 동등물 찾기 어려움.
# 유사한 메타프로그래밍/동적 평가 기능은 Python의 내장 함수, functools, inspect 모듈 등으로 구현.
# 여기서는 pandas의 열 이름 직접 사용 및 함수 인자로 전달하는 방식을 주로 사용.

# 0. 데이터 로드 (adsl_saf)
try:
    adsl = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
    if 'SAFFL' in adsl.columns and 'SEX' in adsl.columns:
        adsl_saf = adsl[adsl['SAFFL'] == "Y"].copy()
        sex_map = {"M": "Male", "F": "Female"}
        adsl_saf['SEX'] = adsl_saf['SEX'].replace(sex_map)
        print("adsl_saf 데이터 로드 및 초기 변환 완료.")
    else:
        print("SAFFL 또는 SEX 열이 adsl 데이터에 없습니다.")
        adsl_saf = pd.DataFrame()
except Exception as e:
    print(f"ADSL 데이터 읽기 오류: {e}")
    adsl_saf = pd.DataFrame()

# tidyeval이란 무엇인가? (Python 관점)
# Python/pandas에서는 열 이름을 주로 문자열로 전달.
# R의 non-standard evaluation (NSE)과 유사한 효과는 pandas 내부에서 일부 처리되거나,
# query() 메서드, 또는 eval() 함수 등에서 볼 수 있음.
# 함수 작성 시에는 열 이름을 명시적인 문자열 인수로 받는 것이 일반적.

# 평가된 인수와 인용된 인수 (Python 관점)
print("\n--- 평가된 인수 vs 인용된 인수 (Python) ---")
# 평가된 인수
print(f"log(10) = {np.log(10)}") # numpy의 log 사용
x_py_eval = 10
print(f"x_py_eval = {x_py_eval}, log(x_py_eval) = {np.log(x_py_eval)}")

# 인용된 인수 (R의 select(mpg)와 유사한 상황)
# pandas에서는 df['mpg'] 또는 df.mpg 형태로 열 선택.
# 전역 변수와 열 이름 충돌은 Python에서 명시적 참조 (df['col'])로 대부분 회피.
mpg_global_var = 5020
# mtcars 데이터셋 로드 (Python에서는 직접 로드하거나 csv 등에서 읽어야 함)
# 예시로 간단한 DataFrame 생성
mtcars_py = pd.DataFrame({'mpg': [21.0, 21.0, 22.8], 'cyl': [6, 6, 4]})
print("\nmtcars_py 예시:")
print(mtcars_py)
print(f"전역 변수 mpg_global_var = {mpg_global_var}")
print("mtcars_py['mpg'].head(5):") # 데이터프레임의 'mpg' 열 선택
print(mtcars_py['mpg'].head(5))


# 열 충돌 (.data 및 .env 대명사)
# Python에서는 .data$var, .env$var 와 같은 명시적 대명사는 없음.
# 함수 내에서 지역 변수, 전역 변수, 데이터프레임 열을 구분하여 사용.
print("\n--- 열 충돌 (.data, .env 와 유사한 구분) ---")
df_py_conflict = pd.DataFrame({'x_col': [1.0], 'y_col': [2.0]}) # R 예제와 유사하게 열 이름 변경
x_env_var = 100.0

# R: mutate(z1 = y / x) -> Python: df['z1'] = df['y_col'] / x_env_var (x가 환경 변수일 때)
df_py_conflict['z1'] = df_py_conflict['y_col'] / x_env_var
# R: mutate(z2 = .data$y / .env$x) -> Python: 동일하게 df['y_col'] / x_env_var
# 만약 x_col 이라는 이름의 열도 있고, x_env_var 라는 환경 변수도 있다면,
# df['y_col'] / df['x_col']  (데이터의 x_col 사용)
# df['y_col'] / x_env_var (환경의 x_env_var 사용)
# 처럼 명시적으로 구분.

print("df_py_conflict (z1 계산 후):")
print(df_py_conflict)

# R의 my_rescale 예제 (Python 버전)
# R: my_rescale1 <- function(data, var, factor = 10) { data %>% dplyr::mutate("{{ var }}" := {{ var }} / factor) }
# Python에서는 열 이름을 문자열로 받고, 새 열 이름도 문자열로 지정.
def my_rescale_py(data, var_col_name, new_col_name_prefix="rescaled", factor_env=10):
    if var_col_name not in data.columns:
        print(f"'{var_col_name}' 열이 데이터프레임에 없습니다.")
        return data

    # 만약 'factor'라는 이름의 열이 데이터프레임에 있고, factor_env 인자와 충돌 가능성이 있다면?
    # Python에서는 함수의 인자 이름(factor_env)과 데이터프레임의 열 이름('factor')이 명확히 구분됨.
    # data[var_col_name] / data['factor'] (데이터의 factor 열 사용)
    # data[var_col_name] / factor_env (함수 인자 factor_env 사용)

    # R의 "{{ var }}" := {{ var }} / factor 와 유사하게, 새 열 이름 동적 생성
    # 여기서는 var_col_name을 직접 사용하고, factor_env를 사용.
    data[f"{new_col_name_prefix}_{var_col_name}"] = data[var_col_name] / factor_env
    return data

print("\nmy_rescale_py 예제:")
df_rescale_test1 = pd.DataFrame({'value_col': [1.0, 2.0]})
print("원본 df_rescale_test1:")
print(df_rescale_test1)
print("my_rescale_py(df_rescale_test1, 'value_col'):")
print(my_rescale_py(df_rescale_test1, 'value_col'))

df_rescale_test2 = pd.DataFrame({'factor_col': [0.5, 0.2], 'value_col': [1.0, 2.0]})
print("\n원본 df_rescale_test2 (factor_col 열 포함):")
print(df_rescale_test2)
# factor_env 인자(기본값 10)를 사용하므로 factor_col 열과 충돌 없음.
print("my_rescale_py(df_rescale_test2, 'value_col'):")
print(my_rescale_py(df_rescale_test2, 'value_col'))
# 만약 데이터의 factor_col을 사용하고 싶다면 함수 로직 변경 필요.


# 동적 점 (Python의 *args, **kwargs)
# R: mpg_filter <- function(...) { mpg %>% filter(...) }
# Python에서는 filter 조건을 문자열로 받거나, 람다 함수 등으로 구현 가능.
# 여기서는 R의 ... 와 유사하게 여러 조건 인자를 받는 대신,
# 조건 딕셔너리를 받아 처리하는 방식으로 유사 기능 구현.
print("\n--- 동적 점 (Python *args, **kwargs) ---")
# mpg 데이터셋 예시 (위에서 mtcars_py로 일부 생성, 여기서는 다시 정의)
mpg_py = pd.DataFrame({
    'manufacturer': ['audi', 'audi', 'dodge', 'ford', 'jeep', 'jeep'],
    'model': ['a4', 'a4 quattro', 'dakota pickup 4wd', 'explorer 4wd', 'grand cherokee 4wd', 'grand cherokee 4wd'],
    'year': [1999, 1999, 2008, 2008, 2008, 1999],
    'cty': [18, 17, 10, 13, 10, 13]
})

def mpg_filter_py(data, **conditions): # **conditions로 키워드 인수 받음
    query_parts = []
    for col, val in conditions.items():
        if isinstance(val, str):
            query_parts.append(f"`{col}` == '{val}'") # 문자열은 따옴표 처리, 백틱으로 열 이름 감싸기
        else:
            query_parts.append(f"`{col}` == {val}")
    query_str = " & ".join(query_parts)
    if not query_str: return data # 조건 없으면 원본 반환
    try:
        return data.query(query_str)
    except Exception as e:
        print(f"필터링 오류 ({query_str}): {e}")
        return pd.DataFrame()

print("mpg_filter_py(mpg_py, manufacturer='jeep', year=2008):")
print(mpg_filter_py(mpg_py, manufacturer='jeep', year=2008))

# R의 mySummary 함수 (MiniProject 7)와 유사하게 **kwargs 사용
def my_summary_py_dynamic(my_data, group_cols=['TRT01AN', 'TRT01A'], summary_col='AGE', **round_options):
    if not all(col in my_data.columns for col in group_cols) or summary_col not in my_data.columns:
        print("필요한 열이 없습니다.")
        return pd.DataFrame()

    digits = round_options.get('digits', 0) # round_options에서 'digits' 가져오기, 없으면 0

    summary = my_data.groupby(group_cols)[summary_col].mean() \
                     .apply(lambda x: round(x, digits)) \
                     .reset_index(name=f'mean_{summary_col}')
    return summary

print("\nmy_summary_py_dynamic (adsl_saf 사용):")
if not adsl_saf.empty:
    print(my_summary_py_dynamic(adsl_saf, summary_col='AGE'))
    print(my_summary_py_dynamic(adsl_saf, summary_col='AGE', digits=1))


# 포옹 연산자 ({{ var }})
# Python에서는 함수 인자로 열 이름을 문자열로 전달하고, f-string 등으로 동적 사용.
# R: plot_mpg <- function(var) { mpg %>% ggplot(aes({{ var }})) + geom_bar() }
def plot_mpg_py(data, var_col_name_str):
    if var_col_name_str not in data.columns:
        print(f"'{var_col_name_str}' 열이 없습니다.")
        return

    plt.figure(figsize=(8,5))
    # data[var_col_name_str].value_counts().plot(kind='bar') # 간단한 막대그래프
    sns.countplot(data=data, x=var_col_name_str) # seaborn countplot 사용
    plt.title(f"'{var_col_name_str}'의 빈도수")
    plt.ylabel("빈도수")
    # plt.show() # 필요시 주석 해제
    print(f"\nplot_mpg_py: '{var_col_name_str}'에 대한 플롯 생성됨 (plt.show() 주석 처리됨)")

print("\n--- 포옹 연산자 (Python 방식) ---")
# plot_mpg_py(mpg_py, 'drv') # mpg_py에 'drv' 열이 없으므로, 'manufacturer'로 대체
plot_mpg_py(mpg_py, 'manufacturer')


# R의 grouped_mean 함수 ({{ group_var }}, {{ summary_var }})
def grouped_mean_py(df, group_var_str, summary_var_str):
    if group_var_str not in df.columns or summary_var_str not in df.columns:
        print("그룹 또는 요약 열이 없습니다.")
        return pd.DataFrame()

    # R의 요약 통계 형식과 유사하게 만들기 (문자열로 포맷)
    summary = df.groupby(group_var_str)[summary_var_str].agg(
        mean=lambda x: f"{x.mean():.0f}", # R의 format(nsmall=0)
        sd=lambda x: f"{x.std():.1f}",   # R의 format(nsmall=1)
        med=lambda x: f"{x.median():.0f}",
        min=lambda x: f"{x.min():.0f}",
        max=lambda x: f"{x.max():.0f}",
        n='count'
    ).reset_index()
    return summary

print("\ngrouped_mean_py(mpg_py, group_var_str='manufacturer', summary_var_str='cty'):")
print(grouped_mean_py(mpg_py, group_var_str='manufacturer', summary_var_str='cty'))


# 바다코끼리 연산자 (:=) 와 뱅뱅 연산자 (!!)
# R: summarize(!!summary_name := mean(!!summary_var))
# Python에서는 새 열 이름을 f-string이나 변수로 지정하고, agg() 등으로 계산.
# R의 enquo(), !! 와 유사한 메타프로그래밍은 Python에서 덜 직접적.
# 보통은 열 이름을 문자열로 명시적으로 다룸.
print("\n--- 바다코끼리/뱅뱅 연산자 (Python 방식) ---")
def summary_mean_py_named(df, summary_var_str, new_summary_name_str):
    if summary_var_str not in df.columns:
        print(f"'{summary_var_str}' 열이 없습니다.")
        return pd.DataFrame()
    # 새 이름으로 요약 결과 저장
    summary_df = df.agg(mean_val=(summary_var_str, 'mean')).rename(columns={'mean_val': new_summary_name_str})
    # 위 코드는 전체 df에 대한 요약. R 예제는 summarize() 내에서 사용되므로,
    # groupby()와 함께 사용되는 경우를 가정.
    # 예: df.groupby(...).agg(**{new_summary_name_str: (summary_var_str, 'mean')})
    return summary_df

# R의 mySummary 패턴들 (Python 버전)
def my_summary_pattern1_py(my_data, summary_var_str, group_cols=['TRT01AN', 'TRT01A'], **round_args):
    # R: summarise(mean = round(mean(!!summary_var), ... ))
    # Python: 열 이름을 문자열로 받아 사용
    if summary_var_str not in my_data.columns or not all(c in my_data.columns for c in group_cols):
        return pd.DataFrame()
    digits = round_args.get('digits', 0)
    return my_data.groupby(group_cols)[summary_var_str].mean().round(digits).reset_index(name=f'mean_{summary_var_str}')

def my_summary_pattern2_py(my_data, summary_var_str, summary_name_str, group_cols=['TRT01AN', 'TRT01A'], **round_args):
    # R: summarise({{summary_name}} := round(mean(!!summary_var), ... ))
    # Python: agg()와 함께 딕셔너리를 사용하여 새 열 이름 지정
    if summary_var_str not in my_data.columns or not all(c in my_data.columns for c in group_cols):
        return pd.DataFrame()
    digits = round_args.get('digits', 0)
    # 동적 집계 함수 이름 생성
    agg_func = {summary_name_str: pd.NamedAgg(column=summary_var_str, aggfunc=lambda x: x.mean().round(digits))}
    return my_data.groupby(group_cols).agg(**agg_func).reset_index()


def my_summary_pattern3_py(my_data, summary_var_str, summary_fn_name_str, summary_fn_actual, group_cols=['TRT01AN', 'TRT01A'], **fn_args):
    # R: summarise({{summary_fn}} := round(summary_fn({{summary_var}}), ... ))
    # Python: 실제 함수(summary_fn_actual)와 그 함수의 인자(fn_args)를 받음
    if summary_var_str not in my_data.columns or not all(c in my_data.columns for c in group_cols):
        return pd.DataFrame()

    def apply_fn_with_args(series):
        # np.round와 같은 함수는 추가 인자를 받을 수 있음 (예: decimals)
        # 여기서는 summary_fn_actual이 Series를 받고, fn_args를 내부에서 사용한다고 가정
        # 또는, round를 별도로 적용
        val = summary_fn_actual(series)
        if 'digits' in fn_args and isinstance(val, (int, float, pd.Series)): # Series에도 round 적용 가능
            return np.round(val, fn_args['digits'])
        return val

    agg_func = {summary_fn_name_str: pd.NamedAgg(column=summary_var_str, aggfunc=apply_fn_with_args)}
    return my_data.groupby(group_cols).agg(**agg_func).reset_index()


if not adsl_saf.empty and 'AGE' in adsl_saf.columns:
    print("mySummary1 (AGE, digits=1):")
    print(my_summary_pattern1_py(adsl_saf, 'AGE', digits=1))
    print("\nmySummary2 (AGE, 'mean_age_val', digits=1):")
    print(my_summary_pattern2_py(adsl_saf, 'AGE', 'mean_age_val', digits=1))
    print("\nmySummary3 (AGE, 'median_age_val', np.median, digits=1):") # np.median은 digits 인자 없음
    # mySummary3의 apply_fn_with_args에서 round를 별도로 처리하도록 수정
    print(my_summary_pattern3_py(adsl_saf, 'AGE', 'median_age_val', np.median, digits=1))


# 기호를 문자 이름으로 변환 (R의 rlang::as_name(substitute(var_value)))
# Python에서는 변수 이름을 얻기 위해 inspect 모듈 등을 사용할 수 있으나,
# 보통은 함수에 문자열로 열 이름을 전달하는 것이 더 명확하고 일반적.
# R 예제의 mpgf는 Python에서 다음과 같이 간단히 구현 가능:
print("\n--- 기호->문자열 변환 (Python 방식) ---")
def mpgf_py(data, var_value_str): # var_value를 문자열로 직접 받음
    return data.assign(var=var_value_str) # 새 열 'var'에 문자열 값 할당 (R 예제와 동일한 결과)

print("mpgf_py(mpg_py, 'test1').head(5):")
print(mpgf_py(mpg_py, 'test1').head(5))


# Mini-Project 4의 get_cat_demo 함수 수정 (Python 버전)
# 이 함수는 매우 길고 복잡하므로, 핵심 아이디어만 설명:
# - R의 {{ variable }} -> Python에서는 variable_col_name_str (문자열) 인자로 받음.
# - 함수 내부에서 이 문자열을 사용하여 데이터프레임 열에 접근 (예: df[variable_col_name_str]).
# - 동적으로 열 이름을 생성해야 할 때 f-string 사용 (예: f"count_{variable_col_name_str}").
# - R의 complete(nesting(...), {{variable}}, fill=...) 와 같은 복잡한 연산은
#   pandas에서 pd.MultiIndex.from_product, merge, reindex, fillna 등으로 조합하여 구현.
# (MiniProject4_ko.py 에서 이미 유사한 함수들이 Pythonic하게 구현됨)
print("\nMini-Project 4의 get_cat_demo 함수는 Python에서 열 이름을 문자열 인자로 받아 처리하는 방식으로 구현됩니다.")
print("동적 열 이름 생성에는 f-string이, 복잡한 데이터 재구조화에는 pandas의 여러 기능 조합이 사용됩니다.")


# 도전 과제: MiniProject6의 플롯 함수 수정 (Python 버전)
# MiniProject6_ko.py의 plot_ALT 함수를 수정하여 축 레이블 등을 인자로 받도록 함.
# (MiniProject6_ko.py에서 이미 유사한 플롯 함수가 Pythonic하게 구현됨)
# 예시: def plot_alt_py(data, x_var_str, y_var_str, title_str="", x_label_str="", y_label_str="", **plot_args):
#           plt.title(title_str if title_str else f"{y_var_str} by {x_var_str}")
#           plt.xlabel(x_label_str if x_label_str else x_var_str)
#           plt.ylabel(y_label_str if y_label_str else y_var_str)
#           ... sns.scatterplot(data=data, x=x_var_str, y=y_var_str, **plot_args) ...
print("\n도전 과제 (MiniProject6 플롯 함수 수정)는 Python에서 플롯 함수의 인자로")
print("x_var, y_var, title, labels 등을 문자열로 받아 동적으로 설정하는 방식으로 구현됩니다.")
print("matplotlib/seaborn 함수들은 이러한 문자열 인자를 직접 지원합니다.")


# `pip install pandas pyreadstat numpy matplotlib seaborn` 필요.
# 이 스크립트는 R의 tidy evaluation 개념을 Python에서 어떻게 유사하게 처리할 수 있는지 보여줌.
# 핵심은 열 이름을 문자열로 명시적으로 다루고, Python의 표준 기능을 활용하는 것.
# R의 NSE와 관련된 복잡한 메타프로그래밍은 Python에서는 다른 방식으로 접근 (덜 일반적).
# 사용자 정의 함수 작성 시, pandas 데이터프레임과 열 이름(문자열)을 인자로 받는 것이 일반적.
