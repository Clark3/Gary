# GitHub Repository Setup

Recommended `main` protection: require pull requests, require CI, resolve conversations, block force pushes and branch deletion, and use at least one approving review when another reviewer is available.

As this is currently a single-maintainer project, do not create a self-blocking rule that makes ordinary maintenance impossible without a second person. The goal is reviewability and CI enforcement, not ceremony.

Also enable Dependabot alerts, secret scanning/push protection, and code scanning where available for the public repository.

The connected GitHub integration can maintain project files but does not expose branch-protection/ruleset mutation here, so those administrative settings must be verified in GitHub's repository Settings rather than assumed.
