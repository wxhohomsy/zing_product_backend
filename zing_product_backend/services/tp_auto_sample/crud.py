from sqlalchemy.ext.asyncio import AsyncSession


class TPautoSampleDataBase:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def test(self):
        return {'data': 'nothing'}