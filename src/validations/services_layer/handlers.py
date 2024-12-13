from datetime import datetime, timedelta

from setup import domain  # type: ignore
from setup.adapters import podemos_mambu
from src.validations.domain import commands, models, queries
from src.validations.services_layer import unit_of_work
from src.validations.utils.validations_rules import ValidationsRules  # type: ignore

from typing import Callable, Dict, Type  # isort:skip


class ValidationException(Exception):
    """Excepcion Validations"""


def add_stage(
    command: commands.ADDStage,
    uow: unit_of_work.UnitOfWorkValidations,
) -> None:
    with uow:
        stage = models.Stage(command.etapa)
        uow.stage.add(stage)
        uow.commit()


def add_rule(
    command: commands.ADDRule,
    uow: unit_of_work.UnitOfWorkValidations,
) -> None:
    with uow:
        rule = models.Rule(command.regla, command.cantidad)
        uow.rule.add(rule)
        uow.commit()


def add_rule_execution_status(
    command: commands.ADDRuleExecutionStatus,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        rule_execution_status = models.RuleExecutionStatus(command.estatus)
        uow.rule_execution_status.add(rule_execution_status)
        uow.commit()


def add_rule_execution(
    command: commands.ADDRuleExecution,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        rule_execution = models.RuleExecution()
        rule_execution.etapa_id = command.etapa_id
        rule_execution.regla_id = command.regla_id
        rule_execution.estatus_ejecucion_regla_id = command.estatus_ejecucion_regla_id
        uow.rule_execution.add(rule_execution)
        uow.commit()


def add_rule_exception_type(
    command: commands.ADDRuleExceptionType,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        rule_exception_type = models.RuleExceptionType(command.tipo)
        uow.rule_exception_type.add(rule_exception_type)
        uow.commit()


def add_rule_exception(
    command: commands.ADDRuleException,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        rule_exception = models.RuleException()
        rule_exception.tipo_excepcion_regla_id = command.tipo_excepcion_regla_id
        rule_exception.id_mambu = command.id_mambu
        rule_exception.regla_id = command.regla_id

        uow.rule_exception.add(rule_exception)
        uow.commit()


def add_role(
    command: commands.ADDRole,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        role = models.Role(command.rol)
        uow.role.add(role)
        uow.commit()


def add_role_rule(
    command: commands.ADDRoleRule,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        role_rule = models.RoleRule()
        role_rule.regla_id = command.regla_id
        role_rule.rol_id = command.rol_id
        uow.role_rule.add(role_rule)
        uow.commit()


def add_custom_rule_set(
    command: commands.ADDCustomRule,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        custom_rule_set = models.CustomRuleSet(
            id_object_mambu=command.id_object_mambu,
            tipo=command.tipo,
        )

        custom_rule_set.regla_id = command.regla_id
        custom_rule_set.etapa_id = command.etapa_id
        custom_rule_set.estatus_ejecucion_regla_personalizada_id = command.estatus_ejecucion_regla_id  # type: ignore
        uow.custom_rule.add(custom_rule_set)
        uow.commit()


def execute_validation(
    command: commands.ADDExcValidation,
    uow: unit_of_work.UnitOfWorkValidations,
    mambu: podemos_mambu.PodemosMambu,
):
    with uow:
        messages = []
        mambu_client = None
        mambu_loan = None
        mambu_group = None
        status = True
        try:

            if command.tipo == models.RuleExceptionType.CREDITO:
                mambu_loan = mambu.loans.get(
                    id=command.id_mambu,
                )
                mambu_group = mambu_loan.account_holder
                mambu_clients = []
                for value in mambu_group.group_members:
                    mambu_clients.append(mambu.clients.get(id=value.client_key))
            elif command.tipo == models.RuleExceptionType.INTEGRANTE:
                mambu_client = mambu.clients.get(
                    id=command.id_mambu,
                )
                mambu_group = mambu_client.group
                mambu_clients = [mambu_client]  # type: ignore
            elif command.tipo == models.RuleExceptionType.GRUPO:
                mambu_group = mambu.groups.get(id=command.id_mambu)
                mambu_clients = [mambu_group.members]
        except Exception:
            status = False
            messages.append(
                {"error": "Error al obtener el ID en Mambu " + command.id_mambu}
            )
            return {
                "id_mambu": command.id_mambu,
                "status": status,
                "messages": messages,
            }

        rule = uow.view_execution_rules.search(command)  # type: ignore

        mambu_products = mambu.products.search([("state", "=", "ACTIVE")])
        for value in rule:
            field_validations = uow.field_validation._get_field_validation_rules(
                rule_id=value[2]
            )
            rule_data_validation = (
                uow.validation_rule_data._get_field_validation_rule_data(rule_id=value[2])
            )
            exec_method = getattr(
                ValidationsRules(
                    type_validation="PCP",
                    clients=mambu_clients,
                    group=mambu_group,
                    loan=mambu_loan,
                    quantity=value[1],
                    field_validations=field_validations,
                    rule_data_validation=rule_data_validation,
                    products=mambu_products,
                ),
                value[0],
            )
            response = exec_method()
            if "data_response" in response:
                for value in response["data_response"]:
                    status = False
                    messages.append(value)  # type: ignore
            elif not response["status"]:
                status = False
                messages.append({"error": response["message"]})  # type: ignore
        uow.commit()
        return {
            "id_mambu": command.id_mambu,
            "status": status,
            "messages": messages,
        }


def execute_validation_cdc(
    command: commands.ADDExcValidationCDC,
    uow: unit_of_work.UnitOfWorkValidations,
    mambu: podemos_mambu.PodemosMambu,
):
    with uow:
        message = None
        mambu_client = None
        status = True
        validate_data = None
        mambu_client = mambu.clients.search_by_curp(command.curp)
        command.id = mambu_client[0].id if mambu_client else ""
        command.state = mambu_client[0].state if mambu_client else ""
        mambu_clients = [
            models.InitClient(
                command.id,
                command.curp,
                command.first_name,
                command.last_name,
                command.middle_name,
                command.birth_date,
                command.state,
            )
        ]

        command.tipo = models.RuleExceptionType.INTEGRANTE
        command.etapa = models.Stage.CONSULTA_CDC
        command.id_mambu = ""
        rule = uow.view_execution_rules.search(command)  # type: ignore

        for value in rule:
            rule_data_validation = (
                uow.validation_rule_data._get_field_validation_rule_data(rule_id=value[2])
            )
            if value[0] == "validate_consult_cdc":
                fecha_inicial = datetime.today().date() - timedelta(days=value[1])
                validate_data = uow.validation_cdc._get_consult(
                    command.curp, fecha_inicial, datetime.now()
                )

            exec_method = getattr(
                ValidationsRules(
                    clients=mambu_clients,
                    quantity=value[1],
                    rule_data_validation=rule_data_validation,
                    validate_data=validate_data,
                ),
                value[0],
            )
            response = exec_method()
            if response["status"]:
                status = True
                message = response["message"]  # type: ignore
            else:  # pragma: no cover
                response["msg_error"] = response.pop("message")
                raise ValidationException(response)

        uow.commit()
        return {"status": status, "message": message, "msg_success": message}


def get_stage(
    query: queries.GetStage,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        stages = uow.stage.list()
        return [
            {
                "id": stg.id,
                "etapa": stg.etapa,
            }
            for stg in stages
        ]


def get_rule(
    query: queries.GetRule,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        rules = uow.rule.list()
        return [
            {
                "id": rule.id,
                "regla": rule.regla,
            }
            for rule in rules
        ]


def get_rule_execution_status(
    query: queries.GetRuleExecutionStatus,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        rule_execution_status = uow.rule_execution_status.list()
        return [
            {
                "id": rule_exc.id,
                "estatus": rule_exc.estatus,
            }
            for rule_exc in rule_execution_status
        ]


def get_rule_exception_type(
    query: queries.GetRuleExceptionType,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        rule_exception_type = uow.rule_exception_type.list()
        return [
            {
                "id": rule_exc.id,
                "tipo": rule_exc.tipo,
            }
            for rule_exc in rule_exception_type
        ]


def get_rule_execution(
    query: queries.GetRuleExecution,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        rule_execution = uow.rule_execution.list(query.estatus, query.etapa)

        return [
            {
                "id": rule_exc[0],
                "regla": rule_exc[1],
                "estatus": rule_exc[2],
                "etapa": rule_exc[3],
            }
            for rule_exc in rule_execution
        ]


def get_rule_exception(
    query: queries.GetRuleException,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        rule_exception = uow.rule_exception.list(query.id_mambu)

        return [
            {
                "id": rule_exc[0],
                "id_mambu": rule_exc[1],
                "regla": rule_exc[2],
                "tipo_excepcion": rule_exc[3],
                "regla_id": rule_exc[4],
            }
            for rule_exc in rule_exception
        ]


def get_role(
    query: queries.GetRole,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        role = uow.role.list()
        return [
            {
                "id": rol.id,
                "rol": rol.rol,
            }
            for rol in role
        ]


def get_role_rule(
    query: queries.GetRoleRule,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        role_rule = uow.role_rule.list()
        return [
            {
                "id": rol.id,
                "rol_id": rol.rol_id,
                "regla_id": rol.regla_id,
            }
            for rol in role_rule
        ]


def add_field_validation(
    command: commands.ADDFieldValidation,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        field_validation = models.FieldValidation()

        field_validation.regla_id = command.regla_id
        field_validation.campo = command.campo
        field_validation.requerido = command.requerido

        uow.field_validation.add(field_validation)
        uow.commit()


def get_field_validation(
    query: queries.GetFieldValidation,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        field_validation = uow.field_validation.list()
        return [
            {
                "id": rol.id,
                "regla_id": rol.regla_id,
                "campo": rol.campo,
                "requerido": rol.requerido,
            }
            for rol in field_validation
        ]


def get_custom_rule_set(
    query: queries.GetCustomRuleSet,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        if query.id:
            custom_rule_set = uow.custom_rule.get(query.id)
        else:
            custom_rule_set = uow.custom_rule.list()

        return [
            {
                "id": custom_rule.id,
                "regla_id": custom_rule.regla_id,
                "id_object_mambu": custom_rule.id_object_mambu,
                "tipo": custom_rule.tipo,
                "etapa_id": custom_rule.etapa_id,
                "estatus_ejecucion": custom_rule.estatus_ejecucion_regla_personalizada_id,  # type: ignore
            }
            for custom_rule in custom_rule_set
        ]


def add_validation_data_identifier(
    command: commands.ADDValidationDataIdentifier,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        validation_data_identifier = models.ValidationDataIdentifier(
            command.identificador,
            command.descripcion,
        )
        uow.validation_data_identifier.add(validation_data_identifier)
        uow.commit()


def add_validation_data(
    command: commands.ADDValidationData,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        validation_data = models.ValidationData()
        validation_data.identificador_dato_validacion_id = (
            command.identificador_dato_validacion_id
        )
        validation_data.llave = command.llave  # type: ignore
        validation_data.valor = command.valor
        validation_data.tipo_dato = command.tipo_dato
        uow.validation_data.add(validation_data)
        uow.commit()


def add_validation_rule_data(
    command: commands.ADDValidationRuleData,
    uow: unit_of_work.UnitOfWorkValidations,
):
    with uow:
        validation_rule_data = models.ValidationRuleData()
        validation_rule_data.identificador_dato_validacion_id = (
            command.identificador_dato_validacion_id
        )
        validation_rule_data.regla_id = command.regla_id
        uow.validation_rule_data.add(validation_rule_data)
        uow.commit()


QUERY_HANDLERS = {
    queries.GetStage: get_stage,
    queries.GetRule: get_rule,
    queries.GetRuleExecutionStatus: get_rule_execution_status,
    queries.GetRuleExceptionType: get_rule_exception_type,
    queries.GetRuleExecution: get_rule_execution,
    queries.GetRuleException: get_rule_exception,
    queries.GetRole: get_role,
    queries.GetRoleRule: get_role_rule,
    queries.GetFieldValidation: get_field_validation,
    queries.GetCustomRuleSet: get_custom_rule_set,
}  # type: Dict[Type[domain.Query], Callable]


COMMAND_HANDLERS = {
    commands.ADDStage: add_stage,
    commands.ADDRule: add_rule,
    commands.ADDRuleExecutionStatus: add_rule_execution_status,
    commands.ADDRuleExceptionType: add_rule_exception_type,
    commands.ADDRuleException: add_rule_exception,
    commands.ADDRuleExecution: add_rule_execution,
    commands.ADDRole: add_role,
    commands.ADDRoleRule: add_role_rule,
    commands.ADDFieldValidation: add_field_validation,
    commands.ADDCustomRule: add_custom_rule_set,
    commands.ADDExcValidation: execute_validation,
    commands.ADDExcValidationCDC: execute_validation_cdc,
    commands.ADDValidationDataIdentifier: add_validation_data_identifier,
    commands.ADDValidationData: add_validation_data,
    commands.ADDValidationRuleData: add_validation_rule_data,
}  # type: Dict[Type[domain.Command], Callable]


EVENT_HANDLERS = {}  # type: ignore
