from km7fox_cw.encoder.straight_key import StraightKeyer


def main():
    print('Started...')

    sk = StraightKeyer()
    decoder = sk.run()
    tone_on = True
    on_air = False
    escape = False

    for text in decoder:
        if text == '~':
            escape = True
            continue
        
        if escape:
            escape = False
            
            if text == 'X ':
                print('Exiting')
                break
            elif text == 'T ':
                tone_on = not tone_on
                sk.set_settings(tone_on=tone_on, on_air=on_air)
                print(f'tone_on: {tone_on}')
            elif text == 'A ':
                on_air = not on_air
                sk.set_settings(on_air=on_air, tone_on=tone_on)
                print(f'on_air: {on_air}')
        
        print(text, end="", flush=True)  
        
if __name__ == '__main__':
    main()
        