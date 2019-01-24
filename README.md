# Load balanced Tor SOCKS Proxy
## It's just Tor behind Haproxy

### Design
![Diagram](https://raw.githubusercontent.com/iakinsey/tor-haproxy/master/diagram.png)

### Build

```
docker build -t tor-proxy .
```

### Run
```
docker run -d -p 5566:5566 -p 4444:4444 tor-proxy
```

### Setting number of instances

Change `TOR_PROXY_COUNT` in `start.py`.
