# Implementation limitation: oracle-style communication signal

This portfolio extract preserves an important detail of the final team
implementation because changing it would make the source code inconsistent
with the reported experiment results.

## What the final implementation does

For the communicating protocols:

- Broadcast
- Gossip
- Trimmed Mean
- Reputation

`send()` uses:

```python
x, y = state.true_hider_pos
```

In the full team environment, `true_hider_pos` is populated directly from the
environment's current hider position.

As a result, an honest communicating agent can send the true hider position
even when its visibility-limited local observation would contain the sentinel
value for an unseen hider.

## Why this matters

The reported MAPPO/Byzantine results therefore measure robustness to message
corruption and aggregation over an **oracle-style shared position channel**.

They should not be interpreted as evidence that the same performance would
hold when every sender can communicate only what it can locally observe.

This is particularly relevant when interpreting the difference between the
wide- and narrow-observability regimes.

## Why the portfolio code is not silently changed

Changing the communicating protocols to read `state.obs[2:4]` would create a
different experiment from the one that produced the original team results.

For transparency, this repository keeps the original behaviour and documents
the limitation explicitly instead.
