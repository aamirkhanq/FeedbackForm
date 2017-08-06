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
                response4 = request.form['t1']

		conn = psycopg2.connect("dbname=feedbacks")
		cursor = conn.cursor()
		cursor.execute("select feedback_no from feedbacks order by feedback_no desc limit 1;")
		last_feedback = cursor.fetchall()
		try:
			feedback_no = int(last_feedback[0][0]) + 1
			cursor.execute('insert into feedbacks ("feedback_no", "response1", "response2", "response3", "response4") values ('+ "'%s', '%s', '%s', '%s', '%s');" %(feedback_no, response1, response2, response3, response4))
			conn.commit()
			conn.close()
		except:
			feedback_no = 1
			cursor.execute('insert into feedbacks ("feedback_no", "response1", "response2", "response3", "response4") values ('+ "'%s', '%s', '%s', '%s', '%s');" %(feedback_no, response1, response2, response3, response4))
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
	if total_feedbacks == 0:
                total_feedbacks = 1;
	cursor.execute("select count(*) from feedbacks where response1='Strongly Disagree'")
	total_1_option1 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Disagree'")
	total_2_option1 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Agree'")
	total_3_option1 = float(cursor.fetchall()[0][0])
        cursor.execute("select count(*) from feedbacks where response1='Strongly Agree'")
	total_4_option1 = float(cursor.fetchall()[0][0])

	cursor.execute("select count(*) from feedbacks where response1='Strongly Disagree'")
	total_1_option2 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Disagree'")
	total_2_option2 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Agree'")
	total_3_option2 = float(cursor.fetchall()[0][0])
        cursor.execute("select count(*) from feedbacks where response1='Strongly Agree'")
	total_4_option2 = float(cursor.fetchall()[0][0])

	cursor.execute("select count(*) from feedbacks where response1='Strongly Disagree'")
	total_1_option3 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Disagree'")
	total_2_option3 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Agree'")
	total_3_option3 = float(cursor.fetchall()[0][0])
        cursor.execute("select count(*) from feedbacks where response1='Strongly Agree'")
	total_4_option3 = float(cursor.fetchall()[0][0])

        cursor.execute("select count(*) from feedbacks where response1='Strongly Disagree'")
	total_1_option4 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Disagree'")
	total_2_option4 = float(cursor.fetchall()[0][0])
	cursor.execute("select count(*) from feedbacks where response1='Agree'")
	total_3_option4 = float(cursor.fetchall()[0][0])
        cursor.execute("select count(*) from feedbacks where response1='Strongly Agree'")
	total_4_option4 = float(cursor.fetchall()[0][0])
        
        data1 = [(total_1_option1/total_feedbacks)*100, (total_2_option1/total_feedbacks)*100, (total_3_option1/total_feedbacks)*100, (total_4_option1/total_feedbacks)*100]
        data2 = [(total_1_option2/total_feedbacks)*100, (total_2_option2/total_feedbacks)*100, (total_3_option2/total_feedbacks)*100, (total_4_option2/total_feedbacks)*100]
        data3 = [(total_1_option3/total_feedbacks)*100, (total_2_option3/total_feedbacks)*100, (total_3_option3/total_feedbacks)*100, (total_4_option3/total_feedbacks)*100]
        data4 = [(total_1_option4/total_feedbacks)*100, (total_2_option4/total_feedbacks)*100, (total_3_option4/total_feedbacks)*100, (total_4_option4/total_feedbacks)*100]

        options = ["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"]

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

        bar_chart4 = pygal.Bar(width=600, height=300,
                          explicit_size=True, title="Q3.",
                          disable_xml_declaration=True)

        bar_chart4.x_labels = options
        
        bar_chart1.add('Answers for Q1.', data1)
        bar_chart2.add('Answers for Q2.', data2)
        bar_chart3.add('Answers for Q3.', data3)
        bar_chart4.add('Answers for Q4.', data4)

	conn.close()

	return render_template('thankyou.html', bar_chart1 = bar_chart1, bar_chart2 = bar_chart2, bar_chart3 = bar_chart3, bar_chart4 = bar_chart4)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
