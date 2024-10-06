# entities.py
import random

class Batch:
    def __init__(self, batch_id, size, subjects):
        self.batch_id = batch_id
        self.size = size
        self.subjects = subjects

class Teacher:
    def __init__(self, teacher_id, name, subjects, availability=None):
        self.teacher_id = teacher_id
        self.name = name
        self.subjects = subjects
        self.availability = availability if availability else []

class Classroom:
    def __init__(self, class_id, size, coordinates, resources=None):
        self.class_id = class_id
        self.size = size
        self.coordinates = coordinates
        self.resources = resources if resources else []

class Timetable:
    def __init__(self, batches, teachers, classrooms, time_slots):
        self.batches = batches
        self.teachers = teachers
        self.classrooms = classrooms
        self.time_slots = time_slots 
        self.schedule = {} 
        self.fitness = None

    def initialize_random(self):
        for batch in self.batches:
            for subject in batch.subjects:
                assigned = False
                while not assigned:
                    time_slot = random.randint(0, self.time_slots - 1)
                    teacher = self.get_teacher_for_subject(subject, time_slot)
                    classroom = self.get_available_classroom(batch.size, time_slot)
                    if teacher and classroom:
                        self.schedule[(batch.batch_id, subject)] = {
                            'time_slot': time_slot,
                            'teacher': teacher,
                            'classroom': classroom
                        }
                        assigned = True

    def get_teacher_for_subject(self, subject, time_slot):
        available_teachers = [
            t for t in self.teachers
            if subject in t.subjects and (not t.availability or time_slot in t.availability)
        ]
        return random.choice(available_teachers) if available_teachers else None

    def get_available_classroom(self, size, time_slot):
        available_rooms = [
            c for c in self.classrooms
            if c.size >= size and self.is_classroom_free(c, time_slot)
        ]
        return random.choice(available_rooms) if available_rooms else None

   
    def is_classroom_free(self, classroom, time_slot):
        for sched in self.schedule.values():
            if sched['classroom'].class_id == classroom.class_id and sched['time_slot'] == time_slot:
                return False
        return True

    
    def calculate_fitness(self):
        penalty = self.check_hard_constraints()
        self.fitness = -penalty 
        return self.fitness

    
    def check_hard_constraints(self):
        penalty = 0
        classroom_time = {}
        teacher_time = {}
        batch_time = {}

        for (batch_id, subject), details in self.schedule.items():
            time_slot = details['time_slot']
            teacher = details['teacher']
            classroom = details['classroom']

            
            if (classroom.class_id, time_slot) in classroom_time:
                penalty += 1
            else:
                classroom_time[(classroom.class_id, time_slot)] = True

            
            if (teacher.teacher_id, time_slot) in teacher_time:
                penalty += 1
            else:
                teacher_time[(teacher.teacher_id, time_slot)] = True

            
            if (batch_id, time_slot) in batch_time:
                penalty += 1
            else:
                batch_time[(batch_id, time_slot)] = True

            
            batch = next(b for b in self.batches if b.batch_id == batch_id)
            if classroom.size < batch.size:
                penalty += 1

            
            if teacher.availability and time_slot not in teacher.availability:
                penalty += 1

        return penalty
