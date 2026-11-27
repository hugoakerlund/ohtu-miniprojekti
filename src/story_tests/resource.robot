*** Settings ***
Library    Browser
Library    OperatingSystem

*** Variables ***
${SERVER}                      localhost:5001
${DELAY}                       500ms
${HOME_URL}                    http://${SERVER}
${RESET_URL}                   http://${SERVER}/reset_db
${NEW_CITATION_URL}            http://${SERVER}/new_citation
${BROWSER}                     chromium
${HEADLESS}                    false
${DOWNLOAD_OUTPUT_DIR}         src/instance/exports

*** Keywords ***
Open And Configure Browser
    IF  $HEADLESS == 'true'
        New Browser  browser=${BROWSER}  headless=True
    ELSE
        New Browser  browser=${BROWSER}  headless=False  slowMo=${DELAY}
    END
    New Context
    New Page  about:blank

Reset Citations
    Go To  ${RESET_URL}

Create Citation Page Should Be Open
    Get Title  ==  Luo uusi viite

Home Page Should Be Open
    Get Title  ==  Viitteidenhallintajärjestelmä
    Get Text  body  *=  Etusivu

Creation Should Succeed
    Home Page Should Be Open
    Get Text  body  *=  Viite luotu.

Creation Should Fail With Message
    [Arguments]  ${message}
    Get Text  body  *=  ${message}

Set Title
    [Arguments]  ${title}
    Fill Text  id=title  ${title}

Set Author
    [Arguments]  ${author}
    Fill Text  id=author  ${author}

Set Editor
    [Arguments]  ${editor}
    Fill Text  id=editor  ${editor}

Set Publisher
    [Arguments]  ${publisher}
    Fill Text  id=publisher  ${publisher}

Set Volume
    [Arguments]  ${volume}
    Fill Text  id=volume  ${volume}

Set Year
    [Arguments]  ${year}
    Fill Text  id=year  ${year}

Set Journal
    [Arguments]  ${journal}
    Fill Text  id=journal  ${journal}

Set Booktitle
    [Arguments]  ${booktitle}
    Fill Text  id=booktitle  ${booktitle}

Set Pages
    [Arguments]  ${pages}
    Fill Text  id=pages  ${pages}
