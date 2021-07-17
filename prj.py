import json
import math

if __name__ == '__main__':
    inputjson = None
    with open("input.json", "r") as read_file:
        # json.dump(inputjson, write_file)
        inputjson = json.load(read_file)

    startTime = inputjson['startTime']
    endTime = inputjson['endTime']

    taskset = inputjson['taskset']

    print('Task Set:')
    for task in taskset:
        print('task',task['taskId'],': (\u03A6,T,C,D,\u0394) = ',end='')
        print('(',task['offset'],',',task['period'],',',task['wcet'],',',task['deadline'],',',task['sections'],')')

    # print(type(taskset[0]))
    finished =[]
    ongoingTasks = {}
    for current_time in range(startTime,endTime+1):
        for task in taskset:
            if not(task['taskId']-1 in ongoingTasks):
                ongoingTasks[task['taskId']-1] = {}
            periodNum =  max(int((current_time-task['offset'] )/ task['period']),0)
            # if(periodNum==1):
            #     print("d")
            newTime = current_time - periodNum * task['period'] - task['offset']
            if not(periodNum in ongoingTasks[task['taskId']-1]):
                if newTime>= 0 and newTime<task['deadline']:
                    if not([task['taskId']-1,periodNum] in finished):
                        print('created',task['taskId'],periodNum,current_time)
                        # ongoingTasks[task['taskId']-1] = {}
                        ongoingTasks[task['taskId']-1][periodNum] = {}
                        ongoingTasks[task['taskId']-1][periodNum]['remaining'] = task['wcet']
        deletingTasks = []
        for task,val in ongoingTasks.items():
            for per,dic in val.items():
                if current_time >= ((per*taskset[task]['period'])+taskset[task]['offset']+ taskset[task]['deadline']) :
                    print('removing task',task+1,'time',current_time)
                    deletingTasks.append([task,periodNum])
                elif dic['remaining'] <= 0:
                    print('finished task',task+1,'time',current_time)
                    # print(ongoingTasks)
                    # print(task,per,dic)

                    deletingTasks.append([task,per])

        
        for (task,per) in deletingTasks:
            # print(task,per,deletingTasks)
            ongoingTasks[task].pop(per)
            finished.append([task,per])
        
        # print(finished,'fiiiin')
            

        rmList = []
        for task, dic1 in ongoingTasks.items():
            for per,dic2 in dic1.items():
                rmList.append((task,per,taskset[task]['period']))
        if len(rmList)>0:
            bestchoice = sorted(rmList ,key=lambda x: x[2])[0]

            ongoingTasks[bestchoice[0]][bestchoice[1]]['remaining'] -=1
            print('time:',current_time,'task:',bestchoice[0]+1)
        else:
            print('time:',current_time,'CPU is free :)')

            
            
    
    