*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations


*** Test Cases ***
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


*** Keywords ***
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

Create Article Page Should Be Open
    Get Title  ==  Luo uusi artikkeli
