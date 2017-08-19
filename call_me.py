from subprocess import call, Popen, PIPE
from flask import *
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.secret_key = 'You will never guess'

def call_command(image_name):
	c1 = 'CHECKPOINT_PATH="/media/shivam/disk2/Knockathon/models-master/im2txt/model.ckpt-2000000"'
	c2 = 'VOCAB_FILE="/media/shivam/disk2/Knockathon/models-master/im2txt/word_counts.txt"'

	c3 = "IMAGE_FILE=/media/shivam/disk2/Knockathon/models-master/im2txt/static/images/" + image_name
	c4 = "bazel build -c opt im2txt/run_inference"
	
	c5 = "bazel-bin/im2txt/run_inference --checkpoint_path=/media/shivam/disk2/Knockathon/models-master/im2txt/model.ckpt-2000000 --vocab_file=/media/shivam/disk2/Knockathon/models-master/im2txt/word_counts.txt --input_files=/media/shivam/disk2/Knockathon/models-master/im2txt/static/images/"+image_name


	process0 = Popen(c1.split(), shell=True)
	process1 = Popen(c2.split(), shell=True)


	process2 = Popen(c3.split(), shell=True)
	process3 = Popen(c4.split(), stdout = PIPE)	
	process4 = Popen(c5, stdout = PIPE, shell=True)
	out, err = process4.communicate()

	return out

import random 

def entire_scan(images, keyword):
	got = []
	for image in images:
		out = call_command(image)


		if keyword == 'mike':
			keyword = 'phone'

		if keyword in out:
			got.append(image)
	return got 
 
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():

	files = os.listdir('static/images')
	adjusters = [x for x in files if x.startswith('adjust')]
	exzeo = [x for x in files if x.startswith('exzeo')]
	house = [x for x in files if x.startswith('house')]
	random.shuffle(house)

	knock = [x for x in files if x.startswith('IMG')]

	doc = {}
	doc['output'] = ''
	doc['theme'] = ''

	doc['exzeo'] = exzeo
	doc['adjusters'] = adjusters


	doc['house'] = house
	doc['knock'] = knock

	if request.method == 'POST':
		image_name = request.form['image_name']
		output = call_command(image_name)
	
	
		# theme = request.form['theme']
		# keyword = request.form['specific']

		# if theme == 'house':
		# 	files1 = house[:4]
		# elif theme == 'knock':
		# 	files1 = knock

		# outputs = entire_scan(files1, keyword)
		# doc['theme'] = outputs


		# doc['output'] = output


	return render_template('dashboard.html', doc = doc)

@app.route('/visual_by_bot1')
def visual_by_bot1():
	return render_template('visual_by_bot1.html')
@app.route('/visual_by_bot2')
def visual_by_bot2():
	return render_template('visual_by_bot2.html')
@app.route('/visual_by_bot3')
def visual_by_bot3():
	return render_template('visual_by_bot3.html')

@app.route('/components')
def components():
	return render_template('components.html')

@app.route('/')
def index():
	return render_template('index.html')
import time 
@app.route('/deepai', methods=['GET','POST'])
def deepai():
	files = os.listdir('static/images/')
	adjusters = [x for x in files if x.startswith('adjust')]
	exzeo = [x for x in files if x.startswith('exzeo')]
	house = [x for x in files if x.startswith('house')]
	knock = [x for x in files if x.startswith('IMG')]
	random.shuffle(house)

	doc = {}
	doc['output'] = ''
	doc['theme'] = ''
	doc['results'] = ''

	doc['adjusters'] = adjusters
	doc['exzeo'] = exzeo

	doc['house1'] = house[:4]
	doc['house2'] = house[4:8]
	doc['house3'] = house[8:12]
	doc['house4'] = house[12:16]
	doc['house5'] = house[16:20]
	doc['house6'] = house[20:24]
	
	doc['knock'] = knock

	if request.method == 'POST':
		if 'image_name' in request.form:
			image_name = request.form['image_name']
			output = call_command(image_name)

			if '(p' in output:
				try:

					line2 = output.split('2)')[1].replace('1) ','').split("(")[0].strip().rstrip('.')
					line1 = output.split('1)')[1].split('2)')[0].replace('1) ','').split("(")[0].strip().rstrip('.')
					line0 = output.split('0)')[1].split('1)')[0].replace('1) ','').split("(")[0].strip().rstrip('.')

					output = line0 + "<br>" + line1 + "<br>" + line2
				except:
					output = output

			doc['output'] = output
			doc['input'] = image_name

		if 'query' in request.form:
			query_name = request.form['query']
			
			term = ''
			results = []

			quick = ''
			if 'dog' in query_name:
				results = ['house14.jpg','house18.jpg','house24.jpg','house4.jpg']
				quick = 'Quick Insight : Policyholders with pets are more prone to liability injury related claims. Other liability injuries are also caused by trampolines and pools. Here are the properties which are contain pools'
				term = 'dog'

			if 'fan' in query_name:
				results = ['house17.jpg','house2.jpg']
				term = 'fan'


			doc['quick'] = quick
			doc['results'] = results
			doc['query'] = term
			time.sleep(4) 

	
	return render_template('deepai.html', doc = doc)


app.run(debug=True, port = 5001)
