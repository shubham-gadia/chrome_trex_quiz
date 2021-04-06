import csv
import sys
import re
import os
import datetime
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QDateTime, QTime

def find_seconds(start, end):
    time = end - start
    time_str = str(time).split(':')
    seconds = float(time_str[0]) * 3600 + float(time_str[1]) * 60 + float(time_str[2])
    return seconds

class Question():

    def __init__(self, question, keywords):
        self.question = question
        self.keywords = keywords
        self.answer = ""

    def get_match_percentage(self, ans_bullets):
        final_percentage = []
        intersections = []
        for ans_bullet in ans_bullets:
            for keyword in self.keywords:
                keyword_set = frozenset(keyword)
                intersection = [x for x in ans_bullet if x in keyword_set]
                if len(intersection) > 0:
                    intersection_percentage = len(intersection) / len(keyword_set) * 100
                    intersections.append(intersection)
                    if intersection_percentage > 100:
                        intersection_percentage = 100
                    final_percentage.append(intersection_percentage)

        final_percentage.sort(reverse=True)
        return final_percentage


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        self.count = 0
        self.mintutes_per_question = 10
        self.marks_per_question = 10

        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ui/sub.ui', self) # Load the .ui file
        self.show() # Show the GUI.
        self.test_ongoing = False

        self.evaluated = False

        # Buttons clicked
        self.begin_button.clicked.connect(self.begin_button_pressed)
        self.next_ques_button.clicked.connect(self.next_button_pressed)
        self.submit_button.clicked.connect(self.submit_button_pressed)
        self.previous_ques_button.clicked.connect(self.previous_button_pressed)
        self.home_button.clicked.connect(self.home_button_pressed)

    def home_button_pressed(self):
        os.system('python main.py')
        sys.exit()

    def showTime(self):

        if self.test_ongoing:
            # add 1 second to current time
            self.curr_time = self.curr_time.addSecs(1)
            # get seconds passed
            self.current_seconds = QTime(0, 0, 0).secsTo(self.curr_time)
            # get seconds left (subtracting from total time)
            self.seconds_left = self.total_seconds - self.current_seconds
            # convert seconds left to time
            self.time_left = datetime.timedelta(seconds=self.seconds_left)
            # finally update time left in label
            self.time_left_label.setText("Time Left" + '\n' + str(self.time_left))

        else:
            self.submit_button_pressed()

    def begin_button_pressed(self):
        self.fetch_questions()
        self.evaluated = False

        self.test_ongoing = True
        self.ques_no = 0

        # Enable and disable respective buttons for the ongoing test
        self.answer_textbox.setEnabled(True)
        self.next_ques_button.setEnabled(True)
        self.previous_ques_button.setEnabled(True)
        self.submit_button.setEnabled(True)
        self.time_left_label.setEnabled(True)
        self.begin_button.setEnabled(False)
        self.marks_obtained_label.setEnabled(False)

        self.marks_obtained_label.setText("")

        # calculate total seconds alloted for the test
        self.total_seconds = self.ques_count * 60 * self.mintutes_per_question

        self.time_left_label.setText("Time Left" + '\n' + str(datetime.timedelta(seconds=self.total_seconds)))
        # set current time as 0 i.e when test will start
        self.curr_time = QtCore.QTime(00,00,00)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.next_button_pressed()
        #TODO

    def submit_button_pressed(self):
        
        # save answer of the current question
        self.questions[self.ques_no-1].answer = self.answer_textbox.toPlainText().lower()
        self.answer_textbox.setText(self.questions[self.ques_no-1].answer)

        self.test_ongoing = False

        # Enable and disable respective buttons for the ongoing test
        self.answer_textbox.setEnabled(False)
        self.next_ques_button.setEnabled(False)
        self.previous_ques_button.setEnabled(False)
        self.submit_button.setEnabled(False)
        self.time_left_label.setEnabled(False)
        self.begin_button.setEnabled(True)      

        self.question_label.setText('')
        self.ques_no_label.setText('')
        self.answer_textbox.setText('')

        self.time_left_label.setText('')

        self.evaluate()

        
        #TODO

    def evaluate(self):

        if self.evaluated:
            return

        self.total_marks = []

        for question in self.questions:
            
            filtered_ans = re.sub('[^A-Za-z0-9 .]+', '', question.answer)

            ans_bullets = filtered_ans.split('.')
            final_ans = []

            for ans_bullet in ans_bullets:
                ele = ans_bullet.split(' ')
                final_ans.append(ele)

            match_unfiltered = list(question.get_match_percentage(final_ans))
            match = match_unfiltered[0:len(question.keywords)]

            marks = 0

            for ele in match:
                marks += ele/100 * self.marks_per_question/len(match)

            marks = round(marks, 3)
            self.total_marks.append(marks)

            print("Keywords:", question.keywords)
            print("Answer:", final_ans)
            print("Match:", match)
            print("Marks: ", marks)
            print()

        print("Count:", self.count)
        self.count += 1
        self.evaluated = True

        string = 'Marks Obtained:\n'
        for ele in self.total_marks:
            string += str(ele) + ' + '
        string += '(end) \n= ' + str(sum(self.total_marks)) + '/' + (str(round(self.ques_count * 10, 3)))

        self.marks_obtained_label.setText(string)

        pass

    def update_question(self):
        self.question_label.setText(self.questions[self.ques_no-1].question)
        self.ques_no_label.setText("Ques No:" + str(self.ques_no) + "/" + str(self.ques_count))
        self.answer_textbox.setText(self.questions[self.ques_no-1].answer)

    def next_button_pressed(self):
        self.questions[self.ques_no-1].answer = self.answer_textbox.toPlainText().lower()
        if self.ques_no != self.ques_count:
            self.ques_no += 1
            self.update_question()

    def previous_button_pressed(self):
        self.questions[self.ques_no-1].answer = self.answer_textbox.toPlainText().lower()
        if self.ques_no != 1:
            self.ques_no -= 1
            self.update_question()
            
    def fetch_questions(self):

        self.questions = []
        with open('questions/subjective.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                keywords_unfiltered = []
                for i in range(2, len(row)):
                    tlist = row[i].split()
                    keywords_unfiltered.append(tlist)

                keywords = [x for x in keywords_unfiltered if x]

                question = Question(row[1], keywords)
                self.questions.append(question)
                
                '''ans_bullets = [['thread', 'switching', 'involves', 'kernel'], ['two', 'mode', 'switch', 'required'], ['ktl', 'switching', 'slower', 'compared', 'utl', 'full', 'process', 'switch']]
                match_unfiltered = list(question.get_match_percentage(ans_bullets))
                match = match_unfiltered[0:len(keywords)]

                print("Keywords:", keywords)
                print("Answer:", ans_bullets)
                print("Match:", match)
                print()'''

        self.ques_count = len(self.questions)
        pass
        #TODO

    def keyPressEvent(self,event):
        key=event.key()
        if key==QtCore.Qt.Key_Up or (event.type()==QtCore.QEvent.KeyPress and key==QtCore.Qt.Key_Space):
            print('space pressed')

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()