# My contribution

**Role: Byzantine & Communications Lead**

My responsibility was the communication/adversary layer used by the MARL experiments.

## Components

- communication interface and message-passing contract
- broadcast baseline
- gossip protocol
- trimmed-mean robust aggregation
- reputation-based robust aggregation
- random-noise Byzantine attack
- omniscient misdirection attack
- sender-identity spoofing attack
- silent/dropout attack
- unit tests and integration checks for these components
- contribution to the communication-focused experimental interpretation

## Boundary of ownership

The portfolio repository deliberately does not present the pursuit environment, MAPPO implementation, iPPO implementation, reward design or training pipeline as my individual work.

A small compatibility module (`src/common.py`) has been added specifically for this standalone extract. It replaces shared team environment types that the original communication modules imported.
