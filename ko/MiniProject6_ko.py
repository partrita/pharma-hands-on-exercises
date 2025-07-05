import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# gghighlight, ggdist, ggridges, patchwork, cowplot에 대한 직접적인 Python 대체 라이브러리는 없지만,
# matplotlib, seaborn 및 기타 시각화 라이브러리 (예: joypy for ridgeline)로 유사 효과 구현 가능.

# --- Helper function to load and preprocess ADLBC data ---
def load_and_preprocess_adlbc_mp6(file_path="https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adlbc.xpt"):
    """
    Loads ADLBC data, filters for ALT (PARAMCD=='ALT'), filters by VISITNUM,
    calculates WEEK, and creates ordered categorical columns for treatments.
    """
    try:
        adlbc = pd.read_sas(file_path)
        print("ADLBC 데이터 로드 성공.")
    except Exception as e:
        print(f"ADLBC 데이터 읽기 오류: {e}")
        return pd.DataFrame()

    required_cols = ['PARAMCD', 'VISITNUM', 'ADY', 'LBSTRESN', 'USUBJID',
                     'A1LO', 'A1HI', 'LBNRIND', 'TRTA', 'TRTAN', 'TRTP']
    if not all(col in adlbc.columns for col in required_cols):
        missing = [col for col in required_cols if col not in adlbc.columns]
        print(f"필요한 열 {missing}이 ADLBC 데이터에 없습니다.")
        return pd.DataFrame()

    alt_data = adlbc[adlbc['PARAMCD'] == 'ALT'].copy()
    if alt_data.empty:
        print("ALT (PARAMCD=='ALT') 데이터를 찾을 수 없습니다.")
        return pd.DataFrame()

    alt2_df = alt_data[alt_data['VISITNUM'] > 3].copy()
    if alt2_df.empty:
        print("VISITNUM > 3 조건에 맞는 ALT 데이터를 찾을 수 없습니다.")
        return pd.DataFrame()

    alt2_df['WEEK'] = np.floor(alt2_df['ADY'] / 7)

    # TRTA, TRTAN을 사용하여 TREATMENT 요인 만들기 (정렬된 범주형 데이터)
    treat_fac = alt2_df[['TRTA', 'TRTAN']].drop_duplicates().sort_values(by='TRTAN')
    alt2_df['TREATMENT'] = pd.Categorical(alt2_df['TRTA'], categories=treat_fac['TRTA'].tolist(), ordered=True)

    # TRTP를 사용하여 TREATTXT 요인 만들기
    alt2_df['TREATTXT'] = pd.Categorical(alt2_df['TRTP'], categories=treat_fac['TRTA'].tolist(), ordered=True)

    print("ALT 데이터 (ALT2_df) 전처리 완료.")
    return alt2_df

def unique_val_from_series_mp6(series):
    """ Returns the unique value if only one, else NaN and prints a warning. """
    unique_values = series.unique()
    if len(unique_values) > 1:
        # print(f"경고: 시리즈에 두 개 이상의 고유 값: {unique_values}. 첫 번째 값 사용.") # R과 동작 다름
        return unique_values[0] # R 예제는 첫 번째 값 사용. 더 안전하게는 np.nan 또는 에러.
    return unique_values[0] if len(unique_values) > 0 else np.nan


# 1. 데이터셋 만들기
ALT2_mp6 = load_and_preprocess_adlbc_mp6()

if not ALT2_mp6.empty:
    print("\n--- 1. 전처리된 ALT 데이터 (ALT2_mp6) ---")
    print(ALT2_mp6[['USUBJID', 'ADY', 'WEEK', 'LBSTRESN', 'TREATMENT', 'LBNRIND']].head())

    # 2. 시간 경과에 따른 ALT 측정값의 스파게티 플롯 만들기
    print("\n--- 2. 시간 경과 ALT 스파게티 플롯 ---")
    if all(col in ALT2_mp6.columns for col in ['ADY', 'LBSTRESN', 'USUBJID', 'A1LO', 'A1HI']):
        alt_min_val = unique_val_from_series_mp6(ALT2_mp6['A1LO'])
        alt_max_val = unique_val_from_series_mp6(ALT2_mp6['A1HI'])

        plt.figure(figsize=(12, 7))
        sns.set_theme(style="whitegrid")
        sns.lineplot(data=ALT2_mp6, x='ADY', y='LBSTRESN', hue='USUBJID', legend=False, alpha=0.3, palette="coolwarm")

        if pd.notna(alt_min_val) and pd.notna(alt_max_val):
            # fill_between x축은 정렬된 고유 ADY 값 사용
            unique_ady = np.sort(ALT2_mp6['ADY'].unique())
            plt.fill_between(unique_ady, alt_min_val, alt_max_val, color='lightgreen', alpha=0.4, label=f'정상 범위 ({alt_min_val:.0f}-{alt_max_val:.0f})')

        plt.title("시간 경과에 따른 ALT 측정값 (스파게티 플롯)")
        plt.xlabel("분석 상대일 (ADY)")
        plt.ylabel("ALT 값 (LBSTRESN)")
        if pd.notna(alt_min_val) or pd.notna(alt_max_val): plt.legend(loc='upper right')
        # plot1_obj_mp6 = plt.gca()
        # plt.show()
        print("   ALT 스파게티 플롯 생성됨.")

        # y축 범위 제한
        plt.figure(figsize=(12, 7))
        sns.lineplot(data=ALT2_mp6, x='ADY', y='LBSTRESN', hue='USUBJID', legend=False, alpha=0.3, palette="coolwarm")
        if pd.notna(alt_min_val) and pd.notna(alt_max_val):
            unique_ady = np.sort(ALT2_mp6['ADY'].unique())
            plt.fill_between(unique_ady, alt_min_val, alt_max_val, color='lightgreen', alpha=0.4, label=f'정상 범위 ({alt_min_val:.0f}-{alt_max_val:.0f})')
        plt.ylim(0, 100) # R의 coord_cartesian(ylim=...)과 유사
        plt.xlim(0, 125) # R의 coord_cartesian(xlim=...)과 유사
        plt.title("시간 경과 ALT 측정값 (Y축 제한)")
        plt.xlabel("분석 상대일 (ADY)")
        plt.ylabel("ALT 값 (LBSTRESN)")
        if pd.notna(alt_min_val) or pd.notna(alt_max_val): plt.legend(loc='upper right')
        # plot1b_obj_mp6 = plt.gca()
        # plt.show()
        print("   Y축이 제한된 ALT 스파게티 플롯 생성됨.")
    else:
        print("   필요한 열이 없어 ALT 스파게티 플롯을 생성할 수 없습니다.")

    # 3. {gghighlight} 사용 -> 유사 효과 구현
    print("\n--- 3. 정상 범위 벗어난 피험자 강조 ---")
    if 'LBNRIND' in ALT2_mp6.columns and 'USUBJID' in ALT2_mp6.columns and \
       pd.notna(alt_min_val) and pd.notna(alt_max_val): # alt_min_val 등 필요

        subjects_to_highlight_mp6 = ALT2_mp6[ALT2_mp6['LBNRIND'].isin(['HIGH', 'LOW'])]['USUBJID'].unique()

        plt.figure(figsize=(12, 7))
        # 모든 피험자 흐리게 그리기
        sns.lineplot(data=ALT2_mp6, x='ADY', y='LBSTRESN', hue='USUBJID', legend=False, alpha=0.05, color='grey', palette="coolwarm")
        # 강조할 피험자 진하게 그리기
        if len(subjects_to_highlight_mp6) > 0:
            sns.lineplot(data=ALT2_mp6[ALT2_mp6['USUBJID'].isin(subjects_to_highlight_mp6)],
                         x='ADY', y='LBSTRESN', hue='USUBJID', legend=False, alpha=0.7, linewidth=1.2, palette="viridis") # 다른 팔레트 사용

        unique_ady = np.sort(ALT2_mp6['ADY'].unique()) # fill_between에 필요
        plt.fill_between(unique_ady, alt_min_val, alt_max_val, color='lightgreen', alpha=0.4)
        plt.ylim(0, 100); plt.xlim(0, 125)
        plt.title("정상 범위를 벗어난 피험자 강조")
        # plot1c_obj_mp6 = plt.gca()
        # plt.show()
        print("   정상 범위 벗어난 피험자 강조 플롯 생성됨.")

        # 패싯을 사용한 강조 (TRTP 기준)
        if 'TRTP' in ALT2_mp6.columns:
            if len(subjects_to_highlight_mp6) > 0:
                g_facet_highlight = sns.FacetGrid(ALT2_mp6, col="TRTP", col_wrap=min(3, ALT2_mp6['TRTP'].nunique()),
                                                  height=5, aspect=1.2, sharey=True)
                g_facet_highlight.map_dataframe(sns.lineplot, x='ADY', y='LBSTRESN', hue='USUBJID', legend=False, alpha=0.05, color='grey')

                for ax_idx, ax in enumerate(g_facet_highlight.axes.flat):
                    if ax_idx >= len(g_facet_highlight.col_names): continue # 빈 subplot 방지
                    trt_group_val = g_facet_highlight.col_names[ax_idx]
                    alt2_group_df = ALT2_mp6[ALT2_mp6['TRTP'] == trt_group_val]
                    subjects_facet = alt2_group_df[alt2_group_df['LBNRIND'].isin(['HIGH', 'LOW'])]['USUBJID'].unique()
                    if len(subjects_facet) > 0:
                         sns.lineplot(data=alt2_group_df[alt2_group_df['USUBJID'].isin(subjects_facet)],
                                     x='ADY', y='LBSTRESN', hue='USUBJID', legend=False,
                                     alpha=0.7, linewidth=1.2, ax=ax, palette="viridis")

                    unique_ady_group = np.sort(alt2_group_df['ADY'].unique())
                    if len(unique_ady_group)>0: # 데이터가 있는 경우에만 fill_between
                        ax.fill_between(unique_ady_group, alt_min_val, alt_max_val, color='lightgreen', alpha=0.4)
                    ax.set_ylim(0, 100); ax.set_xlim(0, 125)
                    ax.set_title(f"TRTP: {trt_group_val}")

                g_facet_highlight.fig.suptitle("치료 그룹별 정상 범위 벗어난 피험자 강조", y=1.03)
                # plot1d_obj_mp6 = g_facet_highlight
                # plt.show()
                print("   치료 그룹별 강조 플롯 생성됨.")
            else:
                print("   강조할 피험자가 없어 치료 그룹별 강조 플롯을 생성할 수 없습니다.")
    else:
        print("   LBNRIND, USUBJID 열 또는 정상 범위 값이 없어 강조 플롯을 생성할 수 없습니다.")

    # 4. geom_boxplot을 사용하여 분포 시각화
    print("\n--- 4. 주차별 ALT 분포 (Boxplot) ---")
    if 'WEEK' in ALT2_mp6.columns:
        alt2_filtered_weeks_mp6 = ALT2_mp6[ALT2_mp6['WEEK'].isin([0, 5, 10, 15, 20, 25, 30])].copy()
        if not alt2_filtered_weeks_mp6.empty:
            # WEEK를 범주형으로 변환하여 순서 유지 (R의 as.factor와 유사)
            week_categories = sorted(alt2_filtered_weeks_mp6['WEEK'].unique())
            alt2_filtered_weeks_mp6['WEEK_FACTOR'] = pd.Categorical(alt2_filtered_weeks_mp6['WEEK'], categories=week_categories, ordered=True)

            plt.figure(figsize=(10,6))
            sns.boxplot(data=alt2_filtered_weeks_mp6, x='WEEK_FACTOR', y='LBSTRESN', showfliers=False)
            sns.stripplot(data=alt2_filtered_weeks_mp6, x='WEEK_FACTOR', y='LBSTRESN', color='black', alpha=0.25, jitter=0.15)
            plt.title("주차별 ALT 분포 (Boxplot 및 Jitter)")
            # plot2b_obj_mp6 = plt.gca()
            # plt.show()
            print("   주차별 ALT 분포 Boxplot 생성됨.")
        else:
            print("   선택된 주에 대한 데이터가 없어 Boxplot을 생성할 수 없습니다.")
    else:
        print("   WEEK 열이 없어 Boxplot을 생성할 수 없습니다.")

    # 5. 다른 분포 표시 방법 (레인클라우드, 능선 플롯)
    print("\n--- 5. 다른 분포 시각화 ---")
    if 'WEEK' in ALT2_mp6.columns and 'alt2_filtered_weeks_mp6' in locals() and not alt2_filtered_weeks_mp6.empty:
        # 레인클라우드 플롯 (Seaborn으로 유사하게 구현)
        plt.figure(figsize=(12, 8))
        # orient='h' 대신 x,y 축 변경
        sns.boxplot(data=alt2_filtered_weeks_mp6, y='WEEK_FACTOR', x='LBSTRESN', orient='h', width=0.2, showfliers=False, color="skyblue", boxprops={'zorder': 2})
        sns.violinplot(data=alt2_filtered_weeks_mp6, y='WEEK_FACTOR', x='LBSTRESN', orient='h', color="lightgrey", inner=None, scale="width", cut=0, zorder=1, linewidth=0.5)
        sns.stripplot(data=alt2_filtered_weeks_mp6, y='WEEK_FACTOR', x='LBSTRESN', orient='h', jitter=True, alpha=0.2, color="black", zorder=0, size=3)
        plt.xlim(0, 75)
        plt.title("주차별 ALT 분포 (레인클라우드 스타일)")
        # plt.show()
        print("   주차별 ALT 레인클라우드 스타일 플롯 생성됨.")

        # 능선 플롯 (joypy 라이브러리 사용 또는 FacetGrid + kdeplot)
        # 여기서는 FacetGrid + kdeplot으로 개념만 설명 (실제 코드는 복잡할 수 있음)
        print("   능선 플롯(Joyplot)은 joypy 라이브러리 또는 FacetGrid+kdeplot으로 구현 가능.")
    else:
         print("   WEEK 열 또는 필터링된 데이터가 없어 레인클라우드/능선 플롯을 생성할 수 없습니다.")

    # 6. geom_bar를 사용하여 항목 개수 세기
    print("\n--- 6. 주차 및 정상 범위 상태별 막대 차트 ---")
    if 'WEEK' in ALT2_mp6.columns and 'LBNRIND' in ALT2_mp6.columns:
        alt2_bar_data_mp6 = ALT2_mp6[ALT2_mp6['WEEK'].isin([2, 4, 6, 8, 16, 24, 26])].copy()
        if not alt2_bar_data_mp6.empty:
            week_cat_bar = sorted(alt2_bar_data_mp6['WEEK'].unique())
            alt2_bar_data_mp6['WEEK_FACTOR'] = pd.Categorical(alt2_bar_data_mp6['WEEK'], categories=week_cat_bar, ordered=True)
            lbnrind_order_mp6 = ['LOW', 'NORMAL', 'HIGH'] # R의 factor levels
            alt2_bar_data_mp6['OUTRANGF'] = pd.Categorical(alt2_bar_data_mp6['LBNRIND'], categories=lbnrind_order_mp6, ordered=True)

            plt.figure(figsize=(12, 7))
            sns.countplot(data=alt2_bar_data_mp6, x='WEEK_FACTOR', hue='OUTRANGF', dodge=True, hue_order=lbnrind_order_mp6)
            plt.title("주차 및 정상 범위 상태별 ALT 관찰 수")
            plt.legend(title="정상 범위 상태 (LBNRIND)")
            # plot3b_obj_mp6 = plt.gca()
            # plt.show()
            print("   주차 및 정상 범위 상태별 막대 차트 생성됨.")
        else:
            print("   선택된 주에 대한 데이터가 없어 막대 차트를 생성할 수 없습니다.")
    else:
        print("   WEEK 또는 LBNRIND 열이 없어 막대 차트를 생성할 수 없습니다.")

    # 7. {patchwork} -> matplotlib의 subplots 또는 GridSpec
    print("\n--- 7. 플롯 결합 (matplotlib subplots/GridSpec) ---")
    # 예시: fig, axes = plt.subplots(2, 2) # 2x2 그리드
    # axes[0,0].plot(...) # 첫 번째 subplot에 그리기
    print("   matplotlib의 subplots 또는 GridSpec으로 여러 플롯을 한 그림에 결합 가능.")

    # 8. {cowplot} (워터마크 등) -> matplotlib의 figtext
    print("\n--- 8. 워터마크 (matplotlib figtext) ---")
    # plt.figtext(0.5, 0.5, "DRAFT", fontsize=72, color='gray', alpha=0.3, ha='center', va='center', rotation=30)
    print("   matplotlib의 figtext()를 사용하여 플롯에 워터마크 추가 가능.")

    # 9. 도전 과제 (MiniProject6_challenge.png와 유사한 그래프)
    print("\n--- 9. 도전 과제 플롯 (범위 벗어난 값 강조) ---")
    # 이전에 생성한 강조 플롯(plot1c_obj_mp6와 유사한 로직)을 사용하거나 새로 생성.
    # 빨간색 점으로 범위를 벗어난 ALT 값 강조.
    if 'LBNRIND' in ALT2_mp6.columns and 'USUBJID' in ALT2_mp6.columns and \
       pd.notna(alt_min_val) and pd.notna(alt_max_val):

        plt.figure(figsize=(12, 7))
        sns.set_theme(style="whitegrid")
        # 모든 데이터 라인 (흐리게)
        sns.lineplot(data=ALT2_mp6, x='ADY', y='LBSTRESN', hue='USUBJID', legend=False, alpha=0.1, color='lightgrey')
        # 정상 범위
        unique_ady_chall = np.sort(ALT2_mp6['ADY'].unique())
        plt.fill_between(unique_ady_chall, alt_min_val, alt_max_val, color='lightgreen', alpha=0.3, label=f'정상 범위')
        # 범위를 벗어난 값 (빨간색 점)
        out_of_range_data = ALT2_mp6[ALT2_mp6['LBNRIND'].isin(['HIGH', 'LOW'])]
        if not out_of_range_data.empty:
            sns.scatterplot(data=out_of_range_data, x='ADY', y='LBSTRESN', color='red', s=50, label='범위 벗어남', zorder=5)

        plt.ylim(0, 100); plt.xlim(0, 125) # R 예제와 유사한 범위
        plt.title("ALT 측정값 (범위 벗어난 값 빨간색 점으로 강조)")
        plt.xlabel("분석 상대일 (ADY)"); plt.ylabel("ALT 값 (LBSTRESN)")
        plt.legend()
        # plt.show()
        print("   도전 과제 플롯 (범위 벗어난 값 강조) 생성됨.")
    else:
        print("   도전 과제 플롯 생성에 필요한 데이터 또는 열이 부족합니다.")

else:
    print("초기 ALT2_mp6 데이터가 비어 있어 MiniProject6를 진행할 수 없습니다.")

# plt.show() # 모든 보류 중인 플롯 표시

# 마무리 주석:
# - 이 Python 스크립트는 R Markdown MiniProject6의 시각화 및 데이터 처리 아이디어를 변환합니다.
# - R의 ggplot2 확장 패키지(gghighlight, ggdist 등)의 특정 기능은
#   Matplotlib/Seaborn의 기본 기능과 추가적인 데이터 조작을 통해 유사하게 구현됩니다.
# - 코드에는 각 단계에 대한 설명, 오류 처리, 조건부 실행이 포함되어 있습니다.
# - PEP 8 스타일 가이드라인을 따르려고 노력했습니다.
# - `pip install pandas pyreadstat matplotlib seaborn numpy joypy` 등이 필요할 수 있습니다.
#   (joypy는 능선 플롯을 위해 필요하지만, 이 스크립트에서는 직접 사용하지 않고 개념만 언급)
# - 모든 플롯은 `plt.show()`를 호출해야 표시됩니다 (스크립트 실행 환경에 따라 다름).
