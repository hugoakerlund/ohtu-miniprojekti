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

User can choose a citation type
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  article
    Click  button >> text=Täytä Lomake
    Get Text  body  *=  Luo uusi artikkeli

Creating an article with correct fields succeeds
    Create Article
    Creation Should Succeed
    Home Page Should Be Open

An article cannot be created without required fields
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  article
    Click  button >> text=Täytä Lomake
    Create Article Page Should Be Open
    Set Title  test title
    Set Journal  test journal
    Set Pages  12-100
    Click  button >> text=Luo
    Create Article Page Should Be Open

Creating an article fails with incorrect fields
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  article
    Click  button >> text=Täytä Lomake
    Create Article Page Should Be Open
    Set Title  test title
    Set Author  test author
    Set Journal  test journal
    Set Pages  12-0
    Click  button >> text=Luo
    Creation Should Fail With Message  Virheelliset sivunumerot.

When a citation exists deleting a citation succeeds
    Handle Future Dialogs  action=accept
    Create Article
    Click  id=delete-button
    Click  button >> text=Poista
    Get Text  body  *=  Järjestelmässä on tällä hetkellä viitteitä 0 kpl.

*** Keywords ***
Creation Should Succeed
    Home Page Should Be Open
    Get Text  body  *=  Viite luotu.

Creation Should Fail With Message
    [Arguments]  ${message}
    Get Text  body  *=  ${message}

Create Article
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  article
    Click  button >> text=Täytä Lomake
    Create Article Page Should Be Open
    Set Title  test title
    Set Author  test author
    Set Journal  test journal
    Set Year  1900
    Click  button >> text=Luo

Set Title
    [Arguments]  ${title}
    Fill Text  id=title  ${title}

Set Author
    [Arguments]  ${author}
    Fill Text  id=author  ${author}

Set Year
    [Arguments]  ${year}
    Fill Text  id=year  ${year}

Set Journal
    [Arguments]  ${journal}
    Fill Text  id=journal  ${journal}

Set Pages
    [Arguments]  ${pages}
    Fill Text  id=pages  ${pages}

Create Article Page Should Be Open
    Get Title  ==  Luo uusi artikkeli
