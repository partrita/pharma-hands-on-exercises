import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# glue 패키지는 Python의 f-string 또는 format()으로 대체 가능

# --- Helper function to load and preprocess ADVS data ---
def load_and_preprocess_advs_mp5(file_path="https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/advs.xpt"):
    """
    Loads ADVS data from a SAS XPT file, filters for heart rate (PARAMN==3),
    calculates StudyWeek, and returns the processed DataFrame.
    """
    try:
        advs = pd.read_sas(file_path)
        print("ADVS 데이터 로드 성공.")
    except Exception as e:
        print(f"ADVS 데이터 읽기 오류: {e}")
        return pd.DataFrame()

    required_cols = ['PARAMN', 'VISITNUM', 'ADY', 'AVAL', 'TRTA', 'USUBJID'] # Added TRTA, USUBJID for later plots
    if not all(col in advs.columns for col in required_cols):
        missing = [col for col in required_cols if col not in advs.columns]
        print(f"필요한 열 {missing}이 ADVS 데이터에 없습니다.")
        return pd.DataFrame()

    # 심박수 데이터 (PARAMN == 3) 및 VISITNUM > 3 필터링
    pr_df = advs[(advs['PARAMN'] == 3) & (advs['VISITNUM'] > 3)].copy()

    if pr_df.empty:
        print("조건에 맞는 심박수 데이터를 찾을 수 없습니다 (PARAMN==3, VISITNUM>3).")
        return pd.DataFrame()

    pr_df['StudyWeek'] = np.floor(pr_df['ADY'] / 7)
    print("심박수 데이터 (PR_df) 전처리 완료.")
    return pr_df

# 1. 데이터셋 만들기
PR_mp5 = load_and_preprocess_advs_mp5()

if not PR_mp5.empty:
    print("\n--- 1. 전처리된 심박수 데이터 (PR_mp5) ---")
    print(PR_mp5[['USUBJID', 'ADY', 'AVAL', 'StudyWeek', 'TRTA']].head())

    # 2. 기본 ggplot 함수 사용 -> matplotlib/seaborn으로 대체
    print("\n--- 2. 기본 플롯 개념 (matplotlib/seaborn) ---")
    # Python에서는 plt.figure()로 새 그림을 시작하고, seaborn 등으로 플롯을 그림.
    # 각 플롯은 별도의 그림에 그리거나 subplots 사용. 여기서는 개별 figure 사용.

    # 3. "캔버스"에 점 추가 (산점도)
    if 'ADY' in PR_mp5.columns and 'AVAL' in PR_mp5.columns:
        print("\n--- 3. ADY에 따른 AVAL 산점도 ---")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=PR_mp5, x='ADY', y='AVAL')
        plt.title("ADY에 따른 AVAL (산점도)")
        plt.xlabel("ADY (분석 상대일)")
        plt.ylabel("AVAL (심박수 값)")
        # plt.show() # 대화형 환경에서는 자동 표시될 수 있음, 스크립트에서는 명시적 호출 필요.
        print("   산점도 생성됨 (표시하려면 plt.show() 주석 해제).")
    else:
        print("   ADY 또는 AVAL 열이 없어 산점도를 생성할 수 없습니다.")

    # 4. 데이터 그룹 식별 (TRTA 기준)
    if 'TRTA' in PR_mp5.columns:
        print("\n--- 4. TRTA별 그룹화된 산점도 ---")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=PR_mp5, x='ADY', y='AVAL', hue='TRTA', style='TRTA', s=100) # s로 점 크기 조절
        plt.title("ADY에 따른 AVAL (TRTA별 그룹화)")
        plt.xlabel("ADY (분석 상대일)")
        plt.ylabel("AVAL (심박수 값)")
        plt.legend(title="치료군 (TRTA)")
        # plt.show()
        print("   TRTA별 그룹화된 산점도 생성됨.")
    else:
        print("   TRTA 열이 없어 그룹화된 산점도를 생성할 수 없습니다.")

    # 5. 각 피험자의 데이터 계열을 식별하여 "스파게티 플롯" 만들기
    if 'USUBJID' in PR_mp5.columns:
        print("\n--- 5. 피험자별 스파게티 플롯 ---")
        plt.figure(figsize=(12, 7))
        # USUBJID별로 선을 그리기 위해 lineplot 사용
        # 모든 피험자를 그리면 복잡할 수 있으므로 alpha 조절
        sns.lineplot(data=PR_mp5, x='ADY', y='AVAL', hue='USUBJID', legend=False, alpha=0.3, palette="tab20")
        plt.title("피험자별 AVAL 변화 (스파게티 플롯)")
        plt.xlabel("ADY (분석 상대일)")
        plt.ylabel("AVAL (심박수 값)")
        # plot1_obj = plt.gca() # 현재 축 객체 (R의 plot1 객체와 유사한 개념)
        # plt.show()
        print("   피험자별 스파게티 플롯 생성됨.")
    else:
        print("   USUBJID 열이 없어 스파게티 플롯을 생성할 수 없습니다.")

    # 6. 레이블 추가 및 플롯 테마 선택
    print("\n--- 6. 레이블 및 테마 적용된 플롯 ---")
    plt.figure(figsize=(12, 7))
    sns.set_theme(style="whitegrid") # R의 theme_bw()와 유사한 스타일 먼저 설정
    if 'USUBJID' in PR_mp5.columns:
        sns.lineplot(data=PR_mp5, x='ADY', y='AVAL', hue='USUBJID', legend=False, alpha=0.3, palette="tab20")
    else:
        sns.scatterplot(data=PR_mp5, x='ADY', y='AVAL') # USUBJID 없으면 산점도

    plt.title("플롯 제목: 피험자별 심박수 변화")
    # 부제목은 suptitle 또는 title 내 \n 사용
    plt.suptitle("플롯 부제목: 연구 기간 동안", y=0.92, fontsize=10) # y로 위치 조절
    plt.xlabel("X축 레이블: 분석 상대일 (ADY)")
    plt.ylabel("Y축 레이블: 심박수 (AVAL)")
    # 그림 하단에 캡션 추가
    plt.figtext(0.5, 0.01, f"플롯 생성 날짜: {pd.Timestamp.now().strftime('%Y-%m-%d')}",
                ha="center", fontsize=9, bbox={"facecolor":"lightgray", "alpha":0.5, "pad":3})
    # plot2_obj = plt.gca()
    # plt.show()
    print("   레이블 및 테마가 적용된 플롯 생성됨.")

    # 7. 치료군별 분할 (TRTA 기준)
    if 'TRTA' in PR_mp5.columns:
        print("\n--- 7. 치료군별 분할된 스파게티 플롯 ---")
        if 'USUBJID' in PR_mp5.columns:
            # R의 facet_wrap과 유사하게, seaborn의 relplot(col=...) 사용
            # col_wrap으로 한 행에 표시할 플롯 수 지정 가능
            g_facet = sns.relplot(
                data=PR_mp5, x='ADY', y='AVAL',
                col='TRTA', kind='line', hue='USUBJID',
                legend=False, col_wrap=min(3, PR_mp5['TRTA'].nunique()), # 한 줄에 최대 3개 또는 TRTA 유니크 수
                height=4, aspect=1.2, alpha=0.3, palette="tab20"
            )
            g_facet.set_titles("치료군: {col_name}")
            g_facet.set_xlabels("분석 상대일 (ADY)")
            g_facet.set_ylabels("심박수 (AVAL)")
            g_facet.fig.suptitle("치료군별 피험자 심박수 변화", y=1.03) # 전체 제목
            # plot4_facet_obj = g_facet # FacetGrid 객체
            # plt.show()
            print("   치료군별 분할된 스파게티 플롯 생성됨.")
        else:
            print("   USUBJID 열이 없어 분할된 스파게티 플롯을 생성할 수 없습니다.")
    else:
        print("   TRTA 열이 없어 치료군별로 분할할 수 없습니다.")

    # 8. 플롯 저장
    print("\n--- 8. 플롯 저장 ---")
    # 현재 활성화된 figure (마지막으로 생성/수정된 figure) 저장
    # 특정 figure 객체를 저장하려면: fig_object.savefig(...)
    # 예: if 'g_facet' in locals(): g_facet.savefig("myPlot_faceted.png", dpi=300)
    # 여기서는 마지막 플롯을 저장한다고 가정
    try:
        plt.savefig("myPlot_MiniProject5.png", dpi=150, bbox_inches='tight') # bbox_inches로 여백 조절
        print("   현재 플롯이 myPlot_MiniProject5.png로 저장됨.")
    except Exception as e:
        print(f"   플롯 저장 오류: {e}")

    # R의 saveRDS(plot_object, file)와 유사한 객체 저장은 Python의 pickle 사용.
    # Matplotlib/Seaborn 플롯 객체 자체를 pickle로 저장하는 것은 권장되지 않을 수 있음 (복잡성, 이식성).
    # 대신, 플롯 생성에 필요한 데이터와 코드를 저장하거나, 플롯을 이미지 파일로 저장하는 것이 일반적.

    # 9. 요약 통계 추가 (예: 중앙값)
    print("\n--- 9. 중앙값이 추가된 스파게티 플롯 ---")
    plt.figure(figsize=(12, 7))
    sns.set_theme(style="whitegrid") # 테마 재설정
    if 'USUBJID' in PR_mp5.columns: # 스파게티 플롯 배경
         sns.lineplot(data=PR_mp5, x='ADY', y='AVAL', hue='USUBJID',
                      legend=False, alpha=0.15, palette="tab20", zorder=1)

    # 전체 기간에 대한 중앙값 선 추가
    sns.lineplot(data=PR_mp5, x='ADY', y='AVAL',
                 estimator=np.median, errorbar=None, # errorbar=None으로 신뢰구간 제거
                 color='red', linewidth=2.5, zorder=2, label="전체 중앙값")
    plt.title("피험자별 심박수 변화 및 전체 중앙값")
    plt.xlabel("분석 상대일 (ADY)")
    plt.ylabel("심박수 (AVAL)")
    plt.legend()
    # plt.show()
    print("   전체 중앙값이 추가된 스파게티 플롯 생성됨.")

    # 특정 주(0, 5, 10, 15, 20, 25, 30)로 필터링하여 중앙값 표시
    if 'StudyWeek' in PR_mp5.columns:
        weeks_of_interest = [0, 5, 10, 15, 20, 25, 30]
        dataWeeks = PR_mp5[PR_mp5['StudyWeek'].isin(weeks_of_interest)].copy()
        if not dataWeeks.empty:
            # ADY 값을 StudyWeek 기준으로 재조정하면 x축이 일관성 없어질 수 있으므로,
            # 원본 ADY를 사용하되, 해당 주의 데이터 포인트에만 중앙값 마커/선 표시.
            # 여기서는 dataWeeks의 ADY를 그대로 사용.

            plt.figure(figsize=(12, 7))
            sns.set_theme(style="whitegrid")
            # 배경 스파게티 플롯 (전체 데이터 사용)
            if 'USUBJID' in PR_mp5.columns:
                sns.lineplot(data=PR_mp5, x='ADY', y='AVAL', hue='USUBJID',
                             legend=False, alpha=0.1, palette="tab20", zorder=1)

            # 선택된 주의 중앙값 포인트 및 선
            sns.lineplot(data=dataWeeks, x='ADY', y='AVAL',
                         estimator=np.median, errorbar=None,
                         color='blue', marker='o', markersize=7,
                         linewidth=2, zorder=2, label="선택된 주 중앙값")
            plt.title("심박수 변화 및 선택된 주 중앙값")
            plt.xlabel("분석 상대일 (ADY)")
            plt.ylabel("심박수 (AVAL)")
            plt.legend()
            # plt.show()
            print("   선택된 주에 대한 중앙값 플롯 생성됨.")
        else:
            print("   선택된 주에 대한 데이터가 없어 중앙값 플롯을 생성할 수 없습니다.")
    else:
        print("   StudyWeek 열이 없어 선택된 주에 대한 중앙값 플롯을 생성할 수 없습니다.")

    # 10. 축 범위
    print("\n--- 10. 축 범위 조정 ---")
    # 예시: 마지막으로 생성된 플롯의 Y축 범위 조정
    # plt.ylim(50, 120) # 데이터 잘림 (R의 scale_y_continuous(limits=...)와 유사)
    # plt.gca().set_ylim(50, 120) # 확대/축소 (R의 coord_cartesian(ylim=...)와 유사)
    # plt.show()
    print("   축 범위 조정은 plt.ylim() 또는 ax.set_ylim() 등으로 가능 (현재 주석 처리됨).")

    # 11. ggplot2 객체 정보 추출 -> matplotlib/seaborn 객체 정보 추출
    print("\n--- 11. 플롯 객체 정보 (예시) ---")
    # current_fig = plt.gcf() # 현재 Figure 객체
    # current_ax = plt.gca()  # 현재 Axes 객체
    # print(f"   현재 그림 크기 (인치): {current_fig.get_size_inches()}")
    # print(f"   현재 축 X 레이블: {current_ax.get_xlabel()}")
    # print(f"   현재 축 Y 레이블: {current_ax.get_ylabel()}")
    # print(f"   현재 축 제목: {current_ax.get_title()}")
    print("   Matplotlib/Seaborn 플롯 객체의 속성을 직접 조회하여 정보 추출 가능.")

    # 12. 데이터 변경 (R의 %+% 와 유사한 효과)
    print("\n--- 12. 데이터 변경하여 플롯 재생성 (개념) ---")
    # SysBP (수축기 혈압, PARAMN == 1) 데이터로 유사한 플롯 생성
    # advs_data_for_bp = load_and_preprocess_advs_mp5() # 원본 데이터 다시 로드 또는 advs 사용
    # if not advs.empty and 'PARAMN' in advs.columns: # advs 사용
    #    SysBP_df = advs[(advs['PARAMN'] == 1) & (advs['VISITNUM'] > 3)].copy()
    #    if not SysBP_df.empty:
    #        SysBP_df['StudyWeek'] = np.floor(SysBP_df['ADY'] / 7)
    #        print("   수축기 혈압(SysBP_df) 데이터 준비됨.")
    #
    #        plt.figure(figsize=(12, 7))
    #        sns.set_theme(style="whitegrid")
    #        sns.lineplot(data=SysBP_df, x='ADY', y='AVAL', estimator=np.median, errorbar=None,
    #                     color='darkgreen', linewidth=2.5, label="SysBP 전체 중앙값")
    #        study_id_bp = SysBP_df['STUDYID'].unique()[0] if SysBP_df['STUDYID'].nunique() > 0 else "N/A"
    #        param_bp = SysBP_df['PARAM'].unique()[0] if 'PARAM' in SysBP_df.columns and SysBP_df['PARAM'].nunique() > 0 else "Systolic BP"
    #        plt.title(f"연구 {study_id_bp}: {param_bp} 중앙값")
    #        plt.xlabel("분석 상대일 (ADY)")
    #        plt.ylabel(f"{param_bp} (AVAL)")
    #        plt.legend()
    #        # plt.show()
    #        print(f"   {param_bp} 데이터로 중앙값 플롯 생성됨.")
    #    else:
    #        print("   수축기 혈압 데이터를 찾을 수 없습니다 (PARAMN==1).")
    # else:
    #    print("   혈압 데이터 처리를 위한 원본 ADVS 데이터 또는 PARAMN 열이 없습니다.")
    print("   새 데이터로 플롯 함수를 다시 호출하여 유사한 효과를 낼 수 있습니다.")

else:
    print("초기 PR_mp5 데이터가 비어 있어 MiniProject5를 진행할 수 없습니다.")

# 스크립트 끝에서 모든 플롯을 한 번에 표시하려면 plt.show() 호출
# plt.show() # 모든 보류 중인 플롯 표시

# 마무리 주석:
# - 이 스크립트는 R의 ggplot2 코드를 Python의 Matplotlib/Seaborn으로 변환하는 과정을 보여줍니다.
# - 각 단계는 원본 Rmd 파일의 번호를 따르며, Pythonic한 방식으로 구현되었습니다.
# - 주석을 통해 R 코드와의 유사점, 차이점, Python 구현의 논리를 설명했습니다.
# - 오류 처리 (try-except), 조건부 실행 (if-else), 데이터 존재 여부 확인 등을 추가하여 코드의 견고성을 높였습니다.
# - PEP 8 스타일 가이드라인 (변수명, 공백 등)을 따르려고 노력했습니다.
# - 플롯 표시는 대화형 환경이 아닌 스크립트 실행 시 `plt.show()`가 필요함을 명시했습니다.
# - 데이터 로드 및 전처리는 재사용성을 위해 함수로 분리했습니다 (`load_and_preprocess_advs_mp5`).
# - 필요한 라이브러리 (`pandas`, `numpy`, `matplotlib`, `seaborn`)는 스크립트 상단에 import했습니다.
# - `pip install pandas pyreadstat matplotlib seaborn numpy` 명령으로 라이브러리 설치가 필요할 수 있습니다.
