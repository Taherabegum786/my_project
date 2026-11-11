# A Security Credential Management System for V2X Communications (arXiv preprint 2018)
url: https://arxiv.org/abs/1802.05323
read: full
problem: Design of a nationwide V2X PKI (SCMS, developed by CAMP for USDOT) giving security and privacy, with efficient revocation despite many pseudonym certificates per vehicle.
method: SCMS with split organizations (e.g., RA, PCA, linkage authorities) so no single insider can link pseudonym certificates; supports bootstrapping, certificate provisioning, misbehavior reporting, revocation; butterfly key expansion for certificate batches; linkage values for revocation.
numbers: ~300 billion certificates per year for 300 million vehicles at full capacity; BSMs up to ten per second; linkage values and pre-linkage values 9 bytes; 64 linkage periods; linkage period one week; ~one linkage value collision per year in a system of 250 million vehicles; devices may need up to 3 years' worth of certificates (covered time-span 1-3 years).
limits: Classical (ECC) design only; no post-quantum analysis; proof-of-concept stage per the paper.
use-for: v2x
