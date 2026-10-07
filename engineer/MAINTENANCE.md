# Engineer Maintenance Cycle

Normal cadence: approximately every 2 months initially, with urgent maintenance outside the cadence for security or critical breakage.

Sequence: read project state → run Engineer checks → inspect Git → research upstream → review issues/PRs → review runtime/model contracts → rehearse meaningful changes → prepare a small change → validate → document → commit → merge/push under repository policy → shut down temporary Engineer runtime/model.

Questions: can Gary bootstrap cleanly, are API contracts stale, are adapters correct, are dependencies secure/supported, can permissions be tightened, do tests cover recent failures, and is the portable backbone still lean?
