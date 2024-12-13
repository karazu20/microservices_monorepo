"""Utils for MS validations"""
import re
import unicodedata
from datetime import datetime


def extract_data_by_id(data_to_extract, key, if_check=False, key_validate=None):
    extract_data = []
    if not data_to_extract:
        return []

    for value in data_to_extract:
        if if_check:
            attr_validate = getattr(value, key_validate)
            if attr_validate:
                extract_data.append(getattr(value, key))
        else:
            extract_data.append(getattr(value, key))

    return extract_data


def extract_data_from_document_mambu(data_to_extract, document_type):
    data_value = None
    for value_documents in data_to_extract:
        if value_documents.document_type == document_type:
            data_value = value_documents.document_id

    return data_value


def validate_data_rfc(id, rfc, curp):
    rfc = rfc.upper()

    if len(rfc) >= 10 and len(rfc) <= 13:
        regex = r"[A-ZÑ]{3,4}[\d]{6}"
        matches = re.match(regex, rfc)
        if not matches:
            return {
                "message": "El formato del RFC de la integrante: "
                + id
                + " es incorrecto",
                "status": False,
            }

    if not (curp[:10].upper() == rfc[:10].upper()):
        return {
            "message": "El RFC de la integrante: " + id + " es incorrecto",
            "status": False,
        }

    return {
        "message": "",
        "status": True,
    }


def convert_value_to_data_type(data_type, value):
    if data_type == "str":
        return str(value)

    if data_type == "int":
        return int(value)

    if data_type == "float":
        return float(value)


def strip_accents(s):
    return "".join(
        (c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    )


def curpinfo(curp, info=""):
    fields = {
        "APPAT": {"ini": 0, "fin": 2},
        "APMAT": {"ini": 2, "fin": 3},
        "NOM": {"ini": 3, "fin": 4},
        "NOMBRE": {"ini": 0, "fin": 4},
        "FECNAC": {"ini": 4, "fin": 10},
        "RFC": {"ini": 0, "fin": 10},
        "GEN": {"ini": 10, "fin": 11},
        "EDONAC": {"ini": 11, "fin": 13},
        "CONS": {"ini": 13, "fin": 16},
        "DIGS": {"ini": 16, "fin": 18},
    }

    return curp[fields[info]["ini"] : fields[info]["fin"]]


def decode(string, code):
    try:
        return string.decode(code)
    except AttributeError:
        return string
    except UnicodeDecodeError:  # pragma: no cover
        pass
    raise Exception("No se puede decodificar string: {}".format(string))


def valida_curp(
    client,
    validar=["NOMBRE", "FECHANACIMIENTO", "GENERO"],
    palabras_inconvenientes=None,
    *args,
    **kargs
):
    message = "El CURP ({}) es invalido".format(client.curp)

    preposiciones = [
        "DA",
        "DAS",
        "DE",
        "DEL",
        "DER",
        "DI",
        "DIE",
        "DD",
        "EL",
        "LA",
        "LOS",
        "LAS",
        "LE",
        "LES",
        "MAC",
        "MC",
        "VAN",
        "VON",
        "Y",
    ]

    try:
        # Longitud del CURP debe ser 18 caracteres
        if len(str(client.curp).encode("utf8").decode("utf8")) != 18:
            message += " (longitud invalida, deben ser 18 caracteres)"
            return False, message

        # No se permiten Ñs, deberia tener X en donde hubiera Ñs segun las reglas
        if "Ñ" in client.curp:
            message += " (no se permiten Ñs en el CURP)"
            return False, message

        if "GENERO" in validar:
            # Generos validos: H o M
            gender = curpinfo(curp=client.curp, info="GEN")
            if gender not in ["H", "M"]:
                message += " (solo se permite genero H o M)"
                return False, message
            clientGender = (
                "MUJER" if client.gender == "FEMALE" else "HOMBRE"
            )  # pragma: no cover
            if clientGender[0] != curpinfo(client.curp, info="GEN"):
                return False, message + " (el genero es incorrecto)"

        if "NOMBRE" in validar:
            nombre = curpinfo(curp=client.curp, info="NOMBRE")
            appat = curpinfo(curp=client.curp, info="APPAT")
            apmat = curpinfo(curp=client.curp, info="APMAT")
            nom = curpinfo(curp=client.curp, info="NOM")

            # El CURP empieza con la primer letra y primer vocal del apellido paterno
            apellido_paterno = re.search(  # type: ignore
                r"(DE[L]? )?(L[A|O][S]? )?([\wÑñÜü\\/\-.\xd1]+)",
                str(client.last_name).upper(),
            ).groups()[2]
            primerletraappat = (
                apellido_paterno.replace("Ñ", "X")
                .replace("ñ", "X")
                .replace("Ü", "U")
                .replace("ü", "U")[0]
            )
            try:
                primervocalappat = (
                    re.findall(
                        r"[AEIOU\\/\-.]",
                        apellido_paterno[1:]
                        .replace("Ñ", "X")
                        .replace("ñ", "X")
                        .replace("Ü", "U")
                        .replace("ü", "U"),
                    )[0]
                    .replace("/", "X")
                    .replace("-", "X")
                    .replace(".", "X")
                    .replace("\\", "X")
                )
            except IndexError:
                primervocalappat = "X"
            if (primerletraappat + primervocalappat) != appat:
                dict_palabras_inconvenientes = dict(
                    [(value.llave, value.valor) for value in palabras_inconvenientes]
                )
                if (
                    primerletraappat + primervocalappat + apmat + nom
                ) in dict_palabras_inconvenientes.keys():
                    if (
                        nombre
                        != dict_palabras_inconvenientes[
                            primerletraappat + primervocalappat + apmat + nom
                        ]
                    ):
                        return False, message + " (revisar palabras inconvenientes)"
                else:
                    return (
                        False,
                        message
                        + " (CURP no coincide con apellido paterno de integrante)",
                    )

            # Le sigue la primer letra del apellido materno (o X si no hay apellido materno)
            if str(client.middle_name).upper():
                apellido_materno = re.search(  # type: ignore
                    r"(DE[L]? )?(L[A|O][S]? )?([\wÑñÜü\\/\-.\xd1]+)",
                    str(client.middle_name).upper(),
                ).groups()[2]
                if (
                    apellido_materno.replace("Ñ", "X")
                    .replace("ñ", "X")
                    .replace("Ü", "U")
                    .replace("ü", "U")[0]
                    != apmat
                ):
                    return (
                        False,
                        message
                        + " (CURP no coincide con apellido materno de integrante)",
                    )
            elif apmat != "X":
                return False, message + " (CURP no coincide, no hay apellido materno)"

            # Le sigue la primer letra del nombre de pila
            # a menos que el primer nombre sea JOSE o MARIA se usa el segundo nombre
            nombres = str(strip_accents(client.first_name)).upper().split(" ")
            nombrepila = nombres[0]
            if len(nombres) > 1 and nombres[0] in [
                "J",
                "J.",
                "M",
                "M.",
                "MARIA",
                decode("MARÍA", "latin"),
                "JOSE",
                decode("JOSÉ", "latin"),
                "MA.",
                "JO.",
                "MA",
                "JO",
            ]:
                nombrepila = nombres[1]
                if len(nombres) > 2 and nombres[1] in preposiciones:
                    nombrepila = nombres[2]
                    if len(nombres) > 3 and nombres[2] in preposiciones:
                        nombrepila = nombres[3]
            if (
                nombrepila.replace("Ñ", "X")
                .replace("ñ", "X")
                .replace("Ü", "U")
                .replace("ü", "U")[0]
                != nom
            ):
                return False, message + " (CURP no coincide con nombre de integrante)"

            # 'consonantes': las ultimas 3 letras del CURP (o casi siempre)
            consonantes = curpinfo(curp=client.curp, info="CONS")

            # 1er consonante: primer consonante no inicial del primer apellido
            appat_sinvocales = re.sub(
                r"[AEIOU\\\-/.]",
                "",
                apellido_paterno.replace("Ñ", "X")
                .replace("ñ", "X")
                .replace("Ü", "U")
                .replace("ü", "U"),
            )
            try:
                if primerletraappat == appat_sinvocales[0]:
                    if appat_sinvocales[1] != consonantes[0]:
                        return (
                            False,
                            message
                            + " (CURP no coincide con apellido paterno de integrante, 1er consonante)",
                        )
                else:
                    if appat_sinvocales[0] != consonantes[0]:
                        return (
                            False,
                            message
                            + " (CURP no coincide con apellido paterno de integrante, 1er consonante)",
                        )
            except IndexError:
                if consonantes[0] != "X":
                    return (
                        False,
                        message
                        + " (CURP no coincide con apellido paterno de integrante, 1er consonante)",
                    )

            # 2da consonante: primer consonante no inicial del segundo apellido (si existe, sino X)
            if client.middle_name.upper():
                apmat_sinvocales = re.sub(
                    r"[AEIOU\\\-/.]",
                    "",
                    apellido_materno.replace("Ñ", "X")
                    .replace("ñ", "X")
                    .replace("Ü", "U")
                    .replace("ü", "U")
                    .replace("Ã", "X"),
                )
                primerletraapmat = (
                    apellido_materno.replace("Ñ", "X")
                    .replace("ñ", "X")
                    .replace("Ü", "U")
                    .replace("ü", "U")[0]
                    .replace("/", "X")
                    .replace("-", "X")
                    .replace(".", "X")
                    .replace("\\", "X")
                )
                try:
                    if primerletraapmat == apmat_sinvocales[0]:
                        if apmat_sinvocales[1] != consonantes[1]:
                            return (
                                False,
                                message
                                + " (CURP no coincide con apellido materno de integrante, 2da consonante)",
                            )
                    else:
                        if apmat_sinvocales[0] != consonantes[1]:
                            return (
                                False,
                                message
                                + " (CURP no coincide con apellido materno de integrante, 2da consonante)",
                            )
                except IndexError:
                    if consonantes[1] != "X":
                        return (
                            False,
                            message
                            + " (CURP no coincide con apellido materno de integrante, 2da consonante)",
                        )
            else:
                if consonantes[1] != "X":
                    return (
                        False,
                        message
                        + " (CURP no coincide con apellido materno de integrante, 2da consonante)",
                    )

            # 3era consonante: primer consonante no inicial del nombre de pila
            nom_sinvocales = re.sub(
                r"[AEIOU]",
                "",
                nombrepila.replace("Ñ", "X")
                .replace("ñ", "X")
                .replace("Ü", "U")
                .replace("ü", "U"),
            )
            primerletranom = (
                nombrepila.replace("Ñ", "X")
                .replace("ñ", "X")
                .replace("Ü", "U")
                .replace("ü", "U")[0]
            )
            if primerletranom == nom_sinvocales[0]:
                try:
                    if nom_sinvocales[1] != consonantes[2]:
                        return (
                            False,
                            message
                            + " (CURP no coincide con nombre de integrante, 3a consonante)",
                        )
                except IndexError:
                    if consonantes[2] != "X":
                        return (
                            False,
                            message
                            + " (CURP no coincide con nombre de integrante, 3a consonante)",
                        )
            else:
                if nom_sinvocales[0] != consonantes[2]:
                    return (
                        False,
                        message
                        + " (CURP no coincide con nombre de integrante, 3a consonante)",
                    )

        if "FECHANACIMIENTO" in validar:
            # el primer 'digito' es numero cuando la fecha de
            # nacimiento sea anterior a 2000 y letra despues
            try:
                fechanac = client.birth_date
                fechanac.strftime("%Y")
            except AttributeError:
                fechanac = datetime.strptime(client.birth_date, "%Y-%m-%d")
            digs = curpinfo(curp=client.curp, info="DIGS")
            if int(fechanac.strftime("%Y")) < 1999 and not digs[0].isdigit():
                return False, message + " (fecha de nacimiento invalida)"
            if int(fechanac.strftime("%Y")) >= 2000 and not digs[0].isalpha():
                return False, message + " (fecha de nacimiento invalida)"
            if curpinfo(curp=client.curp, info="FECNAC") != fechanac.strftime("%y%m%d"):
                return False, message + " (fecha de nacimiento invalida)"

    except Exception as ex:  # pragma: no cover
        return False, message + " " + repr(ex)
    return True, "CURP valido"


def disbursement_date(loan):
    try:
        if loan.disbursement_details.disbursement_date:
            return loan.disbursement_details.disbursement_date
        elif loan.disbursement_details.expected_disbursement_date:
            return loan.disbursement_details.expected_disbursement_date
    except Exception:
        return datetime.now()


def find_client(id, clients):
    for value in clients:
        if value.encoded_key == id:
            return value

    return None


def extract_min_max_levels(data, value_to_extract):
    data_value = []
    for value in data:
        if value_to_extract == value.llave:
            data_value.append(value.valor)

    if value_to_extract == "min":
        return min(data_value)
    elif value_to_extract == "max":
        return max(data_value)

    return data_value


def change_day_spanish(day):
    try:
        days = {
            "MONDAY": "LUNES",
            "TUESDAY": "MARTES",
            "WEDNESDAY": "MIERCOLES",
            "THURSDAY": "JUEVES",
            "FRIDAY": "VIERNES",
            "SATURDAY": "SABADO",
            "SUNDAY": "DOMINGO",
        }
        return days[day]
    except KeyError:
        return None


def extract_streetnumber(streetnumber, info=""):
    fields = {
        "calle": 0,
        "numsimb": 2,
        "numero": -2,
    }

    rex = r"^([\W\w\d\s]+)((#|No\.|NO\.| LT | Lt |Lt\.|LT\.|Lote |Lt-|LT-"
    rex += r"|EDIF -|EDIF-|Edif-|Edif -)([-\w\d\s.,]+)|( SN| S\.N\.| S/N| S-N))$"

    rob = re.compile(rex)
    srch = rob.search(streetnumber)

    try:
        srch.groups()  # type: ignore
    except AttributeError:
        srch = rob.search(streetnumber + " S/N")

    inf = (
        srch.groups()[fields[info]].strip().strip(",")  # type: ignore
        if srch.groups()[fields[info]]  # type: ignore
        else srch.groups()[fields[info] + 1]  # type: ignore
    )

    return inf.strip()
