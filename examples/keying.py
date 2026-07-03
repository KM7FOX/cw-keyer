from km7fox_cw.encoder.straight_key import StraightKeyer


def main():
    print('Started...')

    decoder = StraightKeyer().run()

    for text in decoder:
        print(text, end="", flush=True)
    # pause()   
        
if __name__ == '__main__':
    main()
        