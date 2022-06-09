#!/usr/bin/env python3
import time
import json
# from benedict import benedict
from xhc_whb04b_6 import Xhb04b_6


from dsf.connections import SubscribeConnection
from dsf.initmessages.clientinitmessages import SubscriptionMode


def subscribe():
    subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH, "", ['move/axes/**'])
    subscribe_connection.connect()

    try:
        # Get the complete model once
        machine_model = subscribe_connection.get_machine_model()
        # machX = float(machine_model["move"]["axes"][0]["machinePosition"])
        # machY = float(machine_model["move"]["axes"][1]["machinePosition"])
        # machZ = float(machine_model["move"]["axes"][2]["machinePosition"])

        # cncPendant.displayStatus.X = machX
        # cncPendant.displayStatus.Y = machY
        # cncPendant.displayStatus.Z = machZ
        # cncPendant.UpdateDisplay()
        # print(machine_model)
        # "move":{"axes":[{"machinePosition":10.1,"userPosition":10.1},{},{}]}
        # machX = int(machine_model["move"]["axes"][0]["machinePosition"])
        # mach_y = int(machine_model["move"]["axes"][1]["machinePosition"])
        # mach_z = int(machine_model["move"]["axes"][2]["machinePosition"])

		# cncPendant.displayStatus.X = X
  #       cncPendant.displayStatus.Y = mach_y
		# cncPendant.displayStatus.Z = mach_z
		# cncPendant.UpdateDisplay()

        # Get multiple incremental updates, due to SubscriptionMode.PATCH, only a
        # subset of the object model will be updated
        while 1:
            upd = subscribe_connection.get_machine_model_patch()
            update = json.loads(upd)
            print(update)
            if ('move' in update) and ('axes' in update["move"]):
            	for ind, val in enumerate(update["move"]["axes"]):
            		if val and "machinePosition" in val:
            			print(val)
            			machVal = float(val["machinePosition"])
            			if ind == 0:
            				# cncPendant.displayStatus.X = machVal
            				print(ind, machVal)
            			elif ind == 1:
            				# cncPendant.displayStatus.Y = machVal
            				print(ind, machVal)
            			elif ind == 2:
            				# cncPendant.displayStatus.Z = machVal
            				print(ind, machVal)
            	# cncPendant.UpdateDisplay()
            time.sleep(0.3)
    finally:
        subscribe_connection.close()



# cncPendant = Xhb04b_6()


if __name__ == "__main__":
	subscribe()







# cncPendant = Xhb04b_6()

# while 1:
# 	cncPendant.displayStatus.X = cncPendant.displayStatus.X + 0.01
# 	cncPendant.displayStatus.Y = cncPendant.displayStatus.Y + 0.21
# 	cncPendant.displayStatus.Z = cncPendant.displayStatus.Z + 100
# 	cncPendant.UpdateDisplay()
# 	time.sleep(0.3)

