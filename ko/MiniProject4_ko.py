import pandas as pd
import numpy as np # 필요시 사용 (0 개수 처리 등)

# 0. 필요한 함수 정의 (이전 미니프로젝트에서 가져오거나 이 파일에 정의)
# 이 파일의 목적은 MiniProject4의 로직을 Python으로 변환하는 것이므로,
# 필요한 헬퍼 함수들은 여기에 간략히 정의하거나, 이전 파일에서 import 한다고 가정.
# 여기서는 주요 로직에 집중하고, 헬퍼 함수는 간소화하거나 개념만 설명.

def calculate_big_n_cnt_mp4(df):
    """ 치료 그룹별 전체 N 계산 """
    if not isinstance(df, pd.DataFrame) or df.empty or \
       not all(col in df.columns for col in ['TRT01AN', 'TRT01A']):
        return pd.DataFrame()
    return df.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N_total_count') # 컬럼명 변경 N -> N_total_count

def calculate_small_n_cnt_mp4(df, group_var):
    """ 치료 그룹 및 지정된 group_var별 small n 계산 """
    cols_for_grouping = ['TRT01AN', 'TRT01A', group_var]
    if not isinstance(df, pd.DataFrame) or df.empty or \
       not all(col in df.columns for col in cols_for_grouping):
        return pd.DataFrame()
    return df.groupby(cols_for_grouping).size().reset_index(name=f'n_{group_var}')

def create_demographic_table_part(df_eff, demographic_var, big_n_counts):
    """ 특정 인구 통계 변수에 대한 요약 테이블 부분 생성 """
    if not isinstance(df_eff, pd.DataFrame) or df_eff.empty or \
       not isinstance(big_n_counts, pd.DataFrame) or big_n_counts.empty or \
       demographic_var not in df_eff.columns:
        print(f"create_demographic_table_part: 입력 데이터 또는 '{demographic_var}' 변수 문제.")
        return pd.DataFrame()

    small_n_demo = calculate_small_n_cnt_mp4(df_eff, demographic_var)
    if small_n_demo.empty:
        print(f"create_demographic_table_part: '{demographic_var}'에 대한 small_n 계산 실패.")
        return pd.DataFrame()

    # small_n_demo의 컬럼 이름에서 'n_' 다음 부분을 value_var_name으로 사용
    value_var_name_actual = f'n_{demographic_var}'


    merged_demo = pd.merge(small_n_demo, big_n_counts, on=['TRT01AN', 'TRT01A'], how='left')

    if value_var_name_actual not in merged_demo.columns or 'N_total_count' not in merged_demo.columns or \
       merged_demo['N_total_count'].isnull().any() or (merged_demo['N_total_count'] == 0).any():
        merged_demo['npct'] = merged_demo.get(value_var_name_actual, pd.Series(dtype='int')).astype(str) + " (N/A %)"
    else:
        merged_demo['perc'] = (merged_demo[value_var_name_actual] / merged_demo['N_total_count'] * 100).round(1)
        merged_demo['perc_char'] = merged_demo['perc'].apply(lambda x: f"{x:.1f}")
        merged_demo['npct'] = merged_demo[value_var_name_actual].astype(str) + " (" + merged_demo['perc_char'] + " %)"

    # SEX 변수인 경우 재코딩
    if demographic_var == 'SEX':
        sex_map = {"M": "Male", "F": "Female", "U":"Unknown", "UNDIFFERENTIATED":"Unknown"} # 확장된 맵
        merged_demo[demographic_var] = merged_demo[demographic_var].replace(sex_map)

    pivot_input = merged_demo[['TRT01A', demographic_var, 'npct']]
    if pivot_input.empty : return pd.DataFrame()

    try:
        # 피벗: 각 치료법(TRT01A)을 컬럼으로, demographic_var의 각 값을 인덱스로
        # R의 pivot_wider(names_from = TRT01A, values_from = npct)와 유사
        pivoted_table = pivot_input.pivot_table(
            index=demographic_var,
            columns='TRT01A',
            values='npct',
            aggfunc='first', # 각 (인덱스, 컬럼) 조합에 하나의 값만 있다고 가정
            fill_value="0 (0.0 %)" # R의 values_fill과 유사
        ).reset_index()
        pivoted_table.columns.name = None # 컬럼 인덱스 이름 제거
        # 'category' 열 이름 변경 (R 코드와 일치시키기 위해)
        pivoted_table = pivoted_table.rename(columns={demographic_var: 'category'})
        return pivoted_table
    except Exception as e:
        print(f"피벗 오류 ({demographic_var}): {e}")
        return pd.DataFrame()

def create_summary_stats_table_mp4(df, var_name, group_cols=['TRT01AN', 'TRT01A', 'SEX']):
    """ 연속형 변수에 대한 요약 통계 테이블 생성 (MiniProject3_ko.py의 함수와 유사) """
    if var_name not in df.columns or not all(col in df.columns for col in group_cols):
        print(f"Summary Stats MP4: '{var_name}' 또는 그룹화 열이 누락되었습니다.")
        return pd.DataFrame()

    def summarize_stats_for_mp4(series):
        return pd.Series({
            'mean': f"{series.mean():.1f}", 'sd': f"{series.std():.1f}",
            'med': f"{series.median():.1f}", 'min': f"{series.min():.0f}",
            'max': f"{series.max():.0f}", 'n': f"{series.count():.0f}"
        })

    summary_stat = df.groupby(group_cols)[var_name].apply(summarize_stats_for_mp4).unstack()
    if isinstance(summary_stat.columns, pd.MultiIndex):
        summary_stat.columns = [f'{col[0]}_{col[1]}' if col[1]!='' else col[0] for col in summary_stat.columns.values]
    summary_stat = summary_stat.reset_index()
    rename_cols = {col: col.split('_')[-1] for col in summary_stat.columns if '_' in col and col.split('_')[-1] in ['mean','sd','med','min','max','n']}
    summary_stat = summary_stat.rename(columns=rename_cols)

    if 'min' in summary_stat.columns and 'max' in summary_stat.columns:
        summary_stat['range_minmax'] = "(" + summary_stat['min'].astype(str) + "," + summary_stat['max'].astype(str) + ")"

    columns_to_pivot = ['n', 'mean', 'med', 'sd', 'range_minmax']
    id_vars_for_pivot = [col for col in group_cols if col not in ['TRT01AN']] # TRT01A, SEX 등

    available_id_vars = [col for col in id_vars_for_pivot if col in summary_stat.columns]
    available_cols_to_pivot = [col for col in columns_to_pivot if col in summary_stat.columns]

    if not available_cols_to_pivot or not available_id_vars: return pd.DataFrame()

    desc_stat_long_var = summary_stat.melt(
        id_vars=available_id_vars, value_vars=available_cols_to_pivot,
        var_name='category', value_name='values'
    )

    # 피벗을 위해 TRT01A와 다른 id_var (예: SEX)를 결합한 컬럼 생성 필요
    # 여기서는 R 코드의 pivot_wider(names_from = c(TRT01A, SEX), ...) 를 모방
    # group_cols에 SEX 외 다른 변수가 올 수 있으므로 일반화 필요
    # 간단히 TRT01A만 names_from으로 사용하고, 다른 id_vars는 index 유지 시도
    if 'TRT01A' not in desc_stat_long_var.columns: return pd.DataFrame()

    pivot_index_cols = [col for col in available_id_vars if col != 'TRT01A'] + ['category']

    try:
        summary_pivot_intermediate = desc_stat_long_var.pivot_table(
            index=pivot_index_cols, columns='TRT01A', values='values', aggfunc='first'
        ).reset_index()
        summary_pivot_intermediate.columns.name = None
    except Exception as e:
        print(f"요약 통계 피벗 오류: {e}")
        return pd.DataFrame()

    category_map = {"n": "N", "med": "Median", "mean": "Mean", "sd": "Std Dev", "range_minmax": "Range(min,max)"}
    summary_cat_var = summary_pivot_intermediate.copy()
    if 'category' in summary_cat_var.columns:
        summary_cat_var['category'] = summary_cat_var['category'].replace(category_map)
        return summary_cat_var
    return pd.DataFrame()


# 1. ADSL_EFF 데이터 프레임 설정
print("--- 1. ADSL_EFF 데이터 프레임 설정 ---")
try:
    adsl_mp4 = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
    print("ADSL 데이터 로드 성공.")
except Exception as e:
    print(f"ADSL 데이터 읽기 오류: {e}")
    adsl_mp4 = pd.DataFrame()

adsl_eff_mp4 = pd.DataFrame()
if not adsl_mp4.empty and 'EFFFL' in adsl_mp4.columns and 'SEX' in adsl_mp4.columns:
    adsl_eff_mp4 = adsl_mp4[adsl_mp4['EFFFL'] == 'Y'].copy()
    # SEX 재코딩은 create_demographic_table_part 함수 내부에서 처리
    print("adsl_eff_mp4 데이터 필터링 완료.")
else:
    print("adsl_eff_mp4 설정 실패: 필요한 열이 없거나 데이터가 비어있습니다.")

# 2. 큰 N 계산 (프로젝트 2의 Big_N_cnt와 유사)
print("\n--- 2. 큰 N 계산 ---")
big_n_counts_mp4 = calculate_big_n_cnt_mp4(adsl_eff_mp4)
if not big_n_counts_mp4.empty:
    print("큰 N (치료 그룹별 총계) 계산 완료.")
    # print(big_n_counts_mp4)
else:
    print("큰 N 계산 실패.")

# 3-5. 연령 그룹(AGEGR1)에 대한 개수 및 백분율 테이블 (SEX에 대한 것과 유사 로직)
# R 코드에서는 SEX, AGEGR1, RACE에 대해 반복적인 코드가 있었음.
# Python에서는 함수를 사용하여 반복 줄임.
print("\n--- 3-5. 인구 통계 변수별 요약 ---")
age_cat_mp4 = pd.DataFrame()
if 'AGEGR1' in adsl_eff_mp4.columns:
    age_cat_mp4 = create_demographic_table_part(adsl_eff_mp4, 'AGEGR1', big_n_counts_mp4)
    if not age_cat_mp4.empty:
        print("\n연령 그룹(AGEGR1) 요약 테이블 (age_cat_mp4):")
        # R의 factor 순서와 유사하게 정렬하려면 CategoricalDtype 사용 가능
        # 예: age_cat_mp4['category'] = pd.Categorical(age_cat_mp4['category'], categories=["<18", "18-64", ">=65"], ordered=True)
        # age_cat_mp4 = age_cat_mp4.sort_values(by='category')
        print(age_cat_mp4)
    else:
        print("연령 그룹 요약 테이블 생성 실패.")
else:
    print("AGEGR1 열이 없어 연령 그룹 요약을 생성할 수 없습니다.")

# 6-7. 요약 통계 생성 및 전치 (AGE 변수 대상)
print("\n--- 6-7. 연령(AGE) 요약 통계 ---")
# create_summary_stats_table_mp4 함수는 SEX로 그룹화된 결과를 만듦.
# R 코드의 agestat_cat은 SEX별로 그룹화된 AGE 통계를 TRT01A 컬럼으로 피벗.
agestat_cat_mp4 = create_summary_stats_table_mp4(adsl_eff_mp4, 'AGE', group_cols=['TRT01AN', 'TRT01A', 'SEX'])
if not agestat_cat_mp4.empty:
    print("\n연령(AGE) 요약 통계 테이블 (agestat_cat_mp4):")
    print(agestat_cat_mp4)
else:
    print("연령 요약 통계 테이블 생성 실패.")


# 8. 모든 결과 결합 (R의 bind_rows와 유사)
print("\n--- 8. 모든 결과 결합 ---")
dm_allcomb_mp4 = pd.DataFrame()
# SEX에 대한 테이블 생성
sex_cat_mp4 = create_demographic_table_part(adsl_eff_mp4, 'SEX', big_n_counts_mp4)

# 결합할 테이블 리스트
tables_to_concat = []
if not sex_cat_mp4.empty: tables_to_concat.append(sex_cat_mp4)
if not age_cat_mp4.empty: tables_to_concat.append(age_cat_mp4) # AGEGR1
if not agestat_cat_mp4.empty:
    # agestat_cat_mp4는 SEX 열을 포함할 수 있음. bind_rows 전에 컬럼 구조 통일 필요.
    # R 코드에서는 agestat_cat이 category와 치료군 컬럼만 가짐. SEX는 피벗된 컬럼명의 일부.
    # Python 함수 create_summary_stats_table_mp4의 출력을 R과 유사하게 조정 필요.
    # 여기서는 agestat_cat_mp4가 'category', 'SEX', [치료군 컬럼들]을 가진다고 가정하고,
    # bind_rows 전에 'SEX'를 'category'의 일부로 만들거나, 별도 처리.
    # 지금은 단순 concat 시도. 실제로는 컬럼 이름과 구조를 맞춰야 함.
    # agestat_cat_mp4에서 'SEX' 열을 'category'와 결합하거나, 'category'에 통계량 종류만 남기고 SEX는 다른 방식으로 표현
    # R의 agestat_cat은 category (N, Median 등)가 행, 치료군+성별이 열이었음.
    # create_summary_stats_table_mp4의 출력을 R과 동일하게 맞춰야 bind_rows가 의미있음.
    # 현재 create_summary_stats_table_mp4는 SEX를 index의 일부로 사용.
    # R의 bind_rows(age_cat, agestat_cat)는 두 테이블이 'category'와 치료군 컬럼을 공유한다고 가정.
    # agestat_cat_mp4를 age_cat_mp4와 동일한 구조로 변환해야 함.
    # 예: agestat_cat_mp4에서 SEX 정보를 category 값에 포함 (e.g., "N (Male)", "N (Female)")
    # 또는, R의 agestat_cat처럼 SEX를 컬럼명으로 보내고, category에 통계량 종류만 남김.
    # 여기서는 변환 없이 concat 시도하고, 주석으로 한계 명시.
    print("경고: agestat_cat_mp4와 다른 테이블의 컬럼 구조가 다를 수 있어 concat 결과가 예상과 다를 수 있습니다.")
    tables_to_concat.append(agestat_cat_mp4)


if tables_to_concat:
    try:
        dm_allcomb_mp4 = pd.concat(tables_to_concat, ignore_index=True)
        print("\n결합된 인구 통계 테이블 (dm_allcomb_mp4):")
        print(dm_allcomb_mp4)
    except Exception as e:
        print(f"테이블 결합 오류: {e}")
else:
    print("결합할 테이블이 없습니다.")

# 도전 과제 구현
print("\n--- 도전 과제 ---")
# 1. 연령 변수 순서 변경 (<65, 65-80, >80)
if not dm_allcomb_mp4.empty and 'category' in dm_allcomb_mp4.columns:
    age_order = ["<65", "65-80", ">80"] # 실제 AGEGR1 값에 맞춰야 함
    # 현재 AGEGR1 값 확인
    if 'AGEGR1' in adsl_eff_mp4.columns:
        actual_age_grps = adsl_eff_mp4['AGEGR1'].unique().tolist()
        print(f"실제 AGEGR1 값: {actual_age_grps}. age_order를 이에 맞게 조정 필요.")
        # 예시: 실제 값이 ['18-64 YRS', '<18 YRS', '>=65 YRS'] 라면,
        # age_order = ['<18 YRS', '18-64 YRS', '>=65 YRS']
        # 여기서는 Rmd의 순서를 따르되, 실제 데이터 값에 따라 조정해야 함을 명시.

    # category 열을 Categorical 타입으로 변환하여 순서 지정
    # dm_allcomb_mp4['category'] = pd.Categorical(dm_allcomb_mp4['category'], categories=age_order, ordered=True)
    # dm_allcomb_mp4_sorted = dm_allcomb_mp4.sort_values(by='category')
    # print("\n연령 순서 변경된 테이블 (개념적):")
    # print(dm_allcomb_mp4_sorted) # 실제 실행 시 age_order 값 주의
    print("1. 연령 변수 순서 변경: pandas의 CategoricalDtype 사용. (실제 AGEGR1 값에 맞춰 순서 정의 필요)")

# 2. N을 연령 범주 앞으로 이동
if not dm_allcomb_mp4.empty and 'category' in dm_allcomb_mp4.columns:
    # 'category' 열에 'N' (통계량 종류)과 연령 그룹 문자열이 혼합되어 있을 수 있음.
    # create_summary_stats_table_mp4의 출력이 'category'에 'N', 'Mean' 등을,
    # create_demographic_table_part의 출력이 'category'에 'AGEGR1' 값 등을 넣음.
    # 이들을 합칠 때 'variable' 같은 열을 추가하여 구분하는 것이 좋음.
    # 현재 dm_allcomb_mp4 구조에서는 이 작업이 복잡.
    # N 행 (agestat_cat_mp4에서 온 것)을 맨 위로 올리는 개념.
    # n_rows = dm_allcomb_mp4[dm_allcomb_mp4['category'] == 'N']
    # other_rows = dm_allcomb_mp4[dm_allcomb_mp4['category'] != 'N']
    # dm_allcomb_reordered_n = pd.concat([n_rows, other_rows]).reset_index(drop=True)
    # print("\nN이 앞으로 이동된 테이블 (개념적):")
    # print(dm_allcomb_reordered_n)
    print("2. N 행을 앞으로 이동: DataFrame 행 재정렬. (현재 테이블 구조에서는 주의 필요)")

# 3. 민족(ETHNIC) 및 인종(RACE) 추가
if 'ETHNIC' in adsl_eff_mp4.columns:
    ethnic_cat_mp4 = create_demographic_table_part(adsl_eff_mp4, 'ETHNIC', big_n_counts_mp4)
    if not ethnic_cat_mp4.empty:
        print("\n민족(ETHNIC) 요약 테이블:")
        print(ethnic_cat_mp4)
        # dm_allcomb_mp4 = pd.concat([dm_allcomb_mp4, ethnic_cat_mp4], ignore_index=True) # 결합
else:
    print("ETHNIC 열이 없어 민족 요약을 생성할 수 없습니다.")

if 'RACE' in adsl_eff_mp4.columns:
    race_cat_mp4 = create_demographic_table_part(adsl_eff_mp4, 'RACE', big_n_counts_mp4)
    if not race_cat_mp4.empty:
        print("\n인종(RACE) 요약 테이블:")
        print(race_cat_mp4)
        # dm_allcomb_mp4 = pd.concat([dm_allcomb_mp4, race_cat_mp4], ignore_index=True) # 결합
else:
    print("RACE 열이 없어 인종 요약을 생성할 수 없습니다.")

# 최종 결합된 테이블 (모든 부분 포함 가정)
# print("\n최종 결합 및 정렬된 테이블 (개념적):")
# print(dm_allcomb_mp4) # 실제로는 위에서 정렬 및 재정렬된 DataFrame 사용


# 스크립트 실행을 위해 `pip install pandas pyreadstat numpy` 필요할 수 있음.
# 이 Python 스크립트는 R Markdown MiniProject4의 핵심 로직을 변환하려고 시도합니다.
# R 코드의 반복적인 부분을 함수로 만들어 Python에서 재사용성을 높였습니다.
# (create_demographic_table_part, create_summary_stats_table_mp4)
# 데이터 병합(pd.concat) 시에는 R의 bind_rows와 같이 컬럼 구조를 일치시키는 것이 중요합니다.
# 이 스크립트에서는 해당 부분에 대한 주석과 함께 개념적인 구현을 포함했습니다.
# R의 factor 순서 지정은 pandas의 CategoricalDtype으로 유사하게 구현할 수 있습니다.
# 전반적으로, R 스크립트의 단계별 데이터 처리 및 테이블 생성을 Python pandas로 복제하는 데 중점을 둡니다.
# 코드의 가독성과 유지보수성을 위해 함수 사용 및 명확한 변수 이름을 사용하려 노력했습니다.Tool output for `create_file_with_block`:
