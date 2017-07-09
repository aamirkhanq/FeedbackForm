from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def MainPage():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		return redirect(url_for('saveFeedback'))

@app.route('/savefeedback', methods=['GET', 'POST'])
def saveFeedback():
	if request.method == "POST":
		response1 = request.form['q1']
		response2 = request.form['r1']
		response3 = request.form['s1']
		print response1, response2, response3
	return redirect('thankyou.html')

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)