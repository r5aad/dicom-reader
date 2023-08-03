Feature: Testing DICOM APIs

  Scenario: Store DICOM asset
    When I send a POST request to "/v1/assets" with a file
    Then the response status code should be 200
    And the response JSON should contain "id"

    When I send a GET request to "/v1/assets/<id>"
    Then the response status code should be 200
    And the response JSON should contain "id"

    When I send a GET request to "/v1/assets"
    Then the response status code should be 200
    And the response JSON should be a list of assets

    When I send a GET request to "/v1/assets/<id>/extract" with query parameter "tag=0010,0010"
    Then the response status code should be 200
    And the response JSON should contain the extracted tag information

    When I send a GET request to "/v1/assets/<id>/convert"
    Then the response status code should be 200
    And the response JSON should contain the converted PNG information

  Scenario: Check API health
    When I send a GET request to "/v1/health"
    Then the response status code should be 200
    And the response JSON should show status as passing
