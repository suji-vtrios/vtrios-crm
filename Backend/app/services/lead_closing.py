if student_ready:
    action = "ENROLL"

elif student_uncertain:
    action = "COUNSELOR_CALL"

elif student_evaluating:
    action = "DEMO_SESSION"

else:
    action = "FOLLOW_UP"