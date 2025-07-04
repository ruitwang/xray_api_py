import grpc
from google.protobuf import any_pb2

# ===== 以下 import 请使用你通过 protoc 编译的文件路径 =====
import sys
sys.path.append('./gen')

from proxy.shadowsocks import config_pb2 as shadowsocks_pb2
from app.proxyman.command import command_pb2, command_pb2_grpc
from common.protocol import user_pb2
from common.serial import typed_message_pb2

def remove_shadowsocks_user_via_grpc(email, server_addr="127.0.0.1:10085", inbound_tag="ss-inbound"):
    # 构造 RemoveUserOperation
    remove_user_op = command_pb2.RemoveUserOperation(email=email)

    # 封装为 TypedMessage
    op_msg = typed_message_pb2.TypedMessage(
        type="xray.app.proxyman.command.RemoveUserOperation",
        value=remove_user_op.SerializeToString()
    )

    # 构造请求
    request = command_pb2.AlterInboundRequest(
        tag=inbound_tag,
        operation=op_msg
    )

    # 调用 gRPC
    channel = grpc.insecure_channel(server_addr)
    stub = command_pb2_grpc.HandlerServiceStub(channel)
    stub.AlterInbound(request)
    channel.close()

remove_shadowsocks_user_via_grpc(email="newuser@example.com")
