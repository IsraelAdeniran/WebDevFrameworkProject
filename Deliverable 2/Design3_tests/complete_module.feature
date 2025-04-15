Feature: Employee Completes a Training Module

  As an employee
  I want to complete an assigned module
  So that I meet my training requirements

  Scenario: Mark module as completed
    Given I am logged in as an employee
    And I have an assigned module titled "Fire Safety"
    When I mark the module as completed
    Then the status should update to "Completed"
    And a completion record should be created