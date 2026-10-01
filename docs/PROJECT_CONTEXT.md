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
