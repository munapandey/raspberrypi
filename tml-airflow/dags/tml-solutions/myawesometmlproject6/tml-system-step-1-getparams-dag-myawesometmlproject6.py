from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import datetime
from airflow.decorators import dag, task
import os 
import sys
#import tsslogging

sys.dont_write_bytecode = True
######################################################USER CHOSEN PARAMETERS ###########################################################
default_args = {
 'owner': 'Sebastian Maurice',  # <<< ******** change as needed 
 'start_date': datetime.datetime (2024, 6, 29),
 'brokerhost' : '127.0.0.1',  # <<<<***************** THIS WILL ACCESS LOCAL KAFKA - YOU CAN CHANGE TO CLOUD KAFKA HOST
 'brokerport' : '9092',     # <<<<***************** LOCAL AND CLOUD KAFKA listen on PORT 9092
 'cloudusername' : '',  # <<<< --------FOR KAFKA CLOUD UPDATE WITH API KEY  - OTHERWISE LEAVE BLANK
 'cloudpassword' : '',  # <<<< --------FOR KAFKA CLOUD UPDATE WITH API SECRET - OTHERWISE LEAVE BLANK   
 'ingestdatamethod' : 'localfile', # << CHOOSE BETWEEN: 1. localfle, 2. mqtt, 3. rest, 4. grpc     
 'WRITELASTCOMMIT' : 0,   ## <<<<<<<<< ******************** FOR DETAILS ON BELOW PARAMETER SEE: https://tml.readthedocs.io/en/latest/viper.html
 'NOWINDOWOVERLAP' : 0,
 'NUMWINDOWSFORDUPLICATECHECK' : 5,
 'DATARETENTIONINMINUTES' : 30,
 'USEHTTP' : 0,
 'ONPREM' : 0,
 'WRITETOVIPERDB' : 0,
 'VIPERDEBUG' : 2,
 'MAXOPENREQUESTS' : 10,
 'LOGSTREAMTOPIC' : 'viperlogs',
 'LOGSTREAMTOPICPARTITIONS' : 1,
 'LOGSTREAMTOPICREPLICATIONFACTOR' : 3,
 'LOGSENDTOEMAILS' : '',
 'LOGSENDTOEMAILSSUBJECT' : '[VIPER]',
 'LOGSENDTOEMAILFOOTER' : 'This e-mail is auto-generated by Transactional Machine Learning (TML) Technology Binaries: Viper, HPDE or Viperviz.  For more information please contact your TML Administrator.  Or, e-mail info@otics.ca for any questions or concerns regarding this e-mail. If you received this e-mail in error please delete it and inform your TML Admin or e-mail info@otics.ca, website: https://www.otics.ca.  Thank you for using TML Data Stream Processing and Real-Time Transactional Machine Learning technologies.',
 'LOGSENDINTERVALMINUTES' : 500,
 'LOGSENDINTERVALONLYERROR' : 1,
 'MAXTRAININGROWS' : 300,
 'MAXPREDICTIONROWS' : 50,
 'MAXPREPROCESSMESSAGES' : 5000,
 'MAXPERCMESSAGES' : 5000,
 'MAXCONSUMEMESSAGES' : 5000,
 'MAXVIPERVIZROLLBACKOFFSET' : '',
 'MAXVIPERVIZCONNECTIONS' : 3,
 'MAXURLQUERYSTRINGBYTES' : 10000,
 'MYSQLMAXLIFETIMEMINUTES' : 4,
 'MYSQLMAXCONN' : 4,
 'MYSQLMAXIDLE' : 10,
 'SASLMECHANISM' : 'PLAIN',
 'MINFORECASTACCURACY' : 55,
 'COMPRESSIONTYPE' : 'gzip',
 'MAILSERVER' : '', #i.e.  smtp.broadband.rogers.com,
 'MAILPORT' : '', #i.e. 465,
 'FROMADDR' : '',
 'SMTP_USERNAME' : '',
 'SMTP_PASSWORD' : '',
 'SMTP_SSLTLS' : 'true',
 'SSL_CLIENT_CERT_FILE' : 'client.cer.pem',
 'SSL_CLIENT_KEY_FILE' : 'client.key.pem', 
 'SSL_SERVER_CERT_FILE' : 'server.cer.pem',  
 'KUBERNETES' : 0,
 'solutionname': 'mysolution',   # <<< *** Provide a name for your solution - No spaces or special characters in the name
 'solutiontitle': 'My Solution Title', # <<< *** Provide a descriptive title for your solution
 'description': 'This is an awesome real-time solution built by TSS',   # <<< *** Provide a description of your solution
 'retries': 1,
}

############################################################### DO NOT MODIFY BELOW ####################################################
# Instantiate your DAG
@dag(dag_id="tml_system_step_1_getparams_dag_myawesometmlproject6", default_args=default_args, tags=["tml_system_step_1_getparams_dag_myawesometmlproject6"], schedule=None, start_date=datetime.datetime(2022, 3, 4), catchup=False)
def tmlparams():
    # Define tasks
  basedir = "/"
  viperconfigfile=basedir + "/Viper-produce/viper.env"

  def updateviperenv():
  # update ALL
    
    filepaths = ['/Viper-produce/viper.env','/Viper-preprocess/viper.env','/Viper-ml/viper.env','/Viper-predict/viper.env','/Viperviz/viper.env']
    for mainfile in filepaths:
        with open(mainfile, 'r', encoding='utf-8') as file: 
          data = file.readlines() 
        r=0 
        for d in data:
           if 'KAFKA_CONNECT_BOOTSTRAP_SERVERS' in d: 
             data[r] = "KAFKA_CONNECT_BOOTSTRAP_SERVERS={}:{}".format(default_args['brokerhost'],default_args['brokerport'])
           if 'CLOUD_USERNAME' in d: 
             data[r] = "CLOUD_USERNAME={}".format(default_args['cloudusername'])
           if 'CLOUD_PASSWORD' in d: 
             data[r] = "CLOUD_PASSWORD={}".format(default_args['cloudpassword'])                
           if 'WRITELASTCOMMIT' in d: 
             data[r] = "WRITELASTCOMMIT={}".format(default_args['WRITELASTCOMMIT'])
           if 'NOWINDOWOVERLAP' in d: 
             data[r] = "NOWINDOWOVERLAP={}".format(default_args['NOWINDOWOVERLAP'])
           if 'NUMWINDOWSFORDUPLICATECHECK' in d: 
             data[r] = "NUMWINDOWSFORDUPLICATECHECK={}".format(default_args['NUMWINDOWSFORDUPLICATECHECK'])
           if 'USEHTTP' in d: 
             data[r] = "USEHTTP={}".format(default_args['USEHTTP'])
           if 'ONPREM' in d: 
             data[r] = "ONPREM={}".format(default_args['ONPREM'])
           if 'WRITETOVIPERDB' in d: 
             data[r] = "WRITETOVIPERDB={}".format(default_args['WRITETOVIPERDB'])
           if 'VIPERDEBUG' in d: 
             data[r] = "VIPERDEBUG={}".format(default_args['VIPERDEBUG'])
           if 'MAXOPENREQUESTS' in d: 
             data[r] = "MAXOPENREQUESTS={}".format(default_args['MAXOPENREQUESTS'])
           if 'LOGSTREAMTOPIC' in d: 
             data[r] = "LOGSTREAMTOPIC={}".format(default_args['LOGSTREAMTOPIC'])
           if 'LOGSTREAMTOPICPARTITIONS' in d: 
             data[r] = "LOGSTREAMTOPICPARTITIONS={}".format(default_args['LOGSTREAMTOPICPARTITIONS'])
           if 'LOGSTREAMTOPICREPLICATIONFACTOR' in d: 
             data[r] = "LOGSTREAMTOPICREPLICATIONFACTOR={}".format(default_args['LOGSTREAMTOPICREPLICATIONFACTOR'])
           if 'LOGSENDTOEMAILS' in d: 
             data[r] = "LOGSENDTOEMAILS={}".format(default_args['LOGSENDTOEMAILS'])
           if 'LOGSENDTOEMAILSSUBJECT' in d: 
             data[r] = "LOGSENDTOEMAILSSUBJECT={}".format(default_args['LOGSENDTOEMAILSSUBJECT'])
           if 'LOGSENDTOEMAILFOOTER' in d: 
             data[r] = "LOGSENDTOEMAILFOOTER={}".format(default_args['LOGSENDTOEMAILFOOTER'])
           if 'LOGSENDINTERVALMINUTES' in d: 
             data[r] = "LOGSENDINTERVALMINUTES={}".format(default_args['LOGSENDINTERVALMINUTES'])
           if 'LOGSENDINTERVALONLYERROR' in d: 
             data[r] = "LOGSENDINTERVALONLYERROR={}".format(default_args['LOGSENDINTERVALONLYERROR'])
           if 'MAXTRAININGROWS' in d: 
             data[r] = "MAXTRAININGROWS={}".format(default_args['MAXTRAININGROWS'])
           if 'MAXPREDICTIONROWS' in d: 
             data[r] = "MAXPREDICTIONROWS={}".format(default_args['MAXPREDICTIONROWS'])
           if 'MAXPREPROCESSMESSAGES' in d: 
             data[r] = "MAXPREPROCESSMESSAGES={}".format(default_args['MAXPREPROCESSMESSAGES'])
           if 'MAXPERCMESSAGES' in d: 
             data[r] = "MAXPERCMESSAGES={}".format(default_args['MAXPERCMESSAGES'])
           if 'MAXCONSUMEMESSAGES' in d: 
             data[r] = "MAXCONSUMEMESSAGES={}".format(default_args['MAXCONSUMEMESSAGES'])
           if 'MAXVIPERVIZROLLBACKOFFSET' in d: 
             data[r] = "MAXVIPERVIZROLLBACKOFFSET={}".format(default_args['MAXVIPERVIZROLLBACKOFFSET'])
           if 'MAXVIPERVIZCONNECTIONS' in d: 
             data[r] = "MAXVIPERVIZCONNECTIONS={}".format(default_args['MAXVIPERVIZCONNECTIONS'])
           if 'MAXURLQUERYSTRINGBYTES' in d: 
             data[r] = "MAXURLQUERYSTRINGBYTES={}".format(default_args['MAXURLQUERYSTRINGBYTES'])
           if 'MYSQLMAXLIFETIMEMINUTES' in d: 
             data[r] = "MYSQLMAXLIFETIMEMINUTES={}".format(default_args['MYSQLMAXLIFETIMEMINUTES'])
           if 'MYSQLMAXCONN' in d: 
             data[r] = "MYSQLMAXCONN={}".format(default_args['MYSQLMAXCONN'])
           if 'MYSQLMAXIDLE' in d: 
             data[r] = "MYSQLMAXIDLE={}".format(default_args['MYSQLMAXIDLE'])
           if 'SASLMECHANISM' in d: 
             data[r] = "SASLMECHANISM={}".format(default_args['SASLMECHANISM'])
           if 'MINFORECASTACCURACY' in d: 
             data[r] = "MINFORECASTACCURACY={}".format(default_args['MINFORECASTACCURACY'])
           if 'COMPRESSIONTYPE' in d: 
             data[r] = "COMPRESSIONTYPE={}".format(default_args['COMPRESSIONTYPE'])
           if 'MAILSERVER' in d: 
             data[r] = "MAILSERVER={}".format(default_args['MAILSERVER'])
           if 'MAILPORT' in d: 
             data[r] = "MAILPORT={}".format(default_args['MAILPORT'])
           if 'FROMADDR' in d: 
             data[r] = "FROMADDR={}".format(default_args['FROMADDR'])
           if 'SMTP_USERNAME' in d: 
             data[r] = "SMTP_USERNAME={}".format(default_args['SMTP_USERNAME'])
           if 'SMTP_PASSWORD' in d: 
             data[r] = "SMTP_PASSWORD={}".format(default_args['SMTP_PASSWORD'])
           if 'SMTP_SSLTLS' in d: 
             data[r] = "SMTP_SSLTLS={}".format(default_args['SMTP_SSLTLS'])
           if 'SSL_CLIENT_CERT_FILE' in d: 
             data[r] = "SSL_CLIENT_CERT_FILE={}".format(default_args['SSL_CLIENT_CERT_FILE'])
           if 'SSL_CLIENT_KEY_FILE' in d: 
             data[r] = "SSL_CLIENT_KEY_FILE={}".format(default_args['SSL_CLIENT_KEY_FILE'])
           if 'SSL_SERVER_CERT_FILE' in d: 
             data[r] = "SSL_SERVER_CERT_FILE={}".format(default_args['SSL_SERVER_CERT_FILE'])                
           if 'KUBERNETES' in d: 
             data[r] = "KUBERNETES={}".format(default_args['KUBERNETES'])                

           r += 1
        with open(mainfile, 'w', encoding='utf-8') as file: 
          file.writelines(data)


  @task(task_id="getparams")
  def getparams(args):
        
     VIPERHOST = ""
     VIPERPORT = ""
     HTTPADDR = "http://"
     HPDEHOST = ""
     HPDEPORT = ""
     VIPERTOKEN = ""
     HPDEHOSTPREDICT = ""
     HPDEPORTPREDICT = ""
    
     with open(basedir + "/Viper-produce/admin.tok", "r") as f:
        VIPERTOKEN=f.read()

     if VIPERHOST=="":
        with open(basedir + '/Viper-produce/viper.txt', 'r') as f:
          output = f.read()
          VIPERHOST = HTTPADDR + output.split(",")[0]
          VIPERPORT = output.split(",")[1]
        with open('/Hpde/hpde.txt', 'r') as f:
          output = f.read()
          HPDEHOST = HTTPADDR + output.split(",")[0]
          HPDEPORT = output.split(",")[1]
        with open('/Hpde-predict/hpde.txt', 'r') as f:
          output = f.read()
          HPDEHOSTPREDICT = HTTPADDR + output.split(",")[0]
          HPDEPORTPREDICT = output.split(",")[1]

     sname = args['solutionname']    
     desc = args['description']        
     stitle = args['solutiontitle']    
     method = args['ingestdatamethod'] 
        
     ti.xcom_push(key='VIPERTOKEN',value=VIPERTOKEN)
     ti.xcom_push(key='VIPERHOST',value=VIPERHOST)
     ti.xcom_push(key='VIPERPORT',value=VIPERPORT)
     ti.xcom_push(key='HTTPADDR',value=HTTPADDR)
     ti.xcom_push(key='HPDEHOST',value=HPDEHOST)
     ti.xcom_push(key='HPDEPORT',value=HPDEPORT)
     ti.xcom_push(key='solutionname',value=sname)
     ti.xcom_push(key='solutiondescription',value=desc)
     ti.xcom_push(key='solutiontitle',value=stitle)
     ti.xcom_push(key='ingestdatamethod',value=method)
                 
     updateviperenv()
         
  tmlsystemparams=getparams(default_args)
  
    
dag = tmlparams()
