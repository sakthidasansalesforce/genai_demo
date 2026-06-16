def main():
    mark = int(input("Enter a mark (0-100): "))

    if 90 <= mark <= 100:
        grade = "A"
    elif 80 <= mark <= 89:
        grade = "B"
    elif 70 <= mark <= 79:
        grade = "C"
    elif 60 <= mark <= 69:
        grade = "D"
    elif 0 <= mark < 60:
        grade = "E"
    else:
        print("Invalid mark. Please enter a value between 0 and 100.")
        return

    print(f"Mark: {mark}")
    print(f"Grade: {grade}")


if __name__ == "__main__":
    main()