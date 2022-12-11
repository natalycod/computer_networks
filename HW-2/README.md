Запуск образа:

docker build -t find_mtu .
docker run -i -t find_mtu

Запуск программы внутри запущенного образа:
python3 find_mtu.py --address {host}

Где {host} - это ip или имя хоста, для которого требуется найти MTU. Например:
python3 find_mtu.py --address google.com
