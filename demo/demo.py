
def y():
    return 'hello'

def x():
    return y()


def main():
    print(x())

if __name__== '__main__':
    main()
