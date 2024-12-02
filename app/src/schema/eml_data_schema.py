from pydantic import BaseModel


class EmlDataSchema(BaseModel):
    # From
    from_address: str

    # To
    to_address: str

    # 件名
    subject: str

    # 本文
    body: str
