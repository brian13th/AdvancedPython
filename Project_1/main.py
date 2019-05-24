# N. Avouris May 2018, class Main - project week 3
# persistant data with sqlite3
# dependencies : files <db_file>.sqlite.sql with definition of database
#		acctress.txt and actors.txt downloaded from wikipedia
#               λήμμα: Ελληνες/Εληνίδες ηθοποιοί κινηματογράφου
import os
import os.path
import sqlite3 as lite
import random
import re

VERBOSE = False # δώσε τιμή True για εκτύπωση πληροφοριών των εντολών SQL
#################################################################################################
class Student:
    '''
    Κλάση φοιτητών ενός μαθήματος με 4 εργασίες, 2 εξετάσεις
    '''
    students = []

    @staticmethod
    def order_students_list(student_list):
        '''Ταξινόμηση της λίστας Student.students κατά αλφαβητική σειρά επωνύμου φοιτητή'''
        # TODO (ΤΜΗΜΑ ΕΡΩΤΗΜΑΤΟΣ 3) να ταξινομήσετε τη λίστα students (χρήσιμο για τα ερωτήματα
        sorted_students = sorted(student_list, key=lambda x: x.name.split()[1])
        return sorted_students

    @staticmethod
    def find_am(am):
        '''αναζήτηση φοιτητή με τον αριθμό μητρώου του, επιστρέφει το αντικείμενο Student ή False'''
        for s in Student.students:
            if am == s.am: return s
        return False

    @staticmethod
    def success_rate():
        '''υπολογίζει το πλήθος φοιτητών που πέρασαν και αυτών που απέτυχαν, τυπώνει πλήθος και ποσοστό'''
        # TODO (ΤΜΗΜΑ ΕΡΩΤΗΜΑΤΟΣ 4). να τυπώσετε το πλήθος φοιτητών που πέρασαν και απέτυχαν, καθώς και το ποσοστό επιτυχίας
        sum_fail = 0
        sum_pass = 0
        for student in Student.order_students_list(Student.students):
            # print(student.final_grade(),'parto',type(student.final_grade()))
            if student.final_grade() == -1:
                sum_fail += 1
            elif student.final_grade() < 5:
                sum_fail += 1
            else:
                sum_pass += 1
        percentage = (sum_pass/(sum_pass + sum_fail))*100
        print(f'ΠΕΤΥΧΑΝ = {sum_pass}\tΑΠΕΤΥΧΑΝ = {sum_fail}\tΠΟΣΟΣΤΟ ΕΠΙΤΥΧΙΑΣ: {percentage:.1f}%')

    def __init__(self, am, name):
        self.am = str(am)
        self.name = name  # ονοματεπώνυμο φοιτητή - το επώνυμο η τελευταία λέξη
        self.grades = [-1, -1, -1, -1]  # βαθμολογία εργασιών
        self.exam1 = -1  # τελική εξέταση
        self.exam2 = -1  # επαναληπτική εξέταση
        Student.students.append(self)

    def add_exam1(self, mark):
        try:
            self.exam1 = float(mark)
        except:
            return False

    def add_exam2(self, mark):
        try:
            self.exam2 = float(mark)
        except:
            return False

    def final_grade(self):
        '''Υπολογισμός τελικού βαθμού'''
        score = 0
        for g in self.grades:
            if g >= 0: score += g
        if score < 20: return -1
        exam = max(self.exam1, self.exam2)
        if exam >= 5:
            final = round((0.7 * exam + 0.3 * score / 4) * 2) / 2
            return final
        elif exam >= 0:
            return exam
        else:
            return -1

    def final_score(self):
        ''' επιστρέφει φοιτητή και τελικό βαθμό '''
        return '{} {:30s}\t{:4.1f}'.format(self.am, self.name, self.final_grade())

    def final_exams_check(self):
        '''  έλεγχος αν ο φοιτητής επιτρέπεται να συμμετάσχει στην τελική εξέταση'''
        # TODO : ΕΡΩΤΗΜΑ 1. να υλοποιήσετε τη μέθοδο ώστε να επιτρέπεται η συμμετοχή στην τελική εξέταση
        # μόνο για φοιτητές που ικανοποιούν το κριτήριο
        if self.grades.count(-1) < 2:
            if self.grades.count(-1) == 0:
                sum = 0
                for grade in self.grades:
                    sum += grade
                if sum >= 20:
                    return True
                else:
                    return False
            else:
                sum = 1
                for grade in self.grades:
                    sum += grade
                if sum > 20:
                    return True
                else:
                    return False
        else:
            return False
    def print_scores(self):
        'επιστρέφει λεπτομερή καταγραφή στοιχείων φοιτητή'
        return '{} {:30s}[\t{:.1f} \t{:.1f} \t{:.1f} \t{:.1f}]\t\t\t[{:.1f}. \t{:.1f}]'.format( \
            self.am, self.name, *self.grades, self.exam1, self.exam2)

    def __str__(self):
        'στοιχεία φοιτητή και τελικός βαθμός για τελική βαθμολογία τάξης'
        return '{} {} {:.2f}'.format(self.am, self.name, self.final_grade())


class Create():
    '''
    Εργαλείο για τη δημιουργία εγγραφών στην κλάση Student
    '''

    def __init__(self, default_size=0):
        ''' define size and create new cohort of students if <enter> return False'''
        if not default_size:
            self.class_size = self.define_size()
        else:
            self.class_size = default_size
        # υπόθεση ότι οι κατανομές των βαθμολογιών για τις εργασίες και τελική εξέταση είναι κανονικές
        # με μέσες τιμές όπως παρακάτω (χρησιμοποιούνται στη μέθοδο _random_score)
        self.mean_work = 8
        self.mean_final = 6
        self.mean_resit = 5.5

    def define_size(self):
        while True:  # define size of new cohort
            try:
                class_size = input('Μέγεθος τάξης:(1-500 φοιτητές):')
                if class_size == '': return False
                class_size = int(class_size)
                if class_size >= 1 and class_size <= 500: break
            except:
                print('Παρακαλώ δώστε το πλήθος των φοιτητών')
                return 0
        return class_size

    def _create_names(self):
        class_size = self.class_size
        act_names_files = ('actresses.txt', 'actors.txt')
        names = []
        for f in act_names_files:
            with open(f, 'r', encoding='utf-8') as fin:
                for line in fin:
                    if len(line) > 2:
                        name = re.sub(r'\(.*\)', '', line.strip())
                        if len(name.split()) > 1:
                            names.append(name)
        # Select class_size names from names list
        if class_size < len(names):
            student_names = random.sample(names, class_size)
        else:
            student_names = names
        return student_names

    def _random_score(self, mean=5):
        # επιστρέφει ένα αριθμό από 0 έως 10 με ακρίβεια 0.5, μέση τιμή = mean
        while True:
            score = round(
                random.gauss(mean, 3.0) * 2) / 2  # χρήση κανονικής κατανομής με μέση τιμή mean και τυπικής απόκλιση 3
            if score <= 10.0 and score >= 0.0: return score

    def _remove_students(self):
        for s in Student.students:  # remove instances
            del s
        Student.students = []  # clear class objects list

    def create_new_cohort(self):
        self._remove_students()
        student_names = self._create_names()
        for i in range(self.class_size):  # δημιουργία φοιητών πλήθους class_size
            grades = []
            # υποθέτουμε 80% συμμετοχή στις εργασίες
            for j in range(4):
                if random.randint(1, 100) > 20:  # 20% δεν υποβάλει εργασία
                    grade = self._random_score(self.mean_work)  # μέση τιμή βαθμολογίας self.mean_work
                    grades.append(grade)
                else:
                    grades.append(-1)
            am = str(i + 100)  # υποθέτουμε ότι οι αριθμοί μητρώου είναι ακέραιοι που αρχίζουν από 100
            s = Student(am, student_names[i])  # δημιουργία νέου φοιτητή
            s.grades = grades  # βαθμολογίες εργασιών
            if s.final_exams_check():  # έλεγχος αν ο φοιτητής επιτρέπεται να εξεταστεί
                s.add_exam1(self._random_score(self.mean_final))  # μέση τιμή τελικής εξέτασης self.mean_final
                if s.exam1 < 5:  # αν απέτυχε στην τελική εξέταση συμμετοχή στην επαναληπτική εξέταση
                    s.add_exam2(self._random_score(self.mean_resit))  # μέση τιμή επαναληπτικής εξέτασης self.mean_resit
        Student.order_students_list(Student.students)
        print('...δημιουργήθηκε επιτυχώς νέα τάξη από {} φοιτητές\n'.format(self.class_size))
        return True

########################################################################################################
class Main():
    def __init__(self):
        self.db_file = 'students'
        self.exam_names = ['Εργασία 1', 'Εργασία 2', 'Εργασία 3', 'Εργασία 4', 'Τελική Εξέταση', 'Επαναληπτική Εξέταση']
        self.db = self.db_file + '.sqlite'  # το όνομα της βάσης δεδομένων sqlite3
        # Αν δεν υπάρχει το αρχείο της βάσης δεδομένων κάλεσε την self.create_database
        if not os.path.isfile(self.db):
            self.create_database()
        # διάβασε τη βάση δεδομένων που υπάρχει ήδη
        if os.path.isfile(self.db):
            self.read_sql_database()
        # main MENU
        while True:
            print('\nΠροχωρημένος Προγραμματισμός με την Python [ Εργασία Αλληλοαξιολόγησης 1 ]')
            print('(Υπάρχουν {} φοιτητές στη βάση δεδομένων)'.format(len(Student.students)))
            print('\t\t1. Δημιουργία νέας τάξης' +
                  '\n\t\t2. Λεπτομερής βαθμολογία φοιτητών' +
                  '\n\t\t3. Τελική βαθμολογία φοιτητών\n' +
                  '\t\t4. Μέση βαθμολογία & ποσοστό επιτυχίας ανά εξεταστική\n' +
                  '\t\t<enter> Εξοδος')
            select = '  '
            while select not in '1 2 3 4'.split():
                select = input('>>> ΕΠΙΛΟΓΗ: ')
                if select == '': break
            else:
                if select == '1': # 1. δημιουργία νέας τάξης
                    self.question_1()
                elif select == '2': # 2. λεπτομερής βαθμολογία
                    self.question_2()
                elif select == '3': # 3. τελική βαθμολογία
                    self.question_3()
                elif select == '4': # ποσοστό επιτυχίας στις εξετάσεις
                    self.question_4()
            if select == '': break

    def create_database(self):
        # διάβασε από το αρχείο sql τις εντολές για δημιουργία της βάσης δεδομένων
        if os.path.isfile(self.db + '.sql'):  # αυτό είναι το export του sqlite3 DB Browser
            with open(self.db + '.sql') as f:
                sql = f.read()
                sql = sql.replace('\n', '').replace('\t', '').replace('`', ' ').split(';')

                try:
                    conn = lite.connect(self.db)
                    c = conn.cursor()
                    for query in sql[:6]:
                        c.execute(query)
                except:
                    print('Σφάλμα στην δημιουργία βάσεων δεδομένων')
                    return False

        # πρόσθεσε τα στοιχεία των εξετάσεων στον πίνακα exam
        #TODO: ΕΡΩΤΗΜΑ 2. να υλοποιηθεί η δημιουργία της βάσης δεδομένων
        return True

    def read_sql_database(self):
        try:
            con = lite.connect(self.db)
            with con:
                cur = con.cursor()
                # διάβασε τα στοιχεία φοιτητών και βαθμολογιών από τη βάση δεδομένων
                sql = 'SELECT * FROM student, exam_score WHERE student.id = exam_score.student_id'
                # this sql returns (id, name, surname id, exam, score)
                cur.execute(sql)
                for row in cur.fetchall():
                    if VERBOSE: print(row)
                    st = Student.find_am(str(row[0]))  # έλεγξε αν ο φοιτητής υπάρχει ήδη
                    if not st:
                        name = row[1] + ' ' + row[2]
                        st = Student(str(row[0]), name) # δημιουργία νέου αντικειμένου Student
                    ind = row[4]
                    if ind == '4':
                        st.exam1 = float(row[5])
                    elif ind == '5':
                        st.exam2 = float(row[5])
                    elif ind in '0 1 2 3'.split():
                        st.grades[int(ind)] = float(row[5])
                    else:
                        print('error')
        except:
            print('error in reading students from database')
            return False

    def save_to_sql_database(self):
        '''αποθήκευσε τους φοιτητές της κλάσης Student στη βάση δεδομένων students.sqlite'''
        sql1 = 'INSERT INTO student(id,name,surname) VALUES (?,?,?);'
        sql2 = 'INSERT INTO exam_score(student_id, exam_id, score) VALUES (?,?,?);'
        try:
            con = lite.connect(self.db)
            with con:
                cur = con.cursor()
                # διαγραφή των εγγραφών των πινάκων student και exam_score
                for t in ['student', 'exam_score']:
                    sql = 'DELETE from {};'.format(t)
                    cur.execute(sql)
                    cur.execute('COMMIT;')
                # εισαγωγή των νέων φοιτητών, αντικειμένων της κλάσης Student
                for s in Student.students:
                    name = ' '.join(s.name.split()[:1])
                    surname = s.name.split()[-1]
                    if VERBOSE: print(s.am, name, surname)
                    cur.execute(sql1, (s.am, name, surname))
                    cur.execute('COMMIT;')
                    grades = s.grades + [s.exam1, s.exam2]
                    for i,g in enumerate(grades):
                        if g > -1:
                            if VERBOSE: print(s.am, self.exam_names[i], g)
                            cur.execute(sql2, (s.am, i, g))
                            cur.execute('COMMIT;')
            return True
        except:
            print('σφάλμα στην εισαγωγή φοιτητών στη βάση δεδομένων ')
            return False

    def question_1(self):
        c = Create()
        if c.class_size:
            c.create_new_cohort()
            self.save_to_sql_database()

    def question_2(self):
        print('\nΣυνολικός κατάλογος βαθμολογιών')
        # TODO ΕΡΩΤΗΜΑ 3. να τυπώσετε τις συνολικές βαθμολογίες αλφαβητικά
        for student in Student.order_students_list(Student.students):
            print(student.print_scores())
        Student.success_rate()

    def question_3(self):
        print('\nΤελική βαθμολογία')
        # TODO ΕΡΩΤΗΜΑ 4. να παρουσιάσετε την τελική βαθμολογία με τον τελικό βαθμό, αλφαβητικά
        for student in Student.order_students_list(Student.students):
            print(student)
        Student.success_rate()
    def question_4(self):
        # TODO ΕΡΩΤΗΜΑ 5. Να παρουσιάσετε την τελική βαθμολογία
        sum_final, sum_final_last = 0, 0
        sum_grade, sum_grade_last = 0, 0
        sum_final_succes, sum_final_succes_last = 0, 0

        for student in Student.order_students_list(Student.students):
            if student.final_exams_check():
                sum_final += 1
                sum_grade += student.exam1
                if student.exam1 >= 5:
                    sum_final_succes +=1
                else:
                    sum_final_last += 1
                    sum_grade_last += student.exam2
                    if student.exam2 >= 5:
                        sum_final_succes_last +=1
        if sum_final is not 0:
            print(f'Τελική εξέταση [συμμετοχή {sum_final}]: μέση βαθμολογία = { sum_grade/sum_final:.2f}, ποσοστό επιτυχίας = {(sum_final_succes/sum_final)*100:.1f}%')
            if sum_final_last is not 0:
                print(f'Τελική εξέταση [συμμετοχή {sum_final_last}]: μέση βαθμολογία = {sum_grade_last / sum_final_last:.2f}, ποσοστό επιτυχίας = {( sum_final_succes_last / sum_final_last) * 100:.1f}%')
            elif sum_final_last == 0:
                print(f'Πέρασαν όλοι το μάθημα από την τελική εξέταση!!')
        elif sum_final == 0:
            print(f'Δεν πέρασε κανένας μαθητής το μάθημα..')

if __name__ == "__main__": Main()
