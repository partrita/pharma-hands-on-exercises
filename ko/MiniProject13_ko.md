`{r setup, include=FALSE} knitr::opts_chunk$set(echo = TRUE)`

## 왜요?

코드 스타일은 동료들이 코드가 무엇을 하는지 읽고 이해하는 데 도움이
되며(QC에 필수적임), 나중에 코드를 다시 방문할 때 "미래의 당신"이 무엇을
하고 있었는지 기억하는 데도 도움이 됩니다. 직무 설명에 "프로그래머"가
없더라도 "미래의 당신"이나 제3자가 작성한 코드를 이해할 수 있도록 알아야
할 특정 표준과 좋은 관행이 있습니다.

### 요약:

-   일관된 스타일을 사용하십시오. RStudio IDE 내에서 쉽게 구현할 수 있는
    도구가 있으므로 tidyverse 스타일 가이드를 사용하는 것이 좋습니다.
-   session_info() 또는 {logrx} 패키지 함수 axecute()를 사용하여 R 세션
    및 환경 정보를 캡처하십시오. 이를 일상적으로 수행하십시오.
-   R 패키지의 일부로 R 코드 함수를 작성하는 경우가 아니면 {rmarkdown}
    문서를 사용하여 작업을 시작하고 코드 주위에 설명을 작성하고 HTML로
    렌더링하십시오.
-   반복하지 마십시오: 함수를 작성, 문서화 및 테스트하십시오. 간단한
    함수는 더 복잡한 함수로 구성됩니다. 함수에 문제가 발생하지 않도록
    "가드 레일"을 제공하여 다른 사람들을 도우십시오.

(+ - "너무 길어서 읽지 않음")

이 미니 프로젝트에서는 일관된 스타일 사용과 RStudio IDE가 코드를
정리하는 데 어떻게 도움이 되는지 살펴봅니다.

먼저 더럽고 지저분한 코드가 필요합니다.

\`\`\`{r} library(rio) library(tidyverse) library(gt) library(readr)

## Mike K Smith 작성 코드

## 원본 2023년 10월

## 최종 수정 2022년 12월

## 이 코드는 치료 및 성별별 인구 통계 요약을 계산합니다. 이 코드는 "M"="남성" 및 "F"="여성"이라고 가정합니다.

adsl_saf =
import("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
%\>% filter(SAFFL == "Y")

BIGNcnt= adsl_saf %\>% group_by( TRT01AN,TRT01A ) %\>% count(name="N")

\## 성별 각 범주에 대한 개수 계산

small_n_cnt=adsl_saf %\>% group_by( TRT01AN, TRT01A, SEX ) %\>%
count(name = "n") small_n_cnt

adsl_mrg_cnt\<-small_n_cnt %\>% left_join(BIGNcnt, by = c("TRT01A",
"TRT01AN")) %\>% mutate(perc = round((n/N)\*100, digits=1), perc_char =
format(perc, nsmall=1), npct = paste(n, paste0( "(", perc_char, ")" ) )
) %\>% mutate(SEX = recode(SEX, "M" = "Male", "F" = "Female")) %\>%
ungroup() %\>% select(TRT01A, SEX, npct) %\>%
pivot_wider(names_from=TRT01A,values_from=npct)

adsl_mrg_cnt

      BIGNcnt =  adsl_saf   %>%
    group_by( TRT01AN, TRT01A  ) %>%
    count(name = "N")

\## 성별 각 범주에 대한 개수 계산

small_n_cnt = adsl_saf %\>% group_by( TRT01AN, TRT01A, AGEGR1 ) %\>%
count(name = "n") small_n_cnt

adsl_mgr_cnt \<- small_n_cnt %\>% left_join(BIGNcnt, by = c("TRT01A",
"TRT01AN")) %\>% mutate(perc = round((n/N)\*100, digits=1), perc_char =
format(perc, nsmall=1), npct = paste(n, paste0( "(", perc_char, ")" ) )
) %\>% ungroup() %\>% select(TRT01A, AGEGR1, npct) %\>%
pivot_wider(names_from = TRT01A, values_from = npct)

adsl_mgr_cnt

BIGNcnt = adsl_saf %\>% group_by( TRT01AN, TRT01A ) %\>% count(name =
"N")

\## 성별 각 범주에 대한 개수 계산

small_n_cnt = adsl_saf %\>% group_by( TRT01AN, TRT01A, RACE ) %\>%
count(name = "n") small_n_cnt

adsl_mrg_cnt \<- small_n_cnt %\>% left_join(BIGNcnt, by = c("TRT01A",
"TRT01AN")) %\>% mutate(perc = round((n/N)\*100, digits=1), perc_char =
format(perc, nsmall=1), npct = paste(n, paste0( "(", perc_char, ")" ) )
) %\>% mutate(SEX = recode(SEX, "M" = "Male", "F" = "Female")) %\>%
ungroup() %\>% select(TRT01A, SEX, npct) %\>% pivot_wider(names_from =
TRT01A, values_from = npct)

adsl_mrg_cnt


    ## 들여쓰기 = RStudio IDE 바로 가기 CTRL+I
    가장 먼저 해야 할 쉬운 일은 들여쓰기를 정리하는 것입니다. RStudio IDE에서 다시 포맷하려는 코드를 선택한 다음 코드 메뉴 항목 "코드 다시 들여쓰기" 또는 바로 가기 CTRL+I를 사용하여 이 문제를 해결할 수 있습니다. 위 코드를 아래 청크에 복사하고 RStudio IDE "다시 들여쓰기" 옵션을 사용해 보십시오...

    ```{r}

## 다시 포맷하기 = RStudio IDE 바로 가기 CTRL+SHIFT+A

마찬가지로 코드 메뉴 항목 "코드 다시 포맷하기"를 사용하여 코드 줄을
들여쓰고 다시 포맷하거나 다시 흐르게 할 수 있습니다. 이렇게 해도 아래
코드의 문제가 완전히 다시 포맷되지는 않지만 더 나아집니다. 위 코드를
아래 청크에 복사하고 RStudio IDE "다시 포맷하기" 옵션을 사용해
보십시오...

\`\`\`{r}


    ## 특정 스타일 문제 - 일관성을 유지하십시오

    코드 스타일에 관해서는 선택할 수 있는 다양한 스타일 가이드가 많이 있습니다. 제 조언은 하나를 선택한 다음 일관되게 적용하는 것입니다. 스타일에 대해 까다로운 것보다 일관성을 유지하는 것이 더 중요합니다.

      1. `=` 대신 `<-`를 사용하십시오.
      2. 일관된 명명 규칙을 사용하십시오.
        * snake_case
        * camelCase
      3. 공백을 일관되게 사용하십시오.
        * "<-" 주위에 공백이 있어야 합니다.
        * 쉼표 뒤에 공백이 있어야 합니다.
      4. 줄 바꿈을 적절하게 사용하십시오.
        * 함수 정의에서 `{` 뒤에 줄 바꿈이 있어야 합니다.
        * `%>%` 또는 `|>` 뒤에 줄 바꿈이 있어야 합니다.
        * {ggplot2} 레이어에서 `+` 뒤에 줄 바꿈이 있어야 합니다.
        * 함수에 여러 인수가 있는 경우 함수 인수를 더 쉽게 읽을 수 있도록 줄을 나눌 수 있습니다.

    RStudio IDE에서 항목을 강조 표시하고 코드 메뉴 항목 "범위 내에서 이름 바꾸기" 또는 CTRL+ALT+SHIFT+M을 선택하여 항목의 이름을 빠르게 바꿀 수 있습니다. 예를 들어 코드에서 `BIGNcnt` 항목의 이름을 바꾸고 `small_n_cnt`와 일관성을 유지하기 위해 `big_n_cnt`로 바꾸십시오.

    함수 호출에서 줄 바꿈을 사용하면 모든 것을 한 줄에 로드하는 것보다 수행되는 작업을 더 쉽게 볼 수 있는 경우가 많습니다. 위 코드에서 `mutate` 문 내의 `recode` 함수 호출을 찾아 다음과 같이 다른 경우를 별도의 줄에 배치하십시오.

mutate(SEX = recode(SEX, "M" = "Male", "F" = "Female"))


    여기서 들여쓰기를 사용하면 `=`가 정렬됩니다. 여기서 이점은 `SEX` 변수를 다시 코딩하고 해당 열의 값이 "M"과 "F"이며 각각 "Male"과 "Female"로 다시 코딩하고 있음을 쉽게 알 수 있다는 것입니다. 이 예는 사소하지만 `AGRGR1`과 같이 더 많은 옵션이 있는 다른 변수로 변경하는 경우 가능한 모든 옵션을 다시 코딩했는지 빠르게 확인하고 싶을 수 있습니다.

    ## 주석 확인

    주석 처리된 줄을 무시하고 싶은 유혹이 드는 경우가 많습니다. 그러나 주석은 다른 사람들에게 (그리고 미래의 당신에게 상기시켜 줍니다) 코드에 대한 상황 정보를 알려야 합니다. 코드에서 무슨 일이 일어나고 있는지 ***그리고 왜*** 일어나는지에 대한 설명을 제공합니다. 코드를 읽고 무엇이 일어나고 있는지 파악하기는 쉽지만 종종 이유와 상황은 건너<0xE1><0x8A><0x81>니다.

    주석을 읽으십시오. 여전히 정확하고 관련성이 있는지 확인하십시오. 그렇지 않으면 업데이트하십시오.

    ## 필요한 것보다 많은 라이브러리를 로드하지 마십시오.

    라이브러리를 로드할 때마다 해당 종속성도 로드됩니다. 코드에 필요하지 않은 경우 패키지를 로드하는 이유는 무엇입니까? 코드를 개발할 때는 필요한 모든 것을 손쉽게 사용할 수 있도록 {tidyverse} 라이브러리를 로드하고 싶은 유혹이 듭니다. 그러나 코드가 완료되면 필요한 패키지만으로 축소하는 것이 더 합리적일 수 있습니다. 예를 들어 그래프를 만들지 않았습니까? {ggplot2}를 로드하는 이유는 무엇입니까?

    원래 코드를 아래 청크에 복사하고 정리해 보십시오.

    ```{r}

## 반복하지 마십시오 - DRY 원칙

효과적으로 동일한 작업을 수행하는 세 가지 다른 코드 청크가 있음을
확인하십시오. 누군가가 다른 인구 통계 특성에 대한 계산을 만들기 위해
동일한 코드를 세 번 복사하여 붙여넣었습니다. 이는 문제가 있습니다. 위
경우와 같이 오류가 발생할 수 있기 때문만은 아닙니다. 또한 위 경우와 같이
코드에 오타가 있는 경우 정확히 찾아내기가 어려울 수 있습니다. 찾을 수
있습니까?

또한 코드가 `BIGNcnt`를 세 번 계산한다는 점에 유의하십시오. 이는
불필요합니다. 이제 함수에 대해 알고 있습니다. 그렇다면 여기서 무엇을 할
수 있을까요? 위에서 정리한 코드를 아래 청크에 복사하여 붙여넣고 함수
작성 경험을 사용하여 이 문제를 해결해 보십시오.

\`\`\`{r}

\`\`\`
