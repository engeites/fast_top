from .plugins import DialogsCreated, SuccessRechargePlugin, FailedRechargePlugin, \
RechargedAmountPlugin, RechargedUsers, AgentRecharges, DialogsByTime, RechargeTime, AgentAverageRechargeTime, ChannelEffectiveness

from .manager import PluginManager

plugins = [
    DialogsCreated,
    SuccessRechargePlugin,
    FailedRechargePlugin,
    RechargedAmountPlugin,
    RechargedUsers,
    AgentRecharges,
    DialogsByTime,
    RechargeTime,
    AgentAverageRechargeTime,
    ChannelEffectiveness
]