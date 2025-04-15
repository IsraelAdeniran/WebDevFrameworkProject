Feature: Respond to Feedback

  As a trainer
  I want to respond to feedback left by employees
  So that I can acknowledge and improve training

  Scenario: Respond to a feedback entry
    Given I am logged in as a trainer
    And an employee has left feedback on "Fire Safety"
    When I enter a response and submit
    Then the response should be saved and linked to the feedback