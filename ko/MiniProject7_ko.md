`{r setup, include = FALSE} knitr::opts_chunk$set(echo = TRUE) library(tidyverse) library(haven)`

## 1. 소개

함수, 함수 작성 방법 및 함수에서 문제가 발생했을 때 해결하는 방법을
소개합니다. 함수는 R을 사용하는 데 매우 중요합니다. **코드를 두 번 이상
복사하면 함수를 작성해야 한다는 것이 경험칙입니다**. `library( )` 문을
사용하여 가져오는 R 패키지는 본질적으로 함수, 설명서, 테스트 및 때로는
데이터의 모음입니다. R을 배우는 여정을 더 진행함에 따라 함수 사용 방법,
작성 방법 및 다른 작업을 수행하도록 확장하는 방법을 이해하는 것이 점점
더 중요해질 것입니다.

함수는 SAS 매크로와 약간 비슷합니다. 함수를 처음 작성할 때는 "열린"
코드에서 변환하여 입력(데이터, 목록 또는 객체)을 식별하고 해당 객체에
적용할 작업을 결정합니다. 그런 다음 함수를 구체화하면서 해당 인수의 값에
따라 사용자가 작업을 조정할 수 있도록 하는 인수를 추가할 수 있습니다. 이
미니 프로젝트에서 이를 달성하는 방법을 살펴봅니다.

이를 설명하기 위해 데이터셋 내 관찰 수를 계산하고 범주 내 숫자와 비율을
계산했던 미니 프로젝트 2의 예제로 돌아갑니다. 해당 섹션을 상기하십시오.

\`\`\`{r} adsl_saf \<-
import("https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt")
%\>% filter(SAFFL == "Y")

Big_N_cnt \<- adsl_saf %\>% group_by( TRT01AN, TRT01A ) %\>% count(name
= "N") Big_N_cnt

small_n_cnt \<- adsl_saf %\>% group_by( TRT01AN, TRT01A, SEX ) %\>%
count(name = "n") small_n_cnt

adsl_mrg_cnt \<- small_n_cnt %\>% left_join(Big_N_cnt, by = c("TRT01A",
"TRT01AN")) %\>% mutate(perc = round((n/N)\*100, digits=1)) %\>%
mutate(perc_char = format(perc, nsmall=1)) %\>% mutate(npct = paste(n,
paste0( "(", perc_char, ")" ) ) ) %\>% mutate(SEX = recode(SEX, "M" =
"Male", "F" = "Female")) %\>% ungroup() %\>% select(TRT01A, SEX, npct)
%\>% pivot_wider(names_from = TRT01A, values_from = npct)

adsl_mrg_cnt


    ## 2. 함수의 특징

    위 코드를 보면 다른 연구의 `adsl` 데이터셋에 대해 동일한 코드를 실행하고 싶을 수 있습니다. 코드를 복사할 수도 있지만 여러 연구에 걸쳐 동일한 작업을 수행하려는 경우 위 코드를 함수로 바꾸는 것이 더 유용할 수 있습니다.

    #### 함수 구조

    R의 함수에는 몇 가지 주요 속성이 있습니다.

    -   함수 이름
    -   함수 입력 및 인수
    -   코드를 작성하는 함수 본문
    -   코드에서 반환된 객체 (또는 때로는 객체가 아닌 작업, R에서는 "부작용"이라고 함). 예를 들어 데이터(객체)를 반환할 수 있지만 데이터를 파일에 쓸 수도 있습니다(부작용).

    #### 함수 이름

    함수 이름은 어렵습니다. 사용 중인 (또는 사용할 가능성이 있는) 라이브러리의 기존 함수와 충돌하지 않는 이름을 선택해야 합니다. 예를 들어 `mean`이라는 함수를 호출하는 것은 대부분의 사람들이 기본 `mean` 함수가 수행해야 하는 작업에 대해 잘 알고 있으므로 피해야 합니다. 함수 이름은 ***설명적***이어야 하며 동사인 것이 좋습니다. `addLabels`가 `myFunction4`보다 낫습니다. 입력에 대해 무언가를 ***수행***하기 때문에 동사를 선택합니다.

    명명된 함수가 이미 존재하는지 확인할 수 있습니다. 다음 코드를 복사하여 콘솔에 붙여넣습니다.

        ??mean

    #### 함수 인수

    함수에 인수가 ***필요***하지는 않지만 일반적으로 인수가 있습니다. {tidyverse}에서 첫 번째 인수는 일반적으로 입력 객체 또는 데이터입니다. 이렇게 하면 함수를 {tidyverse} 파이프라인에 쉽게 넣을 수 있습니다. 다른 인수는 함수 사용자가 설정을 조정하거나 함수가 수행하는 작업에 대해 선택하는 데 도움이 됩니다. 함수를 처음 작성할 때는 기본 사항이 작동할 때까지 인수 수를 절대 최소값으로 줄이는 것이 좋습니다. 그런 다음 천천히 인수를 추가할 수 있습니다.

    #### 함수 본문

    여기에 코드가 있습니다. 코드 줄이 두 줄 이상인 경우 함수 본문을 중괄호 `{ }`로 묶어야 합니다. 함수 본문에 마지막으로 작성하는 것은 함수에서 반환된 객체입니다.

    ***참고:*** 함수 본문 내에서 R은 새 환경을 사용합니다. 즉, 함수 내에서 만드는 변수와 객체는 반환된 객체에서 사용할 수 있도록 하지 않는 한 ***함수 내에 유지됩니다***. 이는 함수를 디버깅하려고 할 때 어려움과 혼란을 야기할 수 있지만 나중에 별도로 살펴보겠습니다.

    함수 내에서 함수를 호출할 수 있습니다(*무한정*). 이는 도우미 함수를 만들고 이를 상위 수준 함수에서 사용할 수 있으므로 유용한 트릭이며 본질적으로 많은 R 패키지가 구축되는 방식입니다. 즉, 함수를 번들로 묶은 다음 공유할 수 있도록 만드는 것입니다. 이는 또한 토끼굴로 내려갈수록 함수 디버깅이 약간 까다로워질 수 있음을 의미합니다.

    #### 반환된 객체

    함수에서 만드는 객체는 완전히 별개의 환경에 존재하므로 함수가 완료되었을 때 어떤 객체를 반환할지 R에 알려야 합니다. 이러한 객체는 "반환된" 값이라고 합니다. tidyverse 워크플로에서 사용할 함수를 작성하는 경우 `tibble`을 반환하는 것이 좋습니다. 즉, 반환된 객체를 다른 단계로 계속 파이프할 수 있습니다. tidyverse 워크플로 외부에서 작업하거나 함수가 "마지막 단계"인 경우 원하는 것을 반환하는 데 더 많은 유연성이 있습니다. 예를 들어 함수가 데이터를 파일에 쓰는 경우 함수가 객체를 반환***할 필요는 없습니다***.

    따라서 tidyverse에서는 `tibbles`가 선호되는 출력 객체입니다. `tibbles` 외에도 데이터, 벡터, 기타 목록 등을 포함한 항목 모음을 포함할 수 있으므로 `list` 객체가 좋은 포괄적인 객체입니다.

    다음은 몇 가지 예입니다.

    -   아래 `myFunction1`은 객체를 반환하지 않으므로 함수를 실행하면 아무것도 반환되지 않습니다(함수 작업은 수행되지만). 이 코드를 실행하고 환경에 `output`이라는 객체가 있는지 확인하십시오.

    ```{r, eval = FALSE}
    myData <- tribble(
      ~Treatment, ~value,
      "Placebo", 1,
      "Placebo", 2,
      "Active", 3,
      "Active", 4
    )

    myFunction1 <- function(data){
      output <- data %>%
        group_by(Treatment) %>%
        summarise(n = n())
    }

    myFunction1(myData)

다음 코드에서 `output` 객체에는 함수가 반환하도록 하는 암시적 `print`
문이 있습니다.

\`\`\`{r, eval = FALSE} myFunction2 \<- function(data){ output \<- data
%\>% group_by(Treatment) %\>% summarise(n = n()) output }

myFunction2(myData)


    마지막 스니펫에서는 출력 객체를 공식적으로 반환합니다. `return` 문을 사용하는 것은 함수에서 무엇이 반환되는지 검토자에게 명확하게 보여주므로 좋은 관행입니다.

    ```{r, eval = FALSE}
    myFunction3 <- function(data){
      output <- data %>%
        group_by(Treatment) %>%
        summarise(n = n())
      write.csv(x = output, file = "output.csv")
      return(output)
    }

    myFunction3(myData)

## 3. 함수 만들기

이제 아래 코드를 가져와 함수로 바꿔 보겠습니다. RStudio IDE "스니펫"을
사용하여 함수를 작성할 수 있습니다. RStudio IDE의 콘솔 `>` 프롬프트에서
"fun"을 입력한 다음 TAB 키를 누릅니다. {snippets} 옵션에서 `fun`을
선택합니다. 이렇게 하면 완료할 스캐폴딩 스니펫이 작성됩니다. 함수에
이름(예: "myFunction1")을 지정한 다음 TAB 키를 사용하여 함수 "변수"로
이동하고 이를 "inputVariable"로 이름을 바꿉니다. 이제 TAB 키를 다시 눌러
함수 코드 `{ }` 사이로 이동하여 함수 코드를 작성합니다.

RStudio IDE `fun` 스니펫을 사용하여 아래 코드를 기반으로
"adsl_counts"라는 함수를 만들고 해당 함수 본문에 코드를 복사합니다.
`adsl_counts` 함수에는 `dataFile`이라는 인수가 있어야 하며 이 인수가
`read_xpt` 함수의 `data_file` 인수에 대한 CDISC 데이터셋 경로를 제공하기
위해 `read_xpt` 함수 내에서 사용되는지 확인해야 합니다.

\`\`\`{r}

adsl_counts \<- function(dataFile){ adsl_saf \<- read_xpt( ) %\>%
filter(SAFFL == "Y")

Big_N_cnt \<- adsl_saf %\>% group_by( TRT01AN, TRT01A ) %\>% count(name
= "N") Big_N_cnt

small_n_cnt \<- adsl_saf %\>% group_by( TRT01AN, TRT01A, SEX ) %\>%
count(name = "n") small_n_cnt

adsl_mrg_cnt \<- small_n_cnt %\>% left_join(Big_N_cnt, by = c("TRT01A",
"TRT01AN")) %\>% mutate(perc = round((n/N)\*100, digits=1)) %\>%
mutate(perc_char = format(perc, nsmall=1)) %\>% mutate(npct = paste(n,
paste0( "(", perc_char, ")" ) ) ) %\>% mutate(SEX = recode(SEX, "M" =
"Male", "F" = "Female")) %\>% ungroup() %\>% select(TRT01A, SEX, npct)
%\>% pivot_wider(names_from = TRT01A, values_from = npct)
return(adsl_mrg_cnt) }


    위에서 완성된 함수 코드를 실행하면 함수 유형의 R 객체가 만들어집니다. 환경에서 볼 수 있습니다. 함수 이름 또는 오른쪽의 "스크립트" 아이콘을 클릭하여 함수 코드를 봅니다.

    ## 4. 함수를 CDISC 데이터셋에 적용합니다.

    이제 CDISC `adsl` 데이터셋 경로의 문자열을 만들고 함수를 실행하여 코드를 테스트합니다. 함수 호출에 전체 경로를 넣을 필요는 없습니다. 아래에서는 해당 경로를 포함하는 객체를 만든 다음 이를 함수에 전달합니다.

    ```{r}
    inFile <- "https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt"

    adsl_counts(inFile)

## 5. 방어적 프로그래밍

ADaM 데이터셋을 전달하지 않으면 어떻게 됩니까?

글쎄, 이것은 입력 유형을 확인하고 올바른 유형이 아닌 경우 실행을
중지하기 위해 추가 코드를 작성하고 싶을 수 있는 경우입니다. 데이터셋이
ADaM 형식인지 어떻게 알 수 있습니까? 한 가지 방법은 파일 이름이
`adsl`인지 확인하는 것입니다. `{stringr}` 패키지에는 문자열 작업에
유용한 함수가 포함되어 있습니다... `str_detect`를 사용해 보겠습니다.
여기서 `stringr::` 접두사를 `str_detect`에 붙여 R***(그리고
당신!)***에게 `str_detect`가 `{stringr}` 패키지에서 온다는 것을
명시적으로 알립니다. 이렇게 할 ***필요는 없지만*** 특정 함수가 어떤
패키지에서 왔는지 코드를 검토하는 사람에게 종종 도움이 됩니다.

`{r} stringr::str_detect(inFile, "adsl")`

R에는 사용자에게 메시지, 경고 및 오류 메시지를 다시 전달하는 데 도움이
되는 몇 가지 함수가 있습니다. 함수를 작성할 때 사용자가 무엇이
잘못되었고 이를 수정하는 방법을 파악할 수 있도록 이러한 메시지를 의미
있게 만드는 것이 좋습니다. `try` 함수는 일부 코드를 실행하려고 시도하며
실패하면 `stop` 메시지가 표시됩니다. 다양한 `inFile` 값에 대해 시도해
보십시오.

`{r} try(if(!stringr::str_detect(inFile, "adsl")) stop("입력 데이터가 CDISC adsl 데이터셋이 아닙니다"))`

이제 ADaM 데이터셋이 아닌 데이터셋(또는 `adsl`이 아닌 데이터셋)을
사용하여 `adsl_counts` 함수를 적용해 보십시오.

#### 인수 이름 지정은 어렵습니다

위 함수에서 인수 이름을 `dataFile`로 지정했습니다. 그러나 이것은
사용자에게 어떤 종류의 입력 또는 데이터 파일이 예상되는지에 대한 단서를
거의 제공하지 않습니다. 예상되는 것이 "adsl" ADaM 데이터셋에 대한 문자열
파일 경로라는 것이 즉시 명확하지 않습니다. (다시) 이름을
`adsl_FilePath`로 지정하면 사용자에게 함수에서 어떤 종류의 데이터가
사용되는지에 대한 훨씬 더 많은 단서를 제공하고 문제가 발생하기 전에
어려움을 피할 수 있습니다.

제 권장 사항은 함수를 작성하고 작동하는지 확인한 다음 다시 돌아가서 항목
이름을 변경하는 것입니다. RStudio IDE를 사용하여 다음을 수행할 수
있습니다.

1.  `dataFile` 인수를 두 번 클릭합니다. IDE가 함수 내에서 `dataFile`의
    모든 인스턴스를 찾는 방법을 확인하십시오.
2.  "코드" 메뉴에서 "범위 내에서 이름 바꾸기"를 선택합니다.
    `adsl_File`을 입력하여 인수와 ***함수 내에서*** 이 인수의 인스턴스
    이름을 바꿉니다.

\`\`\`{r} adsl_counts \<- function(dataFile){ adsl_saf \<- read_xpt( )
%\>% filter(SAFFL == "Y")

Big_N_cnt \<- adsl_saf %\>% group_by( TRT01AN, TRT01A ) %\>% count(name
= "N") Big_N_cnt

small_n_cnt \<- adsl_saf %\>% group_by( TRT01AN, TRT01A, SEX ) %\>%
count(name = "n") small_n_cnt

adsl_mrg_cnt \<- small_n_cnt %\>% left_join(Big_N_cnt, by = c("TRT01A",
"TRT01AN")) %\>% mutate(perc = round((n/N)\*100, digits=1)) %\>%
mutate(perc_char = format(perc, nsmall=1)) %\>% mutate(npct = paste(n,
paste0( "(", perc_char, ")" ) ) ) %\>% mutate(SEX = recode(SEX, "M" =
"Male", "F" = "Female")) %\>% ungroup() %\>% select(TRT01A, SEX, npct)
%\>% pivot_wider(names_from = TRT01A, values_from = npct)

adsl_mrg_cnt }


    ## 6. 자주 검토하고 리팩터링하십시오.

    R에서 무언가를 배우면 더 효율적이거나 빠르거나 병렬로 수행할 수 있거나 복잡한 코드를 더 간단하게 만들 수 있는 새로운 방법을 찾을 수 있습니다. 때때로 함수로 돌아가서 여전히 의미가 있는지, 개선할 수 있는 것이 있는지 확인하는 것이 좋습니다.

    좋은 함수는 읽고, 검토하고, 개선하기 쉬워야 합니다. 위 코드에서 함수는 github 경로를 가져와 xpt 데이터셋을 읽는 것부터 테이블 내용을 생성하는 것까지 모든 작업을 수행합니다. 그러나 코드가 데이터를 읽는 대신 요약된 개수만 생성하면 작업을 단순화할 수 있습니다. 네트워크를 통해 데이터를 읽는 것은 비교적 느립니다. 따라서 가능하다면 세션에서 한 번만 수행하려고 합니다.

    앞서 말했듯이 `{tidyverse}` 데이터 파이프라인에서 사용할 함수를 작성하는 경우 입력으로 tibble/데이터셋을 예상하고 다른 tibble/데이터셋을 반환해야 합니다. 그러나 여기서 입력으로 예상되는 것은 ***문자열 파일 경로***입니다. 이는 이상적이지 않습니다. 함수 외부에서 파일 읽기를 수행하고 대신 전달되는 것이 "adsl" ***데이터셋***이라고 가정하도록 코드를 재구성(리팩터링이라고 함)해 보겠습니다.

    입력 데이터셋(예: `adsl_saf` 데이터)을 기반으로 계산하도록 아래 함수 코드를 수정합니다. 함수 입력(입력 데이터셋)을 가리키도록 `Big_N_cnt` 및 `small_n_cnt`에 대한 코드를 업데이트해야 합니다. 청크를 실행하여 코드가 작동하는지 확인하십시오.

    ```{r}
    adsl_counts <- function(adsl_FilePath) {
      adsl_saf <- read_xpt(   ) %>%
        filter(SAFFL == "Y")

      Big_N_cnt <-  adsl_saf   %>%
        group_by( TRT01AN, TRT01A  ) %>%
        count(name = "N")
      Big_N_cnt

      small_n_cnt <-  adsl_saf  %>%
        group_by( TRT01AN, TRT01A,  SEX ) %>%
        count(name = "n")
      small_n_cnt

      adsl_mrg_cnt <- small_n_cnt %>%
        left_join(Big_N_cnt, by = c("TRT01A", "TRT01AN")) %>%
        mutate(perc = round((n/N)*100, digits=1)) %>%
        mutate(perc_char = format(perc, nsmall=1)) %>%
        mutate(npct = paste(n,
                            paste0( "(", perc_char, ")" )
                            )
               ) %>%
        mutate(SEX = recode(SEX,
                            "M" = "Male",
                            "F" = "Female")) %>%
        ungroup() %>%
        select(TRT01A, SEX, npct) %>%
        pivot_wider(names_from = TRT01A, values_from = npct)

      adsl_mrg_cnt
    }

    inFile <- "https://github.com/phuse-org/phuse-scripts/raw/master/data/adam/cdisc/adsl.xpt"

    table1 <- read_xpt(inFile) %>%
        filter(SAFFL == "Y") %>%
      adsl_counts()
    table1

## 7. 함수 문제 해결 및 디버깅

인수나 입력이 하나만 있는 함수는 일반적으로 디버깅하기 쉽습니다.
콘솔에서 인수와 동일한 이름의 객체를 만든 다음 문제가 식별될 때까지 함수
본문의 코드를 한 줄씩 단계별로 실행합니다.

그러나 일반적으로 함수에는 훨씬 더 많은 인수가 있으며 이러한 모든 인수를
객체에 할당한 다음 코드를 단계별로 실행하는 것은 매우 지루해집니다.
그러나 R과 RStudio IDE는 디버깅에 유용한 몇 가지 도구를 제공합니다. 다음
문서를 참조하십시오:
<https://support.rstudio.com/hc/en-us/articles/205612627-Debugging-with-the-RStudio-IDE>

RStudioConf 2020에서 Jenny Bryan의 발표는 코드가 잘못되었을 때 수행할
작업에 대한 훌륭한 설명이었습니다:
<https://www.rstudio.com/resources/rstudioconf-2020/object-of-type-closure-is-not-subsettable/>

여기에 링크된 자료와 비디오를 검토하는 것을 ***강력히 권장합니다***.
***엄청나게*** 도움이 될 것입니다.

## 8. 모든 인수를 지정할 필요는 없습니다 - 생략 부호

함수를 작성하다 보면 함수 내 다양한 옵션을 처리하기 위해 점점 더 많은
인수를 추가하게 될 수 있습니다. 일반적으로 이러한 인수는 주 함수 내에서
사용되는 함수에 대한 추가 인수입니다. 그러나 함수 호출을 확장하여 이를
허용하는 쉬운 방법이 있습니다. 함수에 인수로 `...`을 입력하면 상위 함수
내에서 사용되는 하위 수준 함수로 인수를 전달할 수 있습니다. 다음과 같이
이러한 함수 호출에 동일한 `...`을 추가합니다.

\`\`\`{r} mySummary \<- function(myData, ...){ myData %\>% group_by(
TRT01AN, TRT01A ) %\>% summarise(mean = round(mean(AGE), ... )) }

mySummary(adsl_saf)

mySummary(adsl_saf, digits = 1) \`\`\`

위 코드에서는 사용자가 `digits` 인수를 `round` 함수로 전달할 수 있도록
허용합니다. `.` 생략 부호는 "사용자가 제공하는 추가 인수가 무엇이든
전달하십시오..."라고 말합니다. 그리고 `round` 함수의 `.`은 "사용자가
제공하는 추가 인수가 무엇이든 여기서 사용하십시오..."라고 말합니다. 생략
부호를 통해 전달되는 하위 수준 함수 인수는 유효한 인수여야 합니다...
동일한 이름의 인수가 있는 함수가 두 개 이상 있는 경우에만 주의하면
됩니다... 이름 지정은 어렵습니다.

## 도전 과제

미니 프로젝트 6 도전 과제에서 작성한 코드를 입력 `adlb` 데이터셋을
가져와 그래프를 생성하는 함수로 변환하십시오. 추가 도전 과제로 사용자가
축 레이블을 지정할 수 있도록 허용하십시오.
