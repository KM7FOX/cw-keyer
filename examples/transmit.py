from km7fox_cw.encoder.cw_transmitter import CWTransmitter


CWT = CWTransmitter()

def play(message: str) -> None:
    CWT.send(message)
    print('Sent!')

def main():
    message = ''
    tone_on = True
    on_air = False
    while True:
        response = input('Message: ')
        if response.upper() == '/X':    # exit
            break
        elif response.upper().startswith('/S'):
            try:
                speed = int(response[2:])
            except:
                print(f'Invalid speed: "{response[2:]}"')
                continue
            CWT.speed = speed
            print(f'Speed set to {speed} WPM')
        elif response.upper() == '/R':  # repeat message
            play(message)
        elif response.upper() == '/T':  # toggle side tone
            tone_on = not tone_on
            CWT.set_settings(tone_on=tone_on, on_air=on_air)
            out = 'on' if tone_on else 'off'
            print(f'Side tone is {out}')
        elif response.upper() == '/A':
            on_air = not on_air
            CWT.set_settings(on_air=on_air, tone_on=tone_on)
            out = 'On' if on_air else 'Off'
            print(f'{out} the air')
        else:
            message = response
            play(message)
    print("Exiting")
    
if __name__ == "__main__":
    main()
        
        
