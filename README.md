# xray_api_py
Xray python api example

1 下载安装 protobuf 和 grpcio

pip install grpcio grpcio-tools

2 获取并编译 proto 文件
你可以把官方的 command.proto 下载下来（路径示例）：

xray-core/app/proxyman/command/command.proto

然后用命令生成 Python 代码：

python -m grpc_tools.protoc -I. --python_out=./gen --grpc_python_out=. command.proto

生成的 command_pb2.py 和 command_pb2_grpc.py 就是你调用用的库。
