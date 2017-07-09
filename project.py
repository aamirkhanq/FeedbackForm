from flask import Flask, render_template, request, redirect, url_for
import psycopg2

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
		conn = psycopg2.connect("dbname=feedbacks")
		cursor = conn.cursor()
		cursor.execute("select feedback_no from feedbacks order by desc limit 1;")
		last_feedback = cursor.fetchall()
		try:
			feedback_no = int(last_feedback[0]) + 1
    		cursor.execute("insert into feedbacks values (%s, %s, %s, %s);" %(feedback_no, response1, response2, response3))
    	except:
    		feedback_no = 1
    		cursor.execute("insert into feedbacks values (%s, %s, %s, %s);" %(feedback_no, response1, response2, response3))
    	conn.commit()
    	conn.close()

	return redirect(url_for('thankYouPage'))

@app.route('/thanks')
def thankYouPage():
	return render_template('thankyou.html')

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)