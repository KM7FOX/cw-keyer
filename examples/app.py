from km7fox_cw.encoder.straight_key import Keyer


def main():
    print('Started...')

    decoder = Keyer().run()

    for text in decoder:
        print(text, end="", flush=True)
    # pause()   
        
if __name__ == '__main__':
    main()
        