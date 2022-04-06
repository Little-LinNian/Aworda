from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from graia.ariadne.model import Member


class Amember():
    def __init__(self, member: Member):
        self.member = member


class AmemberDispatcher(BaseDispatcher):

    async def catch(self, interface: DispatcherInterface):
        if interface.annotation == AMember:
            member: Member = interface.lookup_param('member')
            return Amember(member)

