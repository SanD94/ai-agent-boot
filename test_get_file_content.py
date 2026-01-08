from functions.get_file_content import get_file_content

def test():
    print("Result for 'lorem.txt' file")
    res = get_file_content("calculator", "lorem.txt")
    print(res[-70:])

    print("Result for 'main.py' file")
    res = get_file_content("calculator", "main.py")
    print(res)

    print("Result for 'pkg/calculator.py' file")
    res = get_file_content("calculator", "pkg/calculator.py")
    print(res)

    print("Result for '/bin/cat' file")
    res = get_file_content("calculator", "/bin/cat") 
    print(res)

    print("Result for 'pkg/does_not_exist.py' file")
    res = get_file_content("calculator", "pkg/does_not_exist.py")
    print(res)

if __name__ == "__main__":
    test()
