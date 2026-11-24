*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations


*** Test Cases ***
Inproceedings cannot be created without required fields
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  inproceedings
    Click  button >> text=Täytä Lomake
    Create Inproceedings Page Should Be Open
    Set Title  test title
    Set Pages  12-100
    Click  button >> text=Luo
    Create Inproceedings Page Should Be Open

Creating inproceedings fails with incorrect fields
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  inproceedings
    Click  button >> text=Täytä Lomake
    Create Inproceedings Page Should Be Open
    Set Title  test title
    Set Author  test author
    Set Booktitle  test booktitle
    Set Year  1900
    Set Pages  12-0
    Click  button >> text=Luo
    Creation Should Fail With Message  Virheelliset sivunumerot.


Creating an inproceedings with correct fields succeeds
    Create Inproceedings
    Creation Should Succeed
    Home Page Should Be Open


*** Keywords ***
Create Inproceedings
    Go To  ${NEW_CITATION_URL}
    Create Citation Page Should Be Open
    Select Options By  id=entry_type  label  inproceedings
    Click  button >> text=Täytä Lomake
    Create Inproceedings Page Should Be Open
    Set Title  test title
    Set Author  test author
    Set Booktitle  test booktitle
    Set Year  1900
    Click  button >> text=Luo

Create Inproceedings Page Should Be Open
    Get Title  ==  Luo uusi konferenssiartikkeli
