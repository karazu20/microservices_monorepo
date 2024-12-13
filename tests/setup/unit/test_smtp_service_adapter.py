import os
import os.path
import smtplib

import pytest

from setup.adapters.smtp import SmtpEmail

FILENAME = "fake.pdf"


def test_smtp_service(mocker):
    mock_basename = mocker.patch("os.path.basename")
    mock_basename.return_value = FILENAME

    mocker.patch.object(smtplib.SMTP_SSL, "login")
    mocker.patch.object(smtplib.SMTP_SSL, "sendmail")

    with open(FILENAME, "w"):
        pass

    email_data = {
        "to": ["fake.email@domain.com", "cc.faketribu@domain.com"],
        "cc": ["cc.fakecc@domain.com"],
        "subject": "CDC Test",
        "message": "Enviado por user.fake",
        "attachments": [FILENAME],
    }

    SmtpEmail.send(**email_data)
    SmtpEmail.smtp.sendmail.assert_called()
    os.path.basename.assert_called()

    SmtpEmail.smtp.sendmail.side_effect = Exception("STMP Error")
    with pytest.raises(Exception):
        assert SmtpEmail.send(**email_data)
