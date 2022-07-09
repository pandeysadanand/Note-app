import jwt


class EncodeDecode:

    def encode_token(self, payload):
        jwt_encode = jwt.encode(payload, "secret", algorithm="HS256")
        return jwt_encode

    def decode_token(self, token):
        decode_token = jwt.decode(token, "secret", algorithms=["HS256"])
        return decode_token

# todo use generic jwt service , encode and decode for user[utils], registration
