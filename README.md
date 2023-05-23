# PyWeibo
PyWeiboSDK: Sina Weibo Python SDK. 新浪微博 Python SDK, 可以读取用户信息，处理私信、评论等。

# Usage
Run `main.py` to monitor the HTTP 80 port. You can modify the `chatWeibo.py` file to process the messages and events posted by WEIBO server.

```
sudo python main.py 80
```
**Note:** HTTP 80 port requires the `sudo` privileges. If you do not have the `sudo` privileges, a solution is to let the administrator to redirect the 80 port to other ports.

```
iptables -A INPUT -i eth0 -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -i eth0 -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -i eth0 -p tcp --dport 8080 -j ACCEPT
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 20000
```
Then, you can monitor other ports instead of HTTP 80.
```
python main.py 20000
```
