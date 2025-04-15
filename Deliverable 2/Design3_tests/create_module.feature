Feature: Create Training Module

  As a trainer
  I want to create a training module
  So that employees can be trained on specific topics

  Scenario: Successfully create a module
    Given I am logged in as a trainer
    When I fill in the module details and click "Create"
    Then the module should be saved and visible in the module list