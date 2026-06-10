# client.py

import grpc  # Подключение к серверу
import greeting_pb2
import greeting_pb2_grpc


def run():
    # Создаём канал — соединение с сервером на localhost:50051
    channel = grpc.insecure_channel('localhost:50051')

    # Создаём stub — локальный объект, который вызывает удалённый метод
    stub = greeting_pb2_grpc.GreeterStub(channel)

    # Формируем сообщение запроса
    request = greeting_pb2.HelloRequest(name="Мир")

    # Вызываем удалённую функцию SayHello (gRPC автоматически сериализует запрос и десериализует ответ)
    response = stub.SayHello(request)

    # Выводим ответ от сервера
    print("Ответ сервера:", response.message)


if __name__ == '__main__':
    run()
