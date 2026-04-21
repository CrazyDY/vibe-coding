# Redis CLI Tool

A powerful command-line interface for interacting with Redis servers, supporting both **standalone** and **cluster** deployment modes.

## Features

- 🚀 **Dual Mode Support**: Seamlessly switch between standalone and cluster modes
- 🔒 **SSL/TLS Encryption**: Secure connections with SSL support
- 🎨 **Beautiful Output**: Colorful, formatted results using Rich library
- ⌨️ **Interactive Mode**: Command auto-completion with TAB support
- 📜 **Command History**: Persistent history storage
- ⚡ **Connection Pooling**: Efficient connection management
- 📊 **Rich Formatting**: Tables, panels, and syntax highlighting for results
- ⏱️ **Performance Metrics**: Shows execution time for slow commands

## Requirements

- Python 3.7+
- Redis server (standalone or cluster)

### Python Dependencies

```bash
pip install redis prompt-toolkit rich
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vibe-coding
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# Or manually:
pip install redis prompt-toolkit rich
```

3. Make the script executable (optional):
```bash
chmod +x redis_cli.py
```

## Usage

### Basic Connection (Standalone Mode)

```bash
# Connect to localhost:6379 (default)
./redis_cli.py

# Connect to specific host
./redis_cli.py -H redis.example.com

# Connect with port and password
./redis_cli.py -p 6380 -a mypassword

# Connect to specific database
./redis_cli.py -n 2
```

### Cluster Mode

```bash
# Enable cluster mode with default node
./redis_cli.py --cluster

# Specify multiple cluster nodes
./redis_cli.py --cluster --nodes "node1:7000,node2:7001,node3:7002"
```

### SSL Connection

```bash
# Connect using SSL
./redis_cli.py --ssl

# SSL with authentication
./redis_cli.py --ssl -a mypassword -H secure-redis.example.com
```

### Single Command Execution

```bash
# Execute a single command and exit
./redis_cli.py GET mykey

# Execute with JSON output
./redis_cli.py --json HGETALL user:123

# Execute SET command
./redis_cli.py SET mykey "hello world"

# Execute command on cluster
./redis_cli.py --cluster CLUSTER INFO
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-H, --host` | Redis server hostname | `localhost` |
| `-p, --port` | Redis server port | `6379` |
| `-a, --password` | Redis server password | `None` |
| `-n, --db` | Database number (standalone only) | `0` |
| `--cluster` | Enable Redis Cluster mode | `False` |
| `--nodes` | Cluster startup nodes (`host1:port1,host2:port2,...`) | `None` |
| `--ssl` | Use SSL connection | `False` |
| `--no-decode` | Return bytes instead of strings | `False` |
| `-c, --command` | Execute single command and exit | `None` |
| `--json` | Output results in JSON format | `False` |

## Interactive Mode

When launched without the `-c` option, the tool enters interactive mode:

```bash
$ ./redis_cli.py

╭───────────────────── 🔴 Redis ─────────────────────╮
│                                                    │
│              Redis CLI Tool                        │
│                                                    │
│  Connection: Standalone Mode                       │
│  Type 'help' for available commands, 'exit' to    │
│  quit.                                             │
│  Use TAB for auto-completion.                      │
│                                                    │
╰────────────────────────────────────────────────────╯

redis> SET greeting "Hello World"
✓ OK
redis> GET greeting
"Hello World"
redis> 
```

### Features in Interactive Mode

- **TAB Completion**: Auto-complete Redis commands
- **Command History**: Navigate through previous commands with ↑/↓ arrows
- **Syntax Highlighting**: Colored output for better readability
- **Help System**: Type `help` to see available commands
- **Exit Commands**: Use `exit`, `quit`, or `q` to exit

### Supported Command Categories

The tool supports all major Redis command categories:

- **String Commands**: GET, SET, MGET, MSET, DEL, INCR, DECR, etc.
- **Hash Commands**: HGET, HSET, HMGET, HGETALL, HDEL, etc.
- **List Commands**: LPUSH, RPUSH, LPOP, RPOP, LRANGE, etc.
- **Set Commands**: SADD, SMEMBERS, SISMEMBER, SREM, etc.
- **Sorted Set Commands**: ZADD, ZRANGE, ZREVRANGE, ZREM, etc.
- **Key Management**: KEYS, SCAN, TYPE, EXPIRE, TTL, etc.
- **Server Commands**: INFO, DBSIZE, PING, CONFIG, etc.
- **Pub/Sub Commands**: SUBSCRIBE, PUBLISH, etc.
- **Transaction Commands**: MULTI, EXEC, DISCARD, etc.
- **Cluster Commands**: CLUSTER NODES, CLUSTER SLOTS, etc.

## Examples

### String Operations
```bash
redis> SET name "John Doe"
✓ OK
redis> GET name
"John Doe"
redis> INCR counter
(integer) 1
```

### Hash Operations
```bash
redis> HSET user:1001 name "Alice" email "alice@example.com"
(integer) 2
redis> HGETALL user:1001
1) "name"    "Alice"
2) "email"   "alice@example.com"
```

### List Operations
```bash
redis> LPUSH tasks "task1" "task2" "task3"
(integer) 3
redis> LRANGE tasks 0 -1
1) "task3"
2) "task2"
3) "task1"
```

### Cluster Information
```bash
redis-cluster> CLUSTER INFO
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_open:0
...
```

## Project Structure

```
vibe-coding/
├── redis_cli.py      # Main CLI tool
├── README.md         # This file
└── .gitignore        # Git ignore rules
```

## Advanced Usage

### Connection Pooling

The tool automatically uses connection pooling for efficient resource management:
- Maximum 50 connections by default
- Connections are reused across commands
- Automatic connection recovery

### Error Handling

The tool provides clear error messages for:
- Connection failures
- Authentication errors
- Invalid commands
- Network issues

## Troubleshooting

### Connection Refused
```bash
# Check if Redis is running
redis-cli ping

# Verify host and port
./redis_cli.py -H correct-host -p correct-port
```

### Authentication Failed
```bash
# Provide correct password
./redis_cli.py -a your_password
```

### Cluster Mode Issues
```bash
# Ensure cluster is properly configured
# Provide multiple startup nodes for reliability
./redis_cli.py --cluster --nodes "node1:7000,node2:7001,node3:7002"
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Acknowledgments

- [Redis](https://redis.io/) - The amazing in-memory data store
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal output
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Interactive command-line features