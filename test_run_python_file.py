from functions.run_python_file import run_python_file

def test():
    print("Run 'main.py'")
    print(run_python_file("calculator", "main.py"))

    print("Run 'main.py' with args")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print("Run 'tests.py'")
    print(run_python_file("calculator", "tests.py"))

    print("Run '../main.py'")
    print(run_python_file("calculator", "../main.py"))

    print("Run 'nonexistent.py'")
    print(run_python_file("calculator", "nonexistent.py"))

    print("Run 'lorem.txt'")
    print(run_python_file("calculator", "lorem.txt"))

if __name__ == "__main__":
    test()
