*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations

*** Variables ***

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

When a citation exists deleting a citation succeeds
    Handle Future Dialogs  action=accept
    Create New Citation
    Click  id=choose-button
    Click  button >> text=Poista
    Get Text  body  *=  Järjestelmässä on tällä hetkellä viitteitä 0 kpl.

*** Keywords ***
Create New Citation
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  article
    Click  button >> text=Täytä Lomake
    Set Title  test title
    Set Author  test author
    Set Journal  test journal
    Set Year  1900
    Click  button >> text=Luo
