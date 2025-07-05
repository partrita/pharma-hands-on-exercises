import pandas as pd

# 1. 패키지 로드 (pandas는 이미 MiniProject1_ko.py에서 로드됨)
# Python에서는 스크립트 시작 부분에 import 문을 한 번만 사용합니다.

# 2. 데이터 읽기 및 초기 필터링
try:
    adsl = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
except Exception as e:
    print(f"데이터 읽기 오류: {e}")
    adsl = pd.DataFrame()

if not adsl.empty:
    print("원본 ADSL 데이터:")
    print(adsl.head())
    print(f"ADSL 데이터 객체에는 {adsl.shape[0]}개의 행과 {adsl.shape[1]}개의 열이 있습니다.")

    # EFFFL == "Y"로 필터링
    if 'EFFFL' in adsl.columns:
        adsl_eff = adsl[adsl['EFFFL'] == 'Y'].copy()
        print("\nEFFFL == 'Y'로 필터링된 adsl_eff 데이터:")
        print(adsl_eff.head())
        print(f"필터링 후 adsl_eff에는 {adsl_eff.shape[0]}개의 행과 {adsl_eff.shape[1]}개의 열이 있습니다.")
    else:
        print("EFFFL 열을 찾을 수 없어 adsl_eff를 만들 수 없습니다.")
        adsl_eff = pd.DataFrame()
else:
    adsl_eff = pd.DataFrame()

# 3. 한계 총계 (N) 계산
if not adsl_eff.empty and 'TRT01A' in adsl_eff.columns and 'TRT01AN' in adsl_eff.columns:
    # R의 group_by() %>% count()와 유사
    Big_N_cnt = adsl_eff.groupby(['TRT01AN', 'TRT01A']).size().reset_index(name='N')
    print("\nBig_N_cnt (치료 그룹별 총계):")
    print(Big_N_cnt)
else:
    print("\nTRT01A 또는 TRT01AN 열을 찾을 수 없거나 adsl_eff가 비어 있어 Big_N_cnt를 계산할 수 없습니다.")
    Big_N_cnt = pd.DataFrame()

# 4. 작은 n 개수 계산 (치료 그룹 및 SEX별)
if not adsl_eff.empty and 'SEX' in adsl_eff.columns:
    small_n_cnt = adsl_eff.groupby(['TRT01AN', 'TRT01A', 'SEX']).size().reset_index(name='n')
    print("\nsmall_n_cnt (치료 그룹 및 SEX별 개수):")
    print(small_n_cnt)

    # group_by() 순서 변경 예시
    # small_n_cnt_alt_order = adsl_eff.groupby(['SEX', 'TRT01AN', 'TRT01A']).size().reset_index(name='n')
    # print("\n순서 변경된 small_n_cnt:")
    # print(small_n_cnt_alt_order)
else:
    print("\nSEX, TRT01A 또는 TRT01AN 열을 찾을 수 없거나 adsl_eff가 비어 있어 small_n_cnt를 계산할 수 없습니다.")
    small_n_cnt = pd.DataFrame()


# 5. Big_N_cnt와 small_n_cnt 병합
if not small_n_cnt.empty and not Big_N_cnt.empty:
    # R의 left_join과 유사
    adsl_mrg_cnt = pd.merge(small_n_cnt, Big_N_cnt, on=['TRT01AN', 'TRT01A'], how='left')
    print("\n병합된 adsl_mrg_cnt:")
    print(adsl_mrg_cnt)
else:
    print("\nsmall_n_cnt 또는 Big_N_cnt가 비어 있어 병합할 수 없습니다.")
    adsl_mrg_cnt = pd.DataFrame()

# 6. 백분율 계산
if not adsl_mrg_cnt.empty and 'n' in adsl_mrg_cnt.columns and 'N' in adsl_mrg_cnt.columns:
    # R의 mutate(perc = (n/N)*100)와 유사
    adsl_mrg_cnt['perc'] = (adsl_mrg_cnt['n'] / adsl_mrg_cnt['N']) * 100
    print("\n백분율이 추가된 adsl_mrg_cnt:")
    print(adsl_mrg_cnt)
else:
    print("\n필요한 열(n, N)이 없거나 adsl_mrg_cnt가 비어 있어 백분율을 계산할 수 없습니다.")

# 7. 백분율 반올림
if not adsl_mrg_cnt.empty and 'perc' in adsl_mrg_cnt.columns:
    # R의 round(digits=1)와 유사
    adsl_mrg_cnt['perc'] = adsl_mrg_cnt['perc'].round(1)
    print("\n반올림된 백분율이 있는 adsl_mrg_cnt:")
    print(adsl_mrg_cnt)

    # R의 round() 동작에 대한 참고: Python의 round()는 "round half to even"을 사용합니다.
    # x = pd.Series([1.1, 1.499, 1.5, 1.9, 2.5])
    # print("\nPython round() 예시:")
    # print(x.round()) # R과 동일한 동작 (기본적으로)
else:
    print("\nperc 열이 없거나 adsl_mrg_cnt가 비어 있어 반올림할 수 없습니다.")

# 8. 숫자 값 서식 지정
if not adsl_mrg_cnt.empty and 'perc' in adsl_mrg_cnt.columns:
    # R의 format(nsmall=1)과 유사
    # Python에서는 f-string 또는 format() 메서드를 사용하여 문자열 서식을 지정합니다.
    adsl_mrg_cnt['perc_char'] = adsl_mrg_cnt['perc'].apply(lambda x: f"{x:.1f}")
    print("\n서식이 지정된 백분율 문자열이 있는 adsl_mrg_cnt:")
    print(adsl_mrg_cnt[['perc', 'perc_char']])
else:
    print("\nperc 열이 없거나 adsl_mrg_cnt가 비어 있어 서식을 지정할 수 없습니다.")


# 9. 개수와 백분율 함께 붙여넣기
if not adsl_mrg_cnt.empty and 'n' in adsl_mrg_cnt.columns and 'perc_char' in adsl_mrg_cnt.columns:
    # R의 paste()와 유사
    adsl_mrg_cnt['npct'] = adsl_mrg_cnt['n'].astype(str) + " (" + adsl_mrg_cnt['perc_char'] + ")"
    print("\n개수와 백분율이 결합된 adsl_mrg_cnt:")
    print(adsl_mrg_cnt[['n', 'perc_char', 'npct']])

    # paste 예시
    # n_val = 6
    # perc_char_val = "26.1"
    # print(f"\npaste 예시 1: {n_val} ({perc_char_val})")
    # print(f"paste 예시 2: {n_val} ({perc_char_val})")
    # print(f"paste 예시 3: {str(n_val) + '(' + perc_char_val + ')'}")
    # print(f"paste 예시 4: {str(n_val) + '(' + perc_char_val + ')'}")
    # print(f"paste 예시 5: {str(n_val) + ' (' + perc_char_val + ')'}")
else:
    print("\n필요한 열(n, perc_char)이 없거나 adsl_mrg_cnt가 비어 있어 결합할 수 없습니다.")

# 10. SEX 레이블 변경
if not adsl_mrg_cnt.empty and 'SEX' in adsl_mrg_cnt.columns:
    # R의 recode()와 유사
    sex_map = {"M": "Male", "F": "Female"}
    adsl_mrg_cnt['SEX'] = adsl_mrg_cnt['SEX'].replace(sex_map)
    print("\nSEX 레이블이 변경된 adsl_mrg_cnt:")
    print(adsl_mrg_cnt[['SEX', 'npct']])
else:
    print("\nSEX 열이 없거나 adsl_mrg_cnt가 비어 있어 레이블을 변경할 수 없습니다.")

# 11. 그룹 해제 (pandas에서는 명시적인 ungroup이 필요하지 않음, groupby 후 작업은 일반적으로 그룹 해제된 결과를 반환)
# 이전 단계에서 reset_index() 또는 직접 열 할당을 사용하여 이미 그룹 해제됨.

# 12. 파이프라인으로 단계 연결
if not adsl_eff.empty and not Big_N_cnt.empty and not small_n_cnt.empty :
    # R의 파이프라인을 Python 메서드 체인으로 변환
    # (이미 각 단계에서 수행했으므로 여기서는 최종 결과만 표시)
    # 최종 adsl_mrg_cnt는 이미 이전 단계에서 계산되었습니다.
    # 여기서는 필요한 열만 선택하는 과정을 보여줍니다.
    if 'TRT01A' in adsl_mrg_cnt.columns and 'SEX' in adsl_mrg_cnt.columns and 'npct' in adsl_mrg_cnt.columns:
        final_adsl_mrg_cnt_selected = adsl_mrg_cnt[['TRT01A', 'SEX', 'npct']].copy()
        print("\n파이프라인 결과 (선택된 열):")
        print(final_adsl_mrg_cnt_selected)
    else:
        print("\n필요한 열이 adsl_mrg_cnt에 없어 최종 선택을 수행할 수 없습니다.")
        final_adsl_mrg_cnt_selected = pd.DataFrame()
else:
    print("\n초기 데이터가 비어 있어 파이프라인을 실행할 수 없습니다.")
    final_adsl_mrg_cnt_selected = pd.DataFrame()


# 13. 테이블에 맞게 데이터 전치
if not final_adsl_mrg_cnt_selected.empty:
    # R의 pivot_wider()와 유사
    try:
        adsl_pivot = final_adsl_mrg_cnt_selected.pivot_table(index='SEX', columns='TRT01A', values='npct', aggfunc='first').reset_index()
        # 컬럼 이름 정리 (필요한 경우)
        adsl_pivot.columns.name = None
        print("\n피벗된 테이블 adsl_pivot:")
        print(adsl_pivot)
    except Exception as e:
        print(f"피벗 오류: {e}")
        adsl_pivot = pd.DataFrame()
else:
    print("\nfinal_adsl_mrg_cnt_selected가 비어 있어 피벗할 수 없습니다.")
    adsl_pivot = pd.DataFrame()

# 도전 과제 1: AGEGRP 추가
if not adsl_eff.empty and 'AGEGR1' in adsl_eff.columns and 'AGEGR1N' in adsl_eff.columns:
    print("\n--- 도전 과제 1 시작 ---")
    Big_N_cnt_age = adsl_eff.groupby(['TRT01AN', 'TRT01A', 'AGEGR1N', 'AGEGR1']).size().reset_index(name='N_age')
    print("\nBig_N_cnt (AGEGR1 포함):")
    print(Big_N_cnt_age)

    small_n_cnt_age = adsl_eff.groupby(['TRT01AN', 'TRT01A', 'SEX', 'AGEGR1N', 'AGEGR1']).size().reset_index(name='n_age')
    print("\nsmall_n_cnt (AGEGR1 포함):")
    print(small_n_cnt_age)

    if not small_n_cnt_age.empty and not Big_N_cnt_age.empty:
        adsl_mrg_cnt_age = pd.merge(small_n_cnt_age, Big_N_cnt_age, on=['TRT01AN', 'TRT01A', 'AGEGR1N', 'AGEGR1'], how='left')

        # 전체 N (치료 그룹별) 다시 계산 또는 기존 Big_N_cnt 사용
        if not Big_N_cnt.empty:
             adsl_mrg_cnt_age = pd.merge(adsl_mrg_cnt_age, Big_N_cnt, on=['TRT01AN', 'TRT01A'], how='left')

        if 'n_age' in adsl_mrg_cnt_age.columns and 'N' in adsl_mrg_cnt_age.columns: # N은 전체 치료 그룹의 총합
            adsl_mrg_cnt_age['perc_age_total'] = (adsl_mrg_cnt_age['n_age'] / adsl_mrg_cnt_age['N']) * 100 # AGEGR1내 성별 백분율이 아닌, 전체 N에 대한 백분율
            adsl_mrg_cnt_age['perc_age_total'] = adsl_mrg_cnt_age['perc_age_total'].round(1)
            adsl_mrg_cnt_age['perc_char_age_total'] = adsl_mrg_cnt_age['perc_age_total'].apply(lambda x: f"{x:.1f}")
            adsl_mrg_cnt_age['npct_age_total'] = adsl_mrg_cnt_age['n_age'].astype(str) + " (" + adsl_mrg_cnt_age['perc_char_age_total'] + ")"

            # SEX 레이블 변경
            sex_map = {"M": "Male", "F": "Female"}
            adsl_mrg_cnt_age['SEX'] = adsl_mrg_cnt_age['SEX'].replace(sex_map)

            final_adsl_mrg_cnt_age_selected = adsl_mrg_cnt_age[['TRT01A', 'SEX', 'AGEGR1', 'npct_age_total']].copy()

            try:
                adsl_pivot_age = final_adsl_mrg_cnt_age_selected.pivot_table(index=['AGEGR1', 'SEX'], columns='TRT01A', values='npct_age_total', aggfunc='first').reset_index()
                adsl_pivot_age.columns.name = None
                print("\n피벗된 테이블 (AGEGR1 포함):")
                print(adsl_pivot_age)
            except Exception as e:
                print(f"AGEGR1 포함 피벗 오류: {e}")
        else:
            print("\n도전 과제 1: 필요한 열(n_age, N)이 없어 백분율 계산 불가")
    else:
        print("\n도전 과제 1: small_n_cnt_age 또는 Big_N_cnt_age가 비어 있어 병합 또는 계산 불가")
    print("--- 도전 과제 1 종료 ---")
else:
    print("\nAGEGR1 또는 AGEGR1N 열을 찾을 수 없거나 adsl_eff가 비어 있어 도전 과제 1을 수행할 수 없습니다.")


# 도전 과제 2: adae.xpt 데이터로 안전 모집단(SAFFL)에 대한 신체 텍스트 용어(AEBODSYS) 개수 및 백분율 생성
# 이 부분은 adae.xpt 파일 구조와 내용에 따라 유사한 방식으로 구현할 수 있습니다.
# 예시:
# try:
#     adae = pd.read_sas("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adae.xpt")
# except Exception as e:
#     print(f"\nADAE 데이터 읽기 오류: {e}")
#     adae = pd.DataFrame()

# if not adae.empty and 'SAFFL' in adae.columns and 'AEBODSYS' in adae.columns and 'TRT01A' in adae.columns:
#     print("\n--- 도전 과제 2 시작 ---")
#     adae_saffl = adae[adae['SAFFL'] == 'Y'].copy()
#
#     # 전체 N 계산 (SAFFL='Y'인 각 TRT01A 그룹에 대해)
#     Total_N_adae = adae_saffl.groupby('TRT01A')['USUBJID'].nunique().reset_index(name='Total_N_USUBJID')
#
#     # AEBODSYS별 환자 수 계산
#     aebodsys_counts = adae_saffl.groupby(['TRT01A', 'AEBODSYS'])['USUBJID'].nunique().reset_index(name='n_patients_AEBODSYS')
#
#     # 병합
#     adae_summary = pd.merge(aebodsys_counts, Total_N_adae, on='TRT01A', how='left')
#
#     # 백분율 계산
#     if 'n_patients_AEBODSYS' in adae_summary.columns and 'Total_N_USUBJID' in adae_summary.columns:
#         adae_summary['perc_patients_AEBODSYS'] = (adae_summary['n_patients_AEBODSYS'] / adae_summary['Total_N_USUBJID']) * 100
#         adae_summary['perc_patients_AEBODSYS'] = adae_summary['perc_patients_AEBODSYS'].round(1)
#         adae_summary['perc_char_AEBODSYS'] = adae_summary['perc_patients_AEBODSYS'].apply(lambda x: f"{x:.1f}")
#         adae_summary['npct_AEBODSYS'] = adae_summary['n_patients_AEBODSYS'].astype(str) + " (" + adae_summary['perc_char_AEBODSYS'] + ")"
#
#         # 피벗
#         try:
#             adae_pivot = adae_summary.pivot_table(index='AEBODSYS', columns='TRT01A', values='npct_AEBODSYS', aggfunc='first', fill_value="0 (0.0)").reset_index()
#             adae_pivot.columns.name = None
#             print("\nAEBODSYS 요약 테이블:")
#             print(adae_pivot)
#         except Exception as e:
#             print(f"AEBODSYS 피벗 오류: {e}")
#     else:
#         print("\n도전 과제 2: 필요한 열이 없어 백분율 계산 불가")
#
#     print("--- 도전 과제 2 종료 ---")
# else:
#     print("\nSAFFL, AEBODSYS 또는 TRT01A 열을 찾을 수 없거나 adae가 비어 있어 도전 과제 2를 수행할 수 없습니다.")

# 스크립트 실행을 위해 `pip install pandas pyreadstat` 필요할 수 있음
# pyreadstat은 pandas가 .xpt 파일을 읽는 데 사용합니다.
# 이 스크립트는 R의 dplyr 및 tidyr 기능을 pandas로 변환하는 데 중점을 둡니다.
# 각 R 청크는 Python의 해당 섹션으로 변환되었습니다.
# 오류 처리 및 조건부 실행이 추가되어 견고성을 높였습니다.
# R의 파이프(%>%)는 pandas 메서드 체인으로 변환되었습니다.
# R의 count()는 pandas의 groupby().size().reset_index()로 변환되었습니다.
# R의 left_join()은 pandas의 pd.merge()로 변환되었습니다.
# R의 mutate()는 pandas의 직접 열 할당 또는 .assign()으로 변환되었습니다.
# R의 recode()는 pandas의 .replace()로 변환되었습니다.
# R의 pivot_wider()는 pandas의 .pivot_table()로 변환되었습니다.
# R의 format(nsmall=1)은 Python의 문자열 포매팅 (예: f"{x:.1f}")으로 변환되었습니다.
# R의 paste()는 Python의 문자열 연결 (+)로 변환되었습니다.
# 전반적인 목표는 R 스크립트의 핵심 로직을 Python으로 복제하는 것입니다.
# 도전 과제는 Python의 pandas 기능을 사용하여 유사한 분석을 수행하는 방법을 보여줍니다.
# 실제 데이터와 요구 사항에 따라 도전 과제 구현이 달라질 수 있습니다.
