class SeleniumHandler():
    def __init__(self) -> None:
        pass
    
    def handle_events(self, events):
        for event in events:
            print(event)
            
class SeleniumEvent():
    type = 0
    # event types
    # driver event or element event
    
    def __init__(self, event):
        pass