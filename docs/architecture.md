## Architecture Overview

This repository provides a validation-first framework to identify
orphaned (unattached) Azure managed disks safely.

### High-level Flow
1. Enumerate Azure subscriptions
2. Identify unattached managed disks
3. Apply safety checks (age, tags, activity)
4. Classify disks for action
5. Estimate potential cost savings

### Design Principles
- No destructive action by default
- Safety before cleanup
- Subscription-agnostic design
- Cost visibility before deletion
