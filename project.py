from flask import Flask, render_template, request, redirect, url_for
import psycopg2, pygal

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
	cursor.execute("select count(*) as count from feedbacks;")
	total_feedbacks = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Yes'")
	total_yes_option1 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='No'")
	total_no_option1 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Cannot Say'")
	total_cant_option1 = float(cursor.fetchall()[0][0])

	cursor.execute("select count(*) from feedbacks where response2='Yes'")
	total_yes_option2 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response2='No'")
	total_no_option2 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response2='Cannot Say'")
	total_cant_option2 = float(cursor.fetchall()[0][0])

	cursor.execute("select count(*) from feedbacks where response3='Yes'")
	total_yes_option3 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response3='No'")
	total_no_option3 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response3='Cannot Say'")
	total_cant_option3 = float(cursor.fetchall()[0][0])
        
        data1 = [(total_yes_option1/total_feedbacks)*100, (total_no_option1/total_feedbacks)*100, (total_cant_option1/total_feedbacks)*100]
        data2 = [(total_yes_option2/total_feedbacks)*100, (total_no_option2/total_feedbacks)*100, (total_cant_option2/total_feedbacks)*100]
        data3 = [(total_yes_option3/total_feedbacks)*100, (total_no_option3/total_feedbacks)*100, (total_cant_option3/total_feedbacks)*100]

        options = ["Yes", "No", "Can't Say"]

        bar_chart1 = pygal.Bar(width=600, height=300,
                          explicit_size=True, title="Q1.",
                          disable_xml_declaration=True)

        bar_chart1.x_labels = options

        bar_chart2 = pygal.Bar(width=600, height=300,
                          explicit_size=True, title="Q2.",
                          disable_xml_declaration=True)

        bar_chart2.x_labels = options

        bar_chart3 = pygal.Bar(width=600, height=300,
                          explicit_size=True, title="Q3.",
                          disable_xml_declaration=True)

        bar_chart3.x_labels = options
        
        bar_chart1.add('Answers for Q1.', data1)
        bar_chart2.add('Answers for Q2.', data2)
        bar_chart3.add('Answers for Q3.', data3)

	conn.close()

	return render_template('thankyou.html', bar_chart1 = bar_chart1, bar_chart2 = bar_chart2, bar_chart3 = bar_chart3)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
