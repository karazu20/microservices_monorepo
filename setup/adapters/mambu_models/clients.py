from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from mambupy.api.mambuclient import MambuClient
from mambupy.orm.schema_mambu import Client as ORMClient

from setup.adapters.mambu_models.model import EntityMambu, Mode

if TYPE_CHECKING:
    from setup.adapters.mambu_models import (
        Addresses,
        Branches,
        Centres,
        Comments,
        Groups,
        IDDocuments,
        Users,
    )


class Risk(Enum):
    high = "Alto"
    medium = "Medio"
    low = "Bajo"


@dataclass(repr=False)
class Clients(EntityMambu):
    _model_rest = MambuClient
    _model_orm = ORMClient

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Clients), mode, **kwargs)

    state: str = field(
        metadata={"mambu_source": "state", "read_only": False, "is_required": False}
    )

    activation_date: datetime = field(
        metadata={
            "mambu_source": "activationDate",
            "read_only": False,
            "is_required": False,
        }
    )
    approved_date: datetime = field(
        metadata={
            "mambu_source": "approvedDate",
            "read_only": False,
            "is_required": False,
        }
    )
    first_name: str = field(
        metadata={"mambu_source": "firstName", "read_only": False, "is_required": False}
    )
    last_name: str = field(
        metadata={"mambu_source": "lastName", "read_only": False, "is_required": False}
    )
    middle_name: str = field(
        metadata={"mambu_source": "middleName", "read_only": False, "is_required": False}
    )
    home_phone: str = field(
        metadata={"mambu_source": "homePhone", "read_only": False, "is_required": False}
    )
    mobile_phone: str = field(
        metadata={"mambu_source": "mobilePhone", "read_only": False, "is_required": False}
    )
    preferred_language: str = field(
        metadata={
            "mambu_source": "preferredLanguage",
            "read_only": False,
            "is_required": False,
        }
    )
    birth_date: datetime = field(
        metadata={"mambu_source": "birthDate", "read_only": False, "is_required": False}
    )
    gender: str = field(
        metadata={"mambu_source": "gender", "read_only": False, "is_required": False}
    )
    notes: str = field(
        metadata={"mambu_source": "notes", "read_only": False, "is_required": False}
    )
    assigned_branch_key: str = field(
        metadata={
            "mambu_source": "assignedBranchKey",
            "read_only": False,
            "is_required": False,
        }
    )
    client_role_key: str = field(
        metadata={
            "mambu_source": "clientRoleKey",
            "read_only": False,
            "is_required": False,
        }
    )
    loan_cycle: int = field(
        metadata={"mambu_source": "loanCycle", "read_only": False, "is_required": False}
    )
    group_loan_cycle: int = field(
        metadata={
            "mambu_source": "groupLoanCycle",
            "read_only": False,
            "is_required": False,
        }
    )
    group_keys: list[str] = field(
        metadata={"mambu_source": "groupKeys", "read_only": False, "is_required": False}
    )
    addresses: list[Addresses] = field(
        metadata={
            "mambu_source": "addresses",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "model": "Addresses",
        }
    )
    id_documents: list[IDDocuments] = field(
        metadata={
            "mambu_source": "idDocuments",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "model": "IDDocuments",
        }
    )
    customfields_integrante: dict = field(
        metadata={
            "mambu_source": "_customfields_integrante",
            "read_only": False,
            "is_required": False,
        }
    )
    deprecated_integrante: dict = field(
        metadata={
            "mambu_source": "_deprecated_integrante",
            "read_only": False,
            "is_required": False,
        }
    )
    datosdomicilioactual_integrante: dict = field(
        metadata={
            "mambu_source": "_datosdomicilioactual_integrante",
            "read_only": False,
            "is_required": False,
        }
    )
    datossolicitante_integrante: dict = field(
        metadata={
            "mambu_source": "_datossolicitante_integrante",
            "read_only": False,
            "is_required": False,
        }
    )
    profesion_clients: str = field(
        metadata={
            "mambu_source": "Profesion_Clients",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/Profesion_Clients",
        }
    )
    otros_ingresos_clients: int = field(
        metadata={
            "mambu_source": "Otros_Ingresos_Clients",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/Otros_Ingresos_Clients",
        }
    )
    actividad_economica_clients: str = field(
        metadata={
            "mambu_source": "Actividad_economica_Clients",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/Actividad_economica_Clients",
        }
    )
    utilidad_clients: int = field(
        metadata={
            "mambu_source": "Utilidad_Clients",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/Utilidad_Clients",
        }
    )
    gasto_familiar_clients: int = field(
        metadata={
            "mambu_source": "Gasto_Familiar_Clients",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/Gasto_Familiar_Clients",
        }
    )
    ingresos_clients: int = field(
        metadata={
            "mambu_source": "Ingresos_Clients",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/Ingresos_Clients",
        }
    )
    giro_clients: str = field(
        metadata={
            "mambu_source": "Giro_Clients",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/Giro_Clients",
        }
    )
    actividad_economica_clientss: str = field(
        metadata={
            "mambu_source": "Actividad_economica_Clientss",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/Actividad_economica_rel_Clients",
        }
    )
    dependientes_economicos_clients: int = field(
        metadata={
            "mambu_source": "Dependientes_economicos_Clients",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datosdomicilioactual_integrante/Dependientes_economicos_Clients",
        }
    )
    tipo_de_vivienda_clients: str = field(
        metadata={
            "mambu_source": "Tipo_de_vivienda_Clients",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datosdomicilioactual_integrante/Tipo_de_vivienda_Clients",
        }
    )
    estado_civil_clients_old: str = field(
        metadata={
            "mambu_source": "Estado_civil_Clients_old",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datossolicitante_integrante/Estado_civil_Clients_old",
        }
    )

    groups: list[Groups] = field(
        metadata={
            "mambu_source": "groups",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Groups",
            "is_many": True,
        }
    )

    assigned_branch: Branches = field(
        metadata={
            "mambu_source": "assignedBranch",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Branches",
        }
    )
    assigned_centre: Centres = field(
        metadata={
            "mambu_source": "assignedCentre",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Centres",
        }
    )
    assigned_user: Users = field(
        metadata={
            "mambu_source": "assignedUser",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Users",
        }
    )
    assigned_user_key: str = field(
        metadata={
            "mambu_source": "assignedUserKey",
            "read_only": True,
            "is_required": False,
        }
    )
    rfc: str = field(
        metadata={
            "mambu_source": "rfc",
            "read_only": True,
            "is_required": False,
            "is_cf": True,
            "path": "/_datossolicitante_integrante/rfc",
        }
    )
    email_address: str = field(
        metadata={"mambu_source": "emailAddress", "read_only": True, "is_required": False}
    )

    riesgo_integrante: str = field(
        metadata={
            "mambu_source": "niveles_riesgo_clientes",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_riesgo_integrante/niveles_riesgo_clientes",
        }
    )
    comments: list[Comments] = field(
        metadata={
            "mambu_source": "_comments",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "lazy_from_method": "get_comments",
            "model": "Comments",
        }
    )
    people_could_political_exposed: str = field(
        metadata={
            "mambu_source": "people_could_political_exposed",
            "read_only": True,
            "is_required": False,
        }
    )
    vivienda_nombre_arrendador: str = field(
        metadata={
            "mambu_source": "vivienda_nombre_arrendador",
            "read_only": True,
            "is_required": False,
        }
    )
    vivienda_telefono_arrendador: str = field(
        metadata={
            "mambu_source": "vivienda_telefono_arrendador",
            "read_only": True,
            "is_required": False,
        }
    )
    experiencia: int = field(
        metadata={
            "mambu_source": "Experiencia",
            "read_only": True,
            "is_required": False,
        }
    )
    estado_civil_clients: str = field(
        metadata={
            "mambu_source": "Estado_civil_Clients",
            "read_only": True,
            "is_required": False,
            "is_cf": True,
            "path": "/_datossolicitante_integrante/Estado_civil_Clients",
        }
    )
    entidad_nacimiento: str = field(
        metadata={
            "mambu_source": "EntidadNacimiento",
            "read_only": True,
            "is_required": False,
            "is_cf": True,
            "path": "/_datossolicitante_integrante/EntidadNacimiento",
        }
    )
    nivel_educacion: str = field(
        metadata={
            "mambu_source": "niveleducacion",
            "read_only": True,
            "is_required": False,
            "is_cf": True,
            "path": "/_datossolicitante_integrante/niveleducacion",
        }
    )
    vigencia_ine_clients: str = field(
        metadata={
            "mambu_source": "vigencia_ine_clients",
            "read_only": True,
            "is_required": False,
            "is_cf": True,
            "path": "/_datossolicitante_integrante/vigencia_ine_clients",
        }
    )
    mobile_phone_2: str = field(
        metadata={
            "mambu_source": "mobilePhone2",
            "read_only": False,
            "is_required": False,
        }
    )
    antiguedad_en_domicilio: str = field(
        metadata={
            "mambu_source": "antiguedad_en_domicilio",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datosdomicilioactual_integrante/antiguedad_en_domicilio",
        }
    )
    referencia_ubicacion: str = field(
        metadata={
            "mambu_source": "referencia_ubicacion",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datosdomicilioactual_integrante/referencia_ubicacion",
        }
    )
    familiar_mismo_domicilio_nombre: str = field(
        metadata={
            "mambu_source": "familiar_mismo_domicilio_nombre",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datosdomicilioactual_integrante/familiar_mismo_domicilio_nombre",
        }
    )
    familiar_mismo_domicilio_phone: str = field(
        metadata={
            "mambu_source": "familiar_mismo_domicilio_phone",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datosdomicilioactual_integrante/familiar_mismo_domicilio_phone",
        }
    )
    familiar_mismo_domicilio_parent: str = field(
        metadata={
            "mambu_source": "familiar_mismo_domicilio_parent",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datosdomicilioactual_integrante/familiar_mismo_domicilio_parent",
        }
    )
    domicilio_entre_calle_a: str = field(
        metadata={
            "mambu_source": "domicilio_entre_calle_A",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datosdomicilioactual_integrante/domicilio_entre_calle_A",
        }
    )
    domicilio_entre_calle_b: str = field(
        metadata={
            "mambu_source": "domicilio_entre_calle_B",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datosdomicilioactual_integrante/domicilio_entre_calle_B",
        }
    )
    pld_origen_recursos: str = field(
        metadata={
            "mambu_source": "pld_origen_recursos",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/pld_origen_recursos",
        }
    )
    fuente_otros_ingresos_client: str = field(
        metadata={
            "mambu_source": "fuente_otros_ingresos_client",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datoseconomicos_integrante/fuente_otros_ingresos_client",
        }
    )
    monto_max_pagar_client: float = field(
        metadata={
            "mambu_source": "monto_max_pagar_client",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datoseconomicos_integrante/monto_max_pagar_client",
        }
    )
    pld_es_propietario_recursos: bool = field(
        metadata={
            "mambu_source": "pld_es_propietario_recursos",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_integrante/pld_es_propietario_recursos",
        }
    )
    primer_credito_client: bool = field(
        metadata={
            "mambu_source": "primer_credito_client",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datoscrediticios_integrante/primer_credito_client",
        }
    )
    otros_creditos_activos_client: bool = field(
        metadata={
            "mambu_source": "otros_creditos_activos_client",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_datoscrediticios_integrante/otros_creditos_activos_client",
        }
    )
    direccion_del_negocio: str = field(
        metadata={
            "mambu_source": "direccion_del_negocio",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_ocupacionactual_integrante/direccion_del_negocio",
        }
    )
    dias_venta_client: str = field(
        metadata={
            "mambu_source": "dias_venta_client",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_ocupacionactual_integrante/dias_venta_client",
        }
    )
    actividad_adicional_client: str = field(
        metadata={
            "mambu_source": "actividad_adicional_client",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_ocupacionactual_integrante/actividad_adicional_client",
        }
    )
    ubicacion_del_negocio: str = field(
        metadata={
            "mambu_source": "ubicacion_del_negocio",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_ocupacionactual_integrante/ubicacion_del_negocio",
        }
    )
    referencias_integrante: bool = field(
        metadata={
            "mambu_source": "_referencias_integrante",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_referencias_integrante",
        }
    )

    @property
    def full_name(self):
        if not self.middle_name:
            return self.first_name + " " + self.last_name

        return self.first_name + " " + self.middle_name + " " + self.last_name

    @property
    def full_name_ce(self):
        try:
            return self.assigned_user.first_name + " " + self.assigned_user.last_name
        except Exception:
            return ""

        return ""

    @property
    def curp(self):
        document_value = ""
        if self.id_documents:
            for value in self.id_documents:
                if value.document_type == "CURP":
                    document_value = value.document_id
                    break
        return document_value

    @property
    def group(self):
        if len(self.group_keys) > 1:
            raise Exception(f"This client with id '{self.id}' have more then one group ")
        try:
            return self.groups[0]
        except IndexError:
            return None

    def update_risk(self, risk: Risk):
        self.write({"riesgo_integrante": risk.value})

    @property
    def full_addresses(self):
        if self.addresses:
            return [
                address.line_1
                + " "
                + address.line_2
                + " "
                + address.city
                + " "
                + address.region
                + " "
                + str(address.postcode)
                + " "
                + address.country
                for address in self.addresses
            ]
        return []

    @classmethod
    def search_by_curp(cls, curp: str):
        instances_mambu = cls._model_rest.get_all(filters={"idNumber": curp})
        return [cls.get(instance_mambu.id) for instance_mambu in instances_mambu]
