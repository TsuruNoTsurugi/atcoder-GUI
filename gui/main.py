import tkinter
from tkinter import scrolledtext
import subprocess
import shell_communication
import config
from time import sleep
from os import getcwd,path,mkdir
root_window = tkinter.Tk()
test_window = tkinter.Tk()

def command_exec(cmd:str,cwd:str=getcwd()) -> str:
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,cwd=cwd)
    result = proc.communicate()[0].decode()
    return result

def login_atcoder():
    command = "acc login"
    executer = shell_communication.Execute(command.split())
    executer.send(config.USER_NAME)
    executer.send(config.PASSWORD)
    print(executer.recieve())
    executer.close()
    
def logout_atcoder():
    command = "acc logout"
    executer = shell_communication.Execute(command.split())
    print(executer.recieve())
    executer.close()

def submit_atcoder():
    ct : str = string_Var.get()
    cn : str = contest_num.get()
    pb : str = string_Var_problem.get()
    language : str = string_Var_language.get()
    language_num = config.LANGUAGE_NUM_LIST[config.LANGUAGE_LIST.index(language)]
    file_name_to_test = file_name.get()
    contest_name = f"{ct.lower()}{cn.lower()}"
    task_name = f"{ct.lower()}{cn.lower()}_{pb.lower()}"
    URL = f"{config.ATCODER_BASE_URL}/contests/{contest_name}/tasks/{task_name}"
    command = f"oj submit {URL} {file_name_to_test} -l {language_num}"
    proc = subprocess.Popen(command.split(),stdin=subprocess.PIPE,cwd=path.normpath(path.join(config.BASE_ROOT_PATH,contest_name,pb.lower())))
    proc.stdin.write(f"abc{pb.lower()}\n".encode())
    proc.stdin.close()

def select_contest_func(): # acc new
    if contest_num.get()=="":
        contest_num_string_Var.set("Enter correct number")
        return
    ct : str = string_Var.get() # contest type ex) ABC, ARC ...
    cn : str = contest_num.get() # contest num ex) 343 123 002 ...
    language : str = string_Var_language.get()
    contest_name = f"{ct.lower()}{cn.lower()}"
    # get new folder
    command = f"acc new {contest_name} -c all"
    proc = shell_communication.Execute(command.split())
    proc.wait()
    shell_communication.Execute(f"acc add --template {language} --choice all".split(),cwd=path.normpath(path.join(config.BASE_ROOT_PATH,contest_name)))
    file_name.set(f"main.{language}")
    string_Var_problem.set("A")
    label_URL.config(text=f"{config.ATCODER_BASE_URL}/contests/{contest_name}/")

def solve():
    if contest_num.get()=="":
        contest_num_string_Var.set("Enter correct number")
        return
    ct : str = string_Var.get()
    cn : str = contest_num.get()
    pb : str = string_Var_problem.get()
    contest_name = f"{ct.lower()}{cn.lower()}"
    task_name = f"{ct.lower()}{cn.lower()}_{pb.lower()}"
    URL = f"{config.ATCODER_BASE_URL}/contests/{contest_name}/tasks/{task_name}"
    label_URL.config(text=URL)
    return URL

def test_code():
    if contest_num.get()=="":
        contest_num_string_Var.set("Enter correct number")
        return
    if file_name.get()=="":
        file_name.set("Enter file name.")
    ct : str = string_Var.get()
    cn : str = contest_num.get()
    pb : str = string_Var_problem.get()
    language : str = string_Var_language.get()
    file_name_to_test = file_name.get()
    task_name = f"{ct.lower()}{cn.lower()}/{pb.lower()}"
    st.delete("1.0",tkinter.END)
    #code_test_result.config(text="WJ",background="#777777")
    if language == "cpp": # cpp
        compile_out = subprocess.Popen(f"g++ {file_name_to_test}".split(),cwd=path.normpath(path.join(config.BASE_ROOT_PATH,task_name)),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        compile_out_err = compile_out.communicate()[1].decode()
        if compile_out_err!="":
            st.insert(tkinter.END,"COMPILE ERR OUT\n"+"="*50+"\n")
            for char in compile_out_err:
                st.insert(tkinter.END,chars=char)
            st.insert(tkinter.END,"="*50+"\nCOMPILE FAILED")
            code_test_result.config(text="CE",background="#f0ad4e")
            return
        test_out = subprocess.Popen(f"oj t -d tests/ --tle {config.TLE_SECONDS} --mle {config.MLE_MEGABYTES}".split(),cwd=path.normpath(path.join(config.BASE_ROOT_PATH,task_name)),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        test_out_out = test_out.communicate()[0].decode()
        print(test_out_out)
        for string in test_out_out:
            st.insert(tkinter.END,string)
        if "[FAILURE]" in test_out_out: # if AC
            code_test_result.config(text="Not AC",background="#f0ad4e")
        else:
            code_test_result.config(text="AC",background="#5cb65c")
    else: # Python
        #test_out = subprocess.Popen(f'sh {config.PYTHON_SHELL_FILEPATH} "python3 {file_name_to_test}"'.split(),shell=True,cwd=path.normpath(path.join(config.BASE_ROOT_PATH,task_name)),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        test_out = subprocess.run(['sh', f'{config.PYTHON_SHELL_FILEPATH}', f'python3 {file_name_to_test}', '--tle', f'{config.TLE_SECONDS}', '--mle', f'{config.MLE_MEGABYTES}'],cwd=path.normpath(path.join(config.BASE_ROOT_PATH,task_name)),capture_output=True, text=True)
        test_out_err = test_out.stderr
        test_out_out = test_out.stdout
        if test_out_err!="":
            st.insert(tkinter.END,"ERR OUT\n"+"="*50+"\n")
            for char in test_out_err:
                st.insert(tkinter.END,chars=char)
            st.insert(tkinter.END,"="*50+"\nERR HAPPENED")
            code_test_result.config(text="RE",background="#f0ad4e")
            return
        for string in test_out_out:
            st.insert(tkinter.END,string)
        if "[FAILURE]" in test_out_out:
            code_test_result.config(text="Not AC",background="#f0ad4e")
        else:
            code_test_result.config(text="AC",background="#5cb65c")                      

def oj_template():
    if contest_num.get()=="":
        contest_num_string_Var.set("Enter correct number")
        return
    ct : str = string_Var.get()
    cn : str = contest_num.get()
    pb : str = string_Var_problem.get()
    tp : str = string_Var_template.get()
    contest_name = f"{ct.lower()}{cn.lower()}"
    task_name = f"{ct.lower()}{cn.lower()}_{pb.lower()}"
    URL = f"{config.ATCODER_BASE_URL}/contests/{contest_name}/tasks/{task_name}"
    command = f"oj-template -t {tp} {URL}"
    proc = subprocess.Popen(command.split(),cwd=path.normpath(path.join(config.BASE_ROOT_PATH,f"{contest_name}/{pb.lower()}")),stdout=subprocess.PIPE)
    proc_out = proc.communicate()[0].decode()
    with open(path.normpath(path.join(config.BASE_ROOT_PATH,f"{contest_name}/{pb.lower()}/{tp}")),"w") as f:
        f.write(proc_out)
        f.close()
    st.delete("1.0",tkinter.END)
    for char in proc_out:
        st.insert(tkinter.END,chars=char)

root_window.title("acc GUI")
test_window.title("Test Code")

# title row 0
title = tkinter.Label(root_window,text="atcoder-cli GUI")

# login/out button row 0
login_bottun = tkinter.Button(root_window,text="Login",command=lambda:login_atcoder())
logout_button = tkinter.Button(root_window,text="Logout",command=lambda:logout_atcoder())

# Option contest type row 1
string_Var = tkinter.StringVar()
string_Var.set(config.CONTEST_TYPE_LIST[0])
contest_num_string_Var = tkinter.StringVar()
contest_type = tkinter.OptionMenu(root_window,string_Var,*config.CONTEST_TYPE_LIST)
contest_num = tkinter.Entry(root_window,textvariable=contest_num_string_Var,justify=tkinter.CENTER) # contest_type+contest_num ex) -> ABC343
select_contest = tkinter.Button(root_window,text="Select",command=lambda:select_contest_func())
string_Var_problem = tkinter.StringVar()
string_Var_problem.set(config.CONTEST_PROB_LIST[0])
current_problem = tkinter.OptionMenu(root_window,string_Var_problem,*config.CONTEST_PROB_LIST)
solve_problem = tkinter.Button(root_window,text="Solve",command=lambda:solve())

# next button row 2
label_description = tkinter.Label(root_window,text="Template:")
string_Var_language = tkinter.StringVar()
string_Var_language.set(config.LANGUAGE_LIST[config.NORM_LANGUAGE])
language_select = tkinter.OptionMenu(root_window,string_Var_language,*config.LANGUAGE_LIST)
label_file_name = tkinter.Label(root_window,text=None)

# test row 3
code_test_button = tkinter.Button(root_window,text="Test",command=lambda:test_code())
file_name = tkinter.StringVar()
file_name_entry = tkinter.Entry(root_window,textvariable=file_name,justify=tkinter.CENTER,width=40)
code_test_result = tkinter.Label(root_window,text=None)

# Submit and URL row 4
label_URL = tkinter.Label(root_window,text=None)
submit_button = tkinter.Button(root_window,text="Submit",command=lambda:submit_atcoder())

# generate template row 5
generate_button = tkinter.Button(root_window,text="Generate",command=lambda:oj_template())
string_Var_template = tkinter.StringVar()
string_Var_template.set(config.TEMPLATE_TYPE_LIST[0])
template_type = tkinter.OptionMenu(root_window,string_Var_template,*config.TEMPLATE_TYPE_LIST)

# row 0
title.grid(row=0,column=1,columnspan=1,padx=10,pady=5)
logout_button.grid(row=0,column=3,padx=10,pady=5)
login_bottun.grid(row=0,column=4,padx=10,pady=5)

# row 1
contest_type.grid(row=1,column=0,padx=10,pady=5)
contest_num.grid(row=1,column=1,padx=10,pady=5)
select_contest.grid(row=1,column=2,padx=10,pady=5)
current_problem.grid(row=1,column=3,padx=10,pady=5)
solve_problem.grid(row=1,column=4,padx=10,pady=5)

# row 2
label_description.grid(row=2,column=0,padx=10,pady=5)
language_select.grid(row=2,column=1,padx=10,pady=5)
label_file_name.grid(row=2,column=2,padx=10,pady=5,columnspan=3)

# row 3
code_test_button.grid(row=3,column=0,padx=10,pady=5)
file_name_entry.grid(row=3,column=1,padx=10,pady=5,columnspan=3)
code_test_result.grid(row=3,column=4,padx=10,pady=5)

# row 4
submit_button.grid(row=4,column=0,padx=10,pady=5)
label_URL.grid(row=4,column=1,columnspan=4,padx=10,pady=5)

# row 5
generate_button.grid(row=5,column=0,padx=10,pady=5)
template_type.grid(row=5,column=1,padx=10,pady=5)

st = scrolledtext.ScrolledText(test_window)
st.pack()

# display
root_window.mainloop()
test_window.mainloop()