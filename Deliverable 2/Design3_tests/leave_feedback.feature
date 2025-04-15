Feature: Leave Feedback for Completed Module

  As an employee
  I want to leave feedback after completing a module
  So that I can share my learning experience

  Scenario: Submit feedback and rating
    Given I am logged in as an employee
    And I have completed the module "Fire Safety"
    When I leave a comment and a rating of 5
    Then the feedback should be saved and linked to the module