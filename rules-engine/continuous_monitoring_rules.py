# Este arquivo define as regras de negócio para o motor de monitoramento contínuo.
# Essas regras são independentes dos microsserviços e descrevem a lógica de
# compliance e risco de forma declarativa.

SANCTIONED_INTERACTION_RULE = {
    "rule_id": "CONTINUOUS_MONITORING_SANCTIONED_INTERACTION_V1",
    "description": "Acionada quando um cliente com status KYC_APPROVED tem uma carteira associada que interage com uma entidade sancionada, movendo o cliente para revisão imediata.",
    "is_active": True,

    "trigger": {
        "source_service": "onchain-analyzer",
        "event_type": "flag_added",
        "details": {
            "flag_name": "interacted_with_sanctioned_entity",
            "flag_value": True
        }
    },

    "conditions": {
        "all": [
            {
                "fact": "client.kyc_status",
                "operator": "equal",
                "value": "KYC_APPROVED"
            }
        ]
    },

    "actions": [
        {
            "type": "generate_alert",
            "params": {
                "level": "CRITICAL",
                "title": "Interação On-Chain com Entidade Sancionada",
                "message": "Cliente com KYC aprovado teve carteira associada interagindo com entidade sancionada. Perfil de risco comprometido.",
                "context": {
                    "client_id": "{client.id}",
                    "wallet_address": "{wallet.address}",
                    "triggering_flag": "interacted_with_sanctioned_entity"
                }
            }
        },
        {
            "type": "update_client_status",
            "params": {
                "target": "client",
                "identifier": "{client.id}",
                "new_status": "UNDER_REVIEW",
                "reason_code": "AML_004_SANCTIONED_INTERACTION",
                "notes": "Status alterado automaticamente devido à interação on-chain de alto risco."
            }
        },
        {
            "type": "set_recommended_action",
            "params": {
                "recommendation": "Bloqueio preventivo de novas transações e reavaliação manual do perfil de risco."
            }
        }
    ]
}