Feature: View Employee Training Progress

  As a manager
  I want to view the training progress of employees in my department
  So that I can track completion and performance

  Scenario: View progress summary
    Given I am logged in as a manager
    When I navigate to the progress dashboard
    Then I should see a list of employees with their completed modules and status