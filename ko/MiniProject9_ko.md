`{r packages} #install.packages("reprex") library(reprex) library(tidyverse) library(rio)`

Reprex는 재현 가능한 예제(reproducible example)를 의미합니다! 이 미니
프로젝트 시리즈의 새로운 패키지입니다. (tidyverse를 설치할 때 설치되는
많은 패키지 중 하나일 수도 있습니다. 패키지 탭을 보면 이미 설치되어
있는지 확인할 수 있습니다.) reprex는 'rmarkdown' 패키지를 사용하여 작은
코드 조각을 코드와 출력을 모두 포함하는 대상 형식으로 렌더링하는 편의
래퍼입니다. 목표는 작고 재현 가능하며 실행 가능한 예제의 공유를 장려하는
것입니다. 누군가가 코드 디버깅을 도울 때 코드를 다시 포맷하고 결과와
명령 프롬프트를 제거하고 로드한 패키지를 추측할 필요가 없다면 도움이
됩니다. 이는 코드를 다시 생성하거나 동료 그룹에서 디버깅하는 데 매우
유용합니다. Reprex는 코드, 출력 및 문제에 대한 정보를 패키징하여 다른
사람이 쉽게 실행하고 오류를 수정하는 데 도움을 줄 수 있도록 합니다.
\*\*\* R 세션의 스크린샷을 찍는 대신 이 작업을 수행하십시오! \*\*\* 오류
스크린샷을 보내면 도움을 주는 사람은 코드를 직접 다시 실행할 수 없으며
코드를 다시 입력해야 합니다(그리고 필연적으로 필사 과정에서 오타와
실수가 발생합니다). 이는 매우 비효율적입니다...

실행 가능한 코드 + 출력을 Markdown 파일, R 코드 또는 일반 HTML 텍스트로
출력합니다.

1.  가장 기본적인 예입니다. reprex를 실행하려면 Ctrl + C를 사용하여 아래
    코드를 모두 복사한 다음 콘솔 창에서 reprex()를 실행하십시오.

`{r} (y <- 1:4) mean(y)`

    (y <- 1:4)
    #> [1] 1 2 3 4
    mean(y)
    #> [1] 2.5
    2023-03-08에 reprex v2.0.2로 생성됨

이렇게 하면 뷰어 창(R Studio 화면의 오른쪽 하단 섹션일 가능성이 큼)에
reprex가 만들어집니다. 모든 코드와 출력을 이메일, Teams 공간,
프레젠테이션, 포럼 등에 복사하여 붙여넣을 수 있는 코드 청크로 패키징하는
것을 볼 수 있습니다. 중요한 점은 다른 사람이 이 코드를 다시 실행하려는
경우 아무것도 변경하지 않고도 그렇게 할 수 있다는 것입니다.

또한 해당 창의 내용을 클립보드로 다시 복사하므로 이메일이나 MS Teams
게시물에 간단히 붙여넣을 수 있습니다.

2.  이제 미니 프로젝트의 첫 번째 라운드에서 SEX 변수를 다시 코딩하는 데
    사용했던 코드를 가져와 해당 reprex를 살펴보겠습니다. 다시 한 번 다음
    청크의 모든 코드를 복사한 다음 화면 하단의 콘솔에 reprex()를
    입력합니다.

\`\`\`{r age data}

adsl \<-
import("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")

adsl_saf \<- adsl %\>% filter(SAFFL == "Y" ) %\>% mutate(SEX =
recode(SEX, "M" = "Male", "F" = "Female"))


    이렇게 하면 RStudio의 뷰어에 표시될 멋지게 렌더링된 HTML 미리보기가 제공됩니다. 다른 사람이 즉시 복사, 붙여넣기 및 실행할 수 있으므로 스크린샷보다 선호됩니다.

    여기서 발생하는 오류는 reprex가 `read_xpt` 함수를 찾지 못했고 파이프 "%>%" 함수도 식별하지 못했다는 것입니다. 이는 R 환경에 tidyverse를 로드했지만 reprex에 포함되지 않았기 때문입니다.

adsl \<-
read_xpt("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
#\> Error in
read_xpt("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt"):
could not find function "read_xpt"

adsl_saf \<- adsl %\>% filter(SAFFL == "Y" ) %\>% mutate(SEX =
recode(SEX, M = "Male", F = "Female")) #\> Error in adsl %\>%
filter(SAFFL == "Y") %\>% mutate(SEX = recode(SEX, M = "Male", : could
not find function "%\>%" 2023-03-08에 reprex v2.0.2로 생성됨


    ## 재현 가능한 예제에 포함할 내용:

    1.  배경 정보 -- 무엇을 하려고 합니까? 이미 무엇을 했습니까?
    2.  완전한 설정 -- 문제를 재현하는 데 필요한 모든 library() 호출 및 데이터를 포함합니다.
        a.  (따라서 위 코드는 실제로 올바르지 않습니다. 라이브러리 문이 다른 R 청크에 있기 때문입니다.)
    3.  간단하게 유지 -- 제공된 데이터에서 오류를 재현하는 데 필요한 최소한의 코드만 포함합니다.
    4.  따라서 위 코드의 더 나은 버전은 다음과 같습니다. 이 청크의 모든 코드를 복사한 다음 콘솔에서 reprex()를 실행합니다.

    ```{r}
    library(tidyverse)
    library(rio)

    #ADSL 데이터 읽기
    adsl <- import("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")

    #SAFFL에 대한 광고 필터링 및 SEX 변수 재코딩
    adsl_saf <- adsl %>%
      filter(SAFFL == "Y" ) %>%
      mutate(SEX = recode(SEX, "M" = "Male", "F" = "Female"))

여기에는 모든 것이 하나의 깔끔한 코드 청크에 있습니다. 여전히 일부
"경고"가 표시될 수 있지만 청크가 작동하지 않도록 하는 종류의 경고는
아닙니다. 패키지 버전에 대한 경고가 표시됩니다. 이것이 코드가 작동하지
않거나 작동하지 않는다는 의미는 아닙니다. R에 다운로드한 패키지 버전을
다른 사람에게 알리는 것뿐입니다. 그러나 이제 파이프(%\>%)에 대한 경고가
사라진 것을 볼 수 있습니다.

4.  이제 약간 더 복잡한 예를 살펴보겠습니다. 이것은 원래 미니 프로젝트
    6에서 사용된 코드입니다. 이 청크의 모든 코드를 복사한 다음 콘솔에서
    reprex()를 실행합니다. 참고: 데이터를 로드하는 데 시간이 걸릴 수
    있습니다.

\`\`\`{r} library(tidyverse) library(rio)

ALT \<-
import("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adlbhy.xpt")
%\>% filter(PARAMCD == "ALT")

ALT2 \<- ALT %\>% filter(VISITNUM \> 3) %\>% mutate(WEEK = floor(ADY/7))

TREATfac \<- ALT2 %\>% select(TRTA, TRTAN) %\>% unique() %\>%
arrange(TRTAN) %\>% mutate(TREATMENT = factor(TRTA, ordered = TRUE))

ALT2 \<- ALT2 %\>% mutate(TREATTXT = factor(TRTP, levels =
TREATfac\$TRTA))

library(tidyverse) #\> Warning: package 'tidyverse' was built under R
version 3.5.3 #\> Warning: package 'ggplot2' was built under R version
3.5.3 #\> Warning: package 'tibble' was built under R version 3.5.3 #\>
Warning: package 'tidyr' was built under R version 3.5.3 #\> Warning:
package 'readr' was built under R version 3.5.3 #\> Warning: package
'purrr' was built under R version 3.5.3 #\> Warning: package 'dplyr' was
built under R version 3.5.3 #\> Warning: package 'stringr' was built
under R version 3.5.3 #\> Warning: package 'forcats' was built under R
version 3.5.3 library(haven) #\> Warning: package 'haven' was built
under R version 3.5.3

ALT \<-
read_xpt("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adlbhy.xpt")
%\>% filter(PARAMCD == "ALT")

ALT2 \<- ALT %\>% filter(VISITNUM \> 3) %\>% mutate(WEEK = floor(ADY/7))

TREATfac \<- ALT2 %\>% select(TRTA, TRTAN) %\>% unique() %\>%
arrange(TRTAN) %\>% mutate(TREATMENT = factor(TRTA, ordered = TRUE))

ALT2 \<- ALT2 %\>% mutate(TREATTXT = factor(TRTP, levels =
TREATfac\$TRTA)) 2023-03-08에 reprex v2.0.2로 생성됨


    다시 말하지만, reprex에 필요한 패키지가 포함되어 있는 한 이 코드에는 문제가 없습니다.

    5.  플롯을 포함한 reprex 살펴보기.

    ```{r}
    library(tidyverse)
    library(rio)


    ALT <- import("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adlbhy.xpt") %>%
      filter(PARAMCD == "ALT")


    ALT2 <- ALT %>%
      filter(VISITNUM > 3) %>%
      mutate(WEEK = floor(ADY/7))

    ALT2 %>%
      filter(WEEK %in% c(0, 5, 10, 15, 20, 25, 30)) %>%
      ggplot() +
      geom_boxplot(mapping = aes(x = as.factor(WEEK), y = AVAL))

    library(tidyverse)
    #> Warning: package 'tidyverse' was built under R version 3.5.3
    #> Warning: package 'ggplot2' was built under R version 3.5.3
    #> Warning: package 'tibble' was built under R version 3.5.3
    #> Warning: package 'tidyr' was built under R version 3.5.3
    #> Warning: package 'readr' was built under R version 3.5.3
    #> Warning: package 'purrr' was built under R version 3.5.3
    #> Warning: package 'dplyr' was built under R version 3.5.3
    #> Warning: package 'stringr' was built under R version 3.5.3
    #> Warning: package 'forcats' was built under R version 3.5.3
    library(haven)
    #> Warning: package 'haven' was built under R version 3.5.3

    ALT <- read_xpt("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adlbhy.xpt") %>%
      filter(PARAMCD == "ALT")


    ALT2 <- ALT %>%
      filter(VISITNUM > 3) %>%
      mutate(WEEK = floor(ADY/7))

    ALT2 %>%
      filter(WEEK %in% c(0, 5, 10, 15, 20, 25, 30)) %>%
      ggplot() +
      geom_boxplot(mapping = aes(x = as.factor(WEEK), y = AVAL))
    2023-03-08에 reprex v2.0.2로 생성됨

여기서 플롯을 만들고 있지만 reprex는 실제로 변경되지 않는 것을 볼 수
있습니다. 뷰어 창에는 reprex가 표시되고 그 아래에 출력 그래프가
표시되지만 실제로는 reprex의 일부가 아닙니다.

하지만... 이 마지막 두 예는 ***최소한으로 재현 가능한 예제***가
아닙니다. 이를 다시 실행하려면 도움을 주는 사람이 데이터베이스 및/또는
참조하는 데이터셋에 액세스할 수 있어야 합니다. 그리고 해당 데이터셋이
크거나 읽는 데 시간이 오래 걸리는 경우 실제로 플롯 코드에 대해 묻는
것이라면 문제 해결 프로세스에 부담이 됩니다. 그렇다면 이 문제 설명을 더
작고 "최소한"으로 만들려면 어떻게 해야 할까요?

5.5 tribbles로 잠시 옆길로 새겠습니다. 다음 예에서는 `tribble()` 함수를
사용합니다. 그렇다면 tribble이란 무엇일까요? tribble은 작은 데이터
세트를 빠르고 간단하게 설정하는 방법입니다. reprex에서 사용하기에
이상적입니다.

tribble을 만들려면 먼저 SAS의 datalines 또는 cards에서처럼 변수 이름을
정의해야 합니다. 여기서는 변수에 대해 문자 또는 숫자 유형을 지정할
필요가 없습니다. R이 이를 결정할 수 있습니다. 또한 각 데이터 행에 대해
레코드 끝을 지정할 필요도 없습니다. 단순히 열로 값을 구분하면 `tribble`
함수가 나머지를 처리합니다.

변수 이름을 만들려면 '\~' 문자로 시작한 다음 변수 이름을 입력하고 쉼표로
값을 구분합니다.

\`\`\`{r} myData \<- tribble( \~Treatment, \~value, "Placebo", 1,
"Placebo", 2, "Active", 3, "Active", 4 )

myData


    여기서 myData는 4개의 행과 2개의 열이 있는 데이터 프레임임을 알 수 있습니다. Treatment는 문자 변수이고 value는 dbl(숫자) 변수입니다. reprex를 위해 매우 축소되고 단순한 것을 만들면 계산 시간이 덜 걸리고 필요한 변수만으로 문제를 좁힐 수 있으므로 매우 유용할 수 있습니다.

    플롯에 대해 묻기 위해 reprex를 만드는 경우 코드가 이전에 세 단계의 데이터 조작을 거쳤다면 데이터 조작을 복제하지 마십시오. 플롯에 들어가는 데이터 형식을 설명하는 `tribble`로 바로 이동하십시오. 그리고 해당 데이터 조작의 출력이 무엇인지 추측하고 "이상적인" tribble을 지정하지 마십시오. 조작 후 데이터를 검사하고 조작된 데이터에서 보는 것과 정확히 동일하게 플롯에 필요한 열만 전달하십시오. 원하는 경우 연속적인 결과에 대해 임의의 값을 사용할 수 있습니다. 요점은 반드시 ***값***이 무엇인지가 아니라 데이터 구조와 관련이 있는 경우가 많습니다.

    6.  사용자 생성 함수에 대한 Reprex.

    ```{r}
    library(dplyr)
    library(tidyverse)

    myData <- tribble(
      ~Treatment, ~value,
      "Placebo", 1,
      "Placebo", 2,
      "Active", 3,
      "Active", 4
    )

    myData

    myFunction1 <- function(data){
      output <- data %>%
        group_by(Treatment) %>%
        summarise(n = n())
      output
    }

    myFunction1(myData)

    library(dplyr)
    #> Warning: package 'dplyr' was built under R version 3.5.3
    #>
    #> Attaching package: 'dplyr'
    #> The following objects are masked from 'package:stats':
    #>
    #>     filter, lag
    #> The following objects are masked from 'package:base':
    #>
    #>     intersect, setdiff, setequal, union
    library(tidyverse)
    #> Warning: package 'tidyverse' was built under R version 3.5.3
    #> Warning: package 'ggplot2' was built under R version 3.5.3
    #> Warning: package 'tibble' was built under R version 3.5.3
    #> Warning: package 'tidyr' was built under R version 3.5.3
    #> Warning: package 'readr' was built under R version 3.5.3
    #> Warning: package 'purrr' was built under R version 3.5.3
    #> Warning: package 'stringr' was built under R version 3.5.3
    #> Warning: package 'forcats' was built under R version 3.5.3

    myData <- tribble(
      ~Treatment, ~value,
      "Placebo", 1,
      "Placebo", 2,
      "Active", 3,
      "Active", 4
    )

    myData
    #> # A tibble: 4 x 2
    #>   Treatment value
    #>   <chr>     <dbl>
    #> 1 Placebo       1
    #> 2 Placebo       2
    #> 3 Active        3
    #> 4 Active        4

    myFunction1 <- function(data){
      output <- data %>%
        group_by(Treatment) %>%
        summarise(n = n())
      output
    }

    myFunction1(myData)
    #> # A tibble: 2 x 2
    #>   Treatment     n
    #>   <chr>     <int>
    #> 1 Active        2
    #> 2 Placebo       2
    2023-03-08에 reprex v2.0.2로 생성됨

## 마지막으로 해야 할 일과 하지 말아야 할 일.

-   rm(list = ls())로 청크를 시작하지 마십시오. 도움을 주려는 사람의
    현재 환경을 지워버릴 것입니다. 그들은 아마도 감사하지 않을 것입니다.
    (작업 공간은 SAS 작업 디렉터리와 같으며 이 명령은 SAS kill을
    실행하는 것과 같습니다.)
-   다른 사람의 컴퓨터에서는 작동하지 않으므로
    setwd("C:/Users/`<사용자 이름>`{=html}/Documents/")로 시작하지
    마십시오.
-   문제를 설명하는 데 필요한 패키지만 호출하십시오.
-   문제를 설명하는 코드만 포함하십시오.
-   문제를 설명하는 ***가장 작은*** 데이터셋을 포함하십시오.
-   reprex 패키지에서 파일을 만드는 경우 작업이 끝나면 삭제하십시오.
    다시 말하지만 다른 사람의 작업 공간을 망치지 않도록 하기
    위해서입니다.

더 많은 해야 할 일과 하지 말아야 할 일은 여기에 있습니다:
<https://reprex.tidyverse.org/articles/reprex-dos-and-donts.html>

## 추가 자료:

Jennifer Bryan의 "Help me help you: Creating reproducible examples with
reprex":

-   <https://reprex.tidyverse.org/articles/learn-reprex.html>
-   <https://posit.co/resources/videos/help-me-help-you-creating-reproducible-examples/>

## 주의할 점

-   필요한 모든 `library()` 호출을 포함하는 것을 잊었습니까?
-   사용 중인 데이터/tibble에 필요한 모든 변수가 있습니까?
-   `reprex::reprex()`를 실행했지만 클립보드에 새 콘텐츠를 복사하지 않고
    다시 실행했습니까? `reprex`는 `reprex`의 결과를 클립보드에
    복사하므로 이렇게 하면 경고합니다. `reprex`를 다시 실행하면 이전
    `reprex`의 출력에서 `reprex`를 실행하려고 시도합니다.

## 마지막 참고 사항:

훌륭한 reprex를 만드는 데는 노력이 필요합니다. 다른 사람에게 작업을
요청하기 때문에 reprex를 만들 가능성이 높습니다. 이것은 파트너십입니다.
종종 훌륭한 reprex를 작성하는 과정에서 자신의 문제를 해결하게 될
것입니다. 그리고 그렇지 않은 경우 다른 사람과 쉽게 공유하여 문제를
해결하는 데 도움을 받을 수 있는 reprex를 갖게 될 것입니다.

## 도전 과제: 여기서 무엇이 잘못되었습니까?

다른 사람이 문제를 이해하고 해결하는 데 도움이 되는 더 최소한의 reprex를
만드십시오.

\`\`\`{r} library(tidyverse) library(rio)

adlb \<-
import("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adlbh.xpt")

BICARB \<- adlb %\>% filter(SAFFL == "Y") %\>% filter(PARAMCD == "BASO")

ggplot(data = BICARB, mapping = aes(x = ADY, y = AVAL)) +
geom_point(aes(colour = "THERAPY1")) \`\`\`
