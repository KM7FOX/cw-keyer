from km7fox_cw.encoder.cw_transmitter import CWTransmitter


CWT = CWTransmitter(13)

def play(message: str) -> None:
    CWT.send(message)
    print('Sent!')

def main():
    message = ''
    while True:
        response = input('Message: ')
        if response.upper() == '/X':
            break
        elif response.upper() == '/R':
            play(message)
        else:
            message = response
            play(message)
    print("Exiting")
    
if __name__ == "__main__":
    main()
        
        
