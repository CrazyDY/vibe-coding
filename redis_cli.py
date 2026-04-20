#!/usr/bin/env python3
"""
Redis CLI Tool - Support for both standalone and cluster modes

A command-line interface for interacting with Redis servers,
supporting both standalone and cluster deployment modes.
"""

import argparse
import sys
import json
from typing import Optional, List, Any
from redis import Redis
from redis.cluster import RedisCluster
from redis.exceptions import RedisError, ConnectionError


class RedisCLI:
    """Redis Command Line Interface supporting standalone and cluster modes."""

    def __init__(self, host: str = 'localhost', port: int = 6379,
                 password: Optional[str] = None, db: int = 0,
                 cluster_mode: bool = False, startup_nodes: Optional[List[dict]] = None,
                 ssl: bool = False, decode_responses: bool = True):
        """
        Initialize Redis connection.

        Args:
            host: Redis server host (for standalone mode)
            port: Redis server port (for standalone mode)
            password: Redis password
            db: Database number (only for standalone mode)
            cluster_mode: Whether to use cluster mode
            startup_nodes: List of cluster nodes [{'host': '...', 'port': ...}, ...]
            ssl: Whether to use SSL connection
            decode_responses: Whether to decode responses to strings
        """
        self.cluster_mode = cluster_mode
        self.client = self._create_connection(
            host, port, password, db, startup_nodes, ssl, decode_responses
        )

    def _create_connection(self, host: str, port: int, password: Optional[str],
                           db: int, startup_nodes: Optional[List[dict]],
                           ssl: bool, decode_responses: bool):
        """Create Redis connection based on mode."""
        try:
            if self.cluster_mode:
                if not startup_nodes:
                    startup_nodes = [{'host': host, 'port': port}]
                
                return RedisCluster(
                    startup_nodes=startup_nodes,
                    password=password,
                    ssl=ssl,
                    decode_responses=decode_responses,
                    skip_full_coverage_check=True,
                )
            else:
                return Redis(
                    host=host,
                    port=port,
                    password=password,
                    db=db,
                    ssl=ssl,
                    decode_responses=decode_responses,
                )
        except ConnectionError as e:
            print(f"Error: Failed to connect to Redis: {e}", file=sys.stderr)
            sys.exit(1)
        except RedisError as e:
            print(f"Error: Redis error: {e}", file=sys.stderr)
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

    def format_output(self, result: Any) -> str:
        """Format the result for display."""
        if result is None:
            return "(nil)"
        elif isinstance(result, bool):
            return "1" if result else "0"
        elif isinstance(result, (list, tuple)):
            formatted_items = []
            for i, item in enumerate(result):
                formatted_items.append(f"{i + 1}) {self.format_output(item)}")
            return "\n".join(formatted_items) if formatted_items else "(empty list or set)"
        elif isinstance(result, dict):
            formatted_items = []
            for i, (k, v) in enumerate(result.items()):
                formatted_items.append(f"{i + 1}) \"{k}\"\n   {self.format_output(v)}")
            return "\n".join(formatted_items) if formatted_items else "(empty hash)"
        elif isinstance(result, bytes):
            return result.decode('utf-8')
        else:
            return str(result)

    def interactive_mode(self):
        """Run the CLI in interactive mode."""
        print(f"Redis CLI {'(Cluster Mode)' if self.cluster_mode else '(Standalone Mode)'}")
        print("Type 'help' for available commands, 'exit' to quit.")
        print()

        while True:
            try:
                prompt = "redis> " if not self.cluster_mode else "redis-cluster> "
                user_input = input(prompt).strip()

                if not user_input:
                    continue

                if user_input.lower() in ('exit', 'quit', 'q'):
                    print("Goodbye!")
                    break

                if user_input.lower() == 'help':
                    self.show_help()
                    continue

                # Parse command and arguments
                parts = user_input.split()
                command = parts[0]
                args = parts[1:]

                # Execute command
                result = self.execute_command(command, *args)
                print(self.format_output(result))

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")
            except RedisError as e:
                print(f"(error) {e}")
            except EOFError:
                print("\nGoodbye!")
                break

    def show_help(self):
        """Display available commands."""
        help_text = """
Available Commands:
===================

String Commands:
  GET <key>                    - Get the value of key
  SET <key> <value>            - Set the value of key
  MGET <key> [key ...]         - Get the values of all given keys
  MSET <key> <value> [key value ...] - Set multiple keys to multiple values
  DEL <key> [key ...]          - Delete one or more keys
  EXISTS <key> [key ...]       - Check if key exists
  INCR <key>                   - Increment the integer value of key
  DECR <key>                   - Decrement the integer value of key
  APPEND <key> <value>         - Append value to key
  STRLEN <key>                 - Get the length of the string value

Hash Commands:
  HGET <key> <field>           - Get the value of a hash field
  HSET <key> <field> <value>   - Set the value of a hash field
  HMGET <key> <field> [field ...] - Get the values of multiple hash fields
  HMSET <key> <field> <value> [field value ...] - Set multiple hash fields
  HGETALL <key>                - Get all fields and values of a hash
  HDEL <key> <field> [field ...] - Delete one or more hash fields
  HEXISTS <key> <field>        - Check if a hash field exists
  HKEYS <key>                  - Get all fields in a hash
  HVALS <key>                  - Get all values in a hash

List Commands:
  LPUSH <key> <value> [value ...] - Prepend values to a list
  RPUSH <key> <value> [value ...] - Append values to a list
  LPOP <key>                   - Remove and get the first element of a list
  RPOP <key>                   - Remove and get the last element of a list
  LRANGE <key> <start> <stop>  - Get a range of elements from a list
  LLEN <key>                   - Get the length of a list
  LINDEX <key> <index>         - Get an element from a list by index

Set Commands:
  SADD <key> <member> [member ...] - Add members to a set
  SMEMBERS <key>               - Get all members of a set
  SISMEMBER <key> <member>     - Check if member is in a set
  SREM <key> <member> [member ...] - Remove members from a set
  SCARD <key>                  - Get the number of members in a set

Sorted Set Commands:
  ZADD <key> <score> <member> [score member ...] - Add members to a sorted set
  ZRANGE <key> <start> <stop> [WITHSCORES] - Get a range of members in a sorted set
  ZREVRANGE <key> <start> <stop> [WITHSCORES] - Get a range of members in reverse order
  ZREM <key> <member> [member ...] - Remove members from a sorted set
  ZCARD <key>                  - Get the number of members in a sorted set
  ZSCORE <key> <member>        - Get the score associated with a member

Key Management:
  KEYS <pattern>               - Find all keys matching pattern
  SCAN <cursor> [MATCH pattern] [COUNT count] - Incrementally iterate keys
  TYPE <key>                   - Determine the type stored at key
  EXPIRE <key> <seconds>       - Set expiration time for key
  TTL <key>                    - Get time to live for key
  PERSIST <key>                - Remove expiration from key
  RENAME <old_key> <new_key>   - Rename a key

Server Commands:
  INFO [section]               - Get server information
  DBSIZE                       - Return the number of keys in the database
  FLUSHDB                      - Delete all keys in current database
  FLUSHALL                     - Delete all keys in all databases
  PING                         - Ping the server
  TIME                         - Return current server time

Cluster Commands (Cluster Mode Only):
  CLUSTER NODES                - Get cluster node information
  CLUSTER SLOTS                - Get cluster slot mappings
  CLUSTER INFO                 - Get cluster state information

General:
  help                         - Show this help message
  exit/quit/q                  - Exit the CLI

Examples:
  SET mykey hello
  GET mykey
  LPUSH mylist value1 value2
  LRANGE mylist 0 -1
  HSET myhash field1 value1
  HGETALL myhash
  ZADD myzset 1 member1 2 member2
  ZRANGE myzset 0 -1 WITHSCORES
  KEYS *
  CLUSTER NODES
"""
        print(help_text)


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
                print(cli.format_output(result))
        except RedisError as e:
            print(f"(error) {e}", file=sys.stderr)
            sys.exit(1)
    else:
        cli.interactive_mode()


if __name__ == '__main__':
    main()
