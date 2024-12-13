from shared import security


def test_encrypt_decrypt():

    pass_dummy = "dummy_pass"

    pass_encrypted = security.encrypt_pass(pass_dummy)
    pass_decrypted = security.decrypt_pass(pass_encrypted)

    assert pass_dummy == pass_decrypted
