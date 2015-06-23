open("output.txt",'w')

with open('AssessmentTrainSet.txt','r') as AssessmentTrainSet:
    with open('ResultsTrainSet.txt','r') as ResultsTrainSet:

        PR_SUM = [0.0 for i in range(0,11)]
        mAP = [0.0 for i in range(0,16)]
        
        for queryIndex in xrange(0,16):

            def readData(inputstream):
                while True:
                    title = inputstream.readline().split()
                    if len(title) > 0 and title[0] == 'Query':
                        break
                    
                num = int(title[3])
                return [inputstream.readline() for i in range(0,num)]

            #Assessment
            Assessment = readData(AssessmentTrainSet)
            Assessment = [temp[:-2] for temp in Assessment] #-2 is for delete \r\n

            #Results
            Results = readData(ResultsTrainSet)
            Results = [temp.split()[0] for temp in Results]

            class Recall_Precision:
                def __init__(self, R=None, P=None):
                    self.R = R if R is not None else 0.0
                    self.P = P if P is not None else 0.0
            
            #calcualte RP
            RP = []
            for index,query in enumerate(Results,1):
                for ans in Assessment:
                    if query == ans:                        
                        R = (len(RP)+1)*100 / float(len(Assessment))
                        P = (len(RP)+1)*100 / float(index)
                        RP.append(Recall_Precision(R,P))
                        break
                if len(RP) == len(Assessment):
                    break

            #PR10 (formula I)
            PR10 = [0.0 for i in range(0,11)]
            iterRP = len(RP)-1
            PR10[10] = RP[iterRP].P
            
            for i in xrange(9,-1,-1):
                maxP = PR10[i+1]
                while iterRP >= 0:                    
                    if RP[iterRP].R < i*10:
                        break
                    if RP[iterRP].P > maxP:                        
                        maxP = RP[iterRP].P
                    iterRP -= 1
                PR10[i] = maxP
                
            #PR_SUM
            for i in xrange(0,11):
                PR_SUM[i] += PR10[i]

            #mAP (formula III)
            for iterRP in RP:
                mAP[queryIndex] += iterRP.P
            mAP[queryIndex] /= len(Assessment)

            #Print PR and PR10
            with open("output.txt",'a') as output:
                output.write("\nQuery NO." + str(queryIndex))
                output.write("\nP\t\t\tR\n")
                for iterRP in RP:
                    output.write(str(iterRP.P) + "\t\t" + str(iterRP.R) + "\n")
                for index,iterPR10 in enumerate(PR10):
                    output.write(str(index*10) + "%\t\t" + str(iterPR10) + "\n")
                    
        #PR_AVG (formula II)
        PR_AVG = [PR_SUM[i]/16 for i in range(0,11)]

        #mAP_AVG
        mAP_AVG = sum(mAP)/(16*100)

        #Print PR_AVG and mAP_AVG
        with open("output.txt",'a') as output:
            output.write("\nPR_AVG:\n")
            for index,iterPR_AVG in enumerate(PR_AVG):
                output.write(str(iterPR_AVG) + "\t\t" + str(index*10) + "%\n")
            output.write("\nmAP_AVG : " + str(mAP_AVG) + "\n")
