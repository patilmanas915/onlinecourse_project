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

    correct = sum([1 for c in choices if c.is_correct])
    total = choices.count()

    score = (correct / total) * 100 if total > 0 else 0

    return render(request, 'exam_result_bootstrap.html', {
        'score': score,
        'choices': choices
    })

