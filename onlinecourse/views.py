from django.shortcuts import render
from .models import Course, Submission, Choice

def submit(request, course_id):
    selected_choices = request.POST.getlist('choice')
    submission = Submission.objects.create(user=request.user)

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=choice_id)
        submission.choices.add(choice)

    return show_exam_result(request, submission.id)

def show_exam_result(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    choices = submission.choices.all()

    total_questions = len(choices)
    correct_answers = sum([1 for c in choices if c.is_correct])

    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    return render(request, 'exam_result_bootstrap.html', {
        'score': score,
        'choices': choices,
        'total': total_questions,
        'correct': correct_answers
    })

