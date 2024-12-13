from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    func,
)
from sqlalchemy.orm import registry, relationship

from src.cdc.domain import models

mapper_registry = registry()
metadata = MetaData()


person = Table(
    "personas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(50)),
    Column("apellido_paterno", String(50)),
    Column("apellido_materno", String(50)),
    Column("fecha_nacimiento", Date),
    Column("curp", String(18), nullable=True),
    Column("rfc", String(13)),
    Column("nacionalidad", String(2), nullable=True),
    Column("direccion", String(256)),
    Column("colonia", String(64)),
    Column("delegacion", String(64)),
    Column("ciudad", String(64)),
    Column("estado", String(64)),
    Column("codigo_postal", String(5)),
    Column("grupo_id", ForeignKey("grupo.grupo_id"), nullable=True),
    Column("es_referida", Boolean(), nullable=True),
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

query_status = Table(
    "status_consulta_cdc",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("status", String(25), nullable=False),
    Column("id_status", Integer, unique=True, nullable=False),
)

query_cdc = Table(
    "consultas_cdc",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("persona_id", ForeignKey("personas.id")),
    Column("estatus_consulta_id", ForeignKey("status_consulta_cdc.id")),
    Column("folio", String(25)),
    Column("nip", String(25)),
    Column("folio_cdc_consulta", String(10)),
    Column("timestamp_consulta", DateTime),
    Column("timestamp_aprobacion_consulta", DateTime),
    Column("timestamp_aprobacion_tyc", DateTime),
    Column("tipo_consulta", String(2)),
    Column("username", String(50)),
    Column("fallo_regla", String(100)),
    Column("centro_comunitario", String(50), nullable=True),
    Column("archivo_xml", String(512)),
    Column("usuario_cdc", String(15)),
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


# V2
prospecto = Table(
    "cliente",
    metadata,
    Column("cliente_id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String(50), nullable=False),
    Column("middle_name", String(50)),
    Column("first_surname", String(50), nullable=False),
    Column("second_surname", String(50)),
    Column("curp", String(18), unique=True, nullable=False),
    Column("birth_date", Date, nullable=False),
    Column("nationality", String(2)),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)

direccion_prospecto = Table(
    "direccion",
    metadata,
    Column("direccion_id", Integer, primary_key=True, autoincrement=True),
    Column("cliente_id", ForeignKey("cliente.cliente_id")),
    # Column("colonia_id", ForeignKey("cliente.cliente_id")),
    Column("street_name", String(256), nullable=False),
    Column("street_number", String(256), nullable=False),
    Column("indoor_number", String(256)),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)

tipo_contacto = Table(
    "tipo_contacto",
    metadata,
    Column("tipo_contacto_id", Integer, primary_key=True, autoincrement=True),
    Column("cliente_id", ForeignKey("cliente.cliente_id")),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)

dato_contacto = Table(
    "dato_contacto",
    metadata,
    Column("dato_contacto_id", Integer, primary_key=True, autoincrement=True),
    Column(
        "tipo_contacto_id", ForeignKey("tipo_contacto.tipo_contacto_id"), nullable=False
    ),
    Column("cliente_id", ForeignKey("cliente.cliente_id"), nullable=False),
    Column("contact_data", String(128), nullable=False),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)

usuario = Table(
    "usuario",
    metadata,
    Column("usuario_id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(64), unique=True, nullable=False),
    Column("first_name", String(50), nullable=False),
    Column("middle_name", String(50)),
    Column("first_surname", String(50), nullable=False),
    Column("second_surname", String(50)),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)

centro_comunitario = Table(
    "centro_comunitario",
    metadata,
    Column("centro_comunitario_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(64), nullable=False),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)

nip_table = Table(
    "nip_cdc",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nip", String(25), nullable=False),
    Column("curp", String(18), nullable=False),
    Column("fecha", Date, nullable=False),
    Column("vigente", Integer, nullable=False, default=1),
    Column("validado", Integer, nullable=False, default=0),
    Column("num_consultas", Integer, nullable=False, default=0),
)


consulta_cdc = Table(
    "consulta_cdc",
    metadata,
    Column("consulta_cdc_id", Integer, primary_key=True, autoincrement=True),
    Column("cliente_id", ForeignKey("cliente.cliente_id"), nullable=False),
    Column("direccion_id", ForeignKey("direccion.direccion_id"), nullable=False),
    Column("status_consulta_id", ForeignKey("status_consulta_cdc.id"), nullable=False),
    Column(
        "centro_comunitario_id", ForeignKey("centro_comunitario.centro_comunitario_id")
    ),
    Column("usuario_id", ForeignKey("usuario.usuario_id"), nullable=False),
    Column("nip_id", Integer, ForeignKey("nip_cdc.id")),
    Column("cdc_folio", String(10)),
    Column("pp_folio", String(25)),
    Column("consulta_timestamp", DateTime),
    Column("consulta_apr_timestamp", DateTime),
    Column("consulta_tyc_timestamp", DateTime),
    Column("consulta_cdc_tipo", String(2)),
    Column("consulta_cdc_usuario", String(15)),
    Column("pp_rule_failure_reason", String(100)),
    Column("pp_referred_client", Boolean()),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)

grupo = Table(
    "grupo",
    metadata,
    Column("grupo_id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(64)),
    Column("mambu_id", String(50), unique=True, nullable=False),
    Column("usuario_id", ForeignKey("usuario.usuario_id"), nullable=False),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)


def start_mappers():

    mapper_registry.map_imperatively(
        models.QueryCdc,
        query_cdc,
        properties={
            "_query_status": relationship(models.QueryStatus),
        },
    )

    mapper_registry.map_imperatively(
        models.Person,
        person,
        properties={
            "_query_cdc": relationship(models.QueryCdc),
            "_grupo": relationship(models.Grupo),
        },
    )
    mapper_registry.map_imperatively(models.QueryStatus, query_status)

    # V2
    mapper_registry.map_imperatively(
        models.Usuario,
        usuario,
        properties={
            "usuario_id": usuario.c.usuario_id,
        },
    )
    mapper_registry.map_imperatively(models.Nip, nip_table)
    mapper_registry.map_imperatively(models.StatusConsultaCdC, query_status)
    mapper_registry.map_imperatively(models.CentroComunitario, centro_comunitario)
    mapper_registry.map_imperatively(models.Grupo, grupo)
    mapper_registry.map_imperatively(
        models.Prospecto,
        prospecto,
        properties={
            "nombre": prospecto.c.first_name,
            "segundo_nombre": prospecto.c.middle_name,
            "apellido_paterno": prospecto.c.first_surname,
            "apellido_materno": prospecto.c.second_surname,
            "fecha_nacimiento": prospecto.c.birth_date,
            "nacionalidad": prospecto.c.nationality,
            "_consultas": relationship(models.ConsultaCdc),
            "_direcciones": relationship(models.DireccionProspecto),
        },
    )
    mapper_registry.map_imperatively(
        models.DireccionProspecto,
        direccion_prospecto,
        properties={
            "calle": direccion_prospecto.c.street_name,
            "numero_exterior": direccion_prospecto.c.street_number,
            "numero_interior": direccion_prospecto.c.indoor_number,
        },
    )
    mapper_registry.map_imperatively(
        models.ConsultaCdc,
        consulta_cdc,
        properties={
            "folio": consulta_cdc.c.pp_folio,
            "fallo_regla": consulta_cdc.c.pp_rule_failure_reason,
            "es_referido": consulta_cdc.c.pp_referred_client,
            "_prospecto": relationship(models.Prospecto, uselist=False, viewonly=True),
            "_direccion": relationship(models.DireccionProspecto),
            "_nip": relationship(models.Nip),
            "_estatus": relationship(models.StatusConsultaCdC),
            "_usuario": relationship(models.Usuario),
            "_centro_comunitario": relationship(models.CentroComunitario),
        },
    )
