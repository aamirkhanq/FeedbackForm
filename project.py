from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def MainPage():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		response1 = request.form['q1']
		response2 = request.form['r1']
		response3 = request.form['s1']
		conn = psycopg2.connect("dbname=feedbacks")
		cursor = conn.cursor()
		cursor.execute("select feedback_no from feedbacks order by feedback_no desc limit 1;")
		last_feedback = cursor.fetchall()
		try:
			feedback_no = int(last_feedback[0][0]) + 1
			cursor.execute('insert into feedbacks ("feedback_no", "response1", "response2", "response3") values ('+ "'%s', '%s', '%s', '%s');" %(feedback_no, response1, response2, response3))
			conn.commit()
			conn.close()
		except:
			feedback_no = 1
			cursor.execute('insert into feedbacks ("feedback_no", "response1", "response2", "response3") values ('+ "'%s', '%s', '%s', '%s');" %(feedback_no, response1, response2, response3))
			conn.commit()
			conn.close()
		return redirect(url_for('saveFeedback'))

@app.route('/savefeedback', methods=['GET', 'POST'])
def saveFeedback():
	if request.method == "POST":
		pass
	return redirect(url_for('thankYouPage'))

@app.route('/thanks')
def thankYouPage():
	conn = psycopg2.connect("dbname=feedbacks")
	cursor = conn.cursor()
	cursor.execute("select count(*) as count from feedbacks")
	total_feedbacks = cursor.fetchall()[0][0]
	cursor.execute("select count(*) from feedback where option1='Yes'")
	total_yes_option1 = cursor.fetchall()[0][0]
	cursor.execute("select count(*) from feedback where option1='No'")
	total_no_option1 = cursor.fetchall()[0][0]
	cursor.execute("select count(*) from feedback where option1='Cannot Say'")
	total_cant_option1 = cursor.fetchall()[0][0]

	cursor.execute("select count(*) from feedback where option2='Yes'")
	total_yes_option2 = cursor.fetchall()[0][0]
	cursor.execute("select count(*) from feedback where option2='No'")
	total_no_option2 = cursor.fetchall()[0][0]
	cursor.execute("select count(*) from feedback where option2='Cannot Say'")
	total_cant_option2 = cursor.fetchall()[0][0]

	cursor.execute("select count(*) from feedback where option3='Yes'")
	total_yes_option3 = cursor.fetchall()[0][0]
	cursor.execute("select count(*) from feedback where option3='No'")
	total_no_option3 = cursor.fetchall()[0][0]
	cursor.execute("select count(*) from feedback where option3='Cannot Say'")
	total_cant_option3 = cursor.fetchall()[0][0]

	conn.close()

	return render_template('thankyou.html', total_feedback=total_feedback, total_yes_option1=total_yes_option1, 
		total_no_option1=total_no_option1, total_cant_option1=total_cant_option1, total_yes_option2=total_yes_option2,
		total_no_option2=total_no_option2, total_cant_option2=total_cant_option2, total_yes_option3=total_yes_option3,
		total_no_option3=total_no_option3, total_cant_option3=total_cant_option3)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
