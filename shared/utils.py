import ast
import json
import logging

import xmltodict

logger = logging.getLogger(__name__)


def json_to_xml(xml_json_string):
    """Funcion que solicita un JSON o JSON string y lo retorna como XML"""
    try:
        # Se valida que sea JSON o String
        if type(xml_json_string) == dict:
            # Se convierte en string porque es actualmente dict
            string_json = "{'root':" + str(xml_json_string) + "}"
            tmp_json = json.dumps(string_json)
            new_json = json.loads(tmp_json)
            json_xml = xmltodict.unparse(ast.literal_eval(new_json))
            return str(json_xml)
        if type(xml_json_string) == str:
            # Se agrega root para usar la funcion xmltodict -> https://pypi.org/project/xmltodict/
            tmp_json = '{"root":' + xml_json_string + "}"
            new_json = json.loads(tmp_json)
            json_xml = xmltodict.unparse(new_json)
            return str(json_xml)
        else:
            raise Exception("Error en el tipo de Dato {}".format(type(xml_json_string)))
    except ValueError as v:
        return "ValueError: " + str(v)
    except TypeError as t:
        return "TypeError: " + str(t)
    except Exception as e:
        return "Exception: " + str(e)


def xml_to_dict(xml_string) -> dict:
    """Funcion que solicita un XML string y lo retorna como JSON"""
    try:
        # Se valida que sea JSON o String
        return xmltodict.parse(xml_string)
    except Exception as e:
        raise Exception("Error al convertir xml: {}".format(str(e)))


def get_full_name(
    nombres: str = "", apellido_paterno: str = "", apellido_materno: str = ""
) -> str:
    full_name: list = []

    if nombres:
        full_name.append(nombres.strip())
    if apellido_paterno:
        full_name.append(apellido_paterno.strip())
    if apellido_materno:
        full_name.append(apellido_materno.strip())

    name = " ".join(full_name)
    return name.strip()
