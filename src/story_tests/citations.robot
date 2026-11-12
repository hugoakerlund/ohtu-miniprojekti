*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations

*** Test Cases ***
At start there are no citations
    Go To  ${HOME_URL}
    Get Title  ==  Viitteidenhallintajärjestelmä
    Get Text  body  *=  Etusivu
    Get Text  body  *=  Järjestelmässä on tällä hetkellä 0 viitettä.

# After adding a citation, there is one
