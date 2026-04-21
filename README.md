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

---

# Redis CLI 工具（中文版）

一个强大的命令行界面工具，用于与 Redis 服务器交互，支持**单机**和**集群**两种部署模式。

## 功能特性

- 🚀 **双模式支持**: 无缝切换单机和集群模式
- 🔒 **SSL/TLS 加密**: 支持 SSL 安全连接
- 🎨 **美观输出**: 使用 Rich 库提供彩色格式化的结果
- ⌨️ **交互模式**: 支持 TAB 键自动补全命令
- 📜 **命令历史**: 持久化存储命令历史
- ⚡ **连接池**: 高效的连接管理
- 📊 **丰富格式化**: 表格、面板和语法高亮显示结果
- ⏱️ **性能指标**: 显示慢命令的执行时间

## 环境要求

- Python 3.7+
- Redis 服务器（单机或集群）

### Python 依赖

```bash
pip install redis prompt-toolkit rich
```

## 安装步骤

1. 克隆仓库：
```bash
git clone <repository-url>
cd vibe-coding
```

2. 安装依赖：
```bash
pip install -r requirements.txt
# 或者手动安装：
pip install redis prompt-toolkit rich
```

3. 使脚本可执行（可选）：
```bash
chmod +x redis_cli.py
```

## 使用方法

### 基本连接（单机模式）

```bash
# 连接到 localhost:6379（默认）
./redis_cli.py

# 连接到指定主机
./redis_cli.py -H redis.example.com

# 指定端口和密码连接
./redis_cli.py -p 6380 -a mypassword

# 连接到指定数据库
./redis_cli.py -n 2
```

### 集群模式

```bash
# 启用集群模式，使用默认节点
./redis_cli.py --cluster

# 指定多个集群节点
./redis_cli.py --cluster --nodes "node1:7000,node2:7001,node3:7002"
```

### SSL 连接

```bash
# 使用 SSL 连接
./redis_cli.py --ssl

# SSL 加认证
./redis_cli.py --ssl -a mypassword -H secure-redis.example.com
```

### 单条命令执行

```bash
# 执行单条命令后退出
./redis_cli.py GET mykey

# 以 JSON 格式输出
./redis_cli.py --json HGETALL user:123

# 执行 SET 命令
./redis_cli.py SET mykey "hello world"

# 在集群上执行命令
./redis_cli.py --cluster CLUSTER INFO
```

### 命令行选项

| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `-H, --host` | Redis 服务器主机名 | `localhost` |
| `-p, --port` | Redis 服务器端口 | `6379` |
| `-a, --password` | Redis 服务器密码 | `无` |
| `-n, --db` | 数据库编号（仅单机模式） | `0` |
| `--cluster` | 启用 Redis 集群模式 | `False` |
| `--nodes` | 集群启动节点（`host1:port1,host2:port2,...`） | `无` |
| `--ssl` | 使用 SSL 连接 | `False` |
| `--no-decode` | 返回字节而非字符串 | `False` |
| `-c, --command` | 执行单条命令后退出 | `无` |
| `--json` | 以 JSON 格式输出结果 | `False` |

## 交互模式

在不使用 `-c` 选项启动时，工具会进入交互模式：

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

### 交互模式功能

- **TAB 补全**: 自动补全 Redis 命令
- **命令历史**: 使用 ↑/↓ 箭头浏览之前的命令
- **语法高亮**: 彩色输出提高可读性
- **帮助系统**: 输入 `help` 查看可用命令
- **退出命令**: 使用 `exit`、`quit` 或 `q` 退出

### 支持的命令分类

本工具支持所有主要的 Redis 命令类别：

- **字符串命令**: GET, SET, MGET, MSET, DEL, INCR, DECR 等
- **哈希命令**: HGET, HSET, HMGET, HGETALL, HDEL 等
- **列表命令**: LPUSH, RPUSH, LPOP, RPOP, LRANGE 等
- **集合命令**: SADD, SMEMBERS, SISMEMBER, SREM 等
- **有序集合命令**: ZADD, ZRANGE, ZREVRANGE, ZREM 等
- **键管理**: KEYS, SCAN, TYPE, EXPIRE, TTL 等
- **服务器命令**: INFO, DBSIZE, PING, CONFIG 等
- **发布/订阅命令**: SUBSCRIBE, PUBLISH 等
- **事务命令**: MULTI, EXEC, DISCARD 等
- **集群命令**: CLUSTER NODES, CLUSTER SLOTS 等

## 使用示例

### 字符串操作
```bash
redis> SET name "John Doe"
✓ OK
redis> GET name
"John Doe"
redis> INCR counter
(integer) 1
```

### 哈希操作
```bash
redis> HSET user:1001 name "Alice" email "alice@example.com"
(integer) 2
redis> HGETALL user:1001
1) "name"    "Alice"
2) "email"   "alice@example.com"
```

### 列表操作
```bash
redis> LPUSH tasks "task1" "task2" "task3"
(integer) 3
redis> LRANGE tasks 0 -1
1) "task3"
2) "task2"
3) "task1"
```

### 集群信息
```bash
redis-cluster> CLUSTER INFO
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_open:0
...
```

## 项目结构

```
vibe-coding/
├── redis_cli.py      # 主 CLI 工具
├── README.md         # 本文件
└── .gitignore        # Git 忽略规则
```

## 高级用法

### 连接池

本工具自动使用连接池进行高效的资源管理：
- 默认最大 50 个连接
- 连接在命令间复用
- 自动连接恢复

### 错误处理

本工具为以下情况提供清晰的错误消息：
- 连接失败
- 认证错误
- 无效命令
- 网络问题

## 故障排除

### 连接被拒绝
```bash
# 检查 Redis 是否运行
redis-cli ping

# 验证主机和端口
./redis_cli.py -H correct-host -p correct-port
```

### 认证失败
```bash
# 提供正确的密码
./redis_cli.py -a your_password
```

### 集群模式问题
```bash
# 确保集群配置正确
# 提供多个启动节点以提高可靠性
./redis_cli.py --cluster --nodes "node1:7000,node2:7001,node3:7002"
```

## 许可证

MIT License

## 贡献

欢迎贡献！请随时提交问题和拉取请求。

## 致谢

- [Redis](https://redis.io/) - 出色的内存数据存储
- [Rich](https://github.com/Textualize/rich) - 美观的终端输出
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - 交互式命令行功能