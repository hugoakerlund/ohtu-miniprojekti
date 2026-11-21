*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations

*** Variables ***
${NEW_CITATION_URL}   http://${SERVER}/new_citation


*** Test Cases ***
At start there are no citations
    Go To  ${HOME_URL}
    Home Page Should Be Open
    Get Text  body  *=  Järjestelmässä on tällä hetkellä viitteitä 0 kpl.

Creating a citation with correct fields succeeds
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Set Title  test title
    Set Author  test author
    Set Howpublished  https://example.com
    Set Year  1900
    Set Month  1
    Set Address  test address
    Set Publisher  test publisher
    Set Edition  test edition
    Set Pages  12-100
    Click  button >> text=Luo
    Creation Should Succeed
    Home Page Should Be Open

Creating a citation with incorrect fields fails
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Set Title  test title
    Set Publisher  test publisher
    Set Edition  test edition
    Set Pages  12-100
    Click  button >> text=Luo
    Creation Should Fail With Message  Otsikko, viitemerkintätyyppi ja tekijä ovat pakolliset kentät.
    Create Citation Page Should Be Open

When a citation exists deleting a citation succeeds
    Handle Future Dialogs    action=accept
    Create citation
    Click  id=delete-button
    Click  button >> text=Poista
    Get Text  body  *=  Järjestelmässä on tällä hetkellä viitteitä 0 kpl.

*** Keywords ***
Creation Should Succeed
    Home Page Should Be Open
    Get Text  body  *=  Viite luotu.

Creation Should Fail With Message
    [Arguments]  ${message}
    Create Citation Page Should Be Open
    Get Text  body  *=  ${message}

Create citation
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Set Title  test title
    Set Author  test author
    Click  button >> text=Luo
    Creation Should Succeed
    Home Page Should Be Open
    Get Text  body  *=  Järjestelmässä on tällä hetkellä viitteitä 1 kpl.

Set Title
    [Arguments]  ${title}
    Fill Text   id=title  ${title}

Set Author
    [Arguments]  ${author}
    Fill Text  id=author  ${author}

Set Howpublished
    [Arguments]  ${howpublished}
    Fill Text  id=howpublished  ${howpublished}

Set Year
    [Arguments]  ${year}
    Fill Text  id=year  ${year}

Set Month
    [Arguments]  ${month}
    Fill Text  id=month  ${month}

Set Address
    [Arguments]  ${address}
    Fill Text  id=address  ${address}

Set Publisher
    [Arguments]  ${publisher}
    Fill Text  id=publisher  ${publisher}

Set Edition
    [Arguments]  ${edition}
    Fill Text  id=edition  ${edition}

Set Pages
    [Arguments]  ${pages}
    Fill Text  id=pages  ${pages}
