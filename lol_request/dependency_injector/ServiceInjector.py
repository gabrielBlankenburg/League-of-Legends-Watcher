from functools import wraps

class ServiceInjector:

    def __init__(self):
        self.deps = {}

    def register(self, name=None, *args):
        """Register the dependency

        Parameters
        ----------
        name : str, optional
            Default is none

        Returns
        -------
        function
            The decorated function
        """
        name = name
        def decorator(thing):
            """
            thing here can be class or function or anything really
            """

            if not name:
                if not hasattr(thing, "__name__"):
                    raise Exception("no name")
                thing_name = thing.__name__
            else:
                thing_name = name
            self.deps[thing_name] = {
                'thing': thing,
                'args': args
            }
            return thing

        return decorator

    def get(self, thing):
        """
        Get a thing without initialize it
        """
        return self.deps[thing]['thing']

    def get_new_object(self, thing):
        """
        Create a new object of thing
        """
        return self.deps[thing]['thing'](*self.deps[thing]['args'])

    def inject(self, func):
        """Injects the decorator into something
        
        Parameters
        ----------
        func : class

        Returns
        -------
        function
        """
        @wraps(func)
        def decorated(*args, **kwargs):
            new_args = args + (self, )
            return func(*new_args, **kwargs)

        return decorated

di = ServiceInjector()