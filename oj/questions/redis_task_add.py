import redis
conn=redis.Redis('redis')

def add_task(user_id, question_id, code, test_args, expected_output,lang,status,time_limit):

    temp={"question":question_id, "code":code ,"test_args":test_args ,"expected_output":expected_output,"lang":lang,"status":status,"time_limit":time_limit}
    conn.hmset(user_id,temp)
    conn.lpush("tasks",user_id)
    print("Added task to tasks",temp)
def read_file(fName):
        fl=open(fName,"r")
        code=fl.readlines()
        return "".join(code)
def get_output(user_id):
        #user_id=(conn.lpop("completed_tasks")).decode("utf-8")
        temp=conn.hgetall(user_id)
        return temp

#add_task(3,4,read_file("try.py"),read_file("input.txt"),read_file("output.txt"),"py")
#get_output()
