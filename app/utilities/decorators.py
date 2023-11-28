from app.exceptions import ExceptionHandling


def handle_reconnect(func):
    def wrapper(self, *args, **kwargs):
        retries = 3
        for _ in range(retries):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")
                self.reconnect()
        print(f"Failed to execute {func.__name__} after {retries} retries.")
    return wrapper


def handle_exceptions(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            message = f"Error in {func.__name__}: {e}"
            return await ExceptionHandling.custom500(message)
    return wrapper
