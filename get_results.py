import boto3
from Utility import *
import os
import xmltodict
def get_results():

   MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
   MTURK_LIVE = 'https://mturk-requester.us-east-1.amazonaws.com'

   mturk = boto3.client('mturk',
      aws_access_key_id = "AKIAJSHQWKK2WI7PZ4RA",
      aws_secret_access_key = "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",
      region_name='us-east-1',
      #endpoint_url = MTURK_SANDBOX
      endpoint_url = MTURK_LIVE
   )


   # Use the hit_id previously created
   hitList = readCsv('Data/MTurk/hitsinfo.csv')
   #hit_id = str(hitList[2][0])
   hit_id = "3OKP4QVBP2EGFI2JGBMQN21F4ABAGM"
   # We are only publishing this task to one Worker
   # So we will get back an array with one item if it has been completed
   worker_results = mturk.list_assignments_for_hit(HITId=hit_id)
   #print(worker_results)
   
   if os.path.isfile('Data/MTurk/worker_info.csv'):
	   silentRemove('Data/MTurk/worker_info.csv')
   if os.path.isfile('Data/MTurk/result_info.csv'):
	   silentRemove('Data/MTurk/result_info.csv')
   
   workerFile = open('Data/MTurk/worker_info.csv','a')
   resultFile = open('Data/MTurk/result_info.csv','a')
   workerFile.write('workerID,HitID,assignmentID,userid\n')
   #resultFile.write('ID,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16\n')	
   resultFile.write('workerID,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10\n')	
   
   
   if worker_results['NumResults'] > 0:
      k = 0
      for assignment in worker_results['Assignments']:
         k += 1
         xml_doc = xmltodict.parse(assignment['Answer'])
         workerFile.write(assignment['WorkerId'] + ',' + assignment['HITId'] + ',' + assignment['AssignmentId'] + ',')
         #print(xml_doc)
         #print ("Worker's answer was:")
         print (str(k) + "th worker analyzing...")
         if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
            # Multiple fields in HIT layout
            #print("nnnnnnnnnn")
            i = 0
            resultFile.write(assignment['WorkerId'] + ',')
            for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
               #print ("For input field: " + answer_field['QuestionIdentifier'])
               #print ("Submitted answer: " + answer_field['FreeText'])
               i += 1
               if i <= 10:
                  if i == 10:
                     if answer_field['FreeText'] == None:
                        resultFile.write('None' + '\n')
                     else:
                        resultFile.write(answer_field['FreeText'] + '\n')
                  else:
                     if answer_field['FreeText'] == None:
                        resultFile.write('None' + ',')
                     else:
                        resultFile.write(answer_field['FreeText'] + ',')
               else:
                  if i == 11:
                     if answer_field['FreeText'] == None:
                        workerFile.write('None' + '\n')
                     else:
                        workerFile.write(answer_field['FreeText'] + '\n')
                  #else:
                     #if answer_field['FreeText'] == None:
                        #workerFile.write('None' + ',')
                     #else:
                        #workerFile.write(answer_field['FreeText'] + ',')
         else:
            # One field found in HIT layout
            print ("For input field: " + xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
            print ("Submitted answer: " + xml_doc['QuestionFormAnswers']['Answer']['FreeText'])
   else:
      print ("No results ready yet")

get_results()
