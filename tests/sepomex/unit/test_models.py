from src.sepomex.domain.models import Colonia, Estado, Municipio


def test_colonia():
    cdmx = Estado("CMDX")
    hidalgo = Municipio("Miguel Hidalgo")
    escandon = Colonia("Escandon", "Ciudad de México", "Escando", "78965")
    hidalgo.add_colonia(escandon)
    cdmx.add_municipio(hidalgo)
    assert hidalgo in cdmx.get_municipios()
    assert escandon in hidalgo.get_colonias()
    assert escandon in hidalgo.get_colonias()
