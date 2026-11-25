*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations


*** Test Cases ***
Creating a book with correct fields succeeds
    Create Book
    Creation Should Succeed
    Home Page Should Be Open

A book cannot be created without required fields
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  book
    Click  button >> text=Täytä Lomake
    Create Book Page Should Be Open
    Set Title  test title
    Set Pages  12-100
    Click  button >> text=Luo
    Create Book Page Should Be Open

Creating a book fails with incorrect fields
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  book
    Click  button >> text=Täytä Lomake
    Create Book Page Should Be Open
    Set Title  test title
    Set Author  test author
    Set Editor  test editor
    Set Publisher  test publisher
    Set Year  1900
    Set Volume  abc
    Click  button >> text=Luo
    Creation Should Fail With Message  Vuosikerran on oltava numeerinen.


*** Keywords ***
Create Book
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  book
    Click  button >> text=Täytä Lomake
    Create Book Page Should Be Open
    Set Title  test title
    Set Author  test author
    Set Editor  test editor
    Set Publisher  test publisher
    Set Year  1900
    Click  button >> text=Luo

Create Book Page Should Be Open
    Get Title  ==  Luo uusi kirja
