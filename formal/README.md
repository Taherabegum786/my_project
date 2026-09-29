# Formal verification of DAPV (Tamarin)

`dapv.spthy` models a hybrid-authenticated TLS 1.3 handshake in which the
client verifies the classical signature synchronously, enters a PROVISIONAL
state, and verifies the post-quantum signature later (DAPV). It also covers
session tickets and resumption.

The adversary controls the network and may reveal either signature key of
any server at any time.

## Running the proofs

Tested with Tamarin 1.10.0 and Maude 3.5.

```bash
export LANG=C.UTF-8
tamarin-prover --prove dapv.spthy                    # DAPV as specified
tamarin-prover --prove -D=NAIVE_TICKETS dapv.spthy   # tickets usable while provisional
tamarin-prover --prove -D=NO_BINDING dapv.spthy      # PQ signature not bound to the transcript
tamarin-prover --prove -D=NO_FIN_COVER dapv.spthy    # Finished/keys do not cover the signatures
```

Each run takes 12–26 s on 4 cores. The outputs are in `summary_*.txt`.

## Results

| Variant | All-trace lemmas | Attacks found |
|---|---|---|
| DAPV (default) | all verified | — |
| NAIVE_TICKETS | resumption authentication falsified | an adversary holding only the classical key gets a ticket accepted |
| NO_BINDING | 6 falsified | replay of a PQ signature promotes an impersonator |
| NO_FIN_COVER | all verified | — (the transcript signature is the essential binding) |

In every variant, the existence lemmas (executability and non-vacuity) are
verified.
