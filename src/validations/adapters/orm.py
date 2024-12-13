from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    func,
)
from sqlalchemy.orm import registry, relationship

from src.validations.domain import models

mapper_registry = registry()
metadata = MetaData()


MAMBU_OBJECTS_TYPES = (
    "CREDITO",
    "INTEGRANTE",
    "GRUPO",
    "CENTRO_COMUNITARIO",
    "TRIBU",
)

stage = Table(
    "etapas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "etapa",
        Enum(
            *(
                "PENDIENTE DE APROBACION",
                "APROBADO",
                "DESEMBOLSO",
                "ACTIVO",
                "CONSULTA CDC",
            ),
            name="enum_etapas_etapa"
        ),
    ),
)

rule = Table(
    "reglas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("regla", String(256)),
    Column("cantidad", Integer, nullable=True),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se creo el registro",
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
)

rule_execution_status = Table(
    "estatus_ejecucion_reglas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "estatus",
        Enum(*("ACTIVO", "INACTIVO"), name="enum_estatus_ejecucion_reglas_estatus"),
    ),
)

rule_execution = Table(
    "ejecucion_reglas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("etapa_id", ForeignKey("etapas.id"), nullable=False),
    Column("regla_id", ForeignKey("reglas.id"), nullable=False),
    Column(
        "estatus_ejecucion_regla_id",
        ForeignKey("estatus_ejecucion_reglas.id"),
        nullable=False,
    ),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se creo el registro",
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
)

rule_exception_type = Table(
    "tipo_excepcion_reglas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "tipo",
        Enum(*MAMBU_OBJECTS_TYPES, name="enum_reglas_personalizadas_tipo"),
    ),
)

rule_exception = Table(
    "excepcion_reglas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("regla_id", ForeignKey("reglas.id"), nullable=False),
    Column(
        "tipo_excepcion_regla_id", ForeignKey("tipo_excepcion_reglas.id"), nullable=False
    ),
    Column("id_mambu", String(10)),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se creo el registro",
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
)

rule_execution_log = Table(
    "log_ejecucion_reglas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("ejecucion_regla_id", ForeignKey("ejecucion_reglas.id"), nullable=False),
    Column("id_mambu", String(10)),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se creo el registro",
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
)

role = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("rol", String(64)),
)

role_rule = Table(
    "reglas_rol",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("regla_id", ForeignKey("reglas.id"), nullable=False),
    Column("rol_id", ForeignKey("roles.id"), nullable=False),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se creo el registro",
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
)

field_validation = Table(
    "validacion_campos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("regla_id", ForeignKey("reglas.id"), nullable=False),
    Column("campo", String(256)),
    Column("requerido", Boolean, nullable=True),
)

custom_rule = Table(
    "reglas_personalizadas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("regla_id", ForeignKey("reglas.id"), nullable=False),
    Column("id_object_mambu", String(128)),
    Column("tipo", Enum(*MAMBU_OBJECTS_TYPES, name="enum_reglas_personalizadas_tipo")),
    Column("etapa_id", ForeignKey("etapas.id"), nullable=False),
    Column(
        "estatus_ejecucion_regla_personalizada_id",
        ForeignKey("estatus_ejecucion_reglas.id"),
        nullable=False,
    ),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se creo el registro",
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
)


validation_data_identifier = Table(
    "identificador_datos_validaciones",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("identificador", String(128)),
    Column("descripcion", String(256)),
)


validation_data = Table(
    "datos_validaciones",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "identificador_dato_validacion_id",
        ForeignKey("identificador_datos_validaciones.id"),
        nullable=False,
    ),
    Column("llave", String(128), nullable=True),
    Column("valor", String(128)),
    Column(
        "tipo_dato",
        Enum(*("float", "str", "int"), name="enum_datos_validaciones_tipo_dato"),
    ),
)


validation_rule_data = Table(
    "datos_regla_validacion",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("regla_id", ForeignKey("reglas.id"), nullable=False),
    Column(
        "identificador_dato_validacion_id",
        ForeignKey("identificador_datos_validaciones.id"),
        nullable=False,
    ),
)


def start_mappers():
    mapper_registry.map_imperatively(models.Stage, stage)
    mapper_registry.map_imperatively(models.Rule, rule)
    mapper_registry.map_imperatively(models.RuleExecutionStatus, rule_execution_status)
    mapper_registry.map_imperatively(models.Role, role)
    mapper_registry.map_imperatively(models.RuleExceptionType, rule_exception_type)
    mapper_registry.map_imperatively(
        models.ValidationDataIdentifier, validation_data_identifier
    )

    mapper_registry.map_imperatively(
        models.RuleExecution,
        rule_execution,
        properties={
            "_rule": relationship(models.Rule),
            "_stage": relationship(models.Stage),
            "_rule_execution_status": relationship(models.RuleExecutionStatus),
        },
    )

    mapper_registry.map_imperatively(
        models.RuleException,
        rule_exception,
        properties={
            "_rule": relationship(models.Rule),
            "_rule_exception_type": relationship(models.RuleExceptionType),
        },
    )

    mapper_registry.map_imperatively(
        models.RuleExecutionLog,
        rule_execution_log,
        properties={
            "_rule_execution": relationship(models.RuleExecution),
        },
    )

    mapper_registry.map_imperatively(
        models.RoleRule,
        role_rule,
        properties={
            "_role": relationship(models.Role),
            "_rule": relationship(models.Rule),
        },
    )

    mapper_registry.map_imperatively(
        models.FieldValidation,
        field_validation,
        properties={
            "_rule": relationship(models.Rule),
        },
    )

    mapper_registry.map_imperatively(
        models.CustomRuleSet,
        custom_rule,
        properties={
            "_rule": relationship(models.Rule),
            "_stage": relationship(models.Stage),
            "_custom_rule_execution_status": relationship(
                models.RuleExecutionStatus,
            ),
        },
    )

    mapper_registry.map_imperatively(
        models.ValidationData,
        validation_data,
        properties={
            "_validation_data_identifier": relationship(models.ValidationDataIdentifier),
        },
    )

    mapper_registry.map_imperatively(
        models.ValidationRuleData,
        validation_rule_data,
        properties={
            "_rule": relationship(models.Rule),
            "_validation_data_identifier": relationship(models.ValidationDataIdentifier),
        },
    )
