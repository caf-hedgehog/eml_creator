import configparser
from email import generator
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

from pydantic import BaseModel
from src.schema.eml_data_schema import EmlDataSchema

ENCODING_UTF_8 = "utf-8"


def set_base_eml_data(eml_data: EmlDataSchema) -> MIMEText:
    """
    基本的なEMLデータの設定を行う

    Args:
        eml_data (EmlDataSchema)

    Returns:
        MIMEText
    """

    sender_name = Header("Nick Name", ENCODING_UTF_8).encode()

    message = MIMEText(eml_data.body, "plain", ENCODING_UTF_8)
    message["Subject"] = Header(eml_data.subject, ENCODING_UTF_8)
    message["From"] = formataddr((sender_name, eml_data.from_address))
    message["To"] = eml_data.to_address

    # TODO: これは何なのか調査
    message.add_header("X-Unsent", "1")

    return message


# TODO: カスタムメタとベースメタで分けて設定するかも（Typeを見る）
#
def additional_meta_data(message: MIMEText, meta_list: list[str]):

    if "Message-ID" in meta_list:
        message["Message-ID"] = make_msgid(domain="hoge.hoge.com")

    return message
