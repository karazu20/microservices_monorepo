import logging

from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api

from setup.resources import PodemosResource
from src.validations import broker
from src.validations.config import DOCS_PATH_VALIDATIONS
from src.validations.domain import commands, queries
from src.validations.entrypoints import routers
from src.validations.services_layer.handlers import ValidationException

logger = logging.getLogger(__name__)


class StageResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetStage.Schema().load(request.args)  # type: ignore
            logger.info("GetStage: query %s", qry)
            stage = broker.handle(qry)
            return stage, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_stage.yml")
    def post(self):
        try:
            cmd = commands.ADDStage.Schema().load(request.json)  # type: ignore
            logger.info("ADDStage Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class RuleResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetRule.Schema().load(request.args)  # type: ignore
            logger.info("GetRule: query %s", qry)
            rule = broker.handle(qry)
            return rule, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_rule.yml")
    def post(self):
        try:
            cmd = commands.ADDRule.Schema().load(request.json)  # type: ignore
            logger.info("ADDRule Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class RuleExecutionStatusResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetRuleExecutionStatus.Schema().load(request.args)  # type: ignore
            logger.info("GetRuleExecutionStatus: query %s", qry)
            rule_exe = broker.handle(qry)
            return rule_exe, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_rule_execution_status.yml")
    def post(self):
        try:
            cmd = commands.ADDRuleExecutionStatus.Schema().load(request.json)  # type: ignore
            logger.info("ADDRuleExecutionStatus Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class RuleExceptionTypeResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetRuleExceptionType.Schema().load(request.args)  # type: ignore
            logger.info("GetRuleExceptionType: query %s", qry)
            rule_exc = broker.handle(qry)
            return rule_exc, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_rule_exception_type.yml")
    def post(self):
        try:
            cmd = commands.ADDRuleExceptionType.Schema().load(request.json)  # type: ignore
            logger.info("ADDRuleExceptionType Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class RuleExecutionResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetRuleExecution.Schema().load(request.args)  # type: ignore
            logger.info("GetRuleExecution: query %s", qry)
            rule_exec = broker.handle(qry)
            return rule_exec, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_rule_execution.yml")
    def post(self):
        try:
            cmd = commands.ADDRuleExecution.Schema().load(request.json)  # type: ignore
            logger.info("ADDRuleExecution Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class RuleExceptionResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetRuleException.Schema().load(request.args)  # type: ignore
            logger.info("GetRuleException: query %s", qry)
            rule_exec = broker.handle(qry)
            return rule_exec, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_rule_exception.yml")
    def post(self):
        try:
            cmd = commands.ADDRuleException.Schema().load(request.json)  # type: ignore
            logger.info("ADDRuleException Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class RoleResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetRole.Schema().load(request.args)  # type: ignore
            logger.info("GetRole: query %s", qry)
            rule_exec = broker.handle(qry)
            return rule_exec, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_role.yml")
    def post(self):
        try:
            cmd = commands.ADDRole.Schema().load(request.json)  # type: ignore
            logger.info("ADDRole Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class RoleRuleResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetRoleRule.Schema().load(request.args)  # type: ignore
            logger.info("GetRoleRule: query %s", qry)
            rule_exec = broker.handle(qry)
            return rule_exec, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_role_rule.yml")
    def post(self):
        try:
            cmd = commands.ADDRoleRule.Schema().load(request.json)  # type: ignore
            logger.info("ADDRoleRule Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class ExecuteValidationsResource(PodemosResource):
    @swag_from(f"{DOCS_PATH_VALIDATIONS}/execute_validations.yml")
    def post(self):
        try:
            response = []
            for value in request.json:  # type: ignore
                cmd = commands.ADDExcValidation.Schema().load(value)  # type: ignore
                logger.info("ADDExcValidation Resource: command %s", cmd)
                response.append(broker.handle(cmd))
            return {"code": 200, "data": response, "msg": "Success"}, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class ExecuteValidationsCDCResource(PodemosResource):
    @swag_from(f"{DOCS_PATH_VALIDATIONS}/execute_validations_cdc.yml")
    def post(self):
        try:
            cmd = commands.ADDExcValidationCDC.Schema().load(request.json)  # type: ignore
            logger.info("ADDExcValidationCDC Resource: command %s", cmd)
            response = broker.handle(cmd)
            return {"code": "VAL200", "data": response, "msg": "success"}, 200
        except ValidationException as ve:
            return {
                "code": "VAL406",
                "error": ve.args[0],
                "msg": "fail",
            }, 406

        except Exception as e:  # pragma: no cover
            return {"code": "VAL500", "error": {"msg_error": str(e)}, "msg": "fail"}, 500


class FieldValidationResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetFieldValidation.Schema().load(request.args)  # type: ignore
            logger.info("GetFieldValidation: query %s", qry)
            rule_exec = broker.handle(qry)
            return rule_exec, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_field_validation.yml")
    def post(self):
        try:
            cmd = commands.ADDFieldValidation.Schema().load(request.json)  # type: ignore
            logger.info("ADDFieldValidation Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201

        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class CustomRuleSetResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetCustomRuleSet.Schema().load(request.args)  # type: ignore
            logger.info("GetCustomRuleSet: query %s", qry)
            rule_exec = broker.handle(qry)
            return rule_exec, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_custom_rule.yml")
    def post(self):
        try:
            cmd = commands.ADDCustomRule.Schema().load(request.json)  # type: ignore
            logger.info("ADDCustomRule Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class ValidationDataIdentifierResource(PodemosResource):
    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_validation_data_identifier.yml")
    def post(self):
        try:
            cmd = commands.ADDValidationDataIdentifier.Schema().load(request.json)  # type: ignore
            logger.info("ADDValidationDataIdentifier Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class ValidationDataResource(PodemosResource):
    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_validation_data.yml")
    def post(self):
        try:
            cmd = commands.ADDValidationData.Schema().load(request.json)  # type: ignore
            logger.info("ADDValidationData Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class ValidationRuleDataResource(PodemosResource):
    @swag_from(f"{DOCS_PATH_VALIDATIONS}/create_validation_data_identifier.yml")
    def post(self):
        try:
            cmd = commands.ADDValidationRuleData.Schema().load(request.json)  # type: ignore
            logger.info("ADDValidationRuleData Resource: command %s", cmd)
            broker.handle(cmd)
            return "OK", 201
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


validations_blueprint = Blueprint("validations", __name__, url_prefix="/validations")


validations_api = Api(validations_blueprint)

validations_api.add_resource(routers.StageResource, "/stage")
validations_api.add_resource(routers.RuleResource, "/rule")
validations_api.add_resource(
    routers.RuleExecutionStatusResource, "/rule_execution_status"
)
validations_api.add_resource(routers.RuleExceptionTypeResource, "/rule_exception_type")
validations_api.add_resource(routers.RuleExecutionResource, "/rule_execution")
validations_api.add_resource(routers.RuleExceptionResource, "/rule_exception")
validations_api.add_resource(routers.RoleResource, "/role")
validations_api.add_resource(routers.RoleRuleResource, "/role_rule")
validations_api.add_resource(routers.ExecuteValidationsResource, "/execute_validations")
validations_api.add_resource(
    routers.ExecuteValidationsCDCResource, "/execute_validations_cdc"
)
validations_api.add_resource(routers.FieldValidationResource, "/field_validation")
validations_api.add_resource(routers.CustomRuleSetResource, "/custom_rule_set")
validations_api.add_resource(
    routers.ValidationDataIdentifierResource, "/validation_data_identifier"
)
validations_api.add_resource(routers.ValidationDataResource, "/validation_data")
validations_api.add_resource(routers.ValidationRuleDataResource, "/validation_rule_data")
