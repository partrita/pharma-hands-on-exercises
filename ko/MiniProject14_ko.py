import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# usethis 패키지는 RStudio 스니펫 편집과 관련. Python에서는 IDE별 스니펫 관리 방식 따름.
# (예: VSCode는 JSON 파일, PyCharm은 설정 UI)

# --- R 스니펫 개념 및 Python에서의 유사 기능 ---
# R 스니펫: 자주 사용하는 코드 조각을 빠르게 삽입하는 텍스트 매크로.
# Python IDE (VSCode, PyCharm, JupyterLab 등)도 유사한 스니펫 기능 제공.
# 사용자가 직접 스니펫을 정의하고 단축키나 자동완성으로 사용 가능.

# 예시: R의 `fun` 스니펫 -> Python 함수 정의 스니펫
# Python IDE에서 "def" 입력 후 Tab 키 누르면 함수 템플릿 자동 완성되는 경우 많음.
# def function_name(parameters):
#     """Docstring"""
#     pass # 함수 본문

# --- 일반적으로 유용한 스니펫 (Python 버전) ---
# 1. `lib` (R) -> `imp` 또는 `imppd` 등 (Python)
#    snippet: imp
#    import ${1:module}
#    snippet: imppd
#    import pandas as pd
#    snippet: impnp
#    import numpy as np

# 2. `req` (R) -> Python에서는 보통 `import`만 사용. `try-except`로 모듈 존재 확인 가능.

# 3. `source` (R) -> Python에서 다른 .py 파일 실행은 `import` 또는 `runpy` 모듈.
#    스니펫으로 만들 수는 있으나, `import`가 일반적.

# 4. 데이터 프레임 정의 (`df` R) -> `pddef` 등 (Python)
#    snippet: pddef
#    ${1:df_name} = pd.DataFrame({
#        'col1': [${2:val1}, ${3:val2}],
#        'col2': [${4:val3}, ${5:val4}]
#    })

# 5. 행렬 정의 (`mat` R) -> `npmat` 등 (Python)
#    snippet: npmat
#    ${1:matrix_name} = np.array([
#        [${2:1}, ${3:2}],
#        [${4:3}, ${5:4}]
#    ])

# 6. 조건식 (`if`, `el`, `ei` R) -> `if`, `elif`, `else` (Python)
#    Python IDE는 이러한 기본 구문에 대한 자동완성/스니펫 내장.
#    snippet: ifel
#    if ${1:condition}:
#        ${2:pass}
#    else:
#        ${3:pass}
#    snippet: ifelifel
#    if ${1:condition1}:
#        ${2:pass}
#    elif ${3:condition2}:
#        ${4:pass}
#    else:
#        ${5:pass}

# 7. apply 함수 계열 (R) -> pandas의 apply, map 등 (Python)
#    snippet: dfapply
#    ${1:df_name}.apply(lambda ${2:x}: ${3:x.mean()}) # 예시

# 8. 기본 샤이니 앱 (`shinyapp` R) -> Python 웹 프레임워크 (Flask, Django, Streamlit, Dash)
#    각 프레임워크별 기본 앱 구조 스니펫 정의 가능.
#    snippet: streamlit_app
#    import streamlit as st
#    st.title("${1:My Streamlit App}")
#    ${2:# Add Streamlit components here}

print("--- Python 스니펫 개념 설명 ---")
print("Python IDE (VSCode, PyCharm 등)는 사용자 정의 스니펫 기능을 제공합니다.")
print("예를 들어, VSCode에서는 JSON 형식으로 스니펫을 정의할 수 있습니다.")
print("자주 사용하는 import문, 함수 템플릿, 클래스 구조 등을 스니펫으로 만들 수 있습니다.")


# --- 스니펫 사용자 지정 (Python IDE에서) ---
# RStudio의 스니펫 편집기 -> Python IDE의 스니펫 설정 메뉴/파일.
# VSCode 예시: File > Preferences > Configure User Snippets > python.json
# python.json 파일에 스니펫 정의:
# "Print to console": {
#    "prefix": "log", // 스니펫 호출 단축어
#    "body": [
#        "print(f\"${1:Variable Name}: {${1:Variable Name}}\")" // $1은 첫 번째 탭 위치
#    ],
#    "description": "Log output to console"
# }

# --- 스니펫 예제 (Python 버전) ---

# 1. 헤더 템플릿 스니펫
#    snippet: pyheader
#    ######################################################################
#    # Purpose: ${1:Description of the script}
#    # Author: ${2:Your Name}
#    # Date: `strftime("%Y-%m-%d")` (VSCode 스니펫 변수)
#    # Called by: ${3:N/A or script_name.py}
#    # Inputs:
#    #   ${4:input_file.csv}
#    # Outputs:
#    #   ${5:output_file.png or results.txt}
#    # Notes: ${6:Any notes here}
#    ######################################################################
#    # History
#    ######################################################################
#    # Revision    Author      Date          Description
#    # 1.0         ${2:Your Name}  `strftime("%Y-%m-%d")`    Initial creation
#    ######################################################################

print("\n--- 스니펫 예제 (Python) ---")
print("1. 헤더 템플릿: Python 스크립트 상단에 작성자, 목적, 날짜 등 정보 포함.")
# 위 스니펫을 사용하면 아래와 유사한 헤더 자동 생성 가능 (실제 실행은 아님)
# ######################################################################
# # Purpose: Create a plot for analysis
# # Author: Your Name
# # Date: 2023-10-27
# # ...
# ######################################################################

# 2. 라이브러리 로드 스니펫
#    snippet: common_imports
#    import pandas as pd
#    import numpy as np
#    import matplotlib.pyplot as plt
#    import seaborn as sns
#    print("Common libraries imported.")

print("\n2. 라이브러리 스니펫: 자주 사용하는 import문 모음.")
# 위 스니펫 실행 결과 (실제 import는 스크립트 상단에서 수행)
# import pandas as pd
# import numpy as np
# ...

# 3. 플롯 스니펫 (matplotlib/seaborn 기반)
#    snippet: sns_hist
#    plt.figure(figsize=(${1:10}, ${2:6}))
#    sns.histplot(data=${3:df_name}, x="${4:column_name}", kde=${5:True})
#    plt.title("${6:Histogram of ${4:column_name}}")
#    plt.xlabel("${4:column_name}")
#    plt.ylabel("Frequency")
#    plt.show()

print("\n3. 플롯 스니펫: 기본적인 matplotlib/seaborn 플롯 템플릿.")
# 예시 데이터프레임 생성
plot_example_df = pd.DataFrame({
    'value': np.random.randn(100)
})
# 위 스니펫을 사용한 플롯 생성 (실제 스니펫 사용 대신 직접 코드 작성)
# plt.figure(figsize=(10, 6))
# sns.histplot(data=plot_example_df, x="value", kde=True)
# plt.title("Histogram of value")
# plt.xlabel("value")
# plt.ylabel("Frequency")
# plt.show() # 주석 해제 시 플롯 표시
print("   (플롯 생성 코드 실행됨, plt.show() 주석 처리됨)")


# R의 MiniProject 7, 11에서 함수 작성 논의 -> Python에서도 함수 재사용 중요.
# 스니펫은 함수 템플릿을 만드는 데 유용하지만, 잘 정의된 함수를 라이브러리화하는 것이 더 강력.

print("\n--- Python 스니펫 활용 결론 ---")
print("Python에서도 스니펫은 반복적인 코드 작성을 줄이고 일관성을 유지하는 데 유용합니다.")
print("각 IDE의 스니펫 기능을 활용하여 개인 또는 팀의 생산성을 높일 수 있습니다.")
print("자주 사용하는 패턴(데이터 로드, 전처리, 시각화, 모델 학습 등)에 대한 스니펫을 만드는 것이 좋습니다.")

# `pip install pandas numpy matplotlib seaborn` 필요할 수 있음.
# 이 스크립트는 R 스니펫의 개념을 Python 환경에 맞게 설명하고,
# Python IDE에서 스니펫을 어떻게 활용할 수 있는지 예시를 통해 보여줌.
# 실제 스니펫 생성 및 사용은 각자 사용하는 Python IDE의 설명서 참고.
