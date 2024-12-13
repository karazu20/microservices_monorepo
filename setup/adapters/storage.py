from __future__ import annotations

import abc
import logging

import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

from setup.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    EXPIRES_IN,
    PATH_S3,
    SERVICE_NAME,
)

logger = logging.getLogger(__name__)


class S3Error(Exception):
    def __init__(self, message):
        self.message = message


class AbstractStorage(abc.ABC):
    service_name: str = NotImplemented
    aws_access_key_id: str = NotImplemented
    aws_secret_access_key: str = NotImplemented
    path_s3: str = NotImplemented
    expires_in: int = NotImplemented

    @classmethod
    @abc.abstractmethod
    def get(cls, bucket: str, key_file: str):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_url(cls, bucket: str, key_file: str):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def put(cls, bucket: str, path_file_name: str, key: str):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_filter(cls, bucket: str, prefix: str):
        raise NotImplementedError


class S3(AbstractStorage):
    service_name: str = SERVICE_NAME
    aws_access_key_id: str = AWS_ACCESS_KEY_ID
    aws_secret_access_key: str = AWS_SECRET_ACCESS_KEY
    path_s3: str = PATH_S3
    expires_in: int = EXPIRES_IN  # type: ignore

    @classmethod
    def _connect(cls, type_connection: str) -> object:
        if type_connection == "client":
            s3_storage = boto3.client(
                service_name=cls.service_name,
                aws_access_key_id=cls.aws_access_key_id,
                aws_secret_access_key=cls.aws_secret_access_key,
            )
        else:
            s3_storage = boto3.resource(
                service_name=cls.service_name,
                aws_access_key_id=cls.aws_access_key_id,
                aws_secret_access_key=cls.aws_secret_access_key,
            )

        return s3_storage

    @classmethod
    def get(cls, bucket: str, key_file: str) -> str:
        s3_storage = cls._connect(type_connection="resource")
        try:
            s3_storage.Bucket(bucket).download_file(  # type: ignore
                key_file, cls.path_s3 + key_file
            )
            logger.info(
                "Descarga correcta del archivo en: %s, bucket: %s",
                bucket,
                (cls.path_s3 + key_file),
            )
            return cls.path_s3 + key_file
        except ClientError as ex:
            logger.error(
                (
                    "Error al tratar de descargar "
                    "archivo de S3 bucket: %s, key_file: %s: %s"
                ),
                bucket,
                key_file,
                str(ex),
            )
            raise S3Error(ex)

    @classmethod
    def get_url(cls, bucket: str, key_file: str) -> str:
        s3_storage = cls._connect(type_connection="client")

        try:
            url = s3_storage.generate_presigned_url(  # type: ignore
                ClientMethod="get_object", Params={"Bucket": bucket, "Key": key_file}
            )
            logger.info(
                (
                    "Genera URL correctamente del archivo "
                    "en: bucket %s, key_file: %s, url %s"
                ),
                bucket,
                key_file,
                url,
            )
            return url
        except ClientError as ex:
            logger.error(
                (
                    "Error al tratar de generar URL para"
                    " descargar archivo de S3 bucket: %s, key_file: %s: %s"
                ),
                bucket,
                key_file,
                str(ex),
            )
            raise S3Error(ex)

    @classmethod
    def put(cls, bucket: str, path_file_name: str, key: str) -> bool:
        s3_storage = cls._connect(type_connection="resource")
        try:
            s3_storage.Bucket(bucket).upload_file(  # type: ignore
                Filename=path_file_name, Key=key
            )
            logger.info(
                "Se sube correctamente archivo: bucket %s, path_file_name: %s, key %s",
                bucket,
                path_file_name,
                key,
            )
            return True
        except ClientError as ex:
            logger.error(
                (
                    "Error al tratar de subir un archivo "
                    "para descargar archivo de S3 bucket %s, path_file_name %s, key %s: %s"
                ),
                bucket,
                path_file_name,
                key,
                str(ex),
            )
            raise S3Error(ex)
        except Exception as ex:
            logger.error(
                (
                    "Error al tratar de subir un archivo "
                    "para descargar archivo de S3 bucket %s, path_file_name %s, key %s: %s"
                ),
                bucket,
                path_file_name,
                key,
                str(ex),
            )
            raise S3Error(ex)

    @classmethod
    def get_by_filter(cls, bucket: str, prefix: str):
        s3_storage = cls._connect(type_connection="resource")
        try:
            result = [
                value
                for value in s3_storage.Bucket(bucket).objects.filter(Prefix=prefix).all()  # type: ignore
            ]
            return result
        except ClientError as ex:
            logger.error(
                "Error al tratar de obtener los archivos bucket %s, prefix %s: %s",
                bucket,
                prefix,
                str(ex),
            )
            raise S3Error(ex)
        except Exception as ex:
            logger.error(
                "Error al tratar de obtener los archivos bucket %s, prefix %s: %s",
                bucket,
                prefix,
                str(ex),
            )
            raise S3Error(ex)
