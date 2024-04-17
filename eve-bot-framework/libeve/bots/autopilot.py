from asyncio.windows_events import NULL
from operator import contains
import time

from libeve.bots import Bot


class AutoPilotBot(Bot):
    def __init__(
        self,
        log_fn=print,
        pause_interrupt=None,
        pause_callback=None,
        stop_interrupt=None,
        stop_callback=None,
        stop_safely_interrupt=None,
        stop_safely_callback=None,
    ):
        super().__init__(
            log_fn=log_fn,
            pause_interrupt=pause_interrupt,
            pause_callback=pause_callback,
            stop_interrupt=stop_interrupt,
            stop_callback=stop_callback,
            stop_safely_interrupt=stop_safely_interrupt,
            stop_safely_callback=stop_safely_callback,
        )

    def go(self):
        
        def jump():
            jump_btn = self.wait_for(
                {"_setText": "Jump through stargate"},
                type="TextBody",
                until=5,
            )

            if jump_btn:
                self.say("Initializing jump ...")
                x,y = self.click_node(jump_btn)
                self.say(f"Left clicked on jump btn at {x},{y} ...")
                _ = self.wait_for({"_setText": "Establishing Warp Vector"}, until=5)
                if _:
                    self.wait_until_warp_finished()
                else:
                    self.say("Could not find Establishing Warp Vector text ...")
            else:
                self.say("Could not find Jump throught stargate text ...")

        def dock():
            dock_btn = self.wait_for(
                {"_setText": "Dock"}, type="TextBody", until=5
            )

            if not dock_btn:
                return -1

            self.say("docking ...")
            
            x,y = self.click_node(dock_btn)
            self.say(f"Left clicked on Dock button at {x},{y} ...")
            
            _ = self.wait_for({"_setText": "Establishing Warp Vector"}, until=5)
            if _:
                self.wait_until_warp_finished()
            else:
                self.say("Could not find Establishing Warp Vector text ...")

        def jump_or_dock():
            self.say("Looking for route ...")
            route = self.wait_for( {"_name": "markersParent"}, type="Container", until=15)

            if not route:
                return
            
            routeCount = 0
            for child in route.children:
                routeCount += 1 
                
            self.say(f"{routeCount} routes found.")

            count = 1
            for waypoint_id in route.children:
                
                self.say(f"Handling route {count} ...")
                
                waypoint = self.tree.nodes[waypoint_id]
                
                x,y = self.click_node(waypoint, right_click=True)
                
                self.say(f"Right clicked on waypoint {count} at {x},{y} ...")

                if len(route.children) == 1:
                    if dock() == -1:
                        jump()
                    return
                else:
                    jump()
                    return
                count += 1
                
        def check_if_docked():
            undock_btn = self.wait_for(
                {"_setText": "Undock"}, type="EveLabelMedium", until=5
            )
            if undock_btn:
                self.say("Ship is docked ...")
                return (True, undock_btn)
            else:
                self.say("Ship is not docked ...")
                return (False, None)
                
        def take_action():
            self.say("Obversing environment ...")
            
            route = self.wait_for( {"_name": "markersParent"}, type="Container", until=15)

            if not route:
                self.say("No route found ...")
                return;

            is_docked, undock_btn = check_if_docked()
            if is_docked:
                self.say("Undocking ...")
                x,y = self.click_node(undock_btn)
                self.say(f"Left clicked on Undock button at {x},{y} ...")
                time.sleep(10)
            else:
                jump_or_dock()

        while True:
            take_action()
            pass