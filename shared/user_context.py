import contextvars

# Create a context variable for user_id
user_id_var = contextvars.ContextVar("user_id")
cohort_var = contextvars.ContextVar("cohort")


user_id_var.set(None)
cohort_var.set(None)