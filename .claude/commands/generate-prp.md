# Role: Senior Software Architect

# Task: Generate a comprehensive Product Requirements Prompt (PRP)

**Phase 1: Research & Analysis**

1. Read the feature request from `$ARGUMENTS`
2. Analyze existing codebase patterns, especially `examples/` directory
3. Identify dependencies, conflicts, and integration points
4. Review security, performance, and compatibility requirements

**Phase 2: Blueprint Creation** 5. Define clear file structure and module boundaries 6. Create step-by-step implementation plan with:

- File modifications/creations
- Functions/classes to implement
- Integration points and dependencies
- Error handling strategies

7. Define validation gates:
   - Unit tests (`pytest tests/test_feature.py`)
   - Integration tests
   - Code quality checks (`flake8`, `mypy`)
   - Security scans if applicable

**Phase 3: Risk Management** 8. Identify potential failure points and rollback procedures 9. Define acceptance criteria and performance benchmarks 10. Create contingency plans for common issues

**Output:** Save as `PRPs/feature_name_prp.md` with sections: Architecture, Implementation Steps, Validation Gates, Risk Mitigation, Rollback Plan.
