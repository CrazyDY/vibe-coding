#!/usr/bin/env python3
"""
Redis CLI Tool - Support for both standalone and cluster modes

A command-line interface for interacting with Redis servers,
supporting both standalone and cluster deployment modes.
Features:
- Connection pooling for both standalone and cluster modes
- Interactive mode with command auto-completion
- Beautiful colored output using Rich library
"""

import argparse
import sys
import json
from typing import Optional, List, Any
from redis import Redis, ConnectionPool
from redis.cluster import RedisCluster, ClusterNode
from redis.connection import Connection, SSLConnection
from redis.exceptions import RedisError, ConnectionError
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text


# Available Redis commands for auto-completion
REDIS_COMMANDS = [
    # String Commands
    'GET', 'SET', 'MGET', 'MSET', 'DEL', 'EXISTS', 'INCR', 'DECR', 'APPEND', 'STRLEN',
    'SETEX', 'PSETEX', 'SETNX', 'INCRBY', 'DECRBY', 'INCRBYFLOAT', 'GETRANGE', 'SETRANGE',
    'GETSET', 'GETDEL', 'GETEX', 'SUBSTR',
    
    # Hash Commands
    'HGET', 'HSET', 'HMGET', 'HMSET', 'HGETALL', 'HDEL', 'HEXISTS', 'HKEYS', 'HVALS',
    'HLEN', 'HINCRBY', 'HINCRBYFLOAT', 'HSCAN', 'HSETNX', 'HRANDFIELD',
    
    # List Commands
    'LPUSH', 'RPUSH', 'LPOP', 'RPOP', 'LRANGE', 'LLEN', 'LINDEX', 'LINSERT', 'LREM',
    'LSET', 'LTRIM', 'BLPOP', 'BRPOP', 'BRPOPLPUSH', 'RPOPLPUSH', 'LMPOP', 'BLMOVE',
    'LMOVE', 'LPOS',
    
    # Set Commands
    'SADD', 'SMEMBERS', 'SISMEMBER', 'SREM', 'SCARD', 'SINTER', 'SUNION', 'SDIFF',
    'SINTERSTORE', 'SUNIONSTORE', 'SDIFFSTORE', 'SMOVE', 'SPOP', 'SRANDMEMBER', 'SSCAN',
    
    # Sorted Set Commands
    'ZADD', 'ZRANGE', 'ZREVRANGE', 'ZREM', 'ZCARD', 'ZSCORE', 'ZRANK', 'ZREVRANK',
    'ZINCRBY', 'ZCOUNT', 'ZLEXCOUNT', 'ZRANGEBYLEX', 'ZREVRANGEBYLEX', 'ZRANGEBYSCORE',
    'ZREVRANGEBYSCORE', 'ZREMRANGEBYRANK', 'ZREMRANGEBYSCORE', 'ZREMRANGEBYLEX',
    'ZUNIONSTORE', 'ZINTERSTORE', 'ZSCAN', 'ZPOPMAX', 'ZPOPMIN', 'ZRANDMEMBER',
    'ZDIFF', 'ZDIFFSTORE', 'ZINTER', 'ZUNION', 'ZMSCORE',
    
    # Key Management
    'KEYS', 'SCAN', 'TYPE', 'EXPIRE', 'TTL', 'PERSIST', 'RENAME', 'RENAMENX',
    'EXPIREAT', 'PEXPIRE', 'PEXPIREAT', 'PTTL', 'OBJECT', 'DUMP', 'RESTORE',
    'MOVE', 'COPY', 'SORT', 'TOUCH', 'UNLINK', 'WAIT',
    
    # Server Commands
    'INFO', 'DBSIZE', 'FLUSHDB', 'FLUSHALL', 'PING', 'TIME', 'CLIENT', 'CONFIG',
    'SAVE', 'BGSAVE', 'LASTSAVE', 'SHUTDOWN', 'MONITOR', 'SLAVEOF', 'REPLICAOF',
    'ROLE', 'DEBUG', 'MEMORY', 'ACL', 'MODULE', 'COMMAND', 'LATENCY', 'CLUSTER',
    
    # Connection Commands
    'AUTH', 'ECHO', 'SELECT', 'QUIT', 'SWAPDB',
    
    # Pub/Sub Commands
    'SUBSCRIBE', 'UNSUBSCRIBE', 'PSUBSCRIBE', 'PUNSUBSCRIBE', 'PUBLISH', 'PUBSUB',
    
    # Transaction Commands
    'MULTI', 'EXEC', 'DISCARD', 'WATCH', 'UNWATCH',
    
    # Scripting Commands
    'EVAL', 'EVALSHA', 'SCRIPT',
    
    # Cluster Commands
    'CLUSTER NODES', 'CLUSTER SLOTS', 'CLUSTER INFO', 'CLUSTER KEYSLOT',
    'CLUSTER COUNTKEYSINSLOT', 'CLUSTER GETKEYSINSLOT', 'CLUSTER ADDSLOTS',
    'CLUSTER DELSLOTS', 'CLUSTER FAILOVER', 'CLUSTER RESET', 'CLUSTER SETSLOT',
    'CLUSTER MEET', 'CLUSTER FORGET', 'CLUSTER REPLICATE', 'CLUSTER SAVECONFIG',
    'CLUSTER BUMPEPOCH', 'CLUSTER MYID', 'CLUSTER LINKS',
]



class RedisCommandCompleter(Completer):
    """Auto-completion for Redis commands."""
    
    def __init__(self):
        self.commands = REDIS_COMMANDS
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.upper()
        words = text.split()
        
        if not words:
            return
        
        current_word = words[-1] if words else ''
        word_index = len(words) - 1
        
        # If first word, suggest commands
        if word_index == 0:
            for cmd in self.commands:
                if cmd.upper().startswith(current_word.upper()):
                    yield Completion(
                        cmd.upper(),
                        start_position=-len(current_word),
                        style='fg:ansiblue bold'
                    )
        # For subsequent words, we could add key/argument suggestions
        # This is a basic implementation; can be extended


class RedisCLI:
    """Redis Command Line Interface supporting standalone and cluster modes."""

    def __init__(self, host: str = 'localhost', port: int = 6379,
                 password: Optional[str] = None, db: int = 0,
                 cluster_mode: bool = False, startup_nodes: Optional[List[dict]] = None,
                 ssl: bool = False, decode_responses: bool = True,
                 max_connections: int = 50):
        """
        Initialize Redis connection with connection pooling.

        Args:
            host: Redis server host (for standalone mode)
            port: Redis server port (for standalone mode)
            password: Redis password
            db: Database number (only for standalone mode)
            cluster_mode: Whether to use cluster mode
            startup_nodes: List of cluster nodes [{'host': '...', 'port': ...}, ...]
            ssl: Whether to use SSL connection
            decode_responses: Whether to decode responses to strings
            max_connections: Maximum number of connections in the pool
        """
        self.cluster_mode = cluster_mode
        self.console = Console()
        self.client = self._create_connection(
            host, port, password, db, startup_nodes, ssl, decode_responses, max_connections
        )

    def _create_connection(self, host: str, port: int, password: Optional[str],
                           db: int, startup_nodes: Optional[List[dict]],
                           ssl: bool, decode_responses: bool, max_connections: int):
        """Create Redis connection with connection pooling based on mode."""
        try:
            if self.cluster_mode:
                if not startup_nodes:
                    startup_nodes = [{'host': host, 'port': port}]
                
                # Create ClusterNode objects from startup nodes dict
                nodes = []
                for node_info in startup_nodes:
                    node = ClusterNode(
                        host=node_info['host'],
                        port=node_info['port'],
                    )
                    nodes.append(node)
                
                # Prepare common kwargs for cluster connection
                cluster_kwargs = {
                    'startup_nodes': nodes,
                    'password': password,
                    'ssl': ssl,
                    'decode_responses': decode_responses,
                    'require_full_coverage': False,
                }
                
                return RedisCluster(**cluster_kwargs)
            else:
                # Choose connection class based on SSL setting
                connection_class = SSLConnection if ssl else Connection
                
                # Create standalone connection pool
                connection_pool = ConnectionPool(
                    connection_class=connection_class,
                    host=host,
                    port=port,
                    password=password,
                    db=db,
                    decode_responses=decode_responses,
                    max_connections=max_connections,
                )
                
                return Redis(connection_pool=connection_pool)
                
        except ConnectionError as e:
            self.console.print(f"[bold red]✗ Error:[/bold red] Failed to connect to Redis: {e}")
            sys.exit(1)
        except RedisError as e:
            self.console.print(f"[bold red]✗ Error:[/bold red] Redis error: {e}")
            sys.exit(1)

    def execute_command(self, command: str, *args) -> Any:
        """Execute a Redis command and return the result."""
        try:
            # Convert command to uppercase
            cmd = command.upper()
            
            # Execute the command
            result = self.client.execute_command(cmd, *args)
            return result
        except RedisError as e:
            raise RedisError(f"Command failed: {e}")

    def format_output_rich(self, result: Any):
        """Format the result for beautiful display using Rich."""
        if result is None:
            return Text("(nil)", style="gray italic")
        elif isinstance(result, bool):
            return Text("1" if result else "0", style="green bold" if result else "red")
        elif isinstance(result, (list, tuple)):
            if not result:
                return Text("(empty list or set)", style="gray italic")
            
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("#", style="cyan", justify="right")
            table.add_column("Value", style="white")
            
            for i, item in enumerate(result):
                formatted_item = self.format_output_rich(item)
                table.add_row(f"{i + 1})", formatted_item)
            
            return table
        elif isinstance(result, dict):
            if not result:
                return Text("(empty hash)", style="gray italic")
            
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("#", style="cyan", justify="right")
            table.add_column("Key", style="green bold")
            table.add_column("Value", style="white")
            
            for i, (k, v) in enumerate(result.items()):
                formatted_value = self.format_output_rich(v)
                table.add_row(f"{i + 1})", f'"{k}"', formatted_value)
            
            return table
        elif isinstance(result, bytes):
            return Text(result.decode('utf-8'), style="yellow")
        elif isinstance(result, (int, float)):
            return Text(str(result), style="magenta bold")
        elif isinstance(result, str):
            # Check if it's a number string
            try:
                num = float(result)
                return Text(result, style="magenta bold")
            except ValueError:
                return Text(result, style="white")
        else:
            return Text(str(result), style="white")

    def print_result(self, result: Any):
        """Print the result with beautiful formatting."""
        formatted = self.format_output_rich(result)
        self.console.print(formatted)

    def print_error(self, message: str):
        """Print error message with styling."""
        self.console.print(f"[bold red]✗ Error:[/bold red] {message}")

    def print_success(self, message: str):
        """Print success message with styling."""
        self.console.print(f"[bold green]✓[/bold green] {message}")

    def interactive_mode(self):
        """Run the CLI in interactive mode with auto-completion."""
        # Create welcome panel
        mode_text = "[bold cyan]Cluster Mode[/bold cyan]" if self.cluster_mode else "[bold green]Standalone Mode[/bold green]"
        welcome_panel = Panel(
            f"[bold white]Redis CLI Tool[/bold white]\n\n"
            f"Connection: {mode_text}\n"
            f"Type [yellow]'help'[/yellow] for available commands, [yellow]'exit'[/yellow] to quit.\n"
            f"Use [cyan]TAB[/cyan] for auto-completion.",
            title="[bold blue]🔴 Redis[/bold blue]",
            border_style="blue",
            padding=(1, 2),
        )
        self.console.print(welcome_panel)
        self.console.print()

        # Create prompt session with completion and history
        completer = RedisCommandCompleter()
        
        session = PromptSession(
            completer=completer,
            complete_while_typing=True,
            auto_suggest=AutoSuggestFromHistory(),
            history=FileHistory('~/.redis_cli_history'),
            enable_history_search=True,
        )

        while True:
            try:
                # Create styled prompt
                prompt_text = "[bold green]redis[/bold green]> " if not self.cluster_mode else "[bold cyan]redis-cluster[/bold cyan]> "
                
                user_input = session.prompt(prompt_text, style='class:prompt')
                user_input = user_input.strip()

                if not user_input:
                    continue

                if user_input.lower() in ('exit', 'quit', 'q'):
                    goodbye_panel = Panel("[bold white]Goodbye![/bold white]", border_style="green", padding=(0, 2))
                    self.console.print(goodbye_panel)
                    break

                if user_input.lower() == 'help':
                    self.show_help_rich()
                    continue

                # Parse command and arguments
                parts = user_input.split()
                command = parts[0].upper()
                args = parts[1:]

                # Execute command with timing
                import time
                start_time = time.time()
                
                result = self.execute_command(command, *args)
                
                elapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                # Print result
                self.print_result(result)
                
                # Show execution time for slow commands
                if elapsed > 100:
                    self.console.print(f"[dim]({elapsed:.2f}ms)[/dim]")

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Use 'exit' to quit.[/yellow]")
            except RedisError as e:
                self.print_error(str(e))
            except EOFError:
                goodbye_panel = Panel("[bold white]Goodbye![/bold white]", border_style="green", padding=(0, 2))
                self.console.print(goodbye_panel)
                break

    def show_help_rich(self):
        """Display available commands with beautiful Rich formatting."""
        
        # Create main help panel
        self.console.print()
        self.console.print("[bold underline]Available Commands[/bold underline]\n")
        
        # Command categories
        categories = {
            "String Commands": [
                ("GET <key>", "Get the value of key"),
                ("SET <key> <value>", "Set the value of key"),
                ("MGET <key> [key ...]", "Get the values of all given keys"),
                ("MSET <key> <value> [key value ...]", "Set multiple keys to multiple values"),
                ("DEL <key> [key ...]", "Delete one or more keys"),
                ("EXISTS <key> [key ...]", "Check if key exists"),
                ("INCR <key>", "Increment the integer value of key"),
                ("DECR <key>", "Decrement the integer value of key"),
                ("APPEND <key> <value>", "Append value to key"),
                ("STRLEN <key>", "Get the length of the string value"),
            ],
            "Hash Commands": [
                ("HGET <key> <field>", "Get the value of a hash field"),
                ("HSET <key> <field> <value>", "Set the value of a hash field"),
                ("HMGET <key> <field> [field ...]", "Get the values of multiple hash fields"),
                ("HGETALL <key>", "Get all fields and values of a hash"),
                ("HDEL <key> <field> [field ...]", "Delete one or more hash fields"),
                ("HEXISTS <key> <field>", "Check if a hash field exists"),
                ("HKEYS <key>", "Get all fields in a hash"),
                ("HVALS <key>", "Get all values in a hash"),
            ],
            "List Commands": [
                ("LPUSH <key> <value> [value ...]", "Prepend values to a list"),
                ("RPUSH <key> <value> [value ...]", "Append values to a list"),
                ("LPOP <key>", "Remove and get the first element"),
                ("RPOP <key>", "Remove and get the last element"),
                ("LRANGE <key> <start> <stop>", "Get a range of elements from a list"),
                ("LLEN <key>", "Get the length of a list"),
            ],
            "Set Commands": [
                ("SADD <key> <member> [member ...]", "Add members to a set"),
                ("SMEMBERS <key>", "Get all members of a set"),
                ("SISMEMBER <key> <member>", "Check if member is in a set"),
                ("SREM <key> <member> [member ...]", "Remove members from a set"),
                ("SCARD <key>", "Get the number of members in a set"),
            ],
            "Sorted Set Commands": [
                ("ZADD <key> <score> <member>", "Add members to a sorted set"),
                ("ZRANGE <key> <start> <stop> [WITHSCORES]", "Get a range of members"),
                ("ZREVRANGE <key> <start> <stop>", "Get range in reverse order"),
                ("ZREM <key> <member> [member ...]", "Remove members from sorted set"),
                ("ZCARD <key>", "Get the number of members"),
                ("ZSCORE <key> <member>", "Get the score of a member"),
            ],
            "Key Management": [
                ("KEYS <pattern>", "Find all keys matching pattern"),
                ("SCAN <cursor> [MATCH pattern]", "Incrementally iterate keys"),
                ("TYPE <key>", "Determine the type stored at key"),
                ("EXPIRE <key> <seconds>", "Set expiration time for key"),
                ("TTL <key>", "Get time to live for key"),
                ("PERSIST <key>", "Remove expiration from key"),
                ("RENAME <old_key> <new_key>", "Rename a key"),
            ],
            "Server Commands": [
                ("INFO [section]", "Get server information"),
                ("DBSIZE", "Return the number of keys"),
                ("PING", "Ping the server"),
                ("TIME", "Return current server time"),
            ],
        }
        
        # Add cluster commands if in cluster mode
        if self.cluster_mode:
            categories["Cluster Commands"] = [
                ("CLUSTER NODES", "Get cluster node information"),
                ("CLUSTER SLOTS", "Get cluster slot mappings"),
                ("CLUSTER INFO", "Get cluster state information"),
                ("CLUSTER KEYSLOT <key>", "Get the slot for a key"),
            ]
        
        # Display each category
        for category, commands in categories.items():
            self.console.print(f"\n[bold cyan]● {category}[/bold cyan]")
            self.console.print("─" * 60)
            
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Command", style="yellow bold", width=35)
            table.add_column("Description", style="white")
            
            for cmd, desc in commands:
                table.add_row(cmd, desc)
            
            self.console.print(table)
        
        # General commands
        self.console.print(f"\n[bold cyan]● General[/bold cyan]")
        self.console.print("─" * 60)
        self.console.print("  [yellow]help[/yellow]              - Show this help message")
        self.console.print("  [yellow]exit/quit/q[/yellow]     - Exit the CLI")
        self.console.print("  [cyan]TAB[/cyan]               - Auto-completion")
        self.console.print("  [cyan]↑↓[/cyan]                - Navigate history")
        
        # Examples
        self.console.print(f"\n[bold green]● Examples[/bold green]")
        self.console.print("─" * 60)
        examples = [
            "SET mykey hello",
            "GET mykey",
            "LPUSH mylist value1 value2",
            "LRANGE mylist 0 -1",
            "HSET myhash field1 value1",
            "HGETALL myhash",
            "ZADD myzset 1 member1 2 member2",
            "KEYS *",
        ]
        if self.cluster_mode:
            examples.append("CLUSTER NODES")
        
        for example in examples:
            self.console.print(f"  [dim]>[/dim] [white]{example}[/white]")
        
        self.console.print()


def parse_startup_nodes(nodes_str: str) -> List[dict]:
    """Parse startup nodes from string format 'host1:port1,host2:port2,...'"""
    nodes = []
    for node in nodes_str.split(','):
        node = node.strip()
        if ':' in node:
            host, port = node.rsplit(':', 1)
            nodes.append({'host': host, 'port': int(port)})
        else:
            nodes.append({'host': node, 'port': 6379})
    return nodes


def main():
    parser = argparse.ArgumentParser(
        description='Redis CLI Tool - Support for standalone and cluster modes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Connect to localhost:6379 (standalone)
  %(prog)s -h redis.example.com     # Connect to specific host
  %(prog)s -p 6380 -a mypassword    # Connect with port and password
  %(prog)s --cluster                # Enable cluster mode
  %(prog)s --cluster --nodes "node1:7000,node2:7001,node3:7002"  # Cluster with nodes
  %(prog)s --ssl                    # Connect using SSL
  %(prog)s GET mykey                # Execute single command and exit
        """
    )

    parser.add_argument('-H', '--host', default='localhost',
                        help='Redis server hostname (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=6379,
                        help='Redis server port (default: 6379)')
    parser.add_argument('-a', '--password', default=None,
                        help='Redis server password')
    parser.add_argument('-n', '--db', type=int, default=0,
                        help='Database number (default: 0, only for standalone mode)')
    parser.add_argument('--cluster', action='store_true',
                        help='Enable Redis Cluster mode')
    parser.add_argument('--nodes', type=str, default=None,
                        help='Cluster startup nodes (format: "host1:port1,host2:port2,...")')
    parser.add_argument('--ssl', action='store_true',
                        help='Use SSL connection')
    parser.add_argument('--no-decode', action='store_true',
                        help='Do not decode responses (return bytes)')
    parser.add_argument('-c', '--command', nargs='+', metavar='CMD',
                        help='Execute a single command and exit')
    parser.add_argument('--json', action='store_true',
                        help='Output results in JSON format (for single command execution)')

    args = parser.parse_args()

    # Parse startup nodes if provided
    startup_nodes = None
    if args.nodes:
        startup_nodes = parse_startup_nodes(args.nodes)

    # Create CLI instance
    cli = RedisCLI(
        host=args.host,
        port=args.port,
        password=args.password,
        db=args.db,
        cluster_mode=args.cluster,
        startup_nodes=startup_nodes,
        ssl=args.ssl,
        decode_responses=not args.no_decode,
    )

    # Execute single command or enter interactive mode
    if args.command:
        try:
            command = args.command[0]
            cmd_args = args.command[1:]
            result = cli.execute_command(command, *cmd_args)
            
            if args.json:
                print(json.dumps(result, default=str))
            else:
                cli.print_result(result)
        except RedisError as e:
            cli.print_error(str(e))
            sys.exit(1)
    else:
        cli.interactive_mode()


if __name__ == '__main__':
    main()
