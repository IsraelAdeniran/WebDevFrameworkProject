Feature: User Login

  As a user
  I want to log into the system
  So that I can access my dashboard

  Scenario: Successful login
    Given I am a registered user with username "user1" and password "password"
    When I enter my credentials and click login
    Then I should be redirected to my dashboard