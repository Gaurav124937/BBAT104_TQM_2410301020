# PDCA Cycle — ACT

## Standardize Successful Improvements

When verification confirms that an improvement works:

1. Keep the corrected implementation in the main project.
2. Add a regression test or repeatable verification step.
3. Update the defect log status to Closed.
4. Update project documentation where the workflow changed.
5. Use the updated checksheet as the new quality baseline.

## If the Result Is Not Satisfactory

If a defect remains or reappears:

1. Reopen the defect.
2. Reassess the root cause using the Fishbone analysis.
3. Update the FMEA occurrence/detection assessment if evidence supports it.
4. Define a new corrective action.
5. Start the next PDCA cycle.

## Continuous Improvement Loop

```text
PLAN
  ↓
DO
  ↓
CHECK
  ↓
ACT
  ↓
Standardize successful change
  ↓
New baseline
  ↓
Next PDCA cycle
```

This creates a repeatable continuous-improvement loop rather than treating each
bug fix as an isolated activity.
