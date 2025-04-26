import contextvars

# Create a context variable for user_id
user_id_var = contextvars.ContextVar("user_id")
user_id_var.set(None)
skill_var = contextvars.ContextVar("skill")
skill_var.set(None)
location_var = contextvars.ContextVar("location")
location_var.set(None)
