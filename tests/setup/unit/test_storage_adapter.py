import pytest
from botocore.exceptions import ClientError

from setup.adapters.storage import S3, S3Error


def test_get(mocker):
    mock_boto = mocker.patch("setup.adapters.storage.boto3")

    model = S3()
    response = model.get(bucket="prueba_podemos", key_file="12345-ine-202301132028")

    assert response == "/tmp/12345-ine-202301132028"
    mock_boto.resource.assert_called()
    mock_boto.resource().Bucket().download_file.assert_called_with(
        "12345-ine-202301132028", "/tmp/12345-ine-202301132028"
    )

    mock_boto.resource().Bucket().download_file.side_effect = ClientError(
        {"Error": {"Code": "ParameterNotFound", "Message": "Parameter was not found"}},
        "get_parameter",
    )

    model = S3()
    with pytest.raises(S3Error):
        model.get(bucket="prueba_podemos", key_file="12345-ine-202301132028")


def test_get_url(mocker):
    mock_boto = mocker.patch("setup.adapters.storage.boto3")
    mock_boto.client().generate_presigned_url.return_value = "http://prueba.com"

    model = S3()
    response = model.get_url(bucket="prueba_podemos", key_file="12345-cfe-202301132028")

    mock_boto.client().generate_presigned_url.assert_called_with(
        ClientMethod="get_object",
        Params={"Bucket": "prueba_podemos", "Key": "12345-cfe-202301132028"},
    )
    assert response == "http://prueba.com"

    mock_boto.reset_mock()
    mock_boto.client().generate_presigned_url.side_effect = ClientError(
        {"Error": {"Code": "ParameterNotFound", "Message": "Parameter was not found"}},
        "get_parameter",
    )

    model = S3()
    with pytest.raises(S3Error):
        model.get_url(bucket="prueba_podemos", key_file="12345-ine-202301132028")


def test_put(mocker):
    mock_boto = mocker.patch("setup.adapters.storage.boto3")

    model = S3()
    response = model.put(
        bucket="prueba_podemos",
        path_file_name="/tmp/12345-cfe-202301132028.png",
        key="12345-cfe-202301132028",
    )

    assert response
    mock_boto.resource().Bucket().upload_file.assert_called_with(
        Filename="/tmp/12345-cfe-202301132028.png", Key="12345-cfe-202301132028"
    )

    mock_boto.reset_mock()
    mock_boto.resource().Bucket().upload_file.side_effect = ClientError(
        {"Error": {"Code": "ParameterNotFound", "Message": "Parameter was not found"}},
        "get_parameter",
    )
    model = S3()
    with pytest.raises(S3Error):
        response = model.put(
            bucket="prueba_podemos",
            path_file_name="/tmp/12345-cfe-202301132028.png",
            key="12345-cfe-202301132028",
        )

    mock_boto.reset_mock()
    mock_boto.resource().Bucket().upload_file.side_effect = Exception("Prueba")
    model = S3()
    with pytest.raises(Exception):
        response = model.put(
            bucket="prueba_podemos",
            path_file_name="/tmp/12345-cfe-202301132028.png",
            key="12345-cfe-202301132028",
        )


def test_get_by_filter(mocker):
    mock_boto = mocker.patch("setup.adapters.storage.boto3")
    mock_boto.resource().Bucket().objects.filter().all.return_value = ["prueba"]

    mock_boto
    model = S3()
    response = model.get_by_filter(bucket="prueba_podemos", prefix="12345")

    assert response
    mock_boto.resource().Bucket().objects.filter().all.assert_called()

    mock_boto.reset_mock()
    mock_boto.resource().Bucket().objects.filter().all.side_effect = ClientError(
        {"Error": {"Code": "ParameterNotFound", "Message": "Parameter was not found"}},
        "get_parameter",
    )
    model = S3()
    with pytest.raises(S3Error):
        response = model.get_by_filter(bucket="prueba_podemos", prefix="12345")

    mock_boto.reset_mock()
    mock_boto.resource().Bucket().objects.filter().all.side_effect = Exception("Prueba")
    model = S3()
    with pytest.raises(Exception):
        response = model.get_by_filter(bucket="prueba_podemos", prefix="12345")
