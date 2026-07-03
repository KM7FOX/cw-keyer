from km7fox_cw.encoder.cw_transmitter import CWTransmitter


CWT = CWTransmitter(13)

def play(message: str) -> None:
    CWT.send(message)
    print('Sent!')

def main():
    message = ''
    tone_on = True
    while True:
        response = input('Message: ')
        if response.upper() == '/X':    # exit
            break
        elif response.upper() == '/R':  # repeat message
            play(message)
        elif response.upper() == '/T':  # toggle side tone
            tone_on = not tone_on
            CWT.set_settings(tone_on=tone_on)
            out = 'on' if tone_on else 'off'
            print(f'Side tone is {out}')
        else:
            message = response
            play(message)
    print("Exiting")
    
if __name__ == "__main__":
    main()
        
        
