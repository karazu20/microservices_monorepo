#!/bin/sh

mkdir ~/.docker
mv "$DOCKER_AUTH" ~/.docker/config.json
chmod g-r ~/.docker/config.json ; chmod o-r ~/.docker/config.json
mv "$WSDL_CDC_FILE_SANDBOX" src/cdc/templates/ConsultaReporteCCSandbox.wsdl
mv "$WSDL_CDC_FILE_PRODUCTION" src/cdc/templates/ConsultaReporteCCProduction.wsdl
