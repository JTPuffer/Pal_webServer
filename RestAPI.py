

import socket
import json
import select


class Client:
    def __init__(self, host, port):
        """
        :param host: str
        :param port: int
        """

        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recive_data(self, s: socket.socket):
        response = []
        
        while True:
            ready_to_read, _, _ = select.select([s], [], [], 5)  # 5-second timeout
            if not ready_to_read:
                print("Timeout or no data available.")
                return -1
            
            data = s.recv(4096)
            if not data:
                break
            response.append(data.decode())
        return ''.join(response)

    def get_request(self, endpoint):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            
            request = (
                f"GET {endpoint} HTTP/1.0\r\n"
                f"Host: {self.host}\r\n"
                "Connection: keep-alive\r\n"
                "\r\n"
            )
            s.sendall(request.encode())
            
            response_data = self.recive_data(s)
            if response_data == -1:
                return -1
            headers, body = response_data.split("\r\n\r\n", 1)
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return -1
            return -1
        
    def post_request(self, endpoint, data, content_type="text"):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            
            request = (
                f"POST {endpoint} HTTP/1.0\r\n"
                f"Host: {self.host}\r\n"
                f"Content-Type: {content_type}\r\n"
                "Connection: keep-alive\r\n"
                "Content-Length: " + str(len(data)) + "\r\n"
                "\r\n" +
                data
            )
            s.sendall(request.encode())
            response_data = self.recive_data(s)
            if response_data == -1:
                return -1
            if response_data == "":
                return 0
            

            headers, body = response_data.split("\r\n\r\n", 1)
            if headers.split()[1] != "200":
                raise Exception("Error")
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return -1
            return -1

    def get_all_configs(self):
        """
        Returns:
            String[]
        """
        req = self.get_request("/meta/get_all_configs")
        if req == -1:
            return -1
        return req["configs"]
    def get_config(self):
        """
        Returns:
            dict: JSON response from the server.
        """
        return self.get_request(f"/meta/get_config")
    def get_perception(self):
        """
        Returns:
            dict: JSON response from the server.
        """
        return self.get_request("/meta/get_perception")
    
    def set_config(self, data:str):
        json_data = json.dumps({"config": data})
        return self.post_request("/meta/set_config", json_data, "text/json")

    def add_component(self, data):
        return self.post_request("/meta/add_component", data, "text")

    def rem_component(self, data):
        return self.post_request("/meta/rem_component", data, "text")

    def upd_component(self, data):
        return self.post_request("/meta/upd_component", data, "text")

    def upd_arch(self, data):
        return self.post_request("/meta/upd_arch", data, "text/json")

    


