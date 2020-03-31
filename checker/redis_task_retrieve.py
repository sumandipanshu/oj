import redis
import logging
import filterout
conn=redis.Redis('localhost')

fl=""
def get_task():
	user_id=(conn.lpop("tasks")).decode("utf-8")
	temp=conn.hgetall(user_id)
	print(temp,user_id, "Got task from tasks")
	return temp,user_id
def create_files(data):
        print(data)
        temp_code=(data[b'code']).decode("utf-8").strip()
        print("1")
        input_txt=(data[b'test_args']).decode("utf-8").strip()
        print(2)
        output_txt=(data[b'expected_output']).decode("utf-8")+"\n"
        print(r'{} check'.format(output_txt))
        lang=(data[b'lang']).decode("utf-8").strip()
       	question=(data[b'question']).decode("utf-8").strip()
        print("check")
        try:
       	    tempfl=open("Sample.{}".format(lang),"w")
        except Exception as e: print(e)
        print(3)
       	fl="Sample.{}".format(lang)
       	tempfl.write(str(temp_code))
       	tempfl=open("input.txt","w")
       	tempfl.write(input_txt)
       	tempfl=open("expected.txt","w")
       	tempfl.write(output_txt)
       	conn.hdel(user_id,"test_args")
       	conn.hdel(user_id,"code")
       	conn.hdel(user_id,"question")
       	conn.hdel(user_id,"lang")
       	conn.hdel(user_id,"expected_output")
        print(fl)
       	return fl,question
def return_result(result,question,user_id,status):

        temp={"question":question, "result":result,"status":status}
        print("added result in {} for {}".format(temp,user_id))
        conn.hmset(user_id,temp)
        conn.lpush("completed_tasks",user_id)
while True:
    try:
        data,user_id=get_task()
        fl_name,qid=create_files(data)
        print(fl_name)
        result,status=filterout.check(fl_name)
        print(result,status)
        return_result(result,qid,user_id,status)
    except:
        pass
