# Contributing to Red Team Console

## Branch Naming
Please use the following conventions for branches:
- `injection/<name>` for injection test cases
- `jailbreak/<name>` for jailbreak test cases

## One Test Case per PR
Keep PRs focused. Submit only one test case per pull request to make reviewing easier.

## Cross-Pair Review Process
Our team is split into two pairs: an "injection" pair and a "jailbreak" pair. 
When you submit a PR for one category, the `CODEOWNERS` file will automatically assign the opposite pair for review. 
(e.g., Jailbreak cases are reviewed by the Injection pair, and vice versa).

## Reviewer Guidelines
When reviewing a PR, please check the following:
1. **Schema Validity:** (Should be handled by GitHub Actions, but good to verify).
2. **Expected Behavior:** Is the `expected_behavior` actually correct? It should describe the model doing the right thing, not just reflexively saying "should refuse".
3. **Categorization:** Are the `category` and `subcategory` accurate for this attack type?
4. **Severity:** Is the `severity` (Low, Medium, High) reasonable for the given scenario?
