*** Settings ***
Library    SeleniumLibrary 
*** Variables ***

${URL}  https://www.google.com/
${Browser}    chrome
${Url_base}    https://demo.nopcommerce.com/
*** Test Cases ***
Test Google
    [Tags]    FT-2
    Open Browser    ${URL}    ${Browser}
    Input Text    id:APjFqb    Akkodis 
    Click Element    xpath://html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]
    
   
Test Site
    [Tags]    FT-3
    Open Browser    ${Url_base}    ${Browser}
    Input Text    id:small-searchterms    camputers
    Click Button    xpath://*[@id="small-search-box-form"]/button   
    Close All Browsers