import grpc
from google.protobuf import any_pb2

# ===== 以下 import 请使用你通过 protoc 编译的文件路径 =====
import sys
sys.path.append('./gen')

from proxy.shadowsocks import config_pb2 as shadowsocks_pb2
from app.proxyman.command import command_pb2, command_pb2_grpc
from common.protocol import user_pb2
from common.serial import typed_message_pb2

# ============================================================

def add_shadowsocks_user_via_grpc(email,password):
    server_addr="127.0.0.1:10085"
    inbound_tag="ss-inbound"
    cipher="AES-128-GCM"

    # 1. 选择 CipherType
    cipher_enum = shadowsocks_pb2.CipherType.Value(cipher)

    # 2. 构建 Shadowsocks Account
    ss_account = shadowsocks_pb2.Account(
        password=password,
        cipher_type=cipher_enum,
        iv_check=False
    )

    # 3. 封装 Account 为 TypedMessage（注意 type 名必须精确匹配）
    account_msg = typed_message_pb2.TypedMessage(
        type="xray.proxy.shadowsocks.Account",
        value=ss_account.SerializeToString()
    )

    # 4. 构造 User（封装 Account 为其中的 account 字段）
    user = user_pb2.User(
        email=email,
        level=0,
        account=account_msg
    )

    # 5. 构造 AddUserOperation
    add_user_op = command_pb2.AddUserOperation(user=user)

    # 6. 封装 AddUserOperation 为 TypedMessage
    op_msg = typed_message_pb2.TypedMessage(
        type="xray.app.proxyman.command.AddUserOperation",
        value=add_user_op.SerializeToString()
    )

    # 7. 构造 AlterInboundRequest
    request = command_pb2.AlterInboundRequest(
        tag=inbound_tag,
        operation=op_msg
    )

    # 8. 发送请求
    channel = grpc.insecure_channel(server_addr)
    stub = command_pb2_grpc.HandlerServiceStub(channel)
    response = stub.AlterInbound(request)
    print("✅ 添加用户成功:", response)
    channel.close()

# 🔧 示例调用
if __name__ == "__main__":
    add_shadowsocks_user_via_grpc(
        email="newuser@example.com",
        password="testpass123",
        cipher="AES_128_GCM"  # 支持 AES_128_GCM / AES_256_GCM / XCHACHA20_POLY1305 等
    )
