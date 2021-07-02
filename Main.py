import SMO as smo #SMO contains the algo code
import benchmarks #benchmarking functions
import csv #for working with csv files
import numpy #math matrix operations
import time #algo running time
import math #normal math operations


def selector(algo,func_details,popSize,Iter,succ_rate,mean_feval):
    function_name=func_details[0]
    lb=func_details[1]
    ub=func_details[2]
    dim=func_details[3]
    acc_err=func_details[4]
    obj_val=func_details[5]
    #selection of different parameters
       
    if(algo==0):
        x,succ_rate,mean_feval=smo.main(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter,acc_err,obj_val,succ_rate,mean_feval) #getting attributes from different file      
    return x,succ_rate,mean_feval
    
SMO= True 
F1=True

optimizer=[SMO] #list of optimizers, for comparison purposes
benchmarkfunc=[F1] #list of functions 
NumOfRuns=2
PopulationSize = 10
Iterations= 5
Export=True

ExportToFile="experiment"+time.strftime("%Y-%m-%d-%H-%M-%S")+".csv" 
Flag=False

CnvgHeader=[]

for l in range(0,Iterations):
	CnvgHeader.append("Iter"+str(l+1))

mean_error=0
total_feval=0 #feval=function eval
mean1=0
var=0 #variance
sd=0 #std deviations
mean_feval=0
succ_rate=0
GlobalMins=numpy.zeros(NumOfRuns)


for i in range (0, len(optimizer)):
    for j in range (0, len(benchmarkfunc)):
        if((optimizer[i]==True) and (benchmarkfunc[j]==True)): # start experiment if an optimizer and an objective function is selected
            for k in range (0,NumOfRuns):
                    
                func_details=benchmarks.getFunctionDetails(j)
                print("Run: {}".format(k+1)) #to seperate runs
                x,succ_rate,mean_feval=selector(i,func_details,PopulationSize,Iterations,succ_rate,mean_feval)
                mean_error=mean_error+x.error;
                mean1=mean1+x.convergence[-1]
                total_feval=total_feval+x.feval
                GlobalMins[k]=x.convergence[-1]

                if(Export==True):
                    with open(ExportToFile, 'a') as out:
                        writer = csv.writer(out,delimiter=',')
                        if (Flag==False): # just one time to write the header of the CSV file
                            header= numpy.concatenate([["Optimizer","objfname","startTime","EndTime","ExecutionTime"],CnvgHeader])
                            writer.writerow(header) #write into csv
                        a=numpy.concatenate([[x.optimizer,x.objfname,x.startTime,x.endTime,x.executionTime],x.convergence])
                        writer.writerow(a)
                    out.close()
                    print("Results of {} run are saved in 'csv' file.".format(k+1))
                Flag=True # at least one experiment
            mean1=mean1/NumOfRuns
            mean_error=mean_error/NumOfRuns
            if(succ_rate>0):
                mean_feval=mean_feval/succ_rate
            total_feval=total_feval/NumOfRuns
            for k in range (NumOfRuns):
                var=var + math.pow((GlobalMins[k]-mean1),2)
            var=var/NumOfRuns
            sd=math.sqrt(var)
            # print("values after executing are: \n Mean Error \t Mean Function eval \t Total Function eval \t Variance \t STD \n",(mean_error,mean_feval,total_feval,var,sd))
            print("Values after executing SMO: \n Mean Error:{} \n Mean Function eval:{} \n Total Function eval:{} \n Variance:{} \n STD:{}".format(mean_error,mean_feval,total_feval,var,sd))

if (Flag==False): # Faild to run at least one experiment
    print("No Optimizer or Cost function is selected. Check lists of available optimizers and cost functions") 