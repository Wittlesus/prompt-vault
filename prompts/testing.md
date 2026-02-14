# Testing Prompts

A collection of 10 battle-tested prompts for AI-assisted test generation. From unit tests to full test plans, these prompts produce production-ready test code.

---

## 1. Unit Test Generator

**Use Case:** Generate comprehensive unit tests for a function or class, covering happy paths, edge cases, and error conditions.

**Prompt:**

```
You are a senior QA engineer writing thorough unit tests. Generate a complete test suite for the following code.

### Requirements:
1. **Test Framework**: Use [Jest/Vitest/pytest/Go testing] (specify your framework)
2. **Coverage Target**: Aim for 100% branch coverage
3. **Test Categories** (organize tests into describe/context blocks):
   - Happy path: Normal inputs producing expected outputs
   - Edge cases: Empty inputs, boundary values, single-element collections, max/min values
   - Error cases: Invalid inputs, null/undefined, wrong types, out-of-range values
   - Integration boundaries: How this function interacts with its dependencies

### For Each Test:
- Descriptive test name that reads like a sentence: `it('should return empty array when input is null')`
- Arrange: Set up test data and mocks
- Act: Call the function under test
- Assert: Verify the result with specific assertions (not just "toBeTruthy")

### Additional Requirements:
- Mock all external dependencies (database, API calls, file system)
- Use factory functions or fixtures for test data (not inline object literals)
- Add a comment explaining WHY each edge case test matters
- Include negative tests (what should NOT happen)
- Test async behavior if applicable (resolved values, rejected promises, timeouts)

Code to test:
"""
[PASTE YOUR FUNCTION OR CLASS HERE]
"""
```

**Example Output Snippet:**

```javascript
describe('calculateDiscount', () => {
  // Factory for creating test orders
  const createOrder = (overrides = {}) => ({
    items: [{ price: 100, quantity: 1 }],
    customerTier: 'standard',
    couponCode: null,
    ...overrides,
  });

  describe('happy path', () => {
    it('should apply 10% discount for gold tier customers', () => {
      const order = createOrder({ customerTier: 'gold' });
      const result = calculateDiscount(order);
      expect(result.discountAmount).toBe(10);
      expect(result.finalPrice).toBe(90);
    });

    it('should stack coupon discount with tier discount', () => {
      const order = createOrder({
        customerTier: 'gold',
        couponCode: 'SAVE5',
      });
      const result = calculateDiscount(order);
      // Gold (10%) + coupon ($5) = $15 off $100
      expect(result.discountAmount).toBe(15);
    });
  });

  describe('edge cases', () => {
    it('should handle order with zero-priced items', () => {
      // Regression: free promotional items were causing division by zero
      const order = createOrder({
        items: [{ price: 0, quantity: 1 }],
      });
      const result = calculateDiscount(order);
      expect(result.discountAmount).toBe(0);
      expect(result.finalPrice).toBe(0);
    });
  });

  describe('error handling', () => {
    it('should throw ValidationError when order has no items', () => {
      const order = createOrder({ items: [] });
      expect(() => calculateDiscount(order)).toThrow(ValidationError);
    });
  });
});
```

**Tips for Customization:**
- Specify: "Use React Testing Library for component tests"
- Add: "Include snapshot tests for complex objects"
- Mention: "We use dependency injection, so mock via constructor params"

---

## 2. Integration Test Generator

**Use Case:** Generate tests that verify multiple components work together correctly, including API endpoints, database operations, and service interactions.

**Prompt:**

```
You are a test automation engineer writing integration tests that verify components work together in a realistic environment.

Generate integration tests for the following code/system:

### Integration Test Requirements:
1. **Test Real Interactions**: Test actual HTTP requests, database queries, and service calls (not mocked)
2. **Test Environment**: Use test database, test containers, or in-memory alternatives
3. **Data Setup/Teardown**: Each test starts with a clean, known state
4. **Test Scenarios**:
   - Full request-response cycle for each API endpoint
   - Database state verification after operations
   - Multi-step workflows (e.g., create -> update -> delete)
   - Concurrent access patterns
   - External service failure handling (use fault injection)

### For Each Test:
- **Setup**: Database seeding, server startup, auth token generation
- **Execution**: Real HTTP requests with actual payloads
- **Verification**: Check response body, status code, headers, AND database state
- **Cleanup**: Remove test data, close connections

### Structure:
```
describe('Order API Integration', () => {
  beforeAll()  // Start server, connect DB
  beforeEach() // Seed test data
  afterEach()  // Clean test data
  afterAll()   // Close connections

  describe('POST /orders', () => {
    it('should create order, deduct inventory, and send confirmation email')
    it('should rollback order if payment fails')
    it('should handle concurrent orders for last item in stock')
  })
})
```

System/code to test:
"""
[PASTE YOUR API ROUTES, SERVICES, OR SYSTEM DESCRIPTION HERE]
"""
```

**Example Output Snippet:**

```javascript
describe('Order API Integration', () => {
  let server;
  let db;
  let authToken;

  beforeAll(async () => {
    db = await createTestDatabase();
    server = await startTestServer({ db });
    authToken = await getTestAuthToken(server, {
      email: 'test@example.com',
      role: 'customer'
    });
  });

  beforeEach(async () => {
    await db.seed('products', [
      { id: 'prod_1', name: 'Widget', price: 29.99, stock: 5 }
    ]);
  });

  afterEach(async () => {
    await db.truncate(['orders', 'order_items', 'products']);
  });

  afterAll(async () => {
    await server.close();
    await db.destroy();
  });

  describe('POST /api/orders', () => {
    it('should create order and deduct inventory atomically', async () => {
      const response = await request(server)
        .post('/api/orders')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          items: [{ productId: 'prod_1', quantity: 2 }]
        });

      // Verify response
      expect(response.status).toBe(201);
      expect(response.body.order.total).toBe(59.98);

      // Verify database state
      const product = await db.findOne('products', { id: 'prod_1' });
      expect(product.stock).toBe(3); // 5 - 2 = 3

      const order = await db.findOne('orders', { id: response.body.order.id });
      expect(order.status).toBe('confirmed');
    });

    it('should reject order when insufficient stock', async () => {
      const response = await request(server)
        .post('/api/orders')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          items: [{ productId: 'prod_1', quantity: 100 }]
        });

      expect(response.status).toBe(409);
      expect(response.body.error.code).toBe('INSUFFICIENT_STOCK');

      // Verify stock unchanged
      const product = await db.findOne('products', { id: 'prod_1' });
      expect(product.stock).toBe(5);
    });
  });
});
```

**Tips for Customization:**
- Specify: "Use Testcontainers for PostgreSQL and Redis"
- Add: "Include API contract testing with Pact"
- Mention: "We need to test webhook delivery to external services"

---

## 3. Edge Case Identifier

**Use Case:** Given a function, systematically identify all possible edge cases that should be tested but are often missed.

**Prompt:**

```
You are a testing expert who specializes in finding edge cases that crash production systems.

Analyze the following function and generate a comprehensive list of edge cases that should be tested. Think adversarially - what inputs would a fuzzer or malicious user provide?

### Categories of Edge Cases to Consider:

**Data Type Edge Cases:**
- null, undefined, NaN, Infinity, -Infinity
- Empty string, whitespace-only string, very long string (1M+ chars)
- Empty array, single-element array, very large array
- Empty object, deeply nested objects, circular references
- Negative numbers, zero, MAX_SAFE_INTEGER, floating point precision

**Boundary Values:**
- Off-by-one on every loop and range check
- First element, last element, middle element
- Exact boundary values (if limit is 100, test 99, 100, 101)
- Date boundaries (midnight, DST transitions, leap years, year 2038)

**Format Edge Cases:**
- Unicode: emoji, RTL text, zero-width characters, homoglyphs
- Special characters: quotes, backslashes, angle brackets, SQL keywords
- Encoding: mixed UTF-8/ASCII, BOM characters
- Numbers as strings, strings as numbers

**Concurrency Edge Cases:**
- Simultaneous identical requests
- Operation interrupted halfway
- Stale data reads

**Environment Edge Cases:**
- Missing env variables, missing config files
- Network timeout, partial response
- Disk full, permission denied

For each edge case provide:
1. **Case**: Description
2. **Input**: Exact test input
3. **Expected Behavior**: What should happen
4. **Risk If Untested**: What goes wrong in production

Function to analyze:
"""
[PASTE YOUR FUNCTION HERE]
"""
```

**Example Output Snippet:**

```markdown
### Edge Cases for `parseUserAge(input: string): number`

| # | Case | Input | Expected | Risk If Untested |
|---|------|-------|----------|-----------------|
| 1 | Empty string | `""` | Throw ValidationError | Returns NaN, corrupts DB |
| 2 | Negative age | `"-5"` | Throw ValidationError | Negative ages in reports |
| 3 | Zero | `"0"` | Return 0 (valid for newborns) | Rejected as falsy |
| 4 | Decimal age | `"25.5"` | Throw ValidationError | Stored as float, breaks integer column |
| 5 | Very large number | `"999999"` | Throw ValidationError | Unrealistic age accepted |
| 6 | Leading zeros | `"007"` | Return 7 | Interpreted as octal in some parsers |
| 7 | Whitespace | `" 25 "` | Return 25 (trim) | parseInt returns NaN |
| 8 | Number with comma | `"1,000"` | Throw ValidationError | Silently parsed as 1 |
| 9 | Unicode digits | `"２５"` (fullwidth) | Throw ValidationError | Passes regex but fails parseInt |
| 10 | Null input | `null` | Throw TypeError | Crashes toString() call |
| 11 | Scientific notation | `"2.5e1"` | Throw ValidationError | Parsed as 25, bypasses format check |
| 12 | MAX_SAFE_INTEGER | `"9007199254740992"` | Throw ValidationError | Precision loss in JS |
```

**Tips for Customization:**
- Specify: "Focus on financial calculation edge cases (rounding, currency precision)"
- Add: "Include timezone-related edge cases for our date handling"
- Mention: "We accept user input from a multilingual global user base"

---

## 4. Test Data Factory Generator

**Use Case:** Create reusable test data factories/builders that generate realistic, consistent test data.

**Prompt:**

```
You are a test infrastructure engineer creating test data factories that generate realistic, type-safe test data for a test suite.

Based on the following data models, create test data factories that:

### Requirements:
1. **Builder Pattern**: Each factory returns a builder with sensible defaults and chainable overrides
2. **Realistic Data**: Use realistic values (not "test", "foo", "abc123")
3. **Relationships**: Factories can create related entities (User with Orders with Items)
4. **Sequences**: Auto-incrementing IDs and unique emails per test run
5. **Traits**: Named presets for common variations (e.g., `adminUser`, `expiredSubscription`)
6. **State Combinations**: Factories for different entity states (active, suspended, deleted)
7. **Batch Generation**: Create N entities at once for list/pagination testing
8. **Database Compatibility**: Output matches your DB schema exactly

### Factory API Design:
```javascript
// Simple usage
const user = UserFactory.build();

// With overrides
const user = UserFactory.build({ name: 'Jane', role: 'admin' });

// With traits
const user = UserFactory.build('premium', 'verified');

// With relationships
const user = UserFactory.build().withOrders(3).withSubscription('annual');

// Batch
const users = UserFactory.buildMany(50);

// Persisted to DB
const user = await UserFactory.create();
```

Data models:
"""
[PASTE YOUR DATA MODELS, SCHEMAS, OR TYPES HERE]
"""
```

**Example Output Snippet:**

```typescript
// factories/userFactory.ts
import { faker } from '@faker-js/faker';

let sequence = 0;

interface UserOverrides {
  id?: string;
  email?: string;
  name?: string;
  role?: 'user' | 'admin' | 'viewer';
  status?: 'active' | 'suspended' | 'deleted';
  plan?: 'free' | 'pro' | 'enterprise';
  createdAt?: Date;
}

const traits = {
  admin: { role: 'admin' as const },
  premium: { plan: 'enterprise' as const },
  suspended: { status: 'suspended' as const },
  newUser: { createdAt: new Date() },
  veteranUser: { createdAt: new Date('2020-01-01') },
};

export const UserFactory = {
  build(overrides: UserOverrides = {}): User {
    sequence++;
    return {
      id: `usr_${faker.string.alphanumeric(12)}`,
      email: `test-${sequence}@example.com`,
      name: faker.person.fullName(),
      role: 'user',
      status: 'active',
      plan: 'free',
      createdAt: faker.date.past({ years: 2 }),
      ...overrides,
    };
  },

  buildWithTrait(...traitNames: (keyof typeof traits)[]): User {
    const merged = traitNames.reduce(
      (acc, name) => ({ ...acc, ...traits[name] }),
      {}
    );
    return this.build(merged);
  },

  buildMany(count: number, overrides: UserOverrides = {}): User[] {
    return Array.from({ length: count }, () => this.build(overrides));
  },

  async create(overrides: UserOverrides = {}): Promise<User> {
    const user = this.build(overrides);
    return db.users.insert(user);
  },
};
```

**Tips for Customization:**
- Specify: "Use FactoryBot style (Ruby)" or "Use Fishery (TypeScript)"
- Add: "Include factories for all our Prisma models"
- Mention: "We need deterministic data for snapshot tests (use seeded faker)"

---

## 5. Test Plan Creator

**Use Case:** Generate a structured test plan for a new feature or release, covering all testing levels and scenarios.

**Prompt:**

```
You are a QA lead creating a comprehensive test plan for a new feature before development begins.

Based on the following feature specification, create a test plan that covers all testing levels:

### Test Plan Structure:

## 1. Test Scope
- What is being tested (and explicitly what is NOT)
- Dependencies and integrations affected
- Risk assessment (what could go wrong)

## 2. Test Strategy
- Testing levels: Unit, Integration, E2E, Performance, Security
- Test environment requirements
- Test data requirements
- Automation vs manual testing decisions

## 3. Test Scenarios (organize by user story)
For each scenario:
- **ID**: TC-001
- **Priority**: P0 (must pass for release) / P1 (should pass) / P2 (nice to have)
- **Scenario**: Description of what to test
- **Preconditions**: What must be true before the test
- **Steps**: Numbered steps to execute
- **Expected Result**: Precise expected outcome
- **Test Data**: Specific data needed

## 4. Negative Test Scenarios
- Invalid inputs
- Permission violations
- Concurrent operations
- System failures

## 5. Performance Test Scenarios
- Load testing targets
- Stress testing boundaries
- Soak testing duration

## 6. Acceptance Criteria Mapping
- Map each acceptance criterion to specific test cases
- Identify gaps

## 7. Test Schedule & Estimates
- Effort estimate per testing level
- Dependencies and blockers

Feature specification:
"""
[PASTE YOUR FEATURE SPEC, USER STORIES, OR PRD HERE]
"""
```

**Example Output Snippet:**

```markdown
# Test Plan: Multi-Currency Support

## 1. Test Scope

**In Scope:**
- Currency selection during checkout
- Price display in selected currency
- Currency conversion calculation
- Order history with original currency

**Out of Scope:**
- Currency exchange rate provider integration (mocked)
- Tax calculation per currency (separate feature)

**Risk Assessment:**
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Rounding errors in conversion | High | Medium | Test with known precision-lossy currencies (JPY, KWD) |
| Stale exchange rates | Medium | High | Test with rate caching and staleness checks |

## 3. Test Scenarios

### User Story: As a customer, I can see prices in my preferred currency

**TC-001** (P0) - Display price in selected currency
- Precondition: User has set preferred currency to EUR
- Steps:
  1. Navigate to product page for "Widget" (base price: $100 USD)
  2. Observe displayed price
- Expected: Price shows "€92.50" (using test rate 1 USD = 0.925 EUR)
- Test Data: Exchange rate fixture: USD->EUR = 0.925

**TC-002** (P0) - Handle currency with zero decimal places
- Precondition: User selects JPY (Japanese Yen)
- Steps:
  1. View product priced at $9.99 USD
  2. Observe displayed price
- Expected: Price shows "¥1,499" (no decimal places, rounded correctly)
```

**Tips for Customization:**
- Add: "Include accessibility testing scenarios (WCAG 2.1 AA)"
- Specify: "We need cross-browser testing matrix (Chrome, Firefox, Safari, Edge)"
- Mention: "Include mobile-specific test scenarios for iOS and Android"

---

## 6. Snapshot Test Setup

**Use Case:** Generate snapshot tests for React components, API responses, or complex data structures to detect unexpected changes.

**Prompt:**

```
You are a frontend testing expert setting up snapshot tests for a React (or Vue/Angular) application.

Generate snapshot tests for the following components that:

### Requirements:
1. **Render Snapshots**: Capture the rendered output of each component
2. **State Variations**: Snapshot each meaningful state the component can be in:
   - Loading state
   - Empty/no data state
   - Normal state with typical data
   - Error state
   - Overflow state (very long text, many items)
3. **Prop Variations**: Snapshot with different prop combinations
4. **Responsive**: Snapshot at mobile, tablet, and desktop widths (if applicable)
5. **Interaction States**: Snapshot after user interactions (expanded, selected, etc.)

### Best Practices:
- Use inline snapshots for small outputs, external snapshots for large ones
- Mock dates, random values, and IDs for deterministic snapshots
- Name snapshots descriptively
- Keep snapshot scope small (test component in isolation, not entire page)
- Use `toMatchSnapshot()` for structural tests, not pixel-perfect visual tests

### Anti-Patterns to Avoid:
- Don't snapshot entire pages (too brittle)
- Don't snapshot auto-generated CSS class names
- Don't snapshot timestamps or UUIDs

Components to test:
"""
[PASTE YOUR COMPONENT CODE HERE]
"""
```

**Example Output Snippet:**

```jsx
import { render } from '@testing-library/react';
import { UserCard } from './UserCard';

// Freeze time for deterministic snapshots
beforeAll(() => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2025-01-15T10:00:00Z'));
});

describe('UserCard Snapshots', () => {
  const defaultProps = {
    user: {
      id: 'usr_test_001',
      name: 'Jane Doe',
      email: 'jane@example.com',
      avatar: '/avatars/jane.jpg',
      role: 'admin',
      joinedAt: '2024-06-15T00:00:00Z',
    },
  };

  it('renders default state', () => {
    const { container } = render(<UserCard {...defaultProps} />);
    expect(container).toMatchSnapshot();
  });

  it('renders loading state', () => {
    const { container } = render(<UserCard user={null} loading={true} />);
    expect(container).toMatchInlineSnapshot(`
      <div class="user-card user-card--loading">
        <div class="skeleton skeleton--avatar" />
        <div class="skeleton skeleton--text" />
      </div>
    `);
  });

  it('renders with very long name (overflow handling)', () => {
    const longNameUser = {
      ...defaultProps.user,
      name: 'A'.repeat(200),
    };
    const { container } = render(<UserCard user={longNameUser} />);
    expect(container).toMatchSnapshot();
  });
});
```

**Tips for Customization:**
- Specify: "We use Storybook, so generate snapshot tests from stories"
- Add: "Include visual regression tests with Percy or Chromatic"
- Mention: "We use CSS Modules so class names are stable"

---

## 7. Mock & Stub Generator

**Use Case:** Generate type-safe mocks and stubs for external dependencies, APIs, and services.

**Prompt:**

```
You are a testing infrastructure engineer creating reusable mocks and stubs for a test suite.

Based on the following interfaces/services, generate comprehensive mocks:

### Requirements:

1. **Type-Safe Mocks**: Mocks match the real interface exactly
2. **Configurable Responses**: Easy to set up different responses per test
3. **Call Tracking**: Record all calls with arguments for assertions
4. **Default Behaviors**: Sensible defaults that don't require configuration for simple tests
5. **Error Simulation**: Easy to trigger error conditions
6. **Latency Simulation**: Ability to add delays for timeout testing
7. **Mock Categories**:
   - **API Mocks**: HTTP request/response interception
   - **Database Mocks**: Query/mutation recording
   - **Service Mocks**: External service client mocks
   - **Time Mocks**: Clock and timer control
   - **File System Mocks**: File read/write interception

### For Each Mock Provide:
- The mock implementation
- Setup/teardown code
- Example usage in a test
- How to verify calls were made correctly

Interfaces to mock:
"""
[PASTE YOUR INTERFACES, SERVICE CLASSES, OR API SPECS HERE]
"""
```

**Example Output Snippet:**

```typescript
// mocks/paymentGateway.mock.ts

interface PaymentResult {
  transactionId: string;
  status: 'success' | 'declined' | 'error';
  amount: number;
}

export function createMockPaymentGateway() {
  const calls: Array<{ method: string; args: any[] }> = [];
  let chargeResponse: PaymentResult = {
    transactionId: 'txn_mock_001',
    status: 'success',
    amount: 0,
  };
  let shouldFail = false;
  let latencyMs = 0;

  return {
    // The mock implementation
    charge: jest.fn(async (amount: number, currency: string, token: string) => {
      calls.push({ method: 'charge', args: [amount, currency, token] });

      if (latencyMs > 0) {
        await new Promise(resolve => setTimeout(resolve, latencyMs));
      }
      if (shouldFail) {
        throw new PaymentError('Gateway timeout', 'GATEWAY_TIMEOUT');
      }
      return { ...chargeResponse, amount };
    }),

    refund: jest.fn(async (transactionId: string, amount: number) => {
      calls.push({ method: 'refund', args: [transactionId, amount] });
      return { refundId: 'ref_mock_001', status: 'success' };
    }),

    // Configuration helpers
    simulateDecline: () => { chargeResponse.status = 'declined'; },
    simulateError: () => { shouldFail = true; },
    simulateLatency: (ms: number) => { latencyMs = ms; },
    reset: () => {
      calls.length = 0;
      shouldFail = false;
      latencyMs = 0;
      chargeResponse.status = 'success';
    },

    // Assertion helpers
    getCalls: () => [...calls],
    wasChargedWith: (amount: number) =>
      calls.some(c => c.method === 'charge' && c.args[0] === amount),
  };
}

// --- Usage in a test ---
describe('CheckoutService', () => {
  let paymentGateway;

  beforeEach(() => {
    paymentGateway = createMockPaymentGateway();
  });

  it('should handle payment decline gracefully', async () => {
    paymentGateway.simulateDecline();

    const checkout = new CheckoutService({ paymentGateway });
    const result = await checkout.processOrder(order);

    expect(result.status).toBe('payment_failed');
    expect(result.message).toBe('Your card was declined');
    expect(paymentGateway.wasChargedWith(99.99)).toBe(true);
  });
});
```

**Tips for Customization:**
- Specify: "We use MSW (Mock Service Worker) for API mocking"
- Add: "Generate mocks compatible with our dependency injection container"
- Mention: "Include mock for AWS S3 and SES"

---

## 8. Property-Based Test Generator

**Use Case:** Generate property-based tests that verify invariants hold across thousands of random inputs, catching edge cases example-based tests miss.

**Prompt:**

```
You are a testing expert who specializes in property-based testing. Generate property-based tests using [fast-check/Hypothesis/QuickCheck/gopter] for the following code.

### What Are Property-Based Tests?
Instead of testing specific examples, we define PROPERTIES (invariants) that must hold for ALL valid inputs, then generate thousands of random inputs to verify.

### Requirements:
1. **Identify Properties**: For each function, identify mathematical/logical properties:
   - **Idempotency**: f(f(x)) === f(x)
   - **Roundtrip**: decode(encode(x)) === x
   - **Invariants**: sorted(arr).length === arr.length
   - **Commutativity**: f(a, b) === f(b, a)
   - **Associativity**: f(f(a, b), c) === f(a, f(b, c))
   - **Monotonicity**: if a > b then f(a) >= f(b)
   - **Bounds**: output is always within expected range
   - **Conservation**: total input quantity === total output quantity

2. **Custom Generators**: Create generators for domain-specific data types
3. **Shrinking**: Ensure failures produce minimal reproduction cases
4. **Seed Logging**: Log the random seed so failures are reproducible

Code to test:
"""
[PASTE YOUR FUNCTION OR MODULE HERE]
"""
```

**Example Output Snippet:**

```typescript
import fc from 'fast-check';

describe('sortUsers (property-based)', () => {

  // Custom generator for User objects
  const userArb = fc.record({
    id: fc.uuid(),
    name: fc.string({ minLength: 1, maxLength: 100 }),
    age: fc.integer({ min: 0, max: 150 }),
    score: fc.float({ min: 0, max: 100 }),
  });

  // Property: sorting preserves all elements (no data loss)
  it('should preserve all elements after sorting', () => {
    fc.assert(
      fc.property(fc.array(userArb), (users) => {
        const sorted = sortUsers(users, 'name');
        expect(sorted).toHaveLength(users.length);
        // Every input user exists in output
        users.forEach(user => {
          expect(sorted).toContainEqual(user);
        });
      }),
      { numRuns: 1000 }
    );
  });

  // Property: result is actually sorted
  it('should produce correctly ordered output', () => {
    fc.assert(
      fc.property(fc.array(userArb, { minLength: 2 }), (users) => {
        const sorted = sortUsers(users, 'age');
        for (let i = 1; i < sorted.length; i++) {
          expect(sorted[i].age).toBeGreaterThanOrEqual(sorted[i - 1].age);
        }
      })
    );
  });

  // Property: idempotency - sorting an already sorted array gives same result
  it('should be idempotent', () => {
    fc.assert(
      fc.property(fc.array(userArb), (users) => {
        const sorted1 = sortUsers(users, 'score');
        const sorted2 = sortUsers(sorted1, 'score');
        expect(sorted2).toEqual(sorted1);
      })
    );
  });
});
```

**Tips for Customization:**
- Specify your property-based testing library
- Add: "Focus on serialization/deserialization roundtrip properties"
- Mention: "Test our financial calculation functions for precision invariants"

---

## 9. E2E Test Scenario Writer

**Use Case:** Generate end-to-end test scripts for critical user flows using Playwright, Cypress, or Selenium.

**Prompt:**

```
You are an E2E test automation engineer writing Playwright (or Cypress) tests for critical user journeys.

Generate complete E2E test scripts for the following user flows:

### Requirements:
1. **Framework**: Use [Playwright/Cypress] with TypeScript
2. **Page Object Model**: Create page objects for each page involved
3. **Test Flows**: Cover the complete happy path and the most important failure paths
4. **Selectors**: Use data-testid attributes (not CSS classes or XPath)
5. **Assertions**: Verify both UI state and URL changes
6. **Waits**: Use proper waits (not sleep/timeout) - wait for elements, network idle, etc.
7. **Screenshots**: Capture screenshots at key points for visual verification
8. **Data Independence**: Each test creates its own data and cleans up after
9. **Retry Logic**: Handle flaky elements (animations, lazy loading)
10. **Cross-Browser**: Note any browser-specific considerations

### For Each Test:
- Descriptive test name
- Pre-conditions and test data setup
- Step-by-step actions with assertions after each step
- Cleanup

User flows to test:
"""
[PASTE YOUR USER FLOW DESCRIPTIONS OR WIREFRAMES HERE]
"""
```

**Example Output Snippet:**

```typescript
// page-objects/CheckoutPage.ts
export class CheckoutPage {
  constructor(private page: Page) {}

  async fillShippingAddress(address: ShippingAddress) {
    await this.page.getByTestId('shipping-name').fill(address.name);
    await this.page.getByTestId('shipping-address').fill(address.street);
    await this.page.getByTestId('shipping-city').fill(address.city);
    await this.page.getByTestId('shipping-zip').fill(address.zip);
    await this.page.getByTestId('shipping-country').selectOption(address.country);
  }

  async submitOrder() {
    await this.page.getByTestId('place-order-btn').click();
    await this.page.waitForURL(/\/order-confirmation/);
  }

  async getOrderTotal(): Promise<string> {
    return this.page.getByTestId('order-total').textContent();
  }
}

// tests/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { CheckoutPage } from '../page-objects/CheckoutPage';

test.describe('Checkout Flow', () => {
  test('complete purchase with credit card', async ({ page }) => {
    // Setup: Add item to cart via API (faster than UI)
    const cartId = await api.createCart([{ sku: 'WIDGET-001', qty: 2 }]);

    // Navigate to checkout
    await page.goto(`/checkout?cart=${cartId}`);
    const checkout = new CheckoutPage(page);

    // Step 1: Fill shipping
    await checkout.fillShippingAddress({
      name: 'Test User',
      street: '123 Test St',
      city: 'Portland',
      zip: '97201',
      country: 'US',
    });
    await page.getByTestId('continue-to-payment').click();

    // Step 2: Fill payment (using Stripe test card)
    const stripeFrame = page.frameLocator('iframe[name*="stripe"]');
    await stripeFrame.getByPlaceholder('Card number').fill('4242424242424242');
    await stripeFrame.getByPlaceholder('MM / YY').fill('12/30');
    await stripeFrame.getByPlaceholder('CVC').fill('123');

    // Step 3: Submit order
    await checkout.submitOrder();

    // Verify confirmation page
    await expect(page.getByTestId('order-status')).toHaveText('Order Confirmed');
    await expect(page.getByTestId('order-total')).toHaveText('$59.98');
    await page.screenshot({ path: 'screenshots/order-confirmed.png' });
  });
});
```

**Tips for Customization:**
- Specify: "Use Cypress with Testing Library selectors"
- Add: "Include mobile viewport tests (375px width)"
- Mention: "We need tests for OAuth login flow with Google"

---

## 10. Regression Test Identifier

**Use Case:** Given a code change (diff/PR), identify what existing functionality could break and what regression tests to write.

**Prompt:**

```
You are a QA architect analyzing a code change to determine its blast radius and required regression tests.

Analyze the following code diff and provide:

## 1. Change Impact Analysis
- **Direct Changes**: What behavior is being modified
- **Indirect Effects**: What other features depend on the changed code
- **Data Impact**: Does this change affect stored data, cached data, or data formats?
- **API Impact**: Does this change any public APIs or contracts?
- **Config Impact**: Does this require config/env changes?

## 2. Blast Radius Map
```
Changed: UserService.updateProfile()
  └── Affects: ProfilePage component (renders profile data)
  └── Affects: EmailService (sends profile update notifications)
  └── Affects: AuditLog (logs profile changes)
  └── Affects: API response of GET /api/users/:id
  └── Affects: Mobile app (consumes the API)
```

## 3. Regression Test Checklist
For each affected area:
- [ ] Test case description
- [ ] Priority (P0 = must test, P1 = should test, P2 = nice to test)
- [ ] Can be automated? (Yes/No)
- [ ] Estimated effort

## 4. Specific Regression Tests to Write
For the top 5 highest-risk regressions, write complete test code:
- Focus on the most likely breakage points
- Test the boundary between changed and unchanged code
- Test backward compatibility

## 5. Deployment Verification
- Smoke tests to run immediately after deploy
- Metrics to monitor for 24 hours after deploy

Code diff:
"""
[PASTE YOUR GIT DIFF OR PR CHANGES HERE]
"""
```

**Example Output Snippet:**

```markdown
## Change Impact Analysis

**Direct Change**: `calculateShipping()` now factors in package dimensions,
not just weight. Shipping costs will change for all orders.

**Blast Radius:**
```
Changed: calculateShipping(weight) → calculateShipping(weight, dimensions)
  ├── Affects: CheckoutService.getOrderSummary() (calls calculateShipping)
  │   ├── Affects: Checkout UI (displays shipping cost)
  │   └── Affects: Order confirmation email (shows shipping cost)
  ├── Affects: QuoteService.getShippingEstimate() (API endpoint)
  │   └── Affects: Mobile app (shows shipping estimate)
  ├── Affects: Order.shippingCost (stored value in DB)
  │   └── Affects: Financial reports (aggregates shipping revenue)
  └── Affects: ShippingLabelService (prints label with cost)
```

## Regression Test Checklist

- [x] P0: Existing orders display correctly (stored costs unchanged)
- [x] P0: Checkout calculates correct shipping with new formula
- [x] P0: API backward compatibility (old clients sending only weight)
- [ ] P1: Email template renders new shipping breakdown
- [ ] P1: Mobile app handles new API response shape
- [ ] P2: Financial report totals still balance

## Regression Test: API Backward Compatibility

```javascript
it('should accept legacy requests without dimensions', async () => {
  // Old mobile app clients send only weight
  const response = await request(app)
    .post('/api/shipping/estimate')
    .send({ weight: 2.5 });  // No dimensions field

  expect(response.status).toBe(200); // Not 400
  expect(response.body.cost).toBeGreaterThan(0);
  // Should use default dimensions when not provided
  expect(response.body.dimensionsUsed).toBe('default');
});
```
```

**Tips for Customization:**
- Paste your actual git diff: `git diff main..feature-branch`
- Add: "We have 500 API consumers - backward compatibility is critical"
- Specify: "Include performance regression tests - this is a hot path"
