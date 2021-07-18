import json
import math

if __name__ == '__main__':
    inputjson = None
    with open("input.json", "r") as read_file:
        inputjson = json.load(read_file)

    startTime = inputjson['startTime']
    endTime = inputjson['endTime']

    taskset = inputjson['taskset']

    print('Task Set:')
    for task in taskset:
        print('task',task['taskId'],': (\u03A6,T,C,D,\u0394) = ',end='')
        print('(',task['offset'],',',task['period'],',',task['wcet'],',',task['deadline'],',',task['sections'],')')

    finished =[]
    ongoingTasks = {}
    semaphorInUse = []

    flag = False
    for current_time in range(startTime,endTime+1):

        print('******************************************')
        print('               Second:',current_time,'               ')

        for task in taskset:
            if not(task['taskId']-1 in ongoingTasks):
                ongoingTasks[task['taskId']-1] = {}
            periodNum =  max(int((current_time-task['offset'] )/ task['period']),0)
            newTime = current_time - periodNum * task['period'] - task['offset']
            if not(periodNum in ongoingTasks[task['taskId']-1]):
                if newTime>= 0 and newTime<task['deadline']:
                    if not([task['taskId']-1,periodNum] in finished):
                        print('Task',task['taskId'],'created. Period Number:',periodNum)
                        ongoingTasks[task['taskId']-1][periodNum] = {}
                        ongoingTasks[task['taskId']-1][periodNum]['remaining'] = task['wcet']

        deletingTasks = []
        for task,val in ongoingTasks.items():
            for per,dic in val.items():
                if current_time >= ((per*taskset[task]['period'])+taskset[task]['offset']+ taskset[task]['deadline']) :
                    print('removing task',task+1)
                    deletingTasks.append([task,per])
                    print('OH NO... OH NO... OH NO NO NO NO NO... RM-NPP ****FAILED**** !!!!!!!!!')
                    flag = True
                elif dic['remaining'] <= 0:
                    print('finished task',task+1)

                    deletingTasks.append([task,per])

        for (task,per) in deletingTasks:
            ongoingTasks[task].pop(per)
            finished.append([task,per])
        
        if semaphorInUse == []:
            
            rmList = []
            for task, dic1 in ongoingTasks.items():
                for per,dic2 in dic1.items():
                    rmList.append((task,per,taskset[task]['period']))
            if len(rmList)>0:
                bestchoice = sorted(rmList ,key=lambda x: x[2])[0]
                ith_time = taskset[bestchoice[0]]['wcet'] - ongoingTasks[bestchoice[0]][bestchoice[1]]['remaining']
                
                if (ith_time ==0):
                    ongoingTasks[bestchoice[0]][bestchoice[1]]['section'] = taskset[bestchoice[0]]['sections'][0]
                    semaphorInUse= [taskset[bestchoice[0]]['sections'][0][1],bestchoice[0],bestchoice[1],taskset[bestchoice[0]]['sections'][0][0]]
                else:
                    counter = 0
                    for sec in taskset[bestchoice[0]]['sections']:
                        if ith_time == counter:
                            semaphorInUse= [sec[1],bestchoice[0],bestchoice[1],sec[0]]
                            break
                        else:
                            counter += sec[1]

                ongoingTasks[bestchoice[0]][bestchoice[1]]['remaining'] -=1
                print('Executing task:',bestchoice[0]+1,', Period Number:',bestchoice[1],', semaphore:',semaphorInUse[3])
                semaphorInUse[0] -=1
                if semaphorInUse[0] <=0:
                    semaphorInUse = []
            else:
                print('This time slot, CPU is free :)')
            
        else:
            ongoingTasks[semaphorInUse[1]][semaphorInUse[2]]['remaining'] -=1
            print('Executing task:',semaphorInUse[1]+1,', Period Number:',semaphorInUse[2],', semaphore:',semaphorInUse[3])

            semaphorInUse[0] -=1
            if semaphorInUse[0] <=0:
                semaphorInUse = []

    if flag:

        print('')
        print('')
        print('===============================================================')
        print(' // Validating the Alghorithm:')
        print('          RM-NPP is NOT feasible for this task set')
        print('')
    
    else:
        print('')
        print('')
        print('=============================================================')
        print(' // Validating the Alghorithm:')
        print('          RM-NPP IS feasible for this task set')
        print('')




            
            
    
    