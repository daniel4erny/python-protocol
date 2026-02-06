import time
import json
from utils.logger import console

def handle_stream_request(ss, addr, messages_list):
    try:
        # 1. Headers
        headers = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/event-stream\r\n"
            b"Cache-Control: no-cache\r\n"
            b"Connection: keep-alive\r\n"
            b"Access-Control-Allow-Origin: *\r\n\r\n"
        )
        ss.sendall(headers)

        # 2. Data loop
        last_index = len(messages_list)

        console.print(f"[bold cyan][SSE][/] Client connected: {addr}")

        while True:
            current_len = len(messages_list)
            
            if current_len > last_index:
                new_messages = messages_list[last_index:]
                last_index = current_len

                for msg in new_messages:
                    json_data = json.dumps(msg)
                    payload = f"data: {json_data}\n\n".encode('utf-8')
                    ss.sendall(payload)
                    console.print(f"[bold blue][PUSH][/] Sent to {addr}: {json_data}")
            
            time.sleep(0.5)

    except (BrokenPipeError, ConnectionResetError):
        console.print(f"[yellow][SSE][/] Client {addr} disconnected.")
    except Exception as e:
        console.print(f"[bold red][SSE] Error:[/] {e}")
    finally:
        pass