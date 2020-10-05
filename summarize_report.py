#!/usr/bin/env python
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np

def main():
    args = parse_args()
    csv_file = args[0]
    mtg_name = args[1]
    questions = dict()
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            num_cells = len(row)

            # first question is in column 4. zoom always adds an empty cell/additional comma.
            if num_cells <= 5:  # this catches the header comment row
                continue
            datetimestr = row[3]
            for i in range(4, num_cells - 1, 2):
                question = row[i]
                answer = row[i + 1]

                if question not in questions:
                    questions[question] = Question(question)
                questions[question].record_answer(answer)

    poll = Poll(questions,mtg_name,datetimestr)
    for question in questions.values():
        question.print()
    poll.plot()
         
    plt.show()

    


def parse_args():
    meetingName = 'In Meeting'
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <zoom poll report csv file> [meeting title]\n" % (sys.argv[0]))
        sys.stderr.flush()
        sys.exit(1)
    if len(sys.argv) == 3:
        meetingName = sys.argv[2]
    return [ sys.argv[1], meetingName]

class Poll:
    def __init__(self,Qs,mn,ds):
        self.questions = Qs  # dict{str:Question}
        self.nq = len(Qs)
        self.date_time_str = ds
        self.mtg_name = mn
        
    def plot(self):
        plotsize = 3
        vsize = plotsize*len(self.questions)
        fig, axs = plt.subplots(self.nq,1,constrained_layout=True,sharex=True)
        fig.suptitle( self.mtg_name + ' Zoom poll '+self.date_time_str, fontsize=16)
        j=0
        for q in list( self.questions.values()):
            q.graph(fig,axs[j])
            j+=1
            
class Question:
    def __init__(self, question):
        self.question = question
        self.answers = dict()

    def record_answer(self, answer):
        if answer not in self.answers:
            self.answers[answer] = 0
        self.answers[answer] += 1

    def print(self):
        print(self.question)
        for answer in sorted(list(self.answers.keys())):
            print("%s: %s" % (answer, self.answers[answer]))
        print() 
            
        
    def graph(self,fig,ax): 
        ansl    = list(self.answers.keys())
        counts = list(self.answers.values())
        ac = zip(counts,ansl)
        ans_sort = [x for _,x in sorted(ac,reverse=True)]
        c_sort = sorted(counts,reverse=True)
        ansl = ans_sort
        counts = c_sort
        y_pos = np.arange(len(ansl)) 
        ax.barh(y_pos, counts, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(ansl)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Number of Responses')
        ax.set_title(self.question)
        
       

if __name__ == '__main__':
    main()
