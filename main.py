# main.py
from genetic_algorithm import GeneticAlgorithm
from entities import Batch, Teacher, Classroom

def main():
    # Define batches
    batches = [
        Batch(batch_id="Batch1", size=30, subjects=["Math", "Science", "English"]),
        Batch(batch_id="Batch2", size=25, subjects=["Math", "History", "Geography"]),
        Batch(batch_id="Batch3", size=20, subjects=["Science", "English", "Art"]),
        # Add more batches as needed
    ]

   
    teachers = [
        Teacher(teacher_id="T1", name="Ram", subjects=["Math", "Science"], availability=list(range(0, 5))),
        Teacher(teacher_id="T2", name="Shyam", subjects=["English", "History"], availability=list(range(0, 5))),
        Teacher(teacher_id="T3", name="Krishna", subjects=["Geography", "Art"], availability=list(range(0, 5))),
        Teacher(teacher_id="T4", name="Geeta", subjects=["Math", "Art"], availability=list(range(0, 5))),
     
    ]


    classrooms = [
        Classroom(class_id="Room1", size=40, coordinates=(1, 1), resources=["Projector"]),
        Classroom(class_id="Room2", size=30, coordinates=(1, 2), resources=["Lab"]),
        Classroom(class_id="Room3", size=25, coordinates=(2, 1), resources=[]),
        Classroom(class_id="Room4", size=35, coordinates=(2, 2), resources=["Projector"]),
     
    ]

    time_slots = 5  

    ga = GeneticAlgorithm(
        population_size=50,
        mutation_rate=0.1,
        crossover_rate=0.8,
        generations=100,
        batches=batches,
        teachers=teachers,
        classrooms=classrooms,
        time_slots=time_slots
    )

    best_timetable = ga.evolve()
    print("\nBest Timetable:")
    for (batch_id, subject), details in best_timetable.schedule.items():
        teacher = details['teacher'].name if details['teacher'] else "None"
        classroom = details['classroom'].class_id if details['classroom'] else "None"
        print(f"Batch: {batch_id}, Subject: {subject}, Time Slot: {details['time_slot']}, Teacher: {teacher}, Classroom: {classroom}")

if __name__ == "__main__":
    main()
