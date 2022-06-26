class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def aver_grade(self):
        return sum(sum(value) for value in self.grades.values()) / len(self.grades)

    def __lt__(self, other):
        if not isinstance(other, Student):
            return
        else:
            return self.aver_grade() < other.aver_grade()

    def __str__(self):
        text = f'Имя: {self.name}\n'\
               f'Фамилия: {self.surname}\n'\
               f'Средняя оценка за домашние задания: {self.aver_grade()}\n'\
               f'Курсы в процессе изучения:  {", ".join(self.courses_in_progress)}\n'\
               f'Завершенные курсы: {", ".join(self.finished_courses)}'
        return text


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []
        self.grades = {}

    def aver_grade(self):
        return sum(sum(value) for value in self.grades.values()) / len(self.grades)

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return
        else:
            return self.aver_grade() < other.aver_grade()

    def __str__(self):
        text = f'Имя: {self.name}\n'\
               f'Фамилия: {self.surname}\n'\
               f'Средняя оценка за лекции: {self.aver_grade()}'
        return text


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        text = f'Имя: {self.name}\n'\
               f'Фамилия: {self.surname}'
        return text


def s_aver_grade_course(students, course):
    amount = 0
    for student in students:
        if isinstance(student, Student) and course in student.courses_in_progress:
            amount += sum(student.grades[course])
        else:
            return 'Ошибка'
    return amount / len(students)


def l_aver_grade_course(lecturers, course):
    amount, count = 0, 0
    for lecturer in lecturers:
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached:
            amount += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
        else:
            return 'Ошибка'
    return amount / count


student1 = Student('Bonnie', 'Parker', 'female')
student2 = Student('Clyde', 'Barrow', 'male')
student1.courses_in_progress = ['Python', 'Git', 'Django', 'JavaScript']
student2.courses_in_progress = ['Python', 'Git', 'Django', 'JavaScript']

lecturer1 = Lecturer('John', 'Cena')
lecturer2 = Lecturer('Keanu', 'Reeves')
lecturer1.courses_attached = ['Python', 'Git']
lecturer2.courses_attached = ['Python', 'Django']

reviewer1 = Reviewer('Kermit', 'the Frog')
reviewer2 = Reviewer('Pepe', 'the Frog')
reviewer1.courses_attached = ['Python', 'Git']
reviewer2.courses_attached = ['Django']

student1.rate_lecture(lecturer1, 'Python', 10)
student1.rate_lecture(lecturer1, 'Git', 9)
student1.rate_lecture(lecturer2, 'Python', 8)
student1.rate_lecture(lecturer2, 'Django', 9)

student2.rate_lecture(lecturer1, 'Python', 9)
student2.rate_lecture(lecturer1, 'Git', 7)
student2.rate_lecture(lecturer2, 'Python', 10)
student2.rate_lecture(lecturer2, 'Django', 10)

reviewer1.rate_hw(student1, 'Python', 8)
reviewer1.rate_hw(student2, 'Python', 6)
reviewer1.rate_hw(student1, 'Git', 9)
reviewer1.rate_hw(student2, 'Git', 5)

reviewer2.rate_hw(student1, 'Django', 10)
reviewer2.rate_hw(student2, 'Django', 7)


print(student1, student2, lecturer1, lecturer2, reviewer1, reviewer2, sep='\n\n')
print(f'\n{student1.aver_grade()} > {student2.aver_grade()}: {student1 > student2}')
print(f'{lecturer1.aver_grade()} < {lecturer2.aver_grade()}: {lecturer1 < lecturer2}')
print(s_aver_grade_course([student1, student2], 'Git'))
print(l_aver_grade_course([lecturer1, lecturer2], 'Python'))
