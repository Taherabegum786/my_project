changequote(<!,!>)
changecom(<!/*!>,<!*/!>)
pushdef(<!F_State_S4!>, <!L_State_S4($@)!>)dnl
pushdef(<!F_State_C4!>, <!L_State_C4($@)!>)dnl
define(<!State!>,<!F_State_$1(shift($@))!>)dnl
define(<!ClientCertReq!>,<!L_ClientCertReq($@)!>)dnl
define(<!ServerCertReq!>,<!L_ServerCertReq($@)!>)dnl
define(<!CachePSK!>, <!F_CachePSK($@)!>)dnl


theory TLS_13_DAPV_lemmas
begin

include(header.m4i)
include(model.m4i)
include(all_lemmas.m4i)


uniq(C0)
uniq(C1)
uniq(C1_retry)
uniq(S1)
uniq(S1_PSK)
uniq(S1_PSK_DHE)
uniq(C1_PSK)
uniq(C1_PSK_DHE)
uniq(S2a)
uniq(S2b)
uniq(S2c)
uniq(S2c_req)
uniq(S2d)
uniq(S2d_PSK)
uniq(C2a)
uniq(C2b)
uniq(C2c)
uniq(C2c_req)
uniq(C2d)
uniq(C2d_PSK)
uniq(C3)
uniq(C3_cert)
uniq(S3)
uniq(S3_cert)

one_of(S1, S1_PSK_DHE)
one_of(S1_PSK, S1_PSK_DHE)
one_of(S1_PSK, S1)
one_of(C1, C1_PSK_DHE)
one_of(C1_PSK, C1_PSK_DHE)
one_of(C1_PSK, C1)
one_of(S3, S3_cert)
one_of(C3, C3_cert)
one_of(S2d, S2d_PSK)
one_of(C2d, C2d_PSK)


lemma_cert_req_origin/* [typing]:
  "All certificate_request_context certificate_extensions keys #i.
    KU(senc{handshake_record('13', certificate_request_context, certificate_extensions)}keys)@i ==> 
      (Ex #j. KU(certificate_request_context)@j & #j < #i) |
      (Ex #j tid actor role. running(CertReqCtxt, actor, role, certificate_request_context)@j & #j < #i)"
*/

lemma_nst_source/* [typing]:
  "All ticket ticket_age_add tkt_lt tkt_exts app_key #i.
    KU(senc{handshake_record('4', tkt_lt, ticket_age_add, ticket, tkt_exts)}app_key)@i ==>
      (Ex #j #k. KU(ticket)@j & KU(ticket_age_add)@k & #j < #i & #k < #i) |
      (Ex tid S #j. running_server(NST, ticket, ticket_age_add)@j & #j < #i)"
*/

/* ================================================================== */
/* DAPV lemmas.  The existing long-term key (!Ltk) is the classical key;
   !LtkP is the post-quantum key.  The upstream lemmas continue to describe
   the guarantees of the PROVISIONAL state (classical verification). */

/* Sources: where a (hybrid) CertificateVerify signature can come from. */
lemma dapv_sigP_origin [reuse]:
  "All certificate certificate_request_context sigE sigP verify_data hs_key sm ltkP #i.
      KU(senc{handshake_record('11', certificate_request_context, certificate),
               handshake_record('15', <sigE, sigP>),
               handshake_record('20', verify_data)}hs_key)@i
      & (sigP = sign{sm}ltkP) ==>
      (Ex #j. KU(ltkP)@j & #j < #i) | (Ex #k. UseLtkP(ltkP, sigP)@k & #k < #i)"

/* Executability: an honest handshake reaches full authentication. */
lemma dapv_reach_promotion:
  exists-trace
  "Ex tid C S sm m #i. DAPV_Promoted(tid, C, S, sm, m)@i
     & not (Ex #r. RevLtk(S)@r) & not (Ex #r. RevLtkP(S)@r)"

/* Non-vacuity: with the classical key alone, the adversary completes a
   PROVISIONAL handshake for a transcript the server never signed. */
lemma dapv_provisional_impersonation_exists:
  exists-trace
  "Ex tid C S sm m #i. DAPV_Provisional(tid, C, S, sm, m)@i
     & not (Ex tid2 #j. DAPV_ServerSigned(tid2, S, sm)@j)
     & not (Ex #r. RevLtkP(S)@r)"

/* P4a in the full model: promotion implies that the server signed exactly
   this transcript (both hellos, key shares, extensions and certificate)
   with its PQ key, unless that key was compromised -- independently of
   the classical key. */
lemma dapv_promotion_needs_pq_key:
  "All tid C S sm m #i. DAPV_Promoted(tid, C, S, sm, m)@i ==>
     (Ex tid2 #j. DAPV_ServerSigned(tid2, S, sm)@j & #j < #i)
   | (Ex #r. RevLtkP(S)@r & #r < #i)"

/* Ticket rule: a certificate-authenticated session stores a resumption
   ticket only after promotion.  (Falsified with -D DAPV_NAIVE_TICKETS.) */
lemma dapv_ticket_only_after_promotion:
  "All tid C S psk sm m #i #p. DAPV_TicketStored(tid, C, S, psk)@i
       & DAPV_Provisional(tid, C, S, sm, m)@p ==>
     Ex sm2 m2 #j. DAPV_Promoted(tid, C, S, sm2, m2)@j & #j < #i"

/* Attack witness (meaningful with -D DAPV_NAIVE_TICKETS): a client resumes
   with a ticket that the server never issued, obtained in a provisional
   session, while the server's PQ key is uncompromised. */
lemma dapv_resumption_with_unissued_ticket:
  exists-trace
  "Ex tid tid0 C S psk #i #k. DAPV_PSKAuth(tid, C, S, psk)@i
     & DAPV_TicketStored(tid0, C, S, psk)@k
     & not (Ex tid2 C2 #j. DAPV_TicketIssued(tid2, S, C2, psk)@j)
     & not (Ex #r. RevLtkP(S)@r)"

end
