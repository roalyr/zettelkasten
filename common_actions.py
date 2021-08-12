#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ USER OPTIONS ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
default_editor = "nano" # a text editor command to call by default
# use "python" to disable prompt and always use native input
text_width_fallback = 55 #in characters 55...80 should be good

#▒▒▒▒▒▒▒▒▒▒▒▒ IMPORTS / CONSTANTS ▒▒▒▒▒▒▒▒▒▒▒▒▒
import os, fnmatch, shutil, pathlib, sqlite3, time, re, random, tempfile
import subprocess, py_compile, gc, textwrap
from sqlite3 import Error

# SSH for termux to ask for key
os.system("ssh-add /data/data/com.termux/files/usr/etc/ssh/id_ed25519")

#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ WRITING OPS ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
def write_num_not_empty(type, prompt_str):
	while True:
		num = c_prompt(prompt_str)
		try: 
			if type == 'int': num = int(num); return num
			elif type == 'float': num = float(num); return num
			else: print_wrong_num_type(); p()
		except: print_num_wrong_input()
		
def write_not_empty(inject_text, flag, allow_exit):
	name = '';
	while not name: 
		if not flag == 'prompt': name = write_with_editor(inject_text)
		else: name = write_fallback(inject_text)
		name = parse_off_comments(name)
		if name =='': 
			if not allow_exit:
				print_abort_writing()
				inp = c_prompt('')
				if inp == 'qm': main_menu()
			else: 
				print_abort_writing_quit_allowed()
				inp = c_prompt('')
				if inp == 'qm': main_menu()
				elif inp == 'q': return name
	return name

def write_with_editor(inject_text):
	def write_ext(option, inject_text):
		written = ''
		with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
			if inject_text: 
				try: tf.write(inject_text)
				except TypeError: tf.write(inject_text.encode("utf-8"))
				finally: tf.flush()
			try: 
				subprocess.call([option, tf.name])
				tf.seek(0); written = tf.read().decode("utf-8")
				return written.strip()
			except: 
				print_no_default_editor(option); p(); 
				return write_fallback(inject_text)
	#BEGIN
	if default_editor == 'python': return write_fallback(inject_text)
	else: return write_ext(default_editor, inject_text)

def write_fallback(inject_text):
	print_fallback_editor(inject_text)
	return s_prompt('enter text')

def parse_off_comments(text):
	out = ''
	for line in text.splitlines(True):
		if line.lstrip().startswith('#'): continue
		else: out += line
	return out

#▒▒▒▒▒▒▒▒▒▒▒▒ MENUS ▒▒▒▒▒▒▒▒▒▒▒▒▒
def git_menu():
	print_git_ops()
	while True:
		inp = c_prompt('GIT')
		print_git_ops()
		if inp == "": git_info()
		elif inp == "l": git_log_f()
		elif inp == "s": git_status()
		elif inp == "c": git_commit_f()
		elif inp == "p": git_push()
		elif inp == "pu": git_pull()
		elif inp == "r": git_revert_f()
		elif inp == "rb": git_rebase_i()
		elif inp == "ha": git_reset_hard_f()
		elif inp == "u": git_launch_gitui()
		elif inp == "todo": todo()
		elif inp == "g": grep_search()
		elif inp == "t": target_tree()
		elif inp == "q": break
		
#▒▒▒▒▒▒▒▒▒▒▒▒ FORMATTING ▒▒▒▒▒▒▒▒▒▒▒▒▒
indent = '         '; ph = '...'
right_indent = 4; ml = 3

def check_min_width(text_width):
	if text_width < 30: print('minimal text width value is 30'); return 30
	else: return text_width

def width_update():
	return shutil.get_terminal_size((text_width_fallback, 24)).columns
		
def tw_update():
	text_width = width_update()
	check_min_width(text_width)
	return textwrap.TextWrapper(text_width)
		
def tw_i_update():
	text_width = width_update()
	check_min_width(text_width)
	return textwrap.TextWrapper(text_width, subsequent_indent=indent)

#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ PRINT OPS ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#GIT OPS
def print_git_current_head(): 
	tw_i = tw_i_update()
	divider() 
	print(tw_i.fill('Current head:'))
	os.system("git log --branches --oneline -n 1")

def print_git_status():
	cl_divider()
	os.system("git status")

def print_git_log(entries):
	cl_divider()
	os.system("git log --branches --oneline -n "+str(entries)); 
	
def print_git_push():
	cl_divider()
	os.system("git push --all")
	
def print_git_pull():
	cl_divider()
	os.system("git pull")
	
def print_git_add_modified():
	tw_i = tw_i_update()
	cl_divider()
	print(tw_i.fill('New / modified files:'))
	os.system("git add . ")
	os.system("git status --short")

#WRITING OPS
def print_num_wrong_input(): 
	tw = tw_update()
	cl_divider(); 
	print(tw.fill('''
make sure you enter numbers
'''.strip()))

def print_wrong_num_type(): 
	tw = tw_update()
	cl_divider(); 
	print(tw.fill('''
wrong numeric type supplied
'''.strip()))

def print_abort_writing():
	tw = tw_update(); tw_i = tw_i_update()
	cl_divider()
	print(tw.fill('no text was written, you can try again or abort'))
	print(tw_i.fill('() - resume writing'))
	print_qm()
	
def print_abort_writing_quit_allowed():
	tw = tw_update(); tw_i = tw_i_update()
	cl_divider()
	print(tw.fill('no text was written, you can try again or abort'))
	print(tw_i.fill('() - resume writing'))
	print_q()
	print_qm()

#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ MENUS ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
def print_git_ops():
	tw_i = tw_i_update()
	cl_divider()
	print("ZETTELKASTEN OPS")
	divider()
	print(tw_i.fill('() - current'))
	print(tw_i.fill('(l) - log'))
	print(tw_i.fill('(s) - status'))
	print(tw_i.fill('(c) - commit all'))
	print(tw_i.fill('(p) - push'))
	print(tw_i.fill('(pu) - pull'))
	print(tw_i.fill('(r) - revert'))
	print(tw_i.fill('(rb) - rebase (interactive)'))
	print(tw_i.fill('(ha) - hard reset'))
	print(tw_i.fill('(u) - launch "gitui" (must be installed)'))
	divider()
	print(tw_i.fill('(t) - "tree" the target folder'))
	print(tw_i.fill('(g) - "grep" the source folder files'))
	print(tw_i.fill('(todo) - find all "todo" comments'))
	print_q()

#▒▒▒▒▒▒▒▒▒▒▒▒▒▒ STANDARD PROMPTS ▒▒▒▒▒▒▒▒▒▒▒▒▒▒
def c_prompt(prompt): 
	divider(); 
	try: inp = input(prompt+" : ").rstrip()
	except KeyboardInterrupt: inp = ''
	return inp 
	
def s_prompt(prompt):
	divider(); 
	try: inp = input(prompt+" > ").rstrip()
	except KeyboardInterrupt: inp = ''
	return inp 
	
def p(): 
	text_width = width_update()
	divider(); l=(text_width-10)//2; s="░"*l+" CONTINUE "+"░"*l; input(s)
	
def print_qc(ch):
	tw_i = tw_i_update()
	print(tw_i.fill("({0}) - return | confirm".format(ch)))
	
def print_q(): 
	tw_i = tw_i_update()
	print(tw_i.fill('(q) - return'))
	
def print_qm(): 
	tw_i = tw_i_update()
	print(tw_i.fill('(qm) - return to main menu | abort everything'))

#▒▒▒▒▒▒▒▒▒▒▒▒ CLEAR SCREEN AND DIVIDER ▒▒▒▒▒▒▒▒▒▒▒▒▒
def divider(): 
	text_width = width_update()
	d_line = '─' * text_width
	print(d_line)
	
def cl(): os.system('cls' if os.name == 'nt' else 'clear')
def cl_divider(): cl(); divider()

#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ GIT OPS ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
def git_info(): print_git_current_head()
def git_status(): print_git_status()
def git_log_f(): 
	cl()
	entries = write_num_not_empty('int', 'Number of commits to print')
	print_git_log(entries)
	
def git_launch_gitui(): os.system('gitui')
def git_push(): print_git_push()
def git_pull(): print_git_pull()

def git_commit_f():
	print_git_add_modified(); print_git_current_head();p()
	comment = '# Enter the new commit name below\n'
	commit_name = write_not_empty(comment, flag=None, allow_exit=True)
	if commit_name =='': return
	inp = c_prompt("really? ('yes' to proceed)")
	if inp == "yes": os.system("git commit -m "+ '\"'+commit_name+'\"')
	
def git_revert_f():
	git_log_f(); p()
	comment = '# Enter the commit name to revert to below\n'
	commit_name = write_not_empty(comment, flag=None, allow_exit=True)
	if commit_name =='': return
	os.system("git revert "+ '\"'+commit_name+'\"')
	
def git_reset_hard_f():
	git_log_f(); p()
	comment = '# Enter the commit name to RESET to below\n'
	commit_name = write_not_empty(comment, flag=None, allow_exit=True)
	if commit_name =='': return
	inp = c_prompt("really? ('yes' to proceed)")
	if inp == "yes": os.system("git reset --hard "+ '\"'+commit_name+'\"')

def git_rebase_i():
	git_log_f(); p()
	num = write_num_not_empty('int', 'Number of commits to include in rebase')
	os.system("git rebase -i HEAD~"+str(num))

#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ OTHER OPS ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
def todo():
	cl_divider();
	os.system('grep --exclude="*.py" --exclude="*.gitignore" --exclude-dir=".git" -rni --color=always "todo" .')

def target_tree():
	cl_divider();
	os.system('tree -I target'+' '+'.')

def grep_search():
	cl_divider();
	comment = '# Enter the pattern to search in source files below\n'
	pattern = write_not_empty(comment, flag=None, allow_exit=True)
	os.system('grep --exclude="*.py" --exclude-dir=".git" -rn --color=always'+' "'+pattern+'" '+' .')

git_menu()
