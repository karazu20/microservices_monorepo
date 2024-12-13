from typing import Optional, Tuple

from sqlalchemy import func

from setup.adapters.data import SQLView
from src.validations.domain import commands
from src.validations.domain.models import (
    CustomRuleSet,
    Rule,
    RuleException,
    RuleExecution,
    RuleExecutionStatus,
    Stage,
)


class ExecutionRulesView(SQLView):
    def _search(
        self,
        command: commands.ADDExcValidation,
    ) -> Optional[list]:
        sub_query = (
            self.session.query(RuleException.regla_id)
            .filter(RuleException.id_mambu == command.id_mambu)
            .subquery()
        )

        return (
            self.session.query(Rule.regla, Rule.cantidad, Rule.id)
            .join(RuleExecution, RuleExecution.regla_id == Rule.id)
            .join(Stage, RuleExecution.etapa_id == Stage.id)
            .join(
                RuleExecutionStatus,
                RuleExecution.estatus_ejecucion_regla_id == RuleExecutionStatus.id,
            )
            .filter(Stage.etapa == command.etapa)
            .filter(RuleExecutionStatus.estatus == "ACTIVO")
            .filter(Rule.id.not_in(sub_query))  # type: ignore
            .all()
        )


class CustomRuleMambuObjectsView(SQLView):
    def _search(self, command: commands.ADDExcValidation) -> Optional[Tuple]:
        return (
            self.session.query(Rule.regla, Rule.cantidad, Rule.id)  # pragma: no cover
            .join(CustomRuleSet, CustomRuleSet.regla_id == Rule.id)
            .join(Stage, CustomRuleSet.etapa_id == Stage.id)
            .join(
                RuleExecutionStatus,
                CustomRuleSet.estatus_ejecucion_regla_personalizada_id
                == RuleExecutionStatus.id,
            )
            .filter(Stage.etapa == command.etapa)
            .filter(RuleExecutionStatus.estatus == "ACTIVO")
            .filter(CustomRuleSet.id_object_mambu == command.id_mambu)
            .all()
        )

    def mambu_object_has_custom_rules(
        self,
        command: commands.ADDExcValidation,
    ) -> bool:
        result = (
            self.session.query(func.count(CustomRuleSet.id))
            .join(Stage, CustomRuleSet.etapa_id == Stage.id)
            .join(
                RuleExecutionStatus,
                CustomRuleSet.estatus_ejecucion_regla_personalizada_id
                == RuleExecutionStatus.id,
            )
            .filter(Stage.etapa == command.etapa)
            .filter(RuleExecutionStatus.estatus == "ACTIVO")
            .filter(CustomRuleSet.id_object_mambu == command.id_mambu)
            .first()
        )

        return result[0] > 0
