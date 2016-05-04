from . import zenpacklib
CFG = zenpacklib.load_yaml()

# zenpacklib redefines ZenPack
from Products.ZenModel.OperatingSystem import OperatingSystem

from . import schema
import logging
log = logging.getLogger('zen.UserGroup')

class ZenPack(schema.ZenPack):
    def install(self, app):
        super(ZenPack, self).install(app)
        #for d in self.dmd.Devices.getSubDevices():
             #d.os.buildRelations()
        self.rebuildRelations()

    def remove(self, app, leaveObjects=False):
	OperatingSystem._relations = tuple([x for x in OperatingSystem._relations if x[0] not in ['userGroups']])
        self.rebuildRelations()
	#for d in self.dmd.Devices.getSubDevices():
	#     d.os.buildRelations()

        super(ZenPack, self).remove(app, leaveObjects)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self.rebuildRelations()

    def rebuildRelations(self):
        for d in self.dmd.Devices.getSubDevicesGen():
            log.debug('Building relations for: %s', d.id)
            d.buildRelations()
            d.os.buildRelations()
