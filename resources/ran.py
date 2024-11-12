from p2pnetwork.node import Node
import asyncio
import datetime
import json
import logging
import os
import time
from aiohttp import ClientError
from p2pnetwork.node import Node
import qrcode

from victor_aries_cloudagent.demo.runners.agent_container import (  # noqa:E402
   arg_parser,
   create_agent_with_args,
   AriesAgent,
)
from victor_aries_cloudagent.demo.runners.faber import FaberAgent
from victor_aries_cloudagent.demo.runners.support.agent import (  # noqa:E402
   CRED_FORMAT_INDY,
   CRED_FORMAT_JSON_LD,
   SIG_TYPE_BLS,
)
from victor_aries_cloudagent.demo.runners.support.utils import (  # noqa:E402
   log_msg,
   log_status,
   prompt,
   prompt_loop,
)

class RAN(Node):

    CRED_PREVIEW_TYPE = "https://didcomm.org/issue-credential/2.0/credential-preview"
    SELF_ATTESTED = os.getenv("SELF_ATTESTED")
    TAILS_FILE_COUNT = int(os.getenv("TAILS_FILE_COUNT", 100))
    logging.basicConfig(level=logging.WARNING)
    LOGGER = logging.getLogger(__name__)

    connection_id = None
    connection_ready = None
    cred_state = {}
    cred_attrs = {}

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(RAN, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, node):
        print("No de saida conectado (" + self.id + "): " + node.id)

    def inbound_node_connected(self, node):
        print("No de entrada conectado: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        print("No de entrada desconectado: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("No de saida desconectado: (" + self.id + "): " + node.id)

    def node_message(self, node, data):
        print("Mensagem (" + self.id + ") de " + node.id + ": " + str(data))

    def node_disconnect_with_outbound_node(self, node):
        print("No deseja se desconectar de outro no de saida: (" + self.id + "): " + node.id)

    def node_request_to_stop(self):
        print("No eh solicitado a parar (" + self.id + "): ")

    def verifica_credencial(self, vc, vc_id):
        if (vc != None and vc != ""):
            # precisa verificar se a vc existe no VDR
            try:
                self.generate_proof_request_web_request(20, vc, vc_id, None)
            except Exception:
                return False
            else:
                return True
        return False

    def generate_credential_offer(self, aip, cred_type, cred_def_id, exchange_tracing):
       d = datetime.date.today()
       if aip == 10:
           # define attributes to send for credential
           self.cred_attrs[cred_def_id] = {
               "name": "Vehicle",
               "application": "ADAS",
               "datetime": d,
               "timestamp": str(int(time.time())),
           }


           cred_preview = {
               "@type": self.CRED_PREVIEW_TYPE,
               "attributes": [
                   {"name": n, "value": v}
                   for (n, v) in self.cred_attrs[cred_def_id].items()
               ],
           }
           offer_request = {
               "connection_id": self.connection_id,
               "cred_def_id": cred_def_id,
               "comment": f"Offer on cred def id {cred_def_id}",
               "auto_remove": False,
               "credential_preview": cred_preview,
               "trace": exchange_tracing,
           }
           return offer_request


       elif aip == 20:
           if cred_type == CRED_FORMAT_INDY:
               self.cred_attrs[cred_def_id] = {
                   "name": "Vehicle",
                   "application": "ADAS",
                   "datetime": d,
                   "timestamp": str(int(time.time())),
               }


               cred_preview = {
                   "@type": self.CRED_PREVIEW_TYPE,
                   "attributes": [
                       {"name": n, "value": v}
                       for (n, v) in self.cred_attrs[cred_def_id].items()
                   ],
               }
               offer_request = {
                   "connection_id": self.connection_id,
                   "comment": f"Offer on cred def id {cred_def_id}",
                   "auto_remove": False,
                   "credential_preview": cred_preview,
                   "filter": {"indy": {"cred_def_id": cred_def_id}},
                   "trace": exchange_tracing,
               }
               return offer_request


           elif cred_type == CRED_FORMAT_JSON_LD:
               offer_request = {
                   "connection_id": self.connection_id,
                   "filter": {
                       "ld_proof": {
                           "credential": {
                               "@context": [
                                   "https://www.w3.org/2018/credentials/v1",
                                   "https://w3id.org/citizenship/v1",
                                   "https://w3id.org/security/bbs/v1",
                               ],
                               "type": [
                                   "VerifiableCredential",
                                   "PermanentResident",
                               ],
                               "id": "https://credential.example.com/residents/1234567890",
                               "issuer": self.did,
                               "issuanceDate": "2020-01-01T12:00:00Z",
                               "credentialSubject": {
                                   "type": ["PermanentResident"],
                                   "givenName": "Vehicle",
                                   "application": "ADAS",
                               },
                           },
                           "options": {"proofType": SIG_TYPE_BLS},
                       }
                   },
               }
               return offer_request


           else:
               raise Exception(f"Error invalid credential type: {self.cred_type}")


       else:
           raise Exception(f"Error invalid AIP level: {self.aip}")
       
    def generate_proof_request_web_request(self, aip, cred_type, revocation, exchange_tracing, connectionless=False):
       d = datetime.date.today()
       if aip == 10:
           req_attrs = [
               {
                   "name": "name",
                   "restrictions": [{}],
               },
           ]
           if revocation:
               req_attrs.append(
                   {
                       "name": "name",
                       "restrictions": [{}],
                       "non_revoked": {"to": int(time.time() - 1)},
                   },
               )
           else:
               req_attrs.append(
                   {
                       "name": "name",
                       "restrictions": [{}],
                   }
               )
           if self.SELF_ATTESTED:
               # test self-attested claims
               req_attrs.append(
                   {"name": "self_attested_thing"},
               )
           req_preds = [
               # test zero-knowledge proofs
               {
                   "name": "Vehicle",
                   "p_type": "<=",
                   "restrictions": [{}],
               }
           ]
           indy_proof_request = {
               "name": "Proof of Request",
               "version": "1.0",
               "requested_attributes": {
                   f"0_{req_attr['name']}_uuid": req_attr for req_attr in req_attrs
               },
               "requested_predicates": {
                   f"0_{req_pred['name']}_GE_uuid": req_pred for req_pred in req_preds
               },
           }


           if revocation:
               indy_proof_request["non_revoked"] = {"to": int(time.time())}


           proof_request_web_request = {
               "proof_request": indy_proof_request,
               "trace": exchange_tracing,
           }
           if not connectionless:
               proof_request_web_request["connection_id"] = self.connection_id
           return proof_request_web_request


       elif aip == 20:
           if cred_type == CRED_FORMAT_INDY:
               req_attrs = [
                   {
                       "name": "name",
                       "restrictions": [{}],
                   },
                   {
                       "name": "name",
                       "restrictions": [{}],
                   },
               ]
               if revocation:
                   req_attrs.append(
                       {
                           "name": "name",
                           "restrictions": [{""}],
                           "non_revoked": {"to": int(time.time() - 1)},
                       },
                   )
               else:
                   req_attrs.append(
                       {
                           "name": "name",
                           "restrictions": [{""}],
                       }
                   )
               if self.SELF_ATTESTED:
                   # test self-attested claims
                   req_attrs.append(
                       {"name": "self_attested_thing"},
                   )
               req_preds = [
                   # test zero-knowledge proofs
                   {
                   "name": "Vehicle",
                   "p_type": "<=",
                   "restrictions": [{}],
                   }
               ]
               indy_proof_request = {
                   "name": "Proof of Request",
                   "version": "1.0",
                   "requested_attributes": {
                       f"0_{req_attr['name']}_uuid": req_attr for req_attr in req_attrs
                   },
                   "requested_predicates": {
                       f"0_{req_pred['name']}_GE_uuid": req_pred
                       for req_pred in req_preds
                   },
               }


               if revocation:
                   indy_proof_request["non_revoked"] = {"to": int(time.time())}


               proof_request_web_request = {
                   "presentation_request": {"indy": indy_proof_request},
                   "trace": exchange_tracing,
               }
               if not connectionless:
                   proof_request_web_request["connection_id"] = self.connection_id
               return proof_request_web_request


           elif cred_type == CRED_FORMAT_JSON_LD:
               proof_request_web_request = {
                   "comment": "test proof request for json-ld",
                   "presentation_request": {
                       "dif": {
                           "options": {
                               "challenge": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                               "domain": "4jt78h47fh47",
                           },
                           "presentation_definition": {
                               "id": "32f54163-7166-48f1-93d8-ff217bdb0654",
                               "format": {"ldp_vp": {"proof_type": [SIG_TYPE_BLS]}},
                               "input_descriptors": [
                                   {
                                       "id": "citizenship_input_1",
                                       "name": "EU Driver's License",
                                       "schema": [
                                           {
                                               "uri": "https://www.w3.org/2018/credentials#VerifiableCredential"
                                           },
                                           {
                                               "uri": "https://w3id.org/citizenship#PermanentResident"
                                           },
                                       ],
                                       "constraints": {
                                           "limit_disclosure": "required",
                                           "is_holder": [
                                               {
                                                   "directive": "required",
                                                   "field_id": [
                                                       "1f44d55f-f161-4938-a659-f8026467f126"
                                                   ],
                                               }
                                           ],
                                           "fields": [
                                               {
                                                   "id": "1f44d55f-f161-4938-a659-f8026467f126",
                                                   "path": [
                                                       "$.credentialSubject.familyName"
                                                   ],
                                                   "purpose": "The claim must be from one of the specified person",
                                                   "filter": {"const": "SMITH"},
                                               },
                                               {
                                                   "path": [
                                                       "$.credentialSubject.givenName"
                                                   ],
                                                   "purpose": "The claim must be from one of the specified person",
                                               },
                                           ],
                                       },
                                   }
                               ],
                           },
                       }
                   },
               }
               if not connectionless:
                   proof_request_web_request["connection_id"] = self.connection_id
               return proof_request_web_request


           else:
               raise Exception(f"Error invalid credential type: {self.cred_type}")


       else:
           raise Exception(f"Error invalid AIP level: {self.aip}")