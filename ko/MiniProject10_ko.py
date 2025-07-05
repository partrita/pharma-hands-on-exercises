import pandas as pd
import sys # traceback 예시용
import pdb # Python Debugger

# 디버깅 전략 (Python 관점)
# 1. 환경 비우기/재시작: Python에서는 변수 재할당, 커널 재시작(Jupyter), 인터프리터 재시작 등으로 유사 효과.
# 2. 환경 이해: 전역/지역 변수 범위 (LEGB 규칙: Local, Enclosing, Global, Built-in).
# 3. pdb, IDE 디버거, print() 문 사용.
# 4. traceback 모듈, sys.exc_info(), IDE의 예외 정보 활용.

# R의 환경 비우기/재시작 관련 설명은 Python에 직접적으로 동일하게 적용되지는 않지만,
# 깨끗한 상태에서 스크립트를 실행하는 것의 중요성은 동일.

# 전역 및 지역 환경 예시 (Python)
print("--- 전역/지역 환경 예시 ---")
a_global_py = 4 # 전역 변수

def my_function_env_py(x):
    a_local_py = 3 # 함수 내 지역 변수
    print(f"  함수 내: a_local_py = {a_local_py}, a_global_py = {a_global_py}, x = {x}")
    return x + a_local_py # 지역 a_local_py 사용

print(f"호출 전: a_global_py = {a_global_py}")
result_env_py = my_function_env_py(2)
print(f"호출 후: result_env_py = {result_env_py}, a_global_py = {a_global_py}")
# print(a_local_py) # NameError: a_local_py는 함수 외부에서 접근 불가

# R의 debugonce() -> Python의 pdb.set_trace() 또는 IDE 중단점
# pdb.set_trace()는 코드 실행 중 해당 지점에서 디버거를 시작.
def my_function_debug_py(x):
    a = 3
    # pdb.set_trace() # 여기에 중단점 설정. 실행 시 디버거 프롬프트 (Pdb) 표시.
    # 디버거에서 n (다음 줄), c (계속), p <변수명> (변수 값 출력) 등의 명령 사용 가능.
    # 주석 처리된 상태로 두어 자동 실행 방지. 필요시 주석 해제.
    print("  my_function_debug_py 실행 중... (pdb.set_trace() 주석 처리됨)")
    return x + a

print("\n--- pdb.set_trace() 예시 (주석 처리됨) ---")
# my_function_debug_py(2) # 실행 시 디버거 시작 (주석 해제 시)


# 인셉션 - 토끼굴 아래로 (함수 호출 스택 디버깅)
# Python 디버거(pdb 또는 IDE 디버거)는 호출 스택을 탐색하는 기능 (up, down 명령) 제공.
def my_function_inner_py(val):
    # pdb.set_trace() # 내부 함수 중단점
    print(f"    my_function_inner_py({val}) 실행 중...")
    return val * val

def my_function_outer_py(x):
    # pdb.set_trace() # 외부 함수 중단점
    print(f"  my_function_outer_py({x}) 실행 중...")
    y = my_function_inner_py(x + 1) # myFunction(x) 대신 x+1 사용
    return y

print("\n--- 함수 호출 스택 디버깅 예시 (주석 처리됨) ---")
# my_function_outer_py(4) # 실행 시 디버거 시작 (주석 해제 시)

# 디버깅에 도움이 되는 코드 추가
# print() 문 사용 (R과 유사)
def my_function_print_py(x):
    print("  함수 my_function_print_py 내:")
    a_val = 3
    print(f"    a_val: {a_val}")
    print(f"    x: {x}")
    result_val = x + a_val
    print(f"    x + a_val: {result_val}")
    print("  결과:")
    return result_val

print("\n--- print() 문을 사용한 디버깅 예시 ---")
global_a_val = 4
print(f"호출 전 global_a_val: {global_a_val}")
my_function_print_py(2)


# R의 browser() -> Python의 pdb.set_trace() (이미 설명됨)
# R의 중단점(breakpoint) -> Python IDE (VSCode, PyCharm 등)에서 유사한 중단점 기능 제공.
# .R 스크립트 파일을 여는 것과 유사하게 .py 파일을 열고 편집기에서 중단점 설정.
# "MiniProject10_breakpoint_script.py" 와 같은 파일을 만들어 테스트 가능.
# (이 파일에서는 해당 스크립트를 직접 만들지는 않음)

# R의 traceback() -> Python의 traceback 모듈 또는 예외 객체 활용
print("\n--- traceback 예시 ---")
def func_c_py():
    # print(1 / 0) # ZeroDivisionError 발생
    raise ValueError("테스트용 오류 발생 in func_c_py")

def func_b_py():
    func_c_py()

def func_a_py():
    func_b_py()

try:
    func_a_py()
except ValueError as e:
    print(f"예외 발생: {e}")
    import traceback
    print("Traceback 정보:")
    traceback.print_exc() # R의 traceback()과 유사한 정보 출력

# R의 options(error = recover) -> Python의 pdb.pm() (사후 디버깅)
# 스크립트를 `python -m pdb my_script.py`로 실행하거나,
# 예외 발생 후 대화형 세션에서 pdb.pm() 호출.
# 예시 (대화형 세션에서 실행):
# >>> import pdb
# >>> func_a_py() # 오류 발생 가정
# >>> pdb.pm() # 오류 지점에서 디버거 시작

print("\n--- pdb.pm() 개념 설명 (실제 실행은 대화형 세션 또는 스크립트 실행 방식 변경 필요) ---")
print("# 예외 발생 시, 'python -m pdb your_script.py'로 실행하거나,")
print("# 대화형 세션에서 import pdb; pdb.pm()을 사용하면 사후 디버깅 가능.")


# 도전 과제: adsl_counts 함수 오류 찾기 (Python 버전으로 가정)
# MiniProject7_ko.py의 adsl_counts_py 또는 adsl_counts_from_df_py 함수를 사용한다고 가정.
# R 코드의 오류 원인과 유사한 잠재적 오류 지점:
# 1. 입력 데이터(dataFile 또는 DataFrame) 문제: 경로 오류, 파일 형식, 필요한 열 누락.
# 2. count(name="n") -> pandas의 .size().reset_index(name="n")에서 컬럼명 오타 또는 누락.
#    R 코드 원본: `summarise(name = "n")` -> `summarise(n = n())`이 더 일반적.
#    Python 변환 시: `size().reset_index(name='n')`은 맞지만, 이후 `n` 컬럼 참조.
# 3. left_join(Big_N_cnt, by = c("TRT01AN","TRT01A")) -> pd.merge() 시 on 컬럼 또는 how 방식 오류.
# 4. mutate(perc = round((n/N)*100, digits=1)) -> N이 0이거나 NA인 경우 ZeroDivisionError 또는 NaN 발생.
#    Python에서는 N이 0인 경우 np.inf 또는 에러. NA면 결과도 NA.
# 5. recode(SEX, "M" = "Male", "F" = "Female") -> SEX 열에 예기치 않은 값 존재 시 문제.
# 6. select(TRT01A, SEX, npct) -> 이전 단계에서 해당 열이 제대로 생성되지 않은 경우.
# 7. pivot_wider(names_from = TRT01A, values_from = npct) -> 피벗 시 중복 인덱스 또는 예기치 않은 데이터 구조.

# 예시: adsl_counts_from_df_py (MiniProject7_ko.py에서 가져온 버전)의 잠재적 오류 수정
# 원본 R 코드의 `summarise(name = "n")`은 `summarise(n = n())`의 오타로 보임.
# Python 변환 시 `size().reset_index(name='n')`은 올바르지만,
# 만약 `name`이라는 열을 만들고 그 안에 문자열 "n"을 넣으려 했다면 로직 오류.

# MiniProject7_ko.py의 adsl_counts_from_df_py 함수는 이미 N=0 또는 NA인 경우를
# 일부 처리하려고 시도했음 (`merged_df['npct'] = merged_df['n'].astype(str) + " (N/A)"`).
# 이 부분이 R 코드의 오류와 관련된 핵심 수정 사항일 수 있음.

print("\n--- 도전 과제 관련 (adsl_counts_py 함수 디버깅 가정) ---")
# adsl_counts_from_df_py 함수를 여기에 복사하거나 import하여 사용한다고 가정.
# (MiniProject7_ko.py의 정의를 사용)
# from MiniProject7_ko import adsl_counts_from_df_py # 실제로는 이렇게 import

# 테스트 데이터 생성 (오류 유발 가능성 있는 케이스 포함)
test_data_error_py = pd.DataFrame({
    'TRT01AN': [1, 1, 2, 2, 1],
    'TRT01A': ['A', 'A', 'B', 'B', 'A'],
    'SEX': ['Male', 'Female', 'Male', 'Female', 'Male'],
    'SAFFL': ['Y', 'Y', 'Y', 'Y', 'Y'],
    # N이 0이 되는 경우를 만들기 위해 특정 그룹의 데이터가 없는 상황은
    # groupby 후 merge 시 나타날 수 있음. 또는 small_n은 있으나 big_n이 0인 경우.
})
# Big_N_cnt에서 TRT01A='C' 그룹이 없다고 가정. small_n_cnt에는 TRT01A='C'가 있는 경우 left_join 후 N이 NA.
# 또는 N이 0인 경우.

# adsl_counts_from_df_py 함수는 이미 N이 0 또는 NA인 경우를 일부 처리함.
# 해당 함수의 방어적 코드가 R 버전의 오류를 수정한 것으로 볼 수 있음.
# print("테스트 데이터로 adsl_counts_from_df_py 실행:")
# error_result = adsl_counts_from_df_py(test_data_error_py) # MiniProject7_ko.py의 함수 필요
# if not error_result.empty:
#     print(error_result)
# else:
#     print("오류 테스트 결과가 비어있습니다 (함수 내에서 처리되었을 수 있음).")

print("R 코드의 `summarise(name = \"n\")` 부분은 `summarise(n = n())`의 오타일 가능성이 높습니다.")
print("Python으로 변환 시 `groupby().size().reset_index(name='n')`은 올바르며,")
print("이후 `n`과 `N` 열을 사용하여 백분율을 계산합니다.")
print("N이 0이거나 NA인 경우, MiniProject7_ko.py의 Python 함수는 이를 처리하여 오류를 방지합니다.")

# `pip install pandas pyreadstat` 필요할 수 있음.
# 이 스크립트는 R의 디버깅 도구와 개념을 Python의 해당 기능과 비교 설명.
# pdb, IDE 디버거, traceback 모듈, print()문 등이 Python 디버깅의 핵심.
# 도전 과제는 R 코드의 특정 오류를 Python으로 변환된 함수에서 어떻게 수정/방지할 수 있는지 보여줌.
# (주로 MiniProject7_ko.py에서 이미 구현된 방어적 코드를 통해)
