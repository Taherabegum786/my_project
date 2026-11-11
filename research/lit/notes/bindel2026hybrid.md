# Hybrid Signature Spectrums (IETF RFC 9955, Informational, 2026)
url: https://www.rfc-editor.org/rfc/rfc9955.txt (doi 10.17487/RFC9955)
read: full
problem: Hybrid (e.g. post-quantum/traditional) signature designs differ in which security and deployment properties they give; designers lack a shared vocabulary for choosing among them.
method: Classifies design goals and security considerations: hybrid authentication, proof composability, weak and strong non-separability, backwards/forwards compatibility, Simultaneous Verification, hybrid generality, performance, space efficiency, minimal duplicate information. Also gives a non-separability spectrum, an artifacts discussion (artifact locations), a need-for-approval spectrum, and EUF-CMA challenges. Single signer and single verifier only.
numbers: none (conceptual document)
limits: Does not recommend concrete combiners, instantiations or use-case choices. Multiple signers or verifiers are out of scope. Security assumes correct key provisioning and management (entity authentication, revocation).
use-for: framework
