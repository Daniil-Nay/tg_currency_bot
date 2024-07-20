class InjectMiddleware:
    """
    Данная миддлварь нужна для передочи дополнительных параметров в методы (хэндлеры) роутеров.
    """
    def __init__(self, **kwargs):
        self.dependencies = kwargs

    async def __call__(self, handler, event, data):
        data.update(self.dependencies)
        return await handler(event, data)