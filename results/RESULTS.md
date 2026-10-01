# Results summary

These values are taken from the final documented summary in the original team repository.

## Experimental scale

- 240 MAPPO condition/seed cells
- 60 iPPO condition/seed cells
- 100 evaluation episodes per cell
- 30,000 evaluation episodes in total
- 8 seekers on a 16x16 grid
- two observability regimes (`r=7` and `r=3`)
- Byzantine fraction varied up to `f=0.5`

## Honest baseline

| Regime | MAPPO | iPPO | Difference |
|---|---:|---:|---:|
| r=7 | 68.3% | 52.0% | +16.3 pp |
| r=3 | 97.3% | 47.0% | +50.3 pp |

## Degradation at f=0.5 under broadcast

| Attack | r=7 | r=3 |
|---|---:|---:|
| Random noise | -9.3 pp | -10.6 pp |
| Misdirection | -19.6 pp | -33.6 pp |
| Spoofing | approximately 0 pp | approximately 0 pp |
| Silence | -9.4 pp | -48.3 pp |

## Interpretation

The strongest degradation in the narrow-observability condition came from message suppression: when agents depended more heavily on peer information, silence removed information that the local observation could not replace.

Spoofing produced little degradation in the final implementation because the receiving policy consumed peer information through fixed observation slots rather than relying directly on the transmitted sender identity. This is an implementation-specific result, not a general claim that identity spoofing is harmless in MARL systems.

The full team repository should be treated as the authoritative source for the complete environment, training code and experiment runner.
