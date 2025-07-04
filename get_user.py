import grpc
from google.protobuf import any_pb2

# ===== 以下 import 请使用你通过 protoc 编译的文件路径 =====
import sys
sys.path.append('./gen')

from proxy.shadowsocks import config_pb2 as shadowsocks_pb2
from app.proxyman.command import command_pb2, command_pb2_grpc
from common.protocol import user_pb2
from common.serial import typed_message_pb2

def parse_ss_account(raw_bytes):
    account = shadowsocks_pb2.Account()
    account.ParseFromString(raw_bytes)
    cipher_map = {
        5: "AES-128-GCM",
        6: "AES-256-GCM",
        7: "CHACHA20-POLY1305",
        8: "XCHACHA20-POLY1305",
        9: "NONE"
    }
    return {
        "password": account.password,
        "cipher_type": cipher_map.get(account.cipher_type, f"UNKNOWN({account.cipher_type})"),
        "iv_check": account.iv_check
    }

def get_inbound_users_with_account_parsing(server_addr="127.0.0.1:10085", tag="ss-inbound"):
    # 连接 gRPC 接口
    channel = grpc.insecure_channel(server_addr)
    stub = command_pb2_grpc.HandlerServiceStub(channel)

    request = command_pb2.GetInboundUserRequest(tag=tag)
    response = stub.GetInboundUsers(request)

    print(f"📋 Inbound Tag: {tag}")
    for user in response.users:
        print(f"📨 Email: {user.email}")
        print(f"🔐 Account Type: {user.account.type}")

        # 尝试解析 Shadowsocks 账号信息
        if user.account.type == "xray.proxy.shadowsocks.Account":
            try:
                parsed = parse_ss_account(user.account.value)
                print(f"  🔑 Password     : {parsed['password']}")
                print(f"  🔐 Cipher       : {parsed['cipher_type']}")
                print(f"  🧪 IV Check     : {parsed['iv_check']}")
            except Exception as e:
                print("  ⚠️ 解析失败:", e)
        else:
            print(f"📦 Account (Raw): {user.account.value}")

        print("-" * 40)

    channel.close()

# 示例调用
if __name__ == "__main__":
    get_inbound_users_with_account_parsing()
