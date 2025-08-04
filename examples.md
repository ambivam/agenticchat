# BDD Test Scenario Examples

This document provides examples of different types of BDD test scenarios that can be generated using our system. For each category, you can specify the number of scenarios you want to generate.

## How to Request Scenarios

Format your request like:
- "Generate 5 API test scenarios for user authentication"
- "Create 3 security scenarios for payment processing"
- "Write 7 functional test cases for shopping cart"

## Example Scenarios by Category

### Functional (Happy Path)
```gherkin
Feature: Shopping Cart Management

  Scenario: Add item to empty cart
    Given the user is logged in
    And their shopping cart is empty
    When they add "iPhone 14" to the cart
    Then the cart should contain 1 item
    And the item should be "iPhone 14"
    And the cart total should be updated
```

### Negative Tests
```gherkin
Feature: User Authentication

  Scenario: Login with invalid credentials
    Given the user is on the login page
    When they enter invalid email "invalid@example.com"
    And they enter incorrect password "wrong123"
    Then they should see an error message "Invalid credentials"
    And they should remain on the login page
```

### Field Validations
```gherkin
Feature: User Registration

  Scenario Outline: Validate registration fields
    Given the user is on the registration page
    When they enter <field> with value <value>
    Then they should see <error_message>

    Examples:
      | field    | value        | error_message               |
      | email    | notanemail   | "Invalid email format"      |
      | password | short        | "Password too short"        |
      | phone    | abc123       | "Invalid phone number"      |
```

### Edge Cases
```gherkin
Feature: Cart Checkout

  Scenario: Checkout with maximum allowed items
    Given the user has 99 items in cart
    When they try to add one more item
    Then they should see message "Maximum cart limit reached"
    And the item should not be added
```

### API Integration
```gherkin
Feature: Payment API Integration

  Scenario: Process payment with retry mechanism
    Given the payment service is temporarily unavailable
    When the system attempts to process payment of $100
    Then it should retry 3 times
    And log each failed attempt
    And succeed when service becomes available
```

### UI Behavior
```gherkin
Feature: Responsive Design

  Scenario: Mobile view navigation
    Given the user is on a mobile device
    When they click the hamburger menu
    Then the navigation menu should slide in from left
    And show all main navigation options
```

### Security Tests
```gherkin
Feature: Authentication Security

  Scenario: Prevent brute force attacks
    Given a user has failed login 5 times
    When they attempt to login again
    Then their account should be temporarily locked
    And they should receive an email notification
    And they should wait 30 minutes before trying again
```

### Performance Tests
```gherkin
Feature: Search Performance

  Scenario: Search response time
    Given the database has 1 million products
    When user searches for "wireless headphones"
    Then results should return within 200 milliseconds
    And show at least 10 matching products
```

### Integration Tests
```gherkin
Feature: Order Processing Integration

  Scenario: Complete order flow
    Given a user places an order
    When the payment is processed successfully
    Then inventory should be updated
    And shipping service should be notified
    And customer should receive confirmation email
```

### Data Handling
```gherkin
Feature: User Data Management

  Scenario: Export user data in compliance with GDPR
    Given a user requests their data export
    When the export process is initiated
    Then all user data should be collected
    And provided in machine-readable format
    And include all historical transactions
```

### Error Handling
```gherkin
Feature: Payment Error Recovery

  Scenario: Handle payment gateway timeout
    Given the user is checking out
    When the payment gateway times out
    Then the system should save the cart state
    And show a user-friendly error message
    And provide option to retry payment
```

### State Transitions
```gherkin
Feature: Order Status Management

  Scenario: Order status progression
    Given an order is placed
    When payment is confirmed
    Then status should change from "Pending" to "Paid"
    And when order is picked
    Then status should change to "In Progress"
    And when order is shipped
    Then status should change to "Shipped"
```

### Role-based Access
```gherkin
Feature: Admin Panel Access

  Scenario: Regular user accessing admin features
    Given a regular user is logged in
    When they attempt to access "/admin/users"
    Then they should be redirected to home page
    And see "Access Denied" message
```

## Tips for Writing Good Scenarios
1. Make scenarios specific and unambiguous
2. Use realistic test data
3. Include proper setup in "Given" steps
4. Have clear, verifiable outcomes in "Then" steps
5. Keep scenarios independent of each other
6. Use scenario outlines for data-driven tests
7. Include both positive and negative cases
8. Consider edge cases and boundary conditions
