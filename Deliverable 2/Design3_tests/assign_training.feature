Feature: Assign Training to Employees

  As a manager
  I want to assign a training module to an employee in my department
  So that they can complete required training

  Scenario: Assign a module successfully
    Given I am logged in as a manager
    And there is a training module available
    And there is an employee in my department
    When I assign the module "Fire Safety" to the employee
    Then the assignment should appear in the employee's training list
    And the status should be "Not Started"