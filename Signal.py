import signal

HAS_INTERRUPT_OCCURED = False

#-------------------

def __custom_keyboard_interrupt_handler(signum, frame):
    global HAS_INTERRUPT_OCCURED
    HAS_INTERRUPT_OCCURED = True

#-------------------
    
def register_signal():
    signal.signal(signal.SIGINT, __custom_keyboard_interrupt_handler)