from controller import Keyboard

def getKeys(keyboard: Keyboard):
    keysDetected = [keyboard.getKey() for _ in range(4)]
    
    # Filter out -1 and convert to characters in one step
    keysPressed = [chr(key) for key in keysDetected if key != -1]

    if keysPressed:
        print("Keys pressed:", keysPressed)
    
    return keysPressed