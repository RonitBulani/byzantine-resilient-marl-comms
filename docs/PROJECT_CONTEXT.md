# Project context

The original project, **Byzantine-Resilient Cooperative Pursuit**, was completed by a five-person team.

The complete system combined:

- a PettingZoo cooperative-pursuit environment
- independent PPO and MAPPO baselines
- partial-observability experiments
- an explicit inter-agent communication channel
- Byzantine message corruption
- resilient aggregation protocols
- experiment sweeps and statistical/result visualisation

This repository is a portfolio extract of the Byzantine and communications subsystem only.

## Why the extract is separate

Copying the entire group repository into a personal portfolio would make authorship unclear. The environment, reinforcement-learning algorithms, training pipeline and other components were developed across the team.

The original repository remains the best place to inspect the whole project and its commit history:

https://github.com/yshkrum/marl-byzantine-pursuit


## Communication-signal caveat

The final team implementation passed the true hider position into the
communicating protocols through `EnvState.true_hider_pos`. The portfolio
extract preserves this behaviour so that its code remains faithful to the
experiment that generated the published team results.

See `IMPLEMENTATION_LIMITATION.md` for the precise scope of this limitation.
