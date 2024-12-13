from typing import Any, Dict, List, Tuple, Union

from setup.adapters.mambu_models.clients import Clients
from setup.adapters.mambu_models.loans import Loans
from src.mambu.domain.queries import GetClient, GetGroup, GetLoan


def get_json_group(group):
    data = {
        "id": group.id,
        "encoded_key": group.encoded_key,
        "group_name": group.group_name,
        "created": group.creation_date,
        "updated": group.last_modified_date,
        "community_center": group.community_center,
        "tribu": group.tribu,
        "coordinator": group.full_name_ce,
        "cycle": group.loan_cycle,
        "leader": get_json_data_roles(clients=group.group_members, find_role="Lider"),
        "treasurer": get_json_data_roles(
            clients=group.group_members, find_role="Tesorera"
        ),
        "address": group.addresses,
        "mobile_phone": group.mobile_phone,
        "home_phone": group.home_phone,
        "full_addresses": group.full_addresses,
        "location_reference": group.referencia_de_ubicacion_groups,
        "level": group.nivel_groups,
        "type_cicle": group.ciclo_tipo_groups,
        "meeting_day": group.dia_de_reunion_groups,
        "meeting_hour": group.hora_de_reunion_groups,
        "members": [value.client_key for value in group.group_members],
    }

    return data


def get_json_data_roles(clients, find_role="Lider"):
    data = {}  # type: ignore
    if not clients:
        return data

    for value in clients:
        try:
            if value.roles[0].role_name == find_role:
                client = get_attr(propertie_data=value, propertie="client")
                if client:
                    data = {
                        "full_name": get_attr(
                            propertie_data=client, propertie="full_name"
                        ),
                        "mobile_phone": get_attr(
                            propertie_data=client, propertie="mobile_phone"
                        ),
                        "home_phone": get_attr(
                            propertie_data=client, propertie="home_phone"
                        ),
                    }
                    data["full_name"] = data["full_name"].replace("  ", " ")
                    break
        except Exception:
            continue

    return data


def get_criteria_data(
    array_search_key: Dict, criteria: Union[GetLoan, GetGroup, GetClient]
) -> List[Tuple[Any, Any, Any]]:
    ignored_keys = {
        "limit",
        "offset",
        "data_response",
        "tribu",
    }
    data = []
    dictionary_criteria = criteria.__dict__
    find_by_date = ()

    for key, value in dictionary_criteria.items():
        if value and key not in ignored_keys:
            if key == "date_init" or key == "date_end":
                if find_by_date:
                    find_by_date = find_by_date + (value,)
                    data.append(find_by_date)
                else:
                    find_by_date = (
                        array_search_key[key][0],
                        array_search_key[key][1],
                        value,
                    )  # type: ignore
            else:
                data.append(
                    (
                        array_search_key[key][0],
                        array_search_key[key][1],
                        value,
                    )
                )

    return data


def get_json_client(client: Clients) -> Dict[Any, Any]:
    try:
        groups = [{"group_id": value.id} for value in client.groups]
    except Exception:
        groups = []

    try:
        tribu = get_attr(propertie_data=client.assigned_centre, propertie="id")
    except Exception:
        tribu = None

    try:
        tribu = get_attr(propertie_data=client.assigned_centre, propertie="id")
    except Exception:
        tribu = None

    try:
        cc_id = get_attr(propertie_data=client.assigned_branch, propertie="id")
        cc_name = get_attr(propertie_data=client.assigned_branch, propertie="name")
    except Exception:
        cc_id = None
        cc_name = None

    try:
        usuario = get_attr(propertie_data=client.assigned_user, propertie="full_name")
    except Exception:
        usuario = None

    data = {
        "id": client.id,
        "encoded_key": client.encoded_key,
        "full_name": client.full_name,
        "first_name": client.first_name,
        "last_name": client.last_name,
        "home_phone": get_attr(propertie_data=client, propertie="home_phone"),
        "mobile_phone": get_attr(propertie_data=client, propertie="mobile_phone"),
        "email": client.email_address,
        "address": get_json_client_addresses(addresses=client.addresses),
        "curp": client.curp,
        "birth_date": client.birth_date,
        "gender": client.gender,
        "rfc": client.rfc,
        "status": client.state,
        "approved_date": client.approved_date,
        "activation_date": client.activation_date,
        "notes": client.notes,
        "economic_activity": client.actividad_economica_clients,
        "applicant_detailes": client.datossolicitante_integrante,
        "current_address_details": client.datosdomicilioactual_integrante,
        "profession": client.profesion_clients,
        "utility": client.utilidad_clients,
        "family_spending": client.gasto_familiar_clients,
        "income": client.ingresos_clients,
        "turn": client.giro_clients,
        "economic_dependents": client.dependientes_economicos_clients,
        "type_housing": client.tipo_de_vivienda_clients,
        "coordinator": client.full_name_ce,
        "loan_cycle": client.loan_cycle,
        "group_loan_cycle": client.group_loan_cycle,
        "full_addresses": client.full_addresses,
        "lessor_name": client.vivienda_nombre_arrendador,
        "lessor_phone": client.vivienda_telefono_arrendador,
        "marital_status": client.estado_civil_clients,
        "entity_birth": client.entidad_nacimiento,
        "education_level": client.nivel_educacion,
        "ine_validity": client.vigencia_ine_clients,
        "mobile_phone_2": client.mobile_phone_2,
        "seniority_at_home": client.antiguedad_en_domicilio,
        "reference_location": client.referencia_ubicacion,
        "family_name": client.familiar_mismo_domicilio_nombre,
        "family_phone": client.familiar_mismo_domicilio_phone,
        "family_parent": client.familiar_mismo_domicilio_parent,
        "between_streets_a": client.domicilio_entre_calle_a,
        "between_streets_b": client.domicilio_entre_calle_b,
        "another_income": client.otros_ingresos_clients,
        "experience": client.experiencia,
        "people_could_political_exposed": client.people_could_political_exposed,
        "source_resources": client.pld_origen_recursos,
        "origin_other_resources": client.fuente_otros_ingresos_client,
        "maximum_amount_to_pay": client.monto_max_pagar_client,
        "real_owner_resources": client.pld_es_propietario_recursos,
        "is_first_loan": client.primer_credito_client,
        "is_active_loans": client.otros_creditos_activos_client,
        "member_references": client.referencias_integrante,
        "business_address": client.direccion_del_negocio,
        "sale_days": client.dias_venta_client,
        "business_location": client.ubicacion_del_negocio,
        "tribu": tribu,
        "cc_id": cc_id,
        "cc_name": cc_name,
        "usuario": usuario,
        "groups": groups,
        "additional_activity": client.actividad_adicional_client,
    }

    return data


def get_json_client_addresses(addresses):
    data = []  # type: ignore
    if not addresses:
        return data

    for value in addresses:
        data.append(
            {
                "street": value.line_1,
                "colony": value.line_2,
                "municipality": value.city,
                "state": value.region,
                "postal_code": value.postcode,
                "country": value.country,
            }
        )

    return data


def get_json_loan(loan: Loans) -> Dict[Any, Any]:
    try:
        tribu = loan.tribu
    except Exception:
        tribu = None

    try:
        group = get_attr(propertie_data=loan.account_holder, propertie="id")
        group_name = get_attr(propertie_data=loan.account_holder, propertie="group_name")
    except Exception:
        group = None
        group_name = None

    data = {
        "id": loan.id,
        "encoded_key": loan.encoded_key,
        "status": loan.account_state,
        "approved_date": loan.approved_date,
        "product": loan.loan_name,
        "amount": loan.loan_amount,
        "payment_method": loan.payment_method,
        "coordinator": loan.full_name_ce,
        "accrued_interest": loan.accrued_interest,
        "interest_from_arrears_accrued": loan.interest_from_arrears_accrued,
        "disbursement_details": get_disbursement_details(
            disbursement_details=loan.disbursement_details
        ),
        "operational_authorization": loan.autorizacionoperativa_loan,
        "risk_control": loan.controlderiesgo_loan,
        "anchorer": loan.fondeador,
        "cycle": loan.ciclo,
        "payday": loan.dia_de_pago_loan_accounts,
        "first_meeting_date": loan.fecha_de_la_primer_reunion_loan,
        "number_members": loan.num_de_miembros_loan_accounts,
        "number_disbursements": loan.numero_desembolsos,
        "number_already_disbursed": loan.numero_ya_desembolsado,
        "community_center": loan.community_center,
        "tribu": tribu,
        "group": group,
        "group_name": group_name,
        "creation_date": loan.creation_date,
    }

    return data


def get_disbursement_details(disbursement_details):

    if not disbursement_details:
        return {}

    data = {
        "expected_disbursement_date": disbursement_details.expected_disbursement_date,
        "disbursement_date": disbursement_details.disbursement_date,
        "first_payment_date": disbursement_details.first_repayment_date,
        "payment_method": disbursement_details.transaction_details[
            "transactionChannelId"
        ],
    }
    return data


def get_attr(propertie_data, propertie):
    if not propertie_data:
        return ""

    attr = getattr(propertie_data, propertie, "")
    if not attr:
        return ""

    return attr
