# PocketLedger Development Roadmap

## Completed in the initial MVP

- FastAPI expense creation, listing with pagination, and lookup by ID.
- SQLite persistence using SQLAlchemy, exact amount storage, and Pydantic validation.
- Basic HTTP errors and isolated API tests, including restart persistence.
- Local setup documentation and fictional API examples.

## Future work: estimated 46 hours

These tasks are unimplemented. Estimates describe expected hands-on development
and verification effort, not completed work or a guarantee of duration. Implement
them in small, reviewable sessions using fictional data only.

| Work area | Actionable tasks and completion criteria | Estimate |
| --- | --- | --- |
| Expense editing and deletion | Add PATCH and DELETE routes; validate partial updates; verify missing IDs, persistence, and deletion behavior. | 3 h |
| Category management | Add category records and CRUD endpoints; define duplicate-name rules and handling of categories used by expenses; migrate free-text categories. | 4 h |
| Monthly budgets | Model monthly category budgets; add budget endpoints; calculate remaining amounts and month boundaries; verify overspending cases. | 5 h |
| Credit card billing cycles | Model fictional cards and closing/payment days; assign expenses to statement periods; handle short months, year transitions, and due dates. No bank connections. | 5 h |
| Installment calculations | Define rounding and remainder allocation; build monthly installment schedules; test totals, early payoff assumptions, and cross-year schedules. | 4 h |
| Spending analytics | Add date-filtered totals and category/month aggregates; handle empty periods; verify results against fictional fixtures. | 4 h |
| React frontend | Scaffold app; build expense form/list, category controls, and monthly budget view; add loading, empty, and error states; connect to API and verify keyboard usability. | 10 h |
| Expanded automated testing | Add regression coverage for budgets, billing, installments, analytics, database failures, and frontend/API integration; configure CI to run checks. | 5 h |
| Docker and deployment | Add Dockerfile and Compose with persistent SQLite volume; document configuration and backups; choose hosting and prepare a deployment guide with smoke checks. Deployment requires a separate decision. | 3 h |
| Schema migrations and hardening | Introduce versioned migrations before schema expansion; document single-user/local scope and evaluate authentication, access controls, and operational logging before public use. | 3 h |
| **Total future effort** | | **46 h** |

## Suggested sequence

1. Expense mutations, migrations, and categories.
2. Budgets, fictional card billing cycles, and installments.
3. Analytics and React interface.
4. Broader regression testing, CI, containers, and deployment preparation.

Authentication, multi-currency support, and real financial integrations are outside
this initial roadmap's deliverables. Do not introduce real financial data or bank
connections. Review program eligibility separately before applying; planned hours
and a functional MVP do not guarantee BYOP approval.
