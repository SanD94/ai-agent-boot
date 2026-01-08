from functions.write_file import write_file


def test():
    print("Write content into 'lorem_demo.txt'")
    print(write_file("calculator", "lorem_demo.txt", "wait, this isn't lorem ipsum"))

    print("Write content into 'pkg/morelorem.txt'")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    print("Write content into '/tmp/temp.txt'")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))



if __name__ == "__main__":
    test()
